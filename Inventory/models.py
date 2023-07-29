
from django.db import models
from django.urls import reverse
from django.utils import timezone


from Items.models import items
from Orders.models import orders
from Orders.models import orderitem
class location(models.Model):
    name = models.CharField(max_length=100, )
    amount_of_bins = models.IntegerField(max_length=32, )

    class Meta:
        app_label = 'Inventory'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class bin(models.Model):
    name = models.CharField(max_length=100, )
    location = models.ForeignKey(location, on_delete=models.CASCADE, related_name='location')

    class Meta:
        app_label = 'Inventory'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class bin_items(models.Model):
    bin = models.ForeignKey(bin, on_delete=models.CASCADE, related_name='bin')
    items = models.ForeignKey(items, on_delete=models.CASCADE, related_name='items')

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
    items = models.OneToOneField(items, on_delete=models.CASCADE, related_name='items')

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
    inventory = models.ForeignKey(inventory, on_delete=models.CASCADE, related_name='inventory')
    items = models.ForeignKey(items, on_delete=models.CASCADE, related_name='items')

    class Meta:
        app_label = 'Inventory'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class pick(models.Model):
    is_complete = models.BooleanField()
    location = models.ForeignKey(location, on_delete=models.CASCADE, related_name='location')
    orders = models.OneToOneField(orders, on_delete=models.CASCADE, related_name='orders')

    class Meta:
        app_label = 'Inventory'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class pick_items(models.Model):
    orderitem = models.ForeignKey(orderitem, on_delete=models.CASCADE, related_name='orderitem')
    pick = models.ForeignKey(pick, on_delete=models.CASCADE, related_name='pick')

    class Meta:
        app_label = 'Inventory'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



