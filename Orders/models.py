
from django.db import models
from django.urls import reverse
from django.utils import timezone


from Items.models import items
from Customers.models import customers
class orders(models.Model):
    ordered_date = models.DateTimeField(max_length=6, )
    updated_date = models.DateTimeField(max_length=6, )
    customers = models.ForeignKey(customers, on_delete=models.CASCADE, related_name='customers')

    class Meta:
        app_label = 'Orders'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class orderitem(models.Model):
    quantity = models.IntegerField(max_length=32, )
    items = models.ForeignKey(items, on_delete=models.CASCADE, related_name='items')
    orders = models.ForeignKey(orders, on_delete=models.CASCADE, related_name='orders')

    class Meta:
        app_label = 'Orders'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



