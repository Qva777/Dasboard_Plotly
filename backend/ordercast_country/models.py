from django.db import models
from core.behaivours import Timestampable


class Country(Timestampable):
    """ Country models """

    name = models.CharField(max_length=256)
    code = models.CharField(max_length=50)

    def __str__(self):
        """ String representation """
        return self.name
