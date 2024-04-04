from django.apps import AppConfig


class OrdercastProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ordercast_product'

    def ready(self): # todo: ploty
        pass
