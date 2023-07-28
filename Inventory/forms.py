
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
        fields = ('id', 'name', 'location_id', 'Inventory_bin_location_id_1ddfd1cf_fk_Inventory_location_id')

class bin_itemsForm(forms.ModelForm):
    class Meta:
        from .models import bin_items
        model = bin_items
        fields = ('id', 'bin_id', 'items_id', 'Inventory_bin_items_bin_id_ffef0ad8_fk_Inventory_bin_id', 'Inventory_bin_items_items_id_92ca6290_fk_Items_items_id')

class inventoryForm(forms.ModelForm):
    class Meta:
        from .models import inventory
        model = inventory
        fields = ('id', 'quantity', 'last_updated', 'typeI', 'item_id', 'Inventory_inventory_item_id_7b7c9e4a_fk_Items_items_id')

class inventoryhistoryForm(forms.ModelForm):
    class Meta:
        from .models import inventoryhistory
        model = inventoryhistory
        fields = ('id', 'quantity', 'change', 'typeI', 'timestamp', 'inventory_id', 'item_id', 'Inventory_inventoryh_inventory_id_73a70a49_fk_Inventory', 'Inventory_inventoryhistory_item_id_2785e3cf_fk_Items_items_id')

class locationForm(forms.ModelForm):
    class Meta:
        from .models import location
        model = location
        fields = ('id', 'name', 'amount_of_bins')

class pickForm(forms.ModelForm):
    class Meta:
        from .models import pick
        model = pick
        fields = ('id', 'is_complete', 'location_id', 'order_id', 'Inventory_pick_location_id_e5a85fa0_fk_Inventory_location_id', 'Inventory_pick_order_id_9b509292_fk_Orders_orders_id')

class pick_itemsForm(forms.ModelForm):
    class Meta:
        from .models import pick_items
        model = pick_items
        fields = ('id', 'pick_id', 'orderitem_id', 'Inventory_pick_items_orderitem_id_443416dd_fk_Orders_or', 'Inventory_pick_items_pick_id_1a71d8fb_fk_Inventory_pick_id')

