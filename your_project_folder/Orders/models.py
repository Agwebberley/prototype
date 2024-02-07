from django.db import models
from Customers.models import customers, 

class orderItem(models.Model):
    quantity = models.IntegerField()

