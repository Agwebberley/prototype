from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import manufacture
from .forms import manufactureForm

class ManufactureList(ListView):
    model = manufacture
    template_name = 'listview.html'
    model_fields = [field.name for field in manufacture._meta.get_fields()]

    try:
        model_fields.remove('manufacturehistory')
    except: pass
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_fields'] = self.model_fields
        context['h1'] = 'Manufacture'
        context['bpattern'] = 'manufacture:manufacture_create'
        context['bname'] = 'Create Manufacturing Order'
        return context
    
class ManufactureCreate(CreateView):
    model = manufacture
    form_class = manufactureForm
    template_name = 'form.html'
