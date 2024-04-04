from django.db import models
from core.behaivours import Timestampable


class Client(Timestampable):
    """ Client model """

    class StatusChoice(models.TextChoices):
        Tariff0 = "T0", "Tariff 0"
        Tariff1 = "T1", "Tariff 1"
        Tariff2 = "T2", "Tariff 2"
        Tariff3 = "T3", "Tariff 3"
        Tariff4 = "T4", "Tariff 4"
        Tariff5 = "T5", "Tariff 5"

    username = models.CharField(verbose_name='Name', max_length=64, blank=True)
    email = models.EmailField(verbose_name='Email', unique=True, max_length=64, blank=False)

    is_approved = models.BooleanField(default=False)
    tariff_name = models.CharField(max_length=2, choices=StatusChoice.choices, default=StatusChoice.Tariff0, )

    def __str__(self):
        """ String representation """
        return self.username
