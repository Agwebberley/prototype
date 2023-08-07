import json
from django.core.management.base import BaseCommand
from Listeners.flow import Listeners

class Command(BaseCommand):
    help = 'Starts the SQS listeners'

    def handle(self, *args, **options):
        listeners = Listeners()
        # Join the listeners to the main process
        for listener in listeners:
            listener.join()

