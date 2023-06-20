from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Manufacture
from Shared.signals import SNSPublisher

@receiver(post_save, sender=Manufacture)
def inventory_post(sender, instance, **kwargs):
    publisher = SNSPublisher(region_name='us-west-2', topic_arn='arn:aws:sns:us-west-2:710141730058:Manufacture')
    if kwargs.get('created'):
        message = f"manufacture created {instance.id}"
    elif kwargs.get('update_fields'):
        message = f"manufacture updated {instance.id}"
    else:
        return
    publisher.publish(message)
