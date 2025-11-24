from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('collection/', views.CollectionList.as_view(), name='collections'),
    path('collection/<slug:id>/', views.view_collection),
]
