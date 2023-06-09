from django.db import models
from django.urls import reverse
from Customers.models import Customers
from Items.models import Items


class Orders(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
        app_label = 'Orders'
    
    def __str__(self):
        return self.customer
    
    def get_absolute_url(self):
        return reverse('order_list')