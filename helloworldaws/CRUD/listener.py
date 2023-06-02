import boto3

# This is a Python class that listens to an Amazon Simple Queue Service (SQS) queue and handles
# messages received.
import signal
import atexit

class SQSListener:
    def __init__(self, queue_url):
        self.sqs = boto3.client('sqs', region_name='us-west-2')
        self.queue_url = queue_url
        self.should_quit = False

        # Register the cleanup function to be called when the program exits
        atexit.register(self.cleanup)

        # Register a signal handler for SIGINT (Ctrl+C)
        signal.signal(signal.SIGINT, self.handle_signal)

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

    def cleanup(self):
        # This function is called when the program is exiting
        # Add any cleanup code here, such as closing database connections
        # Override this method in a subclass if more cleanup is needed
        self.should_quit = True
        print("Cleaning up...")

    def handle_signal(self, signum, _):
        # This function is called when a signal is received
        # Set the should_quit flag to True to exit the program
        self.should_quit = True
        print("Received signal {}, exiting...".format(signum))
        exit(0)


# This class creates a LogMessage object in Django's models based on a message received from an
# SQSListener.
class LogListener(SQSListener):
    def handle_message(self, message):
        from .models import LogMessage

        # message['Body'] is a dictionary, I need to get the message from the dictionary
        message_Dict = eval(message['Body'])
        print(message_Dict)
        LogMessage.objects.create(message=message_Dict['Message'])


