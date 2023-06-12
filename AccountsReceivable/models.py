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
    

# A model for recording changes to the AccountsReceivable model
class AccountsReceivableHistory(models.Model):
    # The AccountsReceivable object that was changed
    accounts_receivable = models.ForeignKey(AccountsReceivable, on_delete=models.CASCADE)
    # The field that was changed
    field = models.CharField(max_length=100)
    # The value of the field before the change
    old_value = models.CharField(max_length=100)
    # The value of the field after the change
    new_value = models.CharField(max_length=100)
    # The date and time the change was made
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'AccountsReceivable'
    
    def __str__(self):
        return f"{self.accounts_receivable.id} - {self.field} - {self.date}"
    
    def get_absolute_url(self):
        return reverse('accountsreceivable:accounts_receivable_list')
    
    def get_accounts_receivable(self):
        return self.accounts_receivable

# A model for recording payments made to AccountsReceivable objects
class AccountsReceivablePayment(models.Model):
    # The AccountsReceivable object that was paid
    accounts_receivable = models.ForeignKey(AccountsReceivable, on_delete=models.CASCADE)
    # The amount paid
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # The date the payment was made
    date = models.DateField(auto_now_add=True)

    class Meta:
        app_label = 'AccountsReceivable'
    
    def __str__(self):
        return f"{self.accounts_receivable.id} - {self.amount}"
    
    def get_absolute_url(self):
        return reverse('accountsreceivable:accounts_receivable_list')
    
    def get_accounts_receivable(self):
        return self.accounts_receivable
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.accounts_receivable.amount_paid += self.amount
        if self.accounts_receivable.amount_paid >= self.accounts_receivable.amount:
            self.accounts_receivable.paid = True
            self.accounts_receivable.paid_date = self.date
        self.accounts_receivable.save()

        # Create an AccountsReceivableHistory object to record the change
        AccountsReceivableHistory.objects.create(
            accounts_receivable=self.accounts_receivable,
            field='amount_paid',
            old_value=self.accounts_receivable.amount_paid - self.amount,
            new_value=self.accounts_receivable.amount_paid
        )
    
    def delete(self, *args, **kwargs):
        self.accounts_receivable.amount_paid -= self.amount
        if self.accounts_receivable.amount_paid < self.accounts_receivable.amount:
            self.accounts_receivable.paid = False
            self.accounts_receivable.paid_date = None
        self.accounts_receivable.save()

        AccountsReceivableHistory.objects.create(
            accounts_receivable=self.accounts_receivable,
            field='amount_paid',
            old_value=self.accounts_receivable.amount_paid + self.amount,
            new_value=self.accounts_receivable.amount_paid
        )

        super().delete(*args, **kwargs)