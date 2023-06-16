from django import forms
from .models import Inventory, Pick

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('quantity',)
        # Use tailwind classes for styling
        widgets = {
            'quantity': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-half py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }

class PickForm(forms.ModelForm):
    class Meta:
        model = Pick
        fields = ('location', 'is_complete',)
        # Use tailwind classes for styling
        widgets = {
            'location' : forms.Select(attrs={'class': 'shadow appearance-none border rounded w-half py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'is_complete': forms.CheckboxInput(attrs={'class': 'shadow appearance-none border rounded'})
        }