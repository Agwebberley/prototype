from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Manufacture
from .forms import ManufactureForm

class ManufactureList(ListView):
    model = Manufacture
    template_name = 'listview.html'
    model_fields = [field.name for field in Manufacture._meta.get_fields()]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_fields'] = self.model_fields
        context['h1'] = 'Manufacture'
        context['bpattern'] = 'manufacture:manufacture_create'
        context['bname'] = 'Create Manufacturing Order'
        return context
    
class ManufactureCreate(CreateView):
    model = Manufacture
    form_class = ManufactureForm
    template_name = 'form.html'
