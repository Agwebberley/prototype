from django.db import models
from django.urls import reverse
from Orders.models import Orders
from Customers.models import Customers
import datetime

class AccountsReceivable(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Due date defaults to 30 days from now
    due_date = models.DateField(default=datetime.date.today() + datetime.timedelta(days=30))
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        app_label = 'AccountsReceivable'
    
    def __str__(self):
        return f"{self.order.id} - {self.amount}"
    
    def get_absolute_url(self):
        return reverse('accountsreceivable:accounts_receivable_list')