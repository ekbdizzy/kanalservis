import json
import xml.etree.ElementTree as ET  # NOQA N817
from datetime import datetime

import requests

from .redis_services import get_value_from_redis, set_value_to_redis


def _fetch_dollar_exchange_rate(
    date: str | None = None,
) -> tuple[str, str] | None:
    """Parse dollar exchange rate from cbr.ru by date.
    Date format: day/month/year. Example: 14/07/2022.
    More info: https://www.cbr.ru/development/SXML/"""

    date = date or datetime.now().strftime('%d/%m/%Y')

    response = requests.get(
        url='https://www.cbr.ru/scripts/XML_daily.asp',
        params={'date_req': date},
    )
    response.raise_for_status()
    root = ET.fromstring(response.text)
    for element in root.iter('Valute'):
        if element.get('ID') == 'R01235':
            return element.find('Value').text, date


def get_dollar_exchange_rate():
    """Try to get dollar exchange rate from Redis,
    else fetch from cbr.ru."""

    dollar = get_value_from_redis('dollar')
    if dollar:
        if dollar.get('date') == datetime.now().strftime('%d/%m/%Y'):
            return float(dollar.get('value').replace(',', '.'))

    value, date = _fetch_dollar_exchange_rate() or (None, None)
    if value and date:
        set_value_to_redis("dollar", json.dumps({"value": value, "date": date}))
        return float(value.replace(',', '.'))


def compute_rubble_price(dollar_price: str | int | float) -> float:
    exchange_rate = get_dollar_exchange_rate()
    return round(exchange_rate * float(dollar_price), 2)


def parse_date(date: str) -> datetime.date:
    return datetime.strptime(date, '%d.%m.%Y').date()


def serialize_orders_with_rubbles(orders_from_sheets: list) -> dict:
    if orders_from_sheets is None:
        return {}
    orders = dict()
    for order in orders_from_sheets:
        number, order_number, dollar_price, date = order
        orders[int(order_number)] = {
            'number': int(number),
            'order_number': int(order_number),
            'dollar_price': float(dollar_price),
            'rubble_price': compute_rubble_price(dollar_price),
            'delivery_date': parse_date(date),
        }
    return orders
