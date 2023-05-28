from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Data
import boto3

@receiver(post_save, sender=Data)
def publish_to_sns(sender, instance, **kwargs):
    sns = boto3.client('sns', region_name='us-west-2')
    topic_arn = 'arn:aws:sns:us-west-2:710141730058:CustomerLog'
    message = f"Data object {instance.id} was {kwargs['created'] and 'created' or 'updated'}"
    sns.publish(TopicArn=topic_arn, Message=message)