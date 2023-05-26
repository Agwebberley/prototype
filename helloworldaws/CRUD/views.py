from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from .models import Data
from .forms import DataForm
from django.shortcuts import redirect, render

class DataListView(ListView):
    model = Data
    template_name = 'data_list.html'

class DataCreateView(View):
    def get(self, request):
        form = DataForm()
        return render(request, 'data_form.html', {'form': form})
    def post(self, request):
        form = DataForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.author = request.user
            data.save()
            return redirect('data_list')
        return render(request, 'data_form.html', {'form': form})

class DataUpdateView(UpdateView):
    model = Data
    form_class = DataForm
    template_name = 'data_form.html'

class DataDeleteView(DeleteView):
    model = Data
    success_url = reverse_lazy('data_list')
    template_name = 'data_confirm_delete.html'

