from django.core.management.base import BaseCommand
from django.db.models import Q

from orders.models import Order
from orders.services import (
    fetch_from_google_sheets,
    serialize_orders_with_rubbles,
)


def update_orders():
    """Update orders from Google sheets to DB."""
    orders_from_sheets = fetch_from_google_sheets()

    if not orders_from_sheets:
        return

    serialized_orders = serialize_orders_with_rubbles(orders_from_sheets)
    orders_to_create = list(serialized_orders)
    orders_from_db = Order.objects.all()

    orders_to_update = []
    for order in orders_from_db:
        order_from_sheets = serialized_orders.get(order.order_number, None)
        if order_from_sheets is None:
            continue
        try:
            assert order.number == order_from_sheets['number']
            assert order.dollar_price == order_from_sheets['dollar_price']
            assert order.delivery_date == order_from_sheets['delivery_date']
        except AssertionError:
            orders_to_update.append(order.order_number)
        finally:
            orders_to_create.remove(order.order_number)

    Order.objects.filter(
        ~Q(order_number__in=list(serialized_orders))
        | Q(order_number__in=orders_to_update),  # Noqa W503
    ).delete()

    orders_to_create.extend(orders_to_update)
    orders_to_create = [
        value
        for key, value in serialized_orders.items()
        if key in orders_to_create
    ]

    if orders_to_create:
        orders = [Order(**fields) for fields in orders_to_create]
        Order.objects.bulk_create(orders)


class Command(BaseCommand):
    help = 'Update orders from Google sheets to DB.'  # Noqa A003

    def handle(self, *args, **options):
        update_orders()
