
from django.db import models
from django.urls import reverse
from django.utils import timezone


class orderitem(models.Model):
    quantity = models.IntegerField(max_length=32, )
    item_id = models.IntegerField(max_length=64, )
    order_id = models.IntegerField(max_length=64, )

    class Meta:
        app_label = 'Orders'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class orders(models.Model):
    ordered_date = models.DateTimeField(max_length=6, )
    updated_date = models.DateTimeField(max_length=6, )
    customer_id = models.IntegerField(max_length=64, )

    class Meta:
        app_label = 'Orders'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



