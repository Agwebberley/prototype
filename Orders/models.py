
from django.db import models
from django.urls import reverse
from django.utils import timezone


class orderitem(models.Model):
    quantity = models.IntegerField(max_length=32, )
    item_id = models.IntegerField(max_length=64, )
    order_id = models.IntegerField(max_length=64, )
    items = models.ForeignKey('Items_items', on_delete=models.CASCADE, related_name='items')
    orders = models.ForeignKey('Orders_orders', on_delete=models.CASCADE, related_name='orders')

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
    customers = models.ForeignKey('Customers_customers', on_delete=models.CASCADE, related_name='customers')

    class Meta:
        app_label = 'Orders'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



