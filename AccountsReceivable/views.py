from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import AccountsReceivable, AccountsReceivableHistory, AccountsReceivablePayment

# Accounts Receivable
class AccountsReceivableListView(ListView):
    model = AccountsReceivable
    template_name = 'accounts_receivable.html'

class AccountTogglePaidView(View):
    def post(self, request, *args, **kwargs):
        accounts_receivable_id = kwargs.get('pk')
        # Create a payment entry
        payment = AccountsReceivablePayment()
        payment.accounts_receivable = get_object_or_404(AccountsReceivable, pk=accounts_receivable_id)
        if not payment.accounts_receivable.paid:
            payment.amount = payment.accounts_receivable.amount - payment.accounts_receivable.amount_paid
        else:
            payment.amount = -payment.accounts_receivable.amount_paid
        payment.save()
        return reverse_lazy('accountsreceivable:accounts_receivable_list')

class AccountAddPayment(CreateView):
    model = AccountsReceivablePayment
    fields = ['amount']
    template_name = 'accounts_receivable_payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts_receivable'] = get_object_or_404(AccountsReceivable, pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        form.instance.accounts_receivable = get_object_or_404(AccountsReceivable, pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accountsreceivable:accounts_receivable_list')

class AccountChangeDueDateView(UpdateView):
    model = AccountsReceivable
    fields = ['due_date']
    template_name = 'accounts_receivable_due_date.html'

    def get_success_url(self):
        return reverse_lazy('accountsreceivable:accounts_receivable_list')

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