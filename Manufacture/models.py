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

class ManufactureHistory(models.Model):
    manufacture = models.IntegerField(null=True, blank=True)
    item = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.item} - {self.quantity}'

    def get_absolute_url(self):
        return reverse_lazy('manufacture:manufacture_list')
    
    def save(self, *args, **kwargs):
        if self.manufacture:
            self.item = Manufacture.objects.get(id=self.manufacture).item.id
        super().save(*args, **kwargs)