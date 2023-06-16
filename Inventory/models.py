from django.db import models
from django.urls import reverse
from Items.models import Items
from Orders.models import Orders, OrderItem
from django.core.exceptions import ValidationError

class Inventory(models.Model):
    item = models.OneToOneField(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    class Meta:
        app_label = 'Inventory'
    
    def __str__(self):
        return f"{self.item} - {self.quantity}"
    
    def get_absolute_url(self):
        return reverse('inventory_list')

class InventoryHistory(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, editable=False)
    item = models.ForeignKey(Items, on_delete=models.CASCADE, editable=False)
    quantity = models.IntegerField(editable=False, default=0)
    change = models.IntegerField(editable=False, default=0)
    types = ["shipment", "order", "return", "adjustment"]
    type = models.CharField(max_length=10, choices=[(x, x) for x in types], default="shipment", editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        app_label = 'Inventory'
    
    def save(self, *args, **kwargs):
        self.item = self.inventory.item
        # Get the change in quantity
        # Get the last InventoryHistory entry for this item
        last_entry = InventoryHistory.objects.filter(item=self.item).order_by('-timestamp').first()
        if last_entry:
            self.change = self.quantity - last_entry.quantity
        else:
            self.change = self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item} - {self.quantity}"
    
    def get_absolute_url(self):
        return reverse('inventory_list')

class Pick(models.Model):
    order = models.OneToOneField(Orders, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem, blank=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, blank=True, null=True)
    is_complete = models.BooleanField(default=False)
    class Meta:
        app_label = 'Inventory'

    def clean(self):
        if self.is_complete and not self.location:
            raise ValidationError("Location cannot be blank if pick is complete.")
    
    def save(self, *args, **kwargs):
        # Set items to be picked to the items in the order
        super().save(*args, **kwargs)
        self.items.set(OrderItem.objects.filter(order=self.order))
        self.save()

class Bin(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    items = models.ManyToManyField(Items, blank=True)
    class Meta:
        app_label = 'Inventory'
    
    def get_absolute_url(self):
        return reverse('bin_list')
    
    def save(self, *args, **kwargs):
        if not self.pk:
            num_bins = Bin.objects.filter(location=self.location).count()
            self.name = f"{self.location.id}-{num_bins + 1}"
        super().save(*args, **kwargs)

class Location(models.Model):
    name = models.CharField(max_length=100)
    amount_of_bins = models.IntegerField(blank=True, null=True)
    class Meta:
        app_label = 'Inventory'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('location_list')
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # If Location is new, create a bin for it
        if not self.amount_of_bins:
            self.amount_of_bins = 1
        if self.amount_of_bins > 0:
            for i in range(self.amount_of_bins):
                bin = Bin(location=self)
                bin.save()