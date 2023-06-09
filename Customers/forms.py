from django import forms
from .models import Customers, AccountsReceivable, Inventory

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ('name', 'billing_address', 'shipping_address', 'phone', 'email')


class AccountsReceivableForm(forms.ModelForm):
    class Meta:
        model = AccountsReceivable
        fields = ('order', 'amount', 'due_date')

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('item', 'quantity')
