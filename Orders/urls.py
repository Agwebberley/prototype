from django.urls import path
from .views import OrderListView, OrderCreateView, OrderUpdateView, OrderDeleteView
from .views import OrderDetailView, OrderItemCreateView, OrderItemUpdateView, OrderItemDeleteView

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('<int:pk>/details/', OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/item/create/', OrderItemCreateView.as_view(), name='order_item_create'),
    path('<int:pk>/item/<int:order_item_id>/update/', OrderItemUpdateView.as_view(), name='order_item_update'),
    path('<int:pk>/item/<int:order_item_id>/delete/', OrderItemDeleteView.as_view(), name='order_item_delete'),
]
