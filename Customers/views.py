# This is a set of Django views for creating, updating, and deleting instances of a Customer model, with a
# list view to display all instances.
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from .models import Customers, LogMessage, Items, Orders
from .forms import CustomerForm, ItemForm, OrderForm
from django.shortcuts import render

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


class LogView(ListView):
    model = LogMessage
    template_name = 'log.html'

    def get_context_customer(self, **kwargs):
        context = super().get_context_customer(**kwargs)
        context['log_list'] = LogMessage.objects.order_by('-created_at')
        return context

# index.html
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

# Items
class ItemListView(ListView):
    model = Items
    template_name = 'items.html'

class ItemCreateView(CreateView):
    model = Items
    form_class = ItemForm
    template_name = 'item_form.html'

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

    def get_success_url(self):
        return reverse_lazy('item_list')

class ItemUpdateView(UpdateView):
    model = Items
    form_class = ItemForm
    template_name = 'item_form.html'

class ItemDeleteView(DeleteView):
    model = Items
    success_url = reverse_lazy('item_list')
    template_name = 'item_confirm_delete.html'

# Orders
class OrderListView(ListView):
    model = Orders
    template_name = 'orders.html'

class OrderCreateView(CreateView):
    model = Orders
    form_class = OrderForm
    template_name = 'order_form.html'

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

    def get_success_url(self):
        return reverse_lazy('order_list')

class OrderUpdateView(UpdateView):
    model = Orders
    form_class = OrderForm
    template_name = 'order_form.html'

class OrderDeleteView(DeleteView):
    model = Orders
    success_url = reverse_lazy('order_list')
    template_name = 'order_confirm_delete.html'
