
from django import forms

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'w-half px-3 py-2 mb-4 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:outline-none sm:text-sm text-black'


class orderitemForm(forms.ModelForm):
    class Meta:
        from .models import orderitem
        model = orderitem
        fields = ('id', 'quantity', 'item_id', 'order_id', 'Orders_orderitem_item_id_ac00d823_fk_Items_items_id', 'Orders_orderitem_order_id_3570cd78_fk_Orders_orders_id')

class ordersForm(forms.ModelForm):
    class Meta:
        from .models import orders
        model = orders
        fields = ('id', 'ordered_date', 'updated_date', 'customer_id', 'Orders_orders_customer_id_dea32023_fk_Customers_customers_id')

