from django.urls import path
from . import views


urlpatterns = [
    path('', views.RecordList.as_view(), name='all_records'),
    path('<slug:slug>/', views.view_record),
    path('edit/<slug:slug>/', views.edit_record, name='edit_record'),
]
