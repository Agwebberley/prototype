
from django.db import models
from django.urls import reverse
from django.utils import timezone


from Items.models import items
#from Customers.models import customers
class orders(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)
    customers = models.ForeignKey(Customers.models.customers, on_delete=models.CASCADE, related_name="orders")

    class Meta:
        app_label = 'Orders'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class orderitem(models.Model):
    quantity = models.IntegerField()
    items = models.ForeignKey(items, on_delete=models.CASCADE, related_name="orderitem")
    orders = models.ForeignKey(orders, on_delete=models.CASCADE, related_name="_orderitem")

    class Meta:
        app_label = 'Orders'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



