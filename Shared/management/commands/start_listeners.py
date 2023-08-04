import json
from django.core.management.base import BaseCommand
from multi_sqs_listener import QueueConfig, EventBus, MultiSQSListener
import sys
from decimal import Decimal

class Command(BaseCommand):
    help = 'Starts the SQS listeners'

    def handle(self, *args, **options):
        eventbus = EventBus()
        EventBus.register_buses([eventbus])

        log_queue = QueueConfig('CustomerLog', eventbus, region_name='us-west-2')

        listener = PrototypeSQSListener([log_queue])
        listener.listen()

class PrototypeSQSListener(MultiSQSListener):
    def handle_message(self, queue_name, bus_name, priority, message):
        print("Handling message from queue: " + queue_name)
        if queue_name == 'CustomerLog':
                from Shared.models import logmessage
                print("Received message from CustomerLog queue")
                # message['Body'] is a JSON string, parse it to a dictionary
                message_json = json.loads(message.body)
                logmessage.objects.create(message=message_json['Message'])
        message.delete()


if __name__ == "__main__":
    eventbus = EventBus()
    EventBus.register_buses([eventbus])
    log_queue = QueueConfig('CustomerLog', eventbus, region_name='us-west-2')
    accounts_receivable_queue = QueueConfig('AccountsReceivable', eventbus, region_name='us-west-2')
    listener = PrototypeSQSListener([log_queue, accounts_receivable_queue])
    listener.listen()