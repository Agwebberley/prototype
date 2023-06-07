# This code is defining the URL patterns for a Django web application. It imports the `path` function
# from the `django.urls` module and four views (`CustomerListView`, `CustomerCreateView`, `CustomerUpdateView`,
# and `CustomerDeleteView`) from the application's `views.py` file.
from django.urls import path
from .views import CustomerListView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView, LogView, IndexView

urlpatterns = [
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('create/', CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/update/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
    path('log/', LogView.as_view(), name='log'),
    path('', IndexView.as_view(), name='index'),
]