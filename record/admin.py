from django.contrib import admin
from .models import Record, Artist


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('a_side',)}
    list_display = ('__str__', 'artist', 'large_hole', 'collection')

    # Override the save model to create a unique slug of a_side+id
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # only on creation
            obj.slug = f"{obj.slug}-{obj.id}"
            obj.save()


admin.site.register(Artist)
