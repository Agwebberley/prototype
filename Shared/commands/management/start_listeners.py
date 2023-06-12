import signal
from django.core.management.base import BaseCommand
from Shared.listener import LogListener
from AccountsReceivable.listener import AccountsReceivableListener
import sys

class Command(BaseCommand):
    help = 'Starts the SQS listeners'

    def handle(self, *args, **options):
        def signal_handler(signal, frame):
            LogListenerTask.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)


        LogListenerUrl = 'https://sqs.us-west-2.amazonaws.com/710141730058/CustomerLog'
        LogListenerTask = LogListener(LogListenerUrl)
        LogListenerTask.start()
        
        AccountsReceivableListenerUrl = 'https://sqs.us-west-2.amazonaws.com/710141730058/AccountsReceivable'
        AccountsReceivableListenerTask = AccountsReceivableListener(AccountsReceivableListenerUrl)
        AccountsReceivableListenerTask.start()

