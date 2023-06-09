from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Items
from .forms import ItemForm

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