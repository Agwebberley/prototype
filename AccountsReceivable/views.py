from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import AccountsReceivable, AccountsReceivableHistory, AccountsReceivablePayment
from decimal import Decimal

# TODO: Create a new account if the account is marked as paid and the order is updated to be greater than the paid amount
# Accounts Receivable
class AccountsReceivableListView(ListView):
    model = AccountsReceivable
    template_name = 'accounts_receivable.html'

class AccountTogglePaidView(View):
    def get(self, request, *args, **kwargs):
        accounts_receivable_id = kwargs.get('pk')
        # Create a payment entry
        payment = AccountsReceivablePayment()
        payment.accounts_receivable = get_object_or_404(AccountsReceivable, pk=accounts_receivable_id)
        if not payment.accounts_receivable.paid:
            if payment.accounts_receivable.amount_paid is None:
                payment.accounts_receivable.amount_paid = Decimal('0')
            payment.amount = payment.accounts_receivable.amount - payment.accounts_receivable.amount_paid
        else:
            payment.amount = -payment.accounts_receivable.amount_paid
            payment.accounts_receivable.paid = False
        payment.save()
        # Send back to the list view
        return redirect('/accounts_receivable/')

class AccountAddPayment(CreateView):
    model = AccountsReceivablePayment
    fields = ['amount']
    template_name = 'add_payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts_receivable'] = get_object_or_404(AccountsReceivable, pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        form.instance.accounts_receivable = get_object_or_404(AccountsReceivable, pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts_receivable:accounts_receivable_list')

class AccountChangeDueDateView(UpdateView):
    model = AccountsReceivable
    fields = ['due_date']
    template_name = 'accounts_receivable_due_date.html'

    def get_success_url(self):
        return reverse_lazy('accounts_receivable:accounts_receivable_list')

class AccountDetailView(ListView):
    model = AccountsReceivableHistory
    template_name = 'accounts_receivable_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts_receivable'] = get_object_or_404(AccountsReceivable, pk=self.kwargs.get('pk'))
        return context

    def get_queryset(self):
        accounts_receivable = get_object_or_404(AccountsReceivable, pk=self.kwargs.get('pk'))
        return AccountsReceivableHistory.objects.filter(accounts_receivable=accounts_receivable)