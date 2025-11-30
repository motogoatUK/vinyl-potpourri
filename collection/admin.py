from django.contrib import admin
from .models import Collection, Location


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'username')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'collection')
