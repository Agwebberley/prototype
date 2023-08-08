from django.shortcuts import render
from django.views.generic import ListView, View
from .models import logmessage

# Create your views here.
class LogView(ListView):
    model = logmessage
    template_name = 'listview.html'
    
    # Set model_fields to the fields of the model
    model_fields = [field.name for field in logmessage._meta.get_fields()]
    
    try:
        model_fields.remove('id')
        # Move the created_at field to the front
        model_fields.insert(0, model_fields.pop(model_fields.index('created_at')))
    except: pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_fields'] = self.model_fields
        context['h1'] = 'Log'
        # reverse the list so the newest messages are at the top
        context['object_list'] = reversed(context['object_list'])
        return context

# index.html
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')