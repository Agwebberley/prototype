from django.shortcuts import render
from django.views.generic import ListView, View
from .models import LogMessage

# Create your views here.
class LogView(ListView):
    model = LogMessage
    template_name = 'log.html'

    def get_context_customer(self, **kwargs):
        context = super().get_context_customer(**kwargs)
        context['log_list'] = LogMessage.objects.order_by('-created_at')
        return context

# index.html
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')