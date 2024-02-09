from django.db import models
from Customers.models import customers
from datetime import datetime

class orders(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    customers = models.ForeignKey('Customers.customers', on_delete=models.CASCADE)

    def save():
        self.updated_at = datetime.now()
        super().save(*args, **kwargs)


class orderItem(models.Model):
    quantity = models.IntegerField()
    def help():
        print("me")

    def HELLOWORLD():
        print("Hello World")
