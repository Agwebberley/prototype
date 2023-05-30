import boto3
from .models import LogMessage
import time

sqs = boto3.resource('sqs', region_name='us-west-2')

while True:
    queue = sqs.Queue('https://sqs.us-west-2.amazonaws.com/710141730058/CustomerLog')
    for message in queue.receive_messages():
        print(message.body)
        log_message = LogMessage(message=message.body)
        log_message.save()
        message.delete()
    time.sleep(1)