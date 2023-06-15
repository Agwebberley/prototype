from django import forms
from .models import Inventory

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('quantity',)
        # Use tailwind classes for styling
        widgets = {
            'quantity': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-half py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }
