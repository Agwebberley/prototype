import threading
import boto3
import time

class BaseSQSListener(threading.Thread):
    def __init__(self, queue_url):
        threading.Thread.__init__(self)
        self.sqs = boto3.client('sqs')
        self.queue_url = queue_url

    def run(self):
        while True:
            messages = self.sqs.receive_message(QueueUrl=self.queue_url, MaxNumberOfMessages=1)
            if 'Messages' in messages:
                for message in messages['Messages']:
                    self.handle_message(message)
                    self.sqs.delete_message(QueueUrl=self.queue_url, ReceiptHandle=message['ReceiptHandle'])

    def handle_message(self, message):
        raise NotImplementedError

class Queue1Listener(BaseSQSListener):
    def handle_message(self, message):
        print(f"Queue1Listener handling message: {message}")

class Queue2Listener(BaseSQSListener):
    def handle_message(self, message):
        print(f"Queue2Listener handling message: {message}")
