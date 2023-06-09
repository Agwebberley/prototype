from django.db import models
from django.urls import reverse

# Create your models here.
class Items(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    target_inv = models.IntegerField()
    current_inv = models.IntegerField(default=0)
    reorder_level = models.IntegerField()
    class Meta:
        app_label = 'Items'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('item_list')