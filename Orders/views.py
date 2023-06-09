from typing import Any
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Orders, OrderItem
from .forms import OrderForm, OrderItemForm

# Orders
class OrderListView(ListView):
    model = Orders
    template_name = 'listview.html'

    # Set model_fields to the fields of the model
    model_fields = [field.name for field in Orders._meta.get_fields()]
    model_fields.remove('orderitem')
    model_fields.remove('pick')
    model_fields.remove('accountsreceivable')
    model_fields.append('get_total_price')

    patterns = {'Details': 'orders:order_detail' ,'Update': 'orders:order_update', 'Delete': 'orders:order_delete'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_fields'] = self.model_fields
        context['patterns'] = (self.patterns)
        context['h1'] = 'Orders'
        context['bpattern'] = 'orders:order_create'
        context['bname'] = 'Create Order'
        return context

class OrderCreateView(CreateView):
    model = Orders
    form_class = OrderForm
    template_name = 'order_form.html'

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

    def get_success_url(self):
        return reverse_lazy('orders:order_list')

class OrderUpdateView(UpdateView):
    model = Orders
    form_class = OrderForm
    template_name = 'form.html'

class OrderDeleteView(DeleteView):
    model = Orders
    success_url = reverse_lazy('orders:order_list')
    template_name = 'delete.html'

    def get_context_data(self, **kwargs):
        object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Order ' + str(object.pk)
        context['pattern'] = 'orders:order_list'
        return context

# Order Items
class OrderDetailView(ListView):
    model = OrderItem
    template_name = 'order_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(order_id=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = get_object_or_404(Orders, pk=self.kwargs['pk'])
        return context

class OrderItemCreateView(CreateView):
    model = OrderItem
    form_class = OrderItemForm
    template_name = 'form.html'

    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self.object.order.pk}) # type: ignore

    def form_valid(self, form):
        order = get_object_or_404(Orders, pk=self.kwargs['pk'])
        form.instance.order = order
        return super().form_valid(form)

class OrderItemUpdateView(UpdateView):
    model = OrderItem
    form_class = OrderItemForm
    template_name = 'form.html'

    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_object(self, queryset=None):
        order_item_id = self.kwargs.get('order_item_id')
        return OrderItem.objects.get(id=order_item_id)

class OrderItemDeleteView(DeleteView):
    model = OrderItem
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Order Item ' + str(object.pk)
        context['pattern'] = 'orders:order_detail'
        return super().get_context_data(**kwargs)