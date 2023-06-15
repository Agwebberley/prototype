from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Inventory, InventoryHistory, Pick, Bin, Location


# Inventory
class InventoryListView(ListView):
    model = Inventory
    template_name = 'inventory_list.html'

    # Set model_fields to the fields of the model
    model_fields = [field.name for field in Inventory._meta.get_fields()]
    model_fields.remove('inventoryhistory')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_fields'] = self.model_fields
        return context

class InventoryUpdateView(UpdateView):
    model = Inventory
    fields = ('quantity')
    template_name = 'inventory_form.html'

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)
    
    def get_success_url(self):
        return reverse_lazy('inventory_list')
    
    # Create a new InventoryHistory entry when Inventory is updated
    def form_valid(self, form):
        form.instance.inventory = self.object
        form.instance.item = self.object.item
        form.instance.quantity = self.object.quantity
        form.instance.type = "adjustment"
        return super().form_valid(form)

# InventoryHistory
class InventoryHistoryListView(ListView):
    model = InventoryHistory
    template_name = 'inventory_list.html'

    # Set model_fields to the fields of the model
    model_fields = [field.name for field in Inventory._meta.get_fields()]
    patterns = ['inventory_update', 'inventoryhistory_list', 'pick_list', 'pick_update', 'bin_list']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_fields'] = self.model_fields
        context['patterns'] = self.patterns
        return context

    # Limit to InventoryHistory for a specific item
    def get_queryset(self):
        Inventory = self.kwargs['pk']
        return InventoryHistory.objects.filter(Inventory=Inventory.id)
    
# Pick
class PickListView(ListView):
    model = Pick
    template_name = 'pick.html'

    # Set model_fields to the fields of the model
    model_fields = [field.name for field in Inventory._meta.get_fields()]
    model_fields.remove('inventoryhistory')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_fields'] = self.model_fields
        return context

class PickUpdateView(UpdateView):
    model = Pick
    fields = ('is_complete')
    template_name = 'pick_form.html'

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)
    
    def get_success_url(self):
        return reverse_lazy('pick_list')

# Bin
class BinListView(ListView):
    model = Bin
    template_name = 'bin.html'

class BinDetailView(DetailView):
    model = Bin
    template_name = 'bin_detail.html'

# Location
class LocationCreateView(CreateView):
    model = Location
    template_name = 'location.html'

