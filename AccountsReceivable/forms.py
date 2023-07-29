
from django import forms

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'w-half px-3 py-2 mb-4 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:outline-none sm:text-sm text-black'


class accountsreceivableForm(forms.ModelForm):
    class Meta:
        from .models import accountsreceivable
        model = accountsreceivable
        fields = ('amount', 'due_date', 'paid', 'paid_date', 'amount_paid', 'orders')

class accountsreceivablehistoryForm(forms.ModelForm):
    class Meta:
        from .models import accountsreceivablehistory
        model = accountsreceivablehistory
        fields = ('field', 'old_value', 'new_value', 'date', 'accountsreceivable')

class accountsreceivablepaymentForm(forms.ModelForm):
    class Meta:
        from .models import accountsreceivablepayment
        model = accountsreceivablepayment
        fields = ('amount', 'date', 'accountsreceivable')

