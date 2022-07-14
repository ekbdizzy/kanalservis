from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "order_number",
        "dollar_price",
        "rubble_price",
        "delivery_date",
    )

    list_filter = ("delivery_date",)
    search_fields = (
        "number",
        "order_number",
        "dollar_price",
        "rubble_price",
    )
