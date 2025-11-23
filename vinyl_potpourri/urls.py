"""
URL configuration for vinyl_potpourri project.
"""
from django.contrib import admin
from django.urls import path, include
from record import urls as record_urls
from collection import urls as collection_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('record/', include(record_urls), name='record_urls'),
    path('', include(collection_urls), name='collection_urls'),
]
