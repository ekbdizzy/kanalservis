from django.http import HttpResponse

from orders.services import fetch_from_google_sheets
from orders.services.cbr_services import serialize_orders_with_rubbles


def orders_view(request):
    orders = fetch_from_google_sheets()
    response = serialize_orders_with_rubbles(orders)
    return HttpResponse(response)
