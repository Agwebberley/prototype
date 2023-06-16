from django.db import models
from django.urls import reverse_lazy
from Items.models import Items


# Create your models here.
class Manufacture(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.item} - {self.quantity}'

    def get_absolute_url(self):
        return reverse_lazy('manufacture:manufacture_list')