from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Items
from Shared.signals import SNSPublisher

@receiver(post_save, sender=Items)
def order_post(sender, instance, **kwargs):
    publisher = SNSPublisher(region_name='us-west-2', topic_arn='arn:aws:sns:us-west-2:710141730058:Items')
    if kwargs.get('created'):
        message = f"item created {instance.id}"
    elif kwargs.get('update_fields'):
        message = f"item updated {instance.id}"
    else:
        message = f"item updated {instance.id}"
    publisher.publish(message)


@receiver(post_delete, sender=Items)
def order_post_delete(sender, instance, **kwargs):
    publisher = SNSPublisher(region_name='us-west-2', topic_arn='arn:aws:sns:us-west-2:710141730058:Items')
    message = f"item deleted {instance.id}"
    publisher.publish(message)