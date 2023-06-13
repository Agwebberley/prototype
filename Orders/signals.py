from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Orders
from Shared.signals import SNSPublisher

@receiver(post_save, sender=Orders)
@receiver(post_delete, sender=Orders)
def order_post(sender, instance, **kwargs):
    print("order_post")
    publisher = SNSPublisher(region_name='us-west-2', topic_arn='arn:aws:sns:us-west-2:710141730058:Order')
    if kwargs.get('created'):
        message = f"order created {instance.id}"
    elif kwargs.get('update_fields'):
        message = f"order updated {instance.id}"
    else:
        message = f"order deleted {instance.id}"
    publisher.publish(message)