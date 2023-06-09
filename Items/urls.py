from django.urls import path
from .views import ItemListView, ItemCreateView, ItemUpdateView, ItemDeleteView

urlpatterns = [
    path('', ItemListView.as_view(), name='item_list'),
    path('create/', ItemCreateView.as_view(), name='item_create'),
    path('<int:pk>/update/', ItemUpdateView.as_view(), name='item_update'),
    path('<int:pk>/delete/', ItemDeleteView.as_view(), name='item_delete')
]