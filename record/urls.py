from django.urls import path
from . import views


urlpatterns = [
    path('', views.RecordList.as_view(), name='index'),
]
