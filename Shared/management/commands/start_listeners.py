import json
from django.core.management.base import BaseCommand
from multi_sqs_listener import QueueConfig, EventBus, MultiSQSListener
import sys

class Command(BaseCommand):
    help = 'Starts the SQS listeners'

    def handle(self, *args, **options):
        eventbus = EventBus()
        EventBus.register_buses([eventbus])

        log_queue = QueueConfig('CustomerLog', eventbus, region_name='us-west-2')
        accounts_receivable_queue = QueueConfig('AccountsReceivable', eventbus, region_name='us-west-2')
        inventory_queue = QueueConfig('Inventory', eventbus, region_name='us-west-2')

        listener = PrototypeSQSListener([log_queue, accounts_receivable_queue, inventory_queue])
        listener.listen()

class PrototypeSQSListener(MultiSQSListener):
    def handle_message(self, queue_name, bus_name, priority, message):
        print("Handling message from queue: " + queue_name)
        sys.stdout.flush()
        if queue_name == 'CustomerLog':
                from Shared.models import LogMessage
                print("Received message from CustomerLog queue")
                # message['Body'] is a JSON string, parse it to a dictionary
                message_json = json.loads(message.body)
                LogMessage.objects.create(message=message_json['Message'])
        elif queue_name == 'AccountsReceivable':
            from Orders.models import Orders
            from AccountsReceivable.models import AccountsReceivable
                # split the message into a list by spaces
            
            message_json = json.loads(message.body)
            message_body = message_json['Message'].split(' ')


            # if the message is an order created message
            # create an AccountsReceivable object for the order
            if message_body[0] == 'order' and message_body[1] == 'created':
                try:
                    order = Orders.objects.get(id=message_body[2])
                    order_total = float(order.get_order_total())
                    AccountsReceivable.objects.create(order=order, amount=order_total)
                except Orders.DoesNotExist:
                    print(f"Order with id {message_body[2]} does not exist")
            # if the message is an order deleted message
            # delete the AccountsReceivable object for the order if it exists
            elif message_body[0] == 'order' and message_body[1] == 'deleted':    
                try:
                    order = Orders.objects.get(id=message_body[2])
                    accounts_receivable = AccountsReceivable.objects.get(order=order)
                    accounts_receivable.delete()
                except AccountsReceivable.DoesNotExist:
                    pass
                except Orders.DoesNotExist:
                    print(f"Order with id {message_body[2]} does not exist")
            # if the message is an order updated message
            # update the AccountsReceivable object for the order if it exists
            elif message_body[0] == 'order' and message_body[1] == 'updated':
                order = Orders.objects.get(id=message_body[2])
                try:
                    accounts_receivable = AccountsReceivable.objects.get(order=order)
                    order_total = float(order.get_order_total())
                    accounts_receivable.amount = order_total
                    accounts_receivable.save()
                except AccountsReceivable.DoesNotExist:
                    pass
            else:
                raise Exception('Unknown message: {}'.format(message_body))
        elif queue_name == 'Inventory':
            from Inventory.models import Inventory, InventoryHistory, Pick
            from Items.models import Items
            message_json = json.loads(message.body)
            message_body = message_json['Message'].split(' ')
            if message_body[0] == 'item' and message_body[1] == 'created':
                # create an Inventory object for the item
                try:
                    item = Items.objects.get(id=message_body[2])
                    Inventory.objects.create(item=item, quantity=0)
                    # get the id of the Inventory object that was just created
                    inventory = Inventory.objects.get(item_id=message_body[2])
                    InventoryHistory.objects.create(inventory=inventory, item=item, quantity=0, type='adjustment')
                except:
                    print(f"Item with id {message_body[2]} did not create")
            elif message_body[0] == 'order' and message_body[1] == 'created':
                # create a Pick object for the order
                try:
                    order = Orders.objects.get(id=message_body[2])
                    Pick.objects.create(order=order)
                except:
                    print(f"Order with id {message_body[2]} did not create")
        else:
            raise Exception('Unknown queue name: {}'.format(queue_name))


if __name__ == "__main__":
    eventbus = EventBus()
    EventBus.register_buses([eventbus])
    log_queue = QueueConfig('CustomerLog', eventbus, region_name='us-west-2')
    accounts_receivable_queue = QueueConfig('AccountsReceivable', eventbus, region_name='us-west-2')
    listener = PrototypeSQSListener([log_queue, accounts_receivable_queue])
    listener.listen()