
from django.db import models
from django.urls import reverse
from django.utils import timezone


class items(models.Model):
    name = models.CharField(max_length=200, )
    description = models.CharField(max_length=200, )
    price = models.DecimalField(max_length=10, decimal_places=2, )
    target_inv = models.IntegerField(max_length=32, )
    current_inv = models.IntegerField(max_length=32, )
    reorder_level = models.IntegerField(max_length=32, )

    class Meta:
        app_label = 'Items'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



