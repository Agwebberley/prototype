# This is a Django model class for a data object with fields for name, address, phone, and email, and
# methods for returning a string representation and an absolute URL.
from django.db import models
from django.urls import reverse


class Customers(models.Model):
    name = models.CharField(max_length=200)
    billing_address = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    class Meta:
        app_label = 'Customers'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('data_list')

class LogMessage(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Items(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    target_inv = models.IntegerField()
    current_inv = models.IntegerField()
    class Meta:
        app_label = 'Customers'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('items_list')

class Orders(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
        app_label = 'Customers'
    
    def __str__(self):
        return self.customer
    
    def get_absolute_url(self):
        return reverse('orders_list')