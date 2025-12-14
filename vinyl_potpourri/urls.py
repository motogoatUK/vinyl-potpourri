"""
URL configuration for vinyl_potpourri project.
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from record import urls as record_urls
from collection import urls as collection_urls
from my_profile import urls as my_profile_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path("about/", include("about.urls")),
    path('accounts/', include('allauth.urls')),
    path('checkout/', include('checkout.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('record/', include(record_urls)),
    path('', include(collection_urls), name='collection_urls'),
    path('profile/', include(my_profile_urls), name='profile_urls'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
