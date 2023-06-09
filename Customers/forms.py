from django import forms
from .models import Customers, Items, Orders

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ('name', 'billing_address', 'shipping_address', 'phone', 'email')

class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ('name', 'description', 'price', 'target_inv', 'current_inv', 'reorder_level')

class OrderForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customers.objects.all().order_by('name'))
    item = forms.ModelChoiceField(queryset=Items.objects.all().order_by('name'))
    class Meta:
        model = Orders
        fields = ('customer', 'item', 'quantity')