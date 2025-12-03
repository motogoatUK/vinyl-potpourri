from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('collection/add/', views.add_collection, name='add_collection'),
    path('collection/edit/<int:id>/', views.edit_collection),
    path('collection/<int:id>/',
         views.view_collection, name='view_collection'),
    path('collection/', views.CollectionList.as_view(), name='collections'),
    path('my-collection/', views.MyCollection.as_view(), name='my_collection'),
]
