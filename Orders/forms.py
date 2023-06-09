from django import forms
from .models import Orders
from Customers.models import Customers
from Items.models import Items

class OrderForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customers.objects.all().order_by('name'))
    item = forms.ModelChoiceField(queryset=Items.objects.all().order_by('name'))
    class Meta:
        model = Orders
        fields = ('customer', 'item', 'quantity')