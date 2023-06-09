from django.db import models
from django.urls import reverse
from Items.models import Items
from Orders.models import Orders, OrderItem
from django.core.exceptions import ValidationError

class Inventory(models.Model):
    item = models.OneToOneField(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    # The type of change that was made to the inventory to be used in the InventoryHistory object
    types = ["shipment", "order", "return", "adjustment"]
    typeI = models.CharField(max_length=10, choices=[(x, x) for x in types], default="shipment")
    class Meta:
        app_label = 'Inventory'
    
    def __str__(self):
        return f"{self.item} - {self.quantity}"
    
    def get_absolute_url(self):
        return reverse('inventory_list')
    
    def save(self, *args, **kwargs):
        # Add items to bin
        super().save(*args, **kwargs)
        InventoryHistory.objects.create(inventory=self, quantity=self.quantity, typeI=self.typeI)

        if self.typeI == "shipment":
            # Get the last InventoryHistory entry for this item
            last_entry = InventoryHistory.objects.filter(item=self.item).order_by('-timestamp').first()
            if last_entry:
                self.change = self.quantity - last_entry.quantity

                # Add the change into the bins
                # Get the bin with amount of items
                # items is a Many To Many field
                bins = Bin.objects.filter(pk=1)
                for bin in bins:
                    for i in range(self.change):
                        bin.items.add(self.item)
                        bin.save()
                




class InventoryHistory(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, editable=False)
    item = models.ForeignKey(Items, on_delete=models.CASCADE, editable=False)
    quantity = models.IntegerField(editable=False, default=0)
    change = models.IntegerField(editable=False, default=0)
    types = ["shipment", "order", "return", "adjustment"]
    typeI = models.CharField(max_length=10, choices=[(x, x) for x in types], default="shipment", editable=False)
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
        print("Saved pick.")

        # Pull the items from the bins and update the inventory
        # Only pull items if the pick is complete and only pull from bins at the same location as the pick
        if self.is_complete and self.location:
            # For each item in the pick
            for item in self.items.all():
                # Get the bins with the item
                bins = Bin.objects.filter(items=item.item, location=self.location)
                # For each bin
                for bin in bins:
                    # Check if the bin has enough items
                    if bin.items.filter(pk=item.item.pk).count() >= item.quantity:
                        # Remove the item from the bin
                        bin.items.remove(item.item)
                        # Update the inventory
                        inventory = Inventory.objects.get(item=item.item)
                        inventory.quantity -= item.quantity
                        inventory.save()
                        break
                    # Create an inventory history entry
                    inventory = Inventory.objects.get(item=item.item)
                    history = InventoryHistory(inventory=inventory, quantity=inventory.quantity, type="order", change=-item.quantity)
                    history.save()
                        
                
                # If the item was not found in any bin, raise a validation error
                else:
                    raise ValidationError(f"Not enough items in the bins for {item.item}.")

        

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
        # If there are more than 100 items in the bin, put the rest in the next bin
        # If there is no space in any bin, create a new bin
        if self.items.count() > 100:
            extra = self.items.count() - 100
            # For all of the bins in the location except the current one
            for bin in Bin.objects.filter(location=self.location).exclude(pk=self.pk):
                # Check if there is space in the bin
                while bin.items.count() < 100:
                    # If there is, move an item from the current bin to the bin with space
                    bin.items.add(self.items.first())
                    self.items.remove(self.items.first())
                    extra -= 1
                    if extra == 0:
                        break
                if extra == 0:
                    break
            # If there are still items left, create a new bin
            if extra > 0:
                new_bin = Bin(location=self.location)
                new_bin.save()
                for i in range(extra):
                    new_bin.items.add(self.items.first())
                    self.items.remove(self.items.first())



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