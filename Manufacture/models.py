
from django.db import models
from django.urls import reverse
from django.utils import timezone


from Items.models import items
class manufacturehistory(models.Model):
    manufacture = models.IntegerField(null=True, blank=True)
    item = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(max_length=6, )
    is_complete = models.BooleanField()

    class Meta:
        app_label = 'Manufacture'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class manufacture(models.Model):
    quantity = models.IntegerField()
    date = models.DateField()
    items = models.ForeignKey(items, on_delete=models.CASCADE, related_name="manufacture")
    manufacturehistory = models.ForeignKey(manufacturehistory, on_delete=models.CASCADE, related_name="_manufacture")

    class Meta:
        app_label = 'Manufacture'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



