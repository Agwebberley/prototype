import boto3
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from prefect import task, Flow
from prefect.engine.executors import TaskRunner
from prefect.tasks.aws.sqs import SQSReceiveMessage
from prefect.tasks.aws.sns import SNSPublishMessage

class Listener:
    def __init__(self, queue_name, queue_url, topic_arn):
        self.queue_name = queue_name
        self.queue_url = queue_url
        self.topic_arn = topic_arn

    @task
    def process_message(self, message):
        return message

    @task
    def publish_message(self, message):
        sns.publish(TopicArn=self.topic_arn, Message=message)

    def run(self):
        with Flow(f'{self.queue_name}Listener') as flow:
            messages = SQSReceiveMessage(queue_url=self.queue_url, wait_time=20, max_number_of_messages=1)
            processed_message = self.process_message(messages)
            self.publish_message(processed_message)

        executor = ThreadPoolExecutor(max_workers=1)
        TaskRunner(flow).run_in_executor(executor)

class LogMessageListener(Listener):
    @task
    def process_message(self, message):
        sender, message = message.split(':')
        return f'{sender} sent message: {message}'

class Queue1Listener(Listener):
    @task
    def process_message(self, message):
        return message.upper()

class Queue2Listener(Listener):
    @task
    def process_message(self, message):
        return message.lower()

# Create SQS client
sqs = boto3.client('sqs')
queue_urls = {
    'LogMessage': sqs.get_queue_url(QueueName='LogMessage')['QueueUrl'],
    'Queue1': sqs.get_queue_url(QueueName='Queue1')['QueueUrl'],
    'Queue2': sqs.get_queue_url(QueueName='Queue2')['QueueUrl']
}

# Create SNS clients
sns_topic_1 = boto3.client('sns', region_name='us-west-2')
sns_topic_2 = boto3.client('sns', region_name='us-east-1')

# Create SQLite3 database
conn = sqlite3.connect('sender_topic_map.db')
c = conn.cursor()
c.execute('''CREATE TABLE sender_topic_map
             (sender text, topic_arn text)''')
c.execute("INSERT INTO sender_topic_map VALUES ('sender1', 'arn:aws:sns:us-west-2:123456789012:topic1')")
c.execute("INSERT INTO sender_topic_map VALUES ('sender2', 'arn:aws:sns:us-east-1:123456789012:topic2')")
conn.commit()

# Create listeners
listeners = [
    LogMessageListener('LogMessage', queue_urls['LogMessage'], 'arn:aws:sns:us-west-2:123456789012:topic1'),
    Queue1Listener('Queue1', queue_urls['Queue1'], 'arn:aws:sns:us-east-1:123456789012:topic2'),
    Queue2Listener('Queue2', queue_urls['Queue2'], 'arn:aws:sns:us-west-2:123456789012:topic1')
]

# Start listeners
for listener in listeners:
    listener.run()
