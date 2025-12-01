from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProfileDetail.as_view(), name='my_profile'),
]
