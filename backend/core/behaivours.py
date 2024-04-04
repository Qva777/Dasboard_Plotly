import uuid
from django.db import models


class Timestampable(models.Model):
    """ Base class for any models """

    id = models.UUIDField(auto_created=True, primary_key=True, editable=False, default=uuid.uuid4, verbose_name="ID", )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
