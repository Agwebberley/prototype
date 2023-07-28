
from django.db import models
from django.urls import reverse
from django.utils import timezone


class accountsreceivable(models.Model):
    amount = models.DecimalField(max_length=10, decimal_places=2, )
    due_date = models.DateField()
    paid = models.BooleanField()
    paid_date = models.DateField()
    amount_paid = models.DecimalField(max_length=10, decimal_places=2, )
    order_id = models.IntegerField(max_length=64, )

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
    accounts_receivable_id = models.IntegerField(max_length=64, )

    class Meta:
        app_label = 'AccountsReceivable'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class accountsreceivablepayment(models.Model):
    amount = models.DecimalField(max_length=10, decimal_places=2, )
    date = models.DateField()
    accounts_receivable_id = models.IntegerField(max_length=64, )

    class Meta:
        app_label = 'AccountsReceivable'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



