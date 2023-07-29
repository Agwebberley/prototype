
from django.db import models
from django.urls import reverse
from django.utils import timezone


class items(models.Model):
    name = models.CharField(max_length=200, )
    description = models.CharField(max_length=200, )
    price = models.DecimalField(max_digits=10, decimal_places=2, )
    target_inv = models.IntegerField()
    current_inv = models.IntegerField()
    reorder_level = models.IntegerField()

    class Meta:
        app_label = 'Items'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



