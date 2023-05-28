# This is a Django model class for a data object with fields for name, address, phone, and email, and
# methods for returning a string representation and an absolute URL.
from django.db import models
from django.urls import reverse


class Data(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    billing_address = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    class Meta:
        app_label = 'CRUD'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('data_list')
