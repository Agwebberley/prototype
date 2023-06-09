from django import forms
from .models import Customers, Inventory

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ('name', 'billing_address', 'shipping_address', 'phone', 'email')

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('item', 'quantity')
