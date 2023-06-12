from django.urls import path
from .views import AccountsReceivableListView, AccountTogglePaidView, AccountAddPayment, AccountChangeDueDateView, AccountDetailView

app_name = 'accounts_receivable'

urlpatterns = [
    path('', AccountsReceivableListView.as_view(), name='accounts_receivable_list'),
    path('<int:pk>/payment/', AccountAddPayment.as_view(), name='add_payment'),
    path('<int:pk>/delete/', AccountChangeDueDateView.as_view(), name='change_due_date'),
    path('<int:pk>/pay/', AccountTogglePaidView.as_view(), name='toggle_paid'),
    path('<int:pk>/', AccountDetailView.as_view(), name='account_details'),
]