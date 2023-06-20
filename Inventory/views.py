from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Inventory, InventoryHistory, Pick, Bin, Location
from .forms import InventoryForm, PickForm

# Inventory
class InventoryListView(ListView):
    model = Inventory
    template_name = 'listview.html'

    # Set model_fields to the fields of the model
    model_fields = [field.name for field in Inventory._meta.get_fields()]
    model_fields.remove('inventoryhistory')
    model_fields.remove('typeI')
    patterns = {'Update': 'inventory:inventory_update', 'History': 'inventory:inventoryhistory_list'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_fields'] = self.model_fields
        context['patterns'] = self.patterns
        return context

class InventoryUpdateView(UpdateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'form.html'

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)
    
    def get_success_url(self):
        return reverse_lazy('inventory:inventory_list')
    
    
    

# InventoryHistory
class InventoryHistoryListView(ListView):
    model = InventoryHistory
    template_name = 'listview.html'

    # Set model_fields to the fields of the model
    model_fields = [field.name for field in InventoryHistory._meta.get_fields()]
    model_fields.remove('inventory')
    model_fields.remove('item')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_fields'] = self.model_fields
        return context

    # Limit to InventoryHistory for a specific item
    def get_queryset(self):
        Inventory = self.kwargs['pk']
        return InventoryHistory.objects.filter(inventory=Inventory)
    
# Pick
class PickListView(ListView):
    model = Pick
    template_name = 'listview.html'

    # Set model_fields to the fields of the model
    model_fields = [field.name for field in Pick._meta.get_fields()]
    model_fields.remove('items')

    # Action Button Url Patterns
    patterns = {'Pick Order': 'inventory:pick_update'}   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_fields'] = self.model_fields
        context['patterns'] = self.patterns
        context['h1'] = 'Pick List'
        return context

class PickUpdateView(UpdateView):
    model = Pick
    form_class = PickForm
    template_name = 'form.html'

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)
    
    def get_success_url(self):
        return reverse_lazy('pick_list')

# Bin
class BinListView(ListView):
    model = Bin
    template_name = 'listview.html'

    # Set model_fields to the fields of the model
    model_fields = [field.name for field in Bin._meta.get_fields()]
    model_fields.remove('items')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_fields'] = self.model_fields
        context['h1'] = 'Bin List'
        return context

#class BinDetailView(DetailView):
#    model = Bin
#    template_name = 'bin_detail.html'

# Location
#class LocationCreateView(CreateView):
#    model = Location
#    template_name = 'location.html'

