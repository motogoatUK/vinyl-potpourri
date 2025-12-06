"""
URL configuration for vinyl_potpourri project.
"""
from django.contrib import admin
from django.urls import path, include
from record import urls as record_urls
from collection import urls as collection_urls
from my_profile import urls as my_profile_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path("about/", include("about.urls")),
    path('accounts/', include('allauth.urls')),
    path('record/', include(record_urls)),
    path('', include(collection_urls), name='collection_urls'),
    path('profile/', include(my_profile_urls), name='profile_urls'),
    ]
