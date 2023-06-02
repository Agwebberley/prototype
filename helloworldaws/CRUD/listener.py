import boto3
import signal
import sys

# This is a Python class that listens to an Amazon Simple Queue Service (SQS) queue and handles
# messages received.
class SQSListener:
    def __init__(self, queue_url):
        self.sqs = boto3.client('sqs', region_name='us-west-2')
        self.queue_url = queue_url
        self.should_quit = False

    def start(self):

        while not self.should_quit:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20
            )

            if 'Messages' in response:
                for message in response['Messages']:
                    self.handle_message(message)

                    self.sqs.delete_message(
                        QueueUrl=self.queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                    )

    def handle_message(self, message):
        # Override this method in a subclass to handle the message
        pass


# This class creates a LogMessage object in Django's models based on a message received from an
# SQSListener.
class LogListener(SQSListener):
    def handle_message(self, message):
        from .models import LogMessage

        # message['Body'] is a dictionary, I need to get the message from the dictionary
        message_Dict = eval(message['Body'])
        print(message_Dict)
        LogMessage.objects.create(message=message_Dict['Message'])


