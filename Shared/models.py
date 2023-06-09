from django.db import models

# Create your models here.
class LogMessage(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)