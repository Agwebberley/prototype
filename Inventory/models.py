
from django.db import models
from django.urls import reverse
from django.utils import timezone


class bin(models.Model):
    name = models.CharField(max_length=100, )
    location_id = models.IntegerField(max_length=64, )

    class Meta:
        app_label = 'Inventory'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class bin_items(models.Model):
    bin_id = models.IntegerField(max_length=64, )
    items_id = models.IntegerField(max_length=64, )

    class Meta:
        app_label = 'Inventory'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class inventory(models.Model):
    quantity = models.IntegerField(max_length=32, )
    last_updated = models.DateTimeField(max_length=6, )
    typeI = models.CharField(max_length=10, )
    item_id = models.IntegerField(max_length=64, )

    class Meta:
        app_label = 'Inventory'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class inventoryhistory(models.Model):
    quantity = models.IntegerField(max_length=32, )
    change = models.IntegerField(max_length=32, )
    typeI = models.CharField(max_length=10, )
    timestamp = models.DateTimeField(max_length=6, )
    inventory_id = models.IntegerField(max_length=64, )
    item_id = models.IntegerField(max_length=64, )

    class Meta:
        app_label = 'Inventory'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class location(models.Model):
    name = models.CharField(max_length=100, )
    amount_of_bins = models.IntegerField(max_length=32, )

    class Meta:
        app_label = 'Inventory'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class pick(models.Model):
    is_complete = models.BooleanField()
    location_id = models.IntegerField(max_length=64, )
    order_id = models.IntegerField(max_length=64, )

    class Meta:
        app_label = 'Inventory'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class pick_items(models.Model):
    pick_id = models.IntegerField(max_length=64, )
    orderitem_id = models.IntegerField(max_length=64, )

    class Meta:
        app_label = 'Inventory'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



