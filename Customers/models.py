# This is a Django model class for a data object with fields for name, address, phone, and email, and
# methods for returning a string representation and an absolute URL.
from django.db import models
from django.urls import reverse
import datetime

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

class Orders(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
        app_label = 'Customers'
    
    def __str__(self):
        return self.customer
    
    def get_absolute_url(self):
        return reverse('order_list')

class AccountsReceivable(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    amount = models.FloatField()
    # Due date defaults to 30 days from now
    due_date = models.DateField(default=datetime.date.today() + datetime.timedelta(days=30))
    paid = models.BooleanField(default=False)
    class Meta:
        app_label = 'Customers'
    
    def __str__(self):
        return f"{self.order.id} - {self.amount}"
    
    def get_absolute_url(self):
        return reverse('accounts_receivable_list')

class Inventory(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
        app_label = 'Customers'
    
    def __str__(self):
        return f"{self.item} - {self.quantity}"
    
    def get_absolute_url(self):
        return reverse('inventory_list')
