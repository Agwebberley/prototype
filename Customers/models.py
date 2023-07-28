
from django.db import models
from django.urls import reverse
from django.utils import timezone


class customers(models.Model):
    id = models.IntegerField(max_length=64, )
    name = models.CharField(max_length=200, )
    billing_address = models.CharField(max_length=200, )
    shipping_address = models.CharField(max_length=200, )
    phone = models.CharField(max_length=200, )
    email = models.CharField(max_length=200, )

    class Meta:
        app_label = 'Customers'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



