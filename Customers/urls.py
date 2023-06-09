# This code is defining the URL patterns for a Django web application. It imports the `path` function
# from the `django.urls` module and four views (`CustomerListView`, `CustomerCreateView`, `CustomerUpdateView`,
# and `CustomerDeleteView`) from the application's `views.py` file.
from django.urls import path
from .views import CustomerListView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView
from .views import InventoryListView, InventoryCreateView, InventoryUpdateView, InventoryDeleteView

urlpatterns = [
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('create/', CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/update/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
    path('inventory/', InventoryListView.as_view(), name='inventory_list'),
    path('inventory/create/', InventoryCreateView.as_view(), name='inventory_create'),
    path('inventory/<int:pk>/update/', InventoryUpdateView.as_view(), name='inventory_update'),
    path('inventory/<int:pk>/delete/', InventoryDeleteView.as_view(), name='inventory_delete'),
]