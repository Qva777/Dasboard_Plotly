from django.contrib import admin

from ordercast_order.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Order fields in the admin panel """

    list_display = ('get_email', 'get_ref', 'get_color', 'total', 'billing_country', 'shipping_country', 'active')
    list_display_links = ('get_email', 'get_ref',)
    list_editable = ('active',)
    search_fields = ('products__ref', 'client__email')
    ave_on_top = True
    list_per_page = 20

    def get_color(self, obj):
        return obj.products.color

    def get_ref(self, obj):
        return obj.products.ref

    def get_email(self, obj):
        return obj.client.email

    get_color.short_description = 'Color'
    get_email.short_description = 'Email'
    get_ref.short_description = 'Ref'
