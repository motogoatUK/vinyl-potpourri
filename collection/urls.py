from django.urls import path
from . import views


urlpatterns = [
    path('', views.CollectionList.as_view(), name='home'),
    path('collection/<slug:id>/', views.view_collection),
]
