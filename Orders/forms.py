from django import forms
from .models import Orders, OrderItem
from Customers.models import Customers
from Items.models import Items

class OrderForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customers.objects.all().order_by('name'))
    
    class Meta:
        model = Orders
        fields = ('customer',)

        widgets = {
            'customer': forms.Select(attrs={'class': 'w-half px-3 py-2 mb-4 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:outline-none sm:text-sm text-black'})
        }
    

class OrderItemForm(forms.ModelForm):
    item = forms.ModelChoiceField(queryset=Items.objects.all().order_by('name'))
    
    class Meta:
        model = OrderItem
        fields = ('item', 'quantity')

        widgets = {
            'item': forms.Select(attrs={'class': 'w-half px-3 py-2 mb-4 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:outline-none sm:text-sm text-black'}),
            'quantity': forms.NumberInput(attrs={'class': 'w-half px-3 py-2 mb-4 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:outline-none sm:text-sm text-black'})
        }


