from django.forms import forms
from .models import AccountsReceivable

class AccountsReceivableForm(forms.ModelForm):
    class Meta:
        model = AccountsReceivable
        fields = ('order', 'amount', 'due_date')