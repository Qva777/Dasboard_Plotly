from django.contrib import admin

from ordercast_product.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Product fields in the admin panel """

    list_display = ('ref', 'color', 'active')
    list_display_links = ('ref',)
    list_editable = ('active',)
    search_fields = ('ref', 'color',)
    ave_on_top = True
    list_per_page = 20
