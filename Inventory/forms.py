
from django import forms

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'w-half px-3 py-2 mb-4 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:outline-none sm:text-sm text-black'


class binForm(forms.ModelForm):
    class Meta:
        from .models import bin
        model = bin
        fields = ('name', 'location_id')

class bin_itemsForm(forms.ModelForm):
    class Meta:
        from .models import bin_items
        model = bin_items
        fields = ('bin_id', 'items_id')

class inventoryForm(forms.ModelForm):
    class Meta:
        from .models import inventory
        model = inventory
        fields = ('quantity', 'last_updated', 'typeI', 'item_id')

class inventoryhistoryForm(forms.ModelForm):
    class Meta:
        from .models import inventoryhistory
        model = inventoryhistory
        fields = ('quantity', 'change', 'typeI', 'timestamp', 'inventory_id', 'item_id')

class locationForm(forms.ModelForm):
    class Meta:
        from .models import location
        model = location
        fields = ('name', 'amount_of_bins')

class pickForm(forms.ModelForm):
    class Meta:
        from .models import pick
        model = pick
        fields = ('is_complete', 'location_id', 'order_id')

class pick_itemsForm(forms.ModelForm):
    class Meta:
        from .models import pick_items
        model = pick_items
        fields = ('pick_id', 'orderitem_id')

