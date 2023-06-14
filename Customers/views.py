# This is a set of Django views for creating, updating, and deleting instances of a Customer model, with a
# list view to display all instances.
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Customers
from .forms import CustomerForm

class CustomerListView(ListView):
    model = Customers
    template_name = 'customers.html'

    # Set model_fields to the fields of the model
    model_fields = [field.name for field in Customers._meta.get_fields()]
    model_fields.remove('orders')
    print(model_fields)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_fields'] = self.model_fields
        return context

class CustomerCreateView(CreateView):
    model = Customers
    form_class = CustomerForm
    template_name = 'customer_form.html'

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)


    def get_success_url(self):
        return reverse_lazy('customers:customer_list')

class CustomerUpdateView(UpdateView):
    model = Customers
    form_class = CustomerForm
    template_name = 'customer_form.html'

class CustomerDeleteView(DeleteView):
    model = Customers
    success_url = reverse_lazy('customers:customer_list')
    template_name = 'customer_confirm_delete.html'