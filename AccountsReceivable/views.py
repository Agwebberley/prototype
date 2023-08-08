from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import accountsreceivable, accountsreceivablehistory, accountsreceivablepayment
from decimal import Decimal

# TODO: Create a new account if the account is marked as paid and the order is updated to be greater than the paid amount
# Accounts Receivable
class AccountsReceivableListView(ListView):
    model = accountsreceivable
    template_name = 'listview.html'

    # Set model_fields to the fields of the model
    model_fields = [field.name for field in accountsreceivable._meta.get_fields()]

    try: 
        model_fields.remove('_accountsreceivablehistory')
        model_fields.remove('_accountsreceivablepayment')
    except: pass
    
    patterns = {'Toggle Paid': 'accounts_receivable:toggle_paid', 'Details': 'accounts_receivable:account_details', 'Make Payment': 'accounts_receivable:make_payment'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_fields'] = self.model_fields
        context['patterns'] = (self.patterns)
        context['h1'] = 'Accounts Receivable'
        return context

class AccountTogglePaidView(View):
    def get(self, request, *args, **kwargs):
        accounts_receivable_id = kwargs.get('pk')
        # Create a payment entry
        payment = accountsreceivablepayment()
        payment.accounts_receivable = get_object_or_404(accountsreceivable, pk=accounts_receivable_id)
        if not payment.accounts_receivable.paid:
            if payment.accounts_receivable.amount_paid is None:
                payment.accounts_receivable.amount_paid = Decimal('0')
            payment.amount = payment.accounts_receivable.amount - payment.accounts_receivable.amount_paid
        else:
            payment.amount = -payment.accounts_receivable.amount_paid # type: ignore
            payment.accounts_receivable.paid = False
        payment.save()
        # Send back to the list view
        return redirect('/accounts_receivable/')

class AccountAddPayment(CreateView):
    model = accountsreceivablepayment
    fields = ['amount']
    template_name = 'add_payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts_receivable'] = get_object_or_404(accountsreceivable, pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        form.instance.accounts_receivable = get_object_or_404(accountsreceivable, pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts_receivable:accounts_receivable_list')

class AccountChangeDueDateView(UpdateView):
    model = accountsreceivable
    fields = ['due_date']
    template_name = 'accounts_receivable_due_date.html'

    def get_success_url(self):
        return reverse_lazy('accounts_receivable:accounts_receivable_list')

class AccountDetailView(ListView):
    model = accountsreceivablehistory
    template_name = 'accounts_receivable_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts_receivable'] = get_object_or_404(accountsreceivable, pk=self.kwargs.get('pk'))
        return context

    def get_queryset(self):
        accounts_receivable = get_object_or_404(accountsreceivable, pk=self.kwargs.get('pk'))
        return accountsreceivablehistory.objects.filter(accounts_receivable=accounts_receivable)