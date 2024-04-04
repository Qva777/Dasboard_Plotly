from django.db import models

from core.behaivours import Timestampable


class Product(Timestampable):
    """ Product model """

    ref = models.CharField(max_length=255)
    color = models.CharField(max_length=10)

    def __str__(self):
        """ String representation """
        return f"Product {self.ref}"
