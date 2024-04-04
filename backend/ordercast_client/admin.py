from django.contrib import admin
from ordercast_client.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """ Client fields in the admin panel """

    list_display = ('username', 'email', 'tariff_name', 'is_approved', 'active')
    list_display_links = ('username', 'email', 'tariff_name',)
    list_editable = ('is_approved', 'active',)
    search_fields = ('username', 'email', 'tariff_name',)
    list_filter = ('tariff_name',)
    ave_on_top = True
    list_per_page = 20
