
from django.db import models
from django.urls import reverse
from django.utils import timezone


from Items.models import items
class manufacturehistory(models.Model):
    manufacture = models.IntegerField(max_length=32, )
    item = models.IntegerField(max_length=32, )
    quantity = models.IntegerField(max_length=32, )
    timestamp = models.DateTimeField(max_length=6, )
    is_complete = models.BooleanField()

    class Meta:
        app_label = 'Manufacture'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class manufacture(models.Model):
    quantity = models.IntegerField(max_length=32, )
    date = models.DateField()
    items = models.ForeignKey(items, on_delete=models.CASCADE, related_name='items')
    manufacturehistory = models.ForeignKey(manufacturehistory, on_delete=models.CASCADE, related_name='manufacturehistory')

    class Meta:
        app_label = 'Manufacture'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



