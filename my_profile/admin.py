from django.contrib import admin
from my_profile.models import My_Profile


@admin.register(My_Profile)
class My_ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'sub_date', 'exp_date', 'premium']
