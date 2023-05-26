# This is a set of Django views for creating, updating, and deleting instances of a Data model, with a
# list view to display all instances.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from .models import Data
from .forms import DataForm
from django.shortcuts import redirect, render

class DataListView(ListView):
    model = Data
    template_name = 'data_list.html'

class DataCreateView(CreateView):
    model = Data
    form_class = DataForm
    template_name = 'data_form.html'
    success_url = reverse_lazy('data_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('data_list')


        

class DataUpdateView(UpdateView):
    model = Data
    form_class = DataForm
    template_name = 'data_form.html'

class DataDeleteView(DeleteView):
    model = Data
    success_url = reverse_lazy('data_list')
    template_name = 'data_confirm_delete.html'

