import multiprocessing
import boto3
import json
import time
import sqlite3

class BaseSQSListener(multiprocessing.Process):
    def __init__(self, queue_url, barrier):
        multiprocessing.Process.__init__(self)
        self.sqs = boto3.client('sqs')
        self.sns = boto3.client('sns')
        self.queue_url = queue_url
        self.stop_event = multiprocessing.Event()
        print(f"Starting listener for queue {queue_url}")
        multiprocessing.Process.__init__(self)
        self.barrier = barrier

    def run(self):
        while not self.stop_event.is_set():
            messages = self.sqs.receive_message(QueueUrl=self.queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=20)
            if 'Messages' in messages:
                for message in messages['Messages']:
                    self.handle_message(message)
                    self.sqs.delete_message(QueueUrl=self.queue_url, ReceiptHandle=message['ReceiptHandle'])

    def handle_message(self, message):
        raise NotImplementedError

    def stop(self):
        self.stop_event.set()

class LogListener(BaseSQSListener):
    def handle_message(self, message):
        self.barrier.wait()
        from Shared.models import logmessage
        print(f"Log Queue handling message: {message}")
        logmessage.objects.create(message=message["Body"])

        # Forward the message to its respective queue(s)
        # Get the sender's name from the message
        sender = message["Body"].split(" ")[0]
        # Get the queue(s) that are listening to the sender
        conn = sqlite3.connect("queue.db")
        c = conn.cursor()
        topics = c.execute("SELECT topic FROM queues WHERE listeningto=?", (sender,)).fetchall()
        conn.close()
        print(topics)
        # Send the message to each queue
        for topic in topics:
            print("Sending " + topic[0])
            self.sns.publish(TopicArn=f"arn:aws:sns:us-west-2:710141730058:{topic[0]}", Message=message["Body"])


class OrderListener(BaseSQSListener):
    def handle_message(self, message):
        print(f"Order Queue handling message: {message}")

class ManufactureListener(BaseSQSListener):

    def __init__(self, queue_url):
        super().__init__(queue_url)
        self.conn = sqlite3.connect("queue.db")
        self.c = self.conn.cursor()
        self.c.execute("INSERT INTO queues VALUES (?, ?)", ("Manufacture", "pick"))
        self.conn.commit()
        self.conn.close()
    def handle_message(self, message):
        print(f"Queue2Listener handling message: {message}")
