from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import boto3

# The SNSPublisher class is a Python class that initializes an SNS client and publishes a message to a
# specified topic.
from django.core.cache import cache
import time

class SNSPublisher:
    def __init__(self, region_name, topic_arn):
        self.sns = boto3.client('sns', region_name=region_name)
        self.topic_arn = topic_arn

    def publish(self, message):

        self.sns.publish(TopicArn=self.topic_arn, Message=message)


@receiver(post_save)
def post_signal(sender, instance, **kwargs):
    if sender.__name__ != 'LogMessage':
        publisher = SNSPublisher(region_name='us-west-2', topic_arn='arn:aws:sns:us-west-2:710141730058:Log')
        if kwargs.get('created'):
            message = f"{sender.__name__} with ID {instance.id} was created"
        elif kwargs.get('update_fields'):
            message = f"{sender.__name__} with ID {instance.id} was updated" 
        else: 
            message = f"{sender.__name__} with ID {instance.id} was updated"
        publisher.publish(message)


@receiver(post_delete)
def delete_signal(sender, instance, **kwargs):
    if sender.__name__ != 'LogMessage':
        publisher = SNSPublisher(region_name='us-west-2', topic_arn='arn:aws:sns:us-west-2:710141730058:Log')
        message = f"{sender.__name__} with ID {instance.id} was deleted"
        publisher.publish(message)