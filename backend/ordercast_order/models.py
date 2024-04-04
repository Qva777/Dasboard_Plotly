from django.db import models

from core.behaivours import Timestampable
from ordercast_client.models import Client
from ordercast_country.models import Country
from ordercast_product.models import Product


class Order(Timestampable):
    """ Order Model  """
    products = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    billing_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='billing_countries')
    shipping_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='shipping_countries')

    def __str__(self):
        return f"Order {self.pk}"
