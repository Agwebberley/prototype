from django import forms
from .models import Manufacture

class ManufactureForm(forms.Form):
    class Meta:
        model = Manufacture
        fields = ('item', 'quantity')
        widgets = {
            'item': forms.Select(attrs={'class': 'w-half px-3 py-2 mb-4 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:outline-none sm:text-sm text-black'}),
            'quantity': forms.NumberInput(attrs={'class': 'w-half px-3 py-2 mb-4 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:outline-none sm:text-sm text-black'}),
        }