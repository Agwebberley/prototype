from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import inventory, inventoryhistory, pick, bin, location
from .forms import inventoryForm, pickForm

# Inventory
class InventoryListView(ListView):
    model = inventory
    template_name = 'listview.html'

    # Set model_fields to the fields of the model
    model_fields = [field.name for field in inventory._meta.get_fields()]
    print(model_fields)
    try: 
        model_fields.remove('_inventoryhistory')
        model_fields.remove('typeI')
    except: pass
    patterns = {'Update': 'inventory:inventory_update', 'History': 'inventory:inventoryhistory_list'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_fields'] = self.model_fields
        context['patterns'] = self.patterns
        context['h1'] = 'Inventory'
        return context

class InventoryUpdateView(UpdateView):
    model = inventory
    form_class = inventoryForm
    template_name = 'form.html'

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)
    
    def get_success_url(self):
        return reverse_lazy('inventory:inventory_list')
    
    
    

# InventoryHistory
class InventoryHistoryListView(ListView):
    model = inventoryhistory
    template_name = 'listview.html'

    # Set model_fields to the fields of the model
    model_fields = [field.name for field in inventoryhistory._meta.get_fields()]
    try:
        model_fields.remove('inventory')
        model_fields.remove('item')
    except: pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_fields'] = self.model_fields
        context['h1'] = 'Inventory History'
        return context

    # Limit to InventoryHistory for a specific item
    def get_queryset(self):
        inventory = self.kwargs['pk']
        return inventoryhistory.objects.filter(inventory=inventory)
    
# Pick
class PickListView(ListView):
    model = pick
    template_name = 'listview.html'

    # Set model_fields to the fields of the model
    model_fields = [field.name for field in pick._meta.get_fields()]
    try: model_fields.remove('_pick_items')
    except: pass
    # Action Button Url Patterns
    patterns = {'Pick Order': 'inventory:pick_update'}   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_fields'] = self.model_fields
        context['patterns'] = self.patterns
        context['h1'] = 'Pick List'
        return context

class PickUpdateView(UpdateView):
    model = pick
    form_class = pickForm
    template_name = 'form.html'

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)
    
    def get_success_url(self):
        return reverse_lazy('pick_list')

# Bin
class BinListView(ListView):
    model = bin
    template_name = 'listview.html'

    # Set model_fields to the fields of the model
    model_fields = [field.name for field in bin._meta.get_fields()]
    try: model_fields.remove('_bin_items')
    except: pass
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

