import boto3
import logging
import time

logging.basicConfig(filename='sns.log', level=logging.INFO)

# Subscribe to the SNS topic to receive notifications about the Data model.
# log the message to the sns.log file.

sqs = boto3.resource('sqs', region_name='us-west-2')
#topic_arn = 'arn:aws:sns:us-west-2:710141730058:CustomerLog'



while True:
    queue = sqs.Queue('https://sqs.us-west-2.amazonaws.com/710141730058/CustomerLog')
    for message in queue.receive_messages():
        print(message.body)
        logging.info(message.body)
        message.delete()
    time.sleep(1)

