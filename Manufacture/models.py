
from django.db import models
from django.urls import reverse
from django.utils import timezone


class manufacture(models.Model):
    id = models.IntegerField(max_length=64, )
    quantity = models.IntegerField(max_length=32, )
    date = models.DateField()
    item_id = models.IntegerField(max_length=64, )

    class Meta:
        app_label = 'Manufacture'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class manufacturehistory(models.Model):
    id = models.IntegerField(max_length=64, )
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



