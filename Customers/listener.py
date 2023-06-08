import json
import logging
import boto3
import threading
import signal

# This is a Python class that listens to an Amazon Simple Queue Service (SQS) queue and handles
# messages received.

class SQSListener:
    def __init__(self, queue_url):
        self.queue_url = queue_url
        self.should_quit = False

    def start(self):
        self.sqs = boto3.client('sqs', region_name='us-west-2')
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGBREAK, self.handle_signal)
        while not self.should_quit:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20
            )

            if 'Messages' in response:
                for message in response['Messages']:
                    try:
                        self.handle_message(message)
                    except Exception as e:
                        logging.error(f"Error processing message: {e}")

                    self.sqs.delete_message(
                        QueueUrl=self.queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                    )

    def handle_message(self, message):
        # Override this method in a subclass to handle the message
        pass

    def stop(self):
        self.should_quit = True

    def handle_signal(self, signum, frame):
        logging.info(f"Received signal {signum}, stopping listener")
        self.stop()


# This class creates a LogMessage object in Django's models based on a message received from an
# SQSListener.
class LogListener(SQSListener):
    def handle_message(self, message):
        from .models import LogMessage

        # message['Body'] is a JSON string, parse it to a dictionary
        message_dict = json.loads(message['Body'])
        logging.info(f"Received message: {message_dict}")
        LogMessage.objects.create(message=message_dict['Message'])


if __name__ == "__main__":
    
    from django.conf import settings

    logging.basicConfig(level=logging.INFO)
    LogL = LogListener("https://sqs.us-west-2.amazonaws.com/710141730058/CustomerLog")
    
    LogLT = threading.Thread(target=LogL.start)
    LogLT.start()
