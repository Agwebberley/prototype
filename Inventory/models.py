from django.db import models
from django.urls import reverse
from Items.models import Items

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
    item = models.ForeignKey(Items, on_delete=models.CASCADE, editable=False)
    quantity = models.IntegerField(editable=False, default=0)
    types = ["shipment", "order", "return", "adjustment"]
    type = models.CharField(max_length=10, choices=[(x, x) for x in types], default="shipment", editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        app_label = 'Inventory'
    
    def __str__(self):
        return f"{self.item} - {self.quantity}"
    
    def get_absolute_url(self):
        return reverse('inventory_list')

class Pick(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    quantity = models.IntegerField()
    order_number = models.CharField(max_length=100)
    is_complete = models.BooleanField(default=False)
    class Meta:
        app_label = 'Inventory'
    
    def __str__(self):
        return f"{self.item} - {self.quantity} ({self.location}) for order {self.order_number}"
    
    def get_absolute_url(self):
        return reverse('pick_detail', args=[str(self.id)])

class Bin(models.Model):
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    items = models.ManyToManyField(Items)
    class Meta:
        app_label = 'Inventory'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('bin_list')
    
    def restock(self):
        for item in self.items.all():
            inventory = Inventory.objects.get(item=item)
            inventory.quantity += 1
            inventory.save()
        self.restocked = True
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            num_bins = Bin.objects.filter(location=self.location).count()
            self.pk = f"{self.location.id}-{num_bins + 1}"
        super().save(*args, **kwargs)

class Location(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        app_label = 'Inventory'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('location_list')