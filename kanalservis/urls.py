from django.contrib import admin
from django.urls import path

from orders.views import orders_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', orders_view)
]
