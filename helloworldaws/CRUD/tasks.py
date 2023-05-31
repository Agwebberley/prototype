import boto3
from .models import LogMessage
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from celery import shared_task

@shared_task
def get_log_messages():
    sqs = boto3.resource('sqs', region_name='us-west-2')
    print('get_log_messages')
    queue = sqs.Queue('https://sqs.us-west-2.amazonaws.com/710141730058/CustomerLog')
    for message in queue.receive_messages():
        print(message.body)
        log_message = LogMessage(message=message.body)
        log_message.save()
        message.delete()