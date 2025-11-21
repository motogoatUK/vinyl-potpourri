from django.urls import path
from . import views


urlpatterns = [
    path('', views.RecordList.as_view(), name='all_records'),
    path('record/<slug:slug>/', views.view_record),
]
