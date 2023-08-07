
from django.db import models
from django.urls import reverse
from django.utils import timezone


class logmessage(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'Shared'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



