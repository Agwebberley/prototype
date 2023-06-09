from django.urls import path
from .views import AccountsReceivableListView, AccountsReceivableCreateView, AccountsReceivableUpdateView, AccountsReceivableDeleteView, AccountsReceivableTogglePaidView

urlpatterns = [
    path('accounts_receivable/', AccountsReceivableListView.as_view(), name='accounts_receivable_list'),
    path('accounts_receivable/create/', AccountsReceivableCreateView.as_view(), name='accounts_receivable_create'),
    path('accounts_receivable/<int:pk>/update/', AccountsReceivableUpdateView.as_view(), name='accounts_receivable_update'),
    path('accounts_receivable/<int:pk>/delete/', AccountsReceivableDeleteView.as_view(), name='accounts_receivable_delete'),
    path('accounts_receivable/<int:pk>/pay/', AccountsReceivableTogglePaidView.as_view(), name='accounts_receivable_pay')
]