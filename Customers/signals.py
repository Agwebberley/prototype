from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Inventory
from Shared.singals import SNSPublisher

@receiver(post_save, sender=Inventory)
@receiver(post_delete, sender=Inventory)
def inventory_post(sender, instance, **kwargs):
    publisher = SNSPublisher(region_name='us-west-2', topic_arn='arn:aws:sns:us-west-2:710141730058:Inventory')
    if kwargs.get('update_fields'):
        message = f"inventory updated {instance.id}"
    else:
        return
    publisher.publish(message)
