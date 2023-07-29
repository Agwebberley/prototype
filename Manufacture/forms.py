
from django import forms

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'w-half px-3 py-2 mb-4 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:outline-none sm:text-sm text-black'


class manufactureForm(forms.ModelForm):
    class Meta:
        from .models import manufacture
        model = manufacture
        fields = ('quantity', 'date', 'items', 'manufacturehistory')

class manufacturehistoryForm(forms.ModelForm):
    class Meta:
        from .models import manufacturehistory
        model = manufacturehistory
        fields = ('manufacture', 'item', 'quantity', 'timestamp', 'is_complete')

