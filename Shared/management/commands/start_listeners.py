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
        accounts_receivable_queue = QueueConfig('AccountsReceivable', eventbus, region_name='us-west-2')
        inventory_queue = QueueConfig('Inventory', eventbus, region_name='us-west-2')
        manufacture_queue = QueueConfig('Manufacture', eventbus, region_name='us-west-2')

        listener = PrototypeSQSListener([log_queue, accounts_receivable_queue, inventory_queue, manufacture_queue])
        listener.listen()

class PrototypeSQSListener(MultiSQSListener):
    def handle_message(self, queue_name, bus_name, priority, message):
        print("Handling message from queue: " + queue_name)
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
                    order_total = Decimal(order.get_total_price_float())
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
                    order_total = Decimal(order.get_total_price_float())
                    accounts_receivable.amount = order_total
                    accounts_receivable.save()
                except AccountsReceivable.DoesNotExist:
                    pass
            else:
                raise Exception('Unknown message: {}'.format(message_body))
        elif queue_name == 'Inventory':
            from Inventory.models import Inventory, Pick
            from Items.models import Items
            message_json = json.loads(message.body)
            message_body = message_json['Message'].split(' ')
            if message_body[0] == 'item' and message_body[1] == 'created':
                # create an Inventory object for the item
                try:
                    item = Items.objects.get(id=message_body[2])
                    Inventory.objects.create(item=item, quantity=0, typeI="adjustment")
                except Exception as e:
                    print(f"Item with id {message_body[2]} did not create")
                    print(e)
                    
            elif message_body[0] == 'order' and message_body[1] == 'created':
                print("Received message from Inventory queue")
                from Orders.models import Orders
                # create a Pick object for the order
                try:
                    order = Orders.objects.get(id=message_body[2])
                    Pick.objects.create(order=order)
                except Exception as e:
                    print(f"Order with id {message_body[2]} did not create")
                    print(e)
            elif message_body[0] == 'manufacture' and message_body[1] == 'created':
                # If a manufacture object is created, create an InventoryHistory object for the item
                # and update the quantity of the item in the Inventory object
                # and remove the manufacture object
                # Add a manufacturehistory object for the manufacture object
                from Manufacture.models import Manufacture, ManufactureHistory
                from Inventory.models import Inventory
                from Items.models import Items
                try:
                    manufacture = Manufacture.objects.get(id=message_body[2])
                    inventory = Inventory.objects.get(item=manufacture.item)
                    inventory.quantity += manufacture.quantity
                    inventory.save()
                    ManufactureHistory.objects.create(manufacture=manufacture, item=manufacture.item, quantity=manufacture.quantity, is_complete=True)
                    manufacture.delete()
                except Exception as e:
                    print(f"Manufacture with id {message_body[2]} did not create")
                    print(e)
        elif queue_name == 'Manufacture':
            if message[0] == 'pick' and message[1] == 'updated':
                from Inventory.models import Pick, Inventory
                from Items.models import Items
                from Manufacture.models import Manufacture

                # get the pick object
                pick = Pick.objects.get(id=message[2])
                # For each unique item in the pick, check if the item is below the reorder threshold
                # If it is, create a Manufacture object for the item
                for item in pick.items.all().distinct():
                    inventory = Inventory.objects.get(item=item)
                    if inventory.quantity < item.reorder_level:
                        reorder_amount = item.target_inv - inventory.quantity
                        Manufacture.objects.create(item=item, quantity=reorder_amount)

        else:
            raise Exception('Unknown queue name: {}'.format(queue_name))
        
        message.delete()


if __name__ == "__main__":
    eventbus = EventBus()
    EventBus.register_buses([eventbus])
    log_queue = QueueConfig('CustomerLog', eventbus, region_name='us-west-2')
    accounts_receivable_queue = QueueConfig('AccountsReceivable', eventbus, region_name='us-west-2')
    listener = PrototypeSQSListener([log_queue, accounts_receivable_queue])
    listener.listen()