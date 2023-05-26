from django.db import models
from django.urls import reverse


class Data(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    class Meta:
        app_label = 'CRUD'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('data_list')
