# This code is defining the URL patterns for a Django web application. It imports the `path` function
# from the `django.urls` module and four views (`CustomerListView`, `CustomerCreateView`, `CustomerUpdateView`,
# and `CustomerDeleteView`) from the application's `views.py` file.
from django.urls import path
from .views import CustomerListView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView, LogView, IndexView
from .views import OrderListView, OrderCreateView, OrderUpdateView, OrderDeleteView
from .views import AccountsReceivableListView, AccountsReceivableCreateView, AccountsReceivableUpdateView, AccountsReceivableDeleteView, AccountsReceivableTogglePaidView
from .views import InventoryListView, InventoryCreateView, InventoryUpdateView, InventoryDeleteView

urlpatterns = [
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('create/', CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/update/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
    path('log/', LogView.as_view(), name='log'),
    path('', IndexView.as_view(), name='index'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('accounts_receivable/', AccountsReceivableListView.as_view(), name='accounts_receivable_list'),
    path('accounts_receivable/create/', AccountsReceivableCreateView.as_view(), name='accounts_receivable_create'),
    path('accounts_receivable/<int:pk>/update/', AccountsReceivableUpdateView.as_view(), name='accounts_receivable_update'),
    path('accounts_receivable/<int:pk>/delete/', AccountsReceivableDeleteView.as_view(), name='accounts_receivable_delete'),
    path('accounts_receivable/<int:pk>/pay/', AccountsReceivableTogglePaidView.as_view(), name='accounts_receivable_pay'),
    path('inventory/', InventoryListView.as_view(), name='inventory_list'),
    path('inventory/create/', InventoryCreateView.as_view(), name='inventory_create'),
    path('inventory/<int:pk>/update/', InventoryUpdateView.as_view(), name='inventory_update'),
    path('inventory/<int:pk>/delete/', InventoryDeleteView.as_view(), name='inventory_delete'),
]