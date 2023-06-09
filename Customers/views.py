# This is a set of Django views for creating, updating, and deleting instances of a Customer model, with a
# list view to display all instances.
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from .models import Customers, LogMessage, Items, Orders, AccountsReceivable, Inventory
from .forms import CustomerForm, ItemForm, OrderForm, AccountsReceivableForm, InventoryForm
from django.shortcuts import get_object_or_404, render

class CustomerListView(ListView):
    model = Customers
    template_name = 'customers.html'

class CustomerCreateView(CreateView):
    model = Customers
    form_class = CustomerForm
    template_name = 'customer_form.html'

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)


    def get_success_url(self):
        return reverse_lazy('customer_list')

class CustomerUpdateView(UpdateView):
    model = Customers
    form_class = CustomerForm
    template_name = 'customer_form.html'

class CustomerDeleteView(DeleteView):
    model = Customers
    success_url = reverse_lazy('customer_list')
    template_name = 'customer_confirm_delete.html'

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

# Inventory
class InventoryListView(ListView):
    model = Inventory
    template_name = 'inventory.html'

class InventoryCreateView(CreateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventory_form.html'

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

    def get_success_url(self):
        return reverse_lazy('inventory_list')

class InventoryUpdateView(UpdateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventory_form.html'

class InventoryDeleteView(DeleteView):
    model = Inventory
    success_url = reverse_lazy('inventory_list')
    template_name = 'inventory_confirm_delete.html'
