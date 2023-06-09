from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Customers, Items, Orders, Inventory
import boto3

# The SNSPublisher class is a Python class that initializes an SNS client and publishes a message to a
# specified topic.
class SNSPublisher:
    def __init__(self, region_name, topic_arn):
        self.sns = boto3.client('sns', region_name=region_name)
        self.topic_arn = topic_arn

    def publish(self, message):
        self.sns.publish(TopicArn=self.topic_arn, Message=message)


@receiver(post_save)
@receiver(post_delete)
def post_signal(sender, instance, **kwargs):
    if sender.__name__ != 'LogMessage':
        publisher = SNSPublisher(region_name='us-west-2', topic_arn='arn:aws:sns:us-west-2:710141730058:CustomerLog')
        print(f"post {instance.id}")
        if kwargs.get('created'):
            message = f"{sender.__name__} with ID {instance.id} was created"
        elif kwargs.get('update_fields'):
            message = f"{sender.__name__} with ID {instance.id} was updated" 
        else: 
            message = f"{sender.__name__} with ID {instance.id} was deleted"
        publisher.publish(message)

@receiver(post_save, sender=Orders)
@receiver(post_delete, sender=Orders)
def order_post(sender, instance, **kwargs):
    publisher = SNSPublisher(region_name='us-west-2', topic_arn='arn:aws:sns:us-west-2:710141730058:Order')
    if kwargs.get('created'):
        message = f"order created {instance.id}"
    elif kwargs.get('update_fields'):
        message = f"order updated {instance.id}"
    else:
        message = f"order deleted {instance.id}"
    publisher.publish(message)

@receiver(post_save, sender=Inventory)
@receiver(post_delete, sender=Inventory)
def inventory_post(sender, instance, **kwargs):
    publisher = SNSPublisher(region_name='us-west-2', topic_arn='arn:aws:sns:us-west-2:710141730058:Inventory')
    if kwargs.get('update_fields'):
        message = f"inventory updated {instance.id}"
    else:
        return
    publisher.publish(message)
