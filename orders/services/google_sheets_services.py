from __future__ import print_function

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from django.conf import settings

from .redis_services import get_value_from_redis, set_value_to_redis


def get_google_creds() -> dict:
    """Try to get Google credentials (google_token) from Redis and validate it.
    Return google_token if it is valid.
    Else try to fetch Google credentials from Google using settings.GOOGLE_CLIENT_SECRET.
    If success, google_token is updated in Redis.
    """
    creds = None
    google_token = get_value_from_redis(key='google_token')
    if google_token:
        creds = Credentials.from_authorized_user_info(
            google_token,
            settings.GOOGLE_SHEETS_SCOPES,
        )
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                settings.GOOGLE_CLIENT_SECRET,
                settings.GOOGLE_SHEETS_SCOPES,
            )
            creds = flow.run_local_server(port=0)
        set_value_to_redis('google_token', creds.to_json())
    return creds


def fetch_from_google_sheets(orders_amount=settings.ORDERS_DEFAULT_AMOUNT) -> list:
    """Get orders from Google sheets.
    orders_amount - is a number of parsed records in the Google Sheet.
    If len(orders) = orders_amount - 1 then orders_amount
    will be increased on settings.ORDERS_AMOUNT_INCREASE_BY
    and will fetch once more.
    """
    creds = get_google_creds()
    sample_range_name = f'{settings.GOOGLE_SHEET_NAME}!A2:E{orders_amount}'

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=settings.GOOGLE_SPREADSHEET_ID,
            range=sample_range_name,
        ).execute()
        orders = result.get('values', [])
        if len(orders) == orders_amount - 1:
            return fetch_from_google_sheets(orders_amount + settings.ORDERS_AMOUNT_INCREASE_BY)
        return orders

    except HttpError as err:
        print(err)

