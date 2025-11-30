from django.contrib import admin
from my_profile.models import My_Profile


@admin.register(My_Profile)
class My_ProfileAdmin(admin.ModelAdmin):
    verbose_name = "User Profile"
