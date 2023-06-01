from django.core.management.base import BaseCommand
from CRUD.listener import SQSListener, LogListener

class Command(BaseCommand):
    help = 'Starts the SQS listeners'

    def handle(self, *args, **options):
        LogListenerUrl = 'https://sqs.us-west-2.amazonaws.com/710141730058/CustomerLog'
        
        LogListenerTask = LogListener(LogListenerUrl)

        LogListenerTask.start()