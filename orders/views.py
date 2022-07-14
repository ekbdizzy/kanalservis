from django.shortcuts import render
from .services import fetch_from_google_sheets
from django.http import JsonResponse


def orders_view(request):
    fetch_from_google_sheets()
    return JsonResponse({'response': 'ok'})

