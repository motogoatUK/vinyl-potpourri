from django.contrib import admin
from .models import Record, Artist


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('a_side',)}


admin.site.register(Artist)
