# This code is defining the URL patterns for a Django web application. It imports the `path` function
# from the `django.urls` module and four views (`CustomerListView`, `CustomerCreateView`, `CustomerUpdateView`,
# and `CustomerDeleteView`) from the application's `views.py` file.
from django.urls import path
from .views import CustomerListView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView, LogView, IndexView
from .views import OrderListView, OrderCreateView, OrderUpdateView, OrderDeleteView
from .views import ItemListView, ItemCreateView, ItemUpdateView, ItemDeleteView

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
    path('items/', ItemListView.as_view(), name='item_list'),
    path('items/create/', ItemCreateView.as_view(), name='item_create'),
    path('items/<int:pk>/update/', ItemUpdateView.as_view(), name='item_update'),
    path('items/<int:pk>/delete/', ItemDeleteView.as_view(), name='item_delete'),
]