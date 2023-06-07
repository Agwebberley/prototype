from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Customers
import boto3


"""
This function publishes a message to an AWS SNS topic when a Data object is created or updated.

:param sender: The model class that is sending the signal (in this case, the Data model)
:param instance: The instance parameter refers to the instance of the Data model that was just
saved. In other words, it represents the specific object that triggered the post_save signal
"""
@receiver(post_save, sender=Customers)
@receiver(post_delete, sender=Customers)
def publish_to_sns(sender, instance, **kwargs):
    sns = boto3.client('sns', region_name='us-west-2')
    topic_arn = 'arn:aws:sns:us-west-2:710141730058:CustomerLog'
    if kwargs.get('created'):
        message = f"Data object {instance.id} was created"
    elif kwargs.get('update_fields'):
        message = f"Data object {instance.id} was updated" 
    else: 
        message = f"Data object {instance.id} was deleted"
    sns.publish(TopicArn=topic_arn, Message=message)