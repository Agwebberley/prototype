
from django.db import models
from django.urls import reverse
from django.utils import timezone


from Orders.models import orders
class accountsreceivable(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, )
    due_date = models.DateField()
    paid = models.BooleanField()
    paid_date = models.DateField(null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    orders = models.ForeignKey(orders, on_delete=models.CASCADE, related_name="accountsreceivable")

    class Meta:
        app_label = 'AccountsReceivable'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class accountsreceivablehistory(models.Model):
    field = models.CharField(max_length=100, )
    old_value = models.CharField(max_length=100, )
    new_value = models.CharField(max_length=100, )
    date = models.DateTimeField(max_length=6, )
    accountsreceivable = models.ForeignKey(accountsreceivable, on_delete=models.CASCADE, related_name="_accountsreceivablehistory")

    class Meta:
        app_label = 'AccountsReceivable'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class accountsreceivablepayment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, )
    date = models.DateField()
    accountsreceivable = models.ForeignKey(accountsreceivable, on_delete=models.CASCADE, related_name="_accountsreceivablepayment")

    class Meta:
        app_label = 'AccountsReceivable'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



