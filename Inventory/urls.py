# This code is defining the URL patterns for a Django web application. It imports the `path` function
# from the `django.urls` module and four views (`CustomerListView`, `CustomerCreateView`, `CustomerUpdateView`,
# and `CustomerDeleteView`) from the application's `views.py` file.
from django.urls import path
from .views import InventoryListView, InventoryUpdateView, InventoryHistoryListView, PickListView, PickUpdateView, BinListView

app_name = 'inventory'

urlpatterns = [
    path('', InventoryListView.as_view(), name='inventory_list'),
    path('<int:pk>/update/', InventoryUpdateView.as_view(), name='inventory_update'),
    path('<int:pk>/history/', InventoryHistoryListView.as_view(), name='inventoryhistory_list'),
    path('pick/', PickListView.as_view(), name='pick_list'),
    path('pick/<int:pk>/update/', PickUpdateView.as_view(), name='pick_update'),
    path('bin/', BinListView.as_view(), name='bin_list'),
]