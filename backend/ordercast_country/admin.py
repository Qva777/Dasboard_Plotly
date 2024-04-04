from django.contrib import admin

from ordercast_country.models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """ Country fields in the admin panel """

    list_display = ('name', 'code', 'active')
    list_display_links = ('name', 'code',)
    list_editable = ('active',)
    search_fields = ('name', 'code',)
    ave_on_top = True
    list_per_page = 20
