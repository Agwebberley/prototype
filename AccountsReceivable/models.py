from django.db import models
from django.urls import reverse
from Orders.models import Orders
import datetime

class AccountsReceivable(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    amount = models.FloatField()
    # Due date defaults to 30 days from now
    due_date = models.DateField(default=datetime.date.today() + datetime.timedelta(days=30))
    paid = models.BooleanField(default=False)
    class Meta:
        app_label = 'AccountsReceivable'
    
    def __str__(self):
        return f"{self.order.id} - {self.amount}"
    
    def get_absolute_url(self):
        return reverse('accountsreceivable:accounts_receivable_list')