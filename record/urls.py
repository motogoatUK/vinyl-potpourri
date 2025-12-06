from django.urls import path
from . import views


urlpatterns = [
    path('', views.RecordList.as_view(), name='all_records'),
    path('add/', views.add_record, name="add_record"),
    path('edit/<slug:slug>/', views.edit_record, name='edit_record'),
    path('artist-autocomplete',
         views.artist_autocomplete,
         name="artist-autocomplete"),
    path('<slug:slug>/', views.view_record, name='view_record'),
]
