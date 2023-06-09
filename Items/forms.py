from django import forms
from .models import Items

class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ('name', 'description', 'price', 'target_inv', 'current_inv', 'reorder_level')