from django.core.management.base import BaseCommand
from CRUD.listener import SQSListener, LogListener

class Command(BaseCommand):
    help = 'Starts the SQS listeners'

    def handle(self, *args, **options):
        queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/my-queue'
        listener1 = SQSListener(queue_url)
        listener2 = LogListener(queue_url)

        listener1.start()
        listener2.start()