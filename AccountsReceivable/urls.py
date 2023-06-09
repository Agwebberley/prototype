from django.urls import path
from .views import AccountsReceivableListView, AccountsReceivableCreateView, AccountsReceivableUpdateView, AccountsReceivableDeleteView, AccountsReceivableTogglePaidView

urlpatterns = [
    path('', AccountsReceivableListView.as_view(), name='accounts_receivable_list'),
    path('create/', AccountsReceivableCreateView.as_view(), name='accounts_receivable_create'),
    path('<int:pk>/update/', AccountsReceivableUpdateView.as_view(), name='accounts_receivable_update'),
    path('<int:pk>/delete/', AccountsReceivableDeleteView.as_view(), name='accounts_receivable_delete'),
    path('<int:pk>/pay/', AccountsReceivableTogglePaidView.as_view(), name='accounts_receivable_pay')
]