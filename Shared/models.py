
from django.db import models
from django.urls import reverse
from django.utils import timezone


class logmessage(models.Model):
    id = models.IntegerField(max_length=64, )
    message = models.TextField()
    created_at = models.DateTimeField(max_length=6, )

    class Meta:
        app_label = 'Shared'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



