from django.db import models
from django.urls import reverse
from Customers.models import Customers
from Items.models import Items
from django.utils import timezone


class Orders(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        app_label = 'Orders'
    
    def __str__(self):
        return str(self.pk)
    
    def get_absolute_url(self):
        return reverse('orders:order_list')
    
    def get_total_price(self):
        order_items = OrderItem.objects.filter(order=self)
        total_price = sum([item.get_item_price() for item in order_items])
        return "{:,}".format(total_price)
    
    def get_total_price_float(self):
        order_items = OrderItem.objects.filter(order=self)
        total_price = sum([item.get_item_price() for item in order_items])
        return total_price

class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
        app_label = 'Orders'
    
    def __str__(self):
        return self.order
    
    def get_absolute_url(self):
        return reverse('orders:order_list')
    
    def get_item_price(self):
        return self.item.price * self.quantity
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.updated_date = timezone.now()
        self.order.save()

    def delete(self, *args, **kwargs):
        self.order.updated_date = timezone.now()
        self.order.save()
        super().delete(*args, **kwargs)