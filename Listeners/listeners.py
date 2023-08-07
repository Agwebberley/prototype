import multiprocessing
import boto3
import time

class BaseSQSListener(multiprocessing.Process):
    def __init__(self, queue_url):
        multiprocessing.Process.__init__(self)
        self.sqs = boto3.client('sqs')
        self.queue_url = queue_url
        self.stop_event = multiprocessing.Event()

    def run(self):
        while not self.stop_event.is_set():
            messages = self.sqs.receive_message(QueueUrl=self.queue_url, MaxNumberOfMessages=1)
            if 'Messages' in messages:
                for message in messages['Messages']:
                    self.handle_message(message)
                    self.sqs.delete_message(QueueUrl=self.queue_url, ReceiptHandle=message['ReceiptHandle'])
            time.sleep(1)

    def handle_message(self, message):
        raise NotImplementedError

    def stop(self):
        self.stop_event.set()


class OrderListener(BaseSQSListener):
    def handle_message(self, message):
        print(f"Queue1Listener handling message: {message}")

class ManufactureListener(BaseSQSListener):
    def handle_message(self, message):
        print(f"Queue2Listener handling message: {message}")
