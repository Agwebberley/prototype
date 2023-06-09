from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import AccountsReceivable
from .forms import AccountsReceivableForm

# Accounts Receivable
class AccountsReceivableListView(ListView):
    model = AccountsReceivable
    template_name = 'accounts_receivable.html'

class AccountsReceivableCreateView(CreateView):
    model = AccountsReceivable
    form_class = AccountsReceivableForm
    template_name = 'accounts_receivable_form.html'

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

    def get_success_url(self):
        return reverse_lazy('accounts_receivable_list')

class AccountsReceivableUpdateView(UpdateView):
    model = AccountsReceivable
    form_class = AccountsReceivableForm
    template_name = 'accounts_receivable_form.html'

class AccountsReceivableDeleteView(DeleteView):
    model = AccountsReceivable
    success_url = reverse_lazy('accounts_receivable_list')
    template_name = 'accounts_receivable_confirm_delete.html'

class AccountsReceivableTogglePaidView(View):
    def post(self, request, *args, **kwargs):
        accounts_receivable_id = kwargs.get('pk')
        accounts_receivable = get_object_or_404(AccountsReceivable, pk=accounts_receivable_id)
        accounts_receivable.paid = not accounts_receivable.paid
        accounts_receivable.save()
        return reverse_lazy('accounts_receivable_list')