from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import items
from .forms import itemsForm

# items
class ItemListView(ListView):
    model = items
    template_name = 'listview.html'

    # Set model_fields to the fields of the model
    model_fields = [field.name for field in items._meta.get_fields()]
    try: 
        model_fields.remove('orderitem')
        model_fields.remove('inventory')
        model_fields.remove('inventoryhistory')
        model_fields.remove('bin_items')
        model_fields.remove('manufacture')
    except: pass
    
    patterns = {'Update': 'items:item_update', 'Delete': 'items:item_delete'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_fields'] = self.model_fields
        context['patterns'] = (self.patterns)
        context['h1'] = 'Items'
        context['bpattern'] = 'items:item_create'
        context['bname'] = 'Create Item'
        return context

class ItemCreateView(CreateView):
    model = items
    form_class = itemsForm
    template_name = 'form.html'

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

    def get_success_url(self):
        return reverse_lazy('items:item_list')

class ItemUpdateView(UpdateView):
    model = items
    form_class = itemsForm
    template_name = 'form.html'
    success_url = reverse_lazy('items:item_list')

class ItemDeleteView(DeleteView):
    model = items
    success_url = reverse_lazy('items:item_list')
    template_name = 'delete.html'

    def get_context_data(self, **kwargs):
        object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Item ' + str(object.pk)
        context['pattern'] = 'items:item_list'
        return context