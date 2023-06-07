from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Customers, Items, Orders
import boto3

# The SNSPublisher class is a Python class that initializes an SNS client and publishes a message to a
# specified topic.
class SNSPublisher:
    def __init__(self, region_name, topic_arn):
        self.sns = boto3.client('sns', region_name=region_name)
        self.topic_arn = topic_arn

    def publish(self, message):
        self.sns.publish(TopicArn=self.topic_arn, Message=message)


@receiver(post_save, sender=Customers)
@receiver(post_delete, sender=Customers)
def Customer(sender, instance, **kwargs):
    publisher = SNSPublisher(region_name='us-west-2', topic_arn='arn:aws:sns:us-west-2:710141730058:CustomerLog')
    if kwargs.get('created'):
        message = f"Customer {instance.id} was created"
    elif kwargs.get('update_fields'):
        message = f"Customer {instance.id} was updated" 
    else: 
        message = f"Customer {instance.id} was deleted"
    publisher.publish(message)

@receiver(post_save, sender=Items)
@receiver(post_delete, sender=Items)
def Item(sender, instance, **kwargs):
    publisher = SNSPublisher(region_name='us-west-2', topic_arn='arn:aws:sns:us-west-2:710141730058:CustomerLog')
    if kwargs.get('created'):
        message = f"Item {instance.id} was created"
    elif kwargs.get('update_fields'):
        message = f"Item {instance.id} was updated" 
    else: 
        message = f"Item {instance.id} was deleted"
    publisher.publish(message)

@receiver(post_save, sender=Orders)
@receiver(post_delete, sender=Orders)
def Order(sender, instance, **kwargs):
    publisher = SNSPublisher(region_name='us-west-2', topic_arn='arn:aws:sns:us-west-2:710141730058:CustomerLog')
    if kwargs.get('created'):
        message = f"Order {instance.id} was created"
    elif kwargs.get('update_fields'):
        message = f"Order {instance.id} was updated" 
    else: 
        message = f"Order {instance.id} was deleted"
    publisher.publish(message)