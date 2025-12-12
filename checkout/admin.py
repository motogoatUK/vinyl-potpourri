from django.contrib import admin
from .models import Order, Product


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('order_number', 'date', 'item',
                       'order_total', 'stripe_pid')

    fields = ('order_number', 'user_profile', 'date', 'full_name', 'email',
              'phone_number', 'street_address1', 'street_address2',
              'town_or_city', 'county', 'postcode', 'country', 'item',
              'order_total', 'stripe_pid')

    list_display = ('order_number', 'date', 'full_name',
                    'user_profile', 'item', 'order_total')

    ordering = ('date',)


admin.site.register(Order, OrderAdmin)
admin.site.register(Product)
