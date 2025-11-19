"""
URL configuration for vinyl_potpourri project.
"""
from django.contrib import admin
from django.urls import path, include
from record import urls as record_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(record_urls), name='record_urls'),
]
