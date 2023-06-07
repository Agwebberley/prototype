from django import forms
from .models import Customers

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ('name', 'billing_address', 'shipping_address', 'phone', 'email')

 