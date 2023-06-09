from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Inventory
from .forms import InventoryForm


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
