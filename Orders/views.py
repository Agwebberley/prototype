from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Orders
from .forms import OrderForm

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