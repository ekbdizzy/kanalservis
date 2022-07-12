from django.contrib import admin
from django.urls import path
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', render, kwargs={'template_name': 'frontend/index.html'}, name='start_page')
]
