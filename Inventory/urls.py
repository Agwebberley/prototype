# This code is defining the URL patterns for a Django web application. It imports the `path` function
# from the `django.urls` module and four views (`CustomerListView`, `CustomerCreateView`, `CustomerUpdateView`,
# and `CustomerDeleteView`) from the application's `views.py` file.
from django.urls import path
from .views import InventoryListView, InventoryUpdateView

app_name = 'inventory'

urlpatterns = [
    path('', InventoryListView.as_view(), name='inventory_list'),
    path('<int:pk>/update/', InventoryUpdateView.as_view(), name='inventory_update'),
]