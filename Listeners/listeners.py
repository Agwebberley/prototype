from decimal import Decimal
import multiprocessing
import boto3
import json
import sqlite3

class BaseSQSListener(multiprocessing.Process):
    def __init__(self, queue_url):
        multiprocessing.Process.__init__(self)
        self.sqs = boto3.client('sqs')
        self.sns = boto3.client('sns')
        self.queue_url = queue_url
        self.stop_event = multiprocessing.Event()
        print(f"Starting listener for queue {queue_url}")
        multiprocessing.Process.__init__(self)

    def run(self):
        while not self.stop_event.is_set():
            messages = self.sqs.receive_message(QueueUrl=self.queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=20)
            if 'Messages' in messages:
                for message in messages['Messages']:
                    self.handle_message(message)
                    self.sqs.delete_message(QueueUrl=self.queue_url, ReceiptHandle=message['ReceiptHandle'])

    def handle_message(self, message):
        raise NotImplementedError

    def stop(self):
        self.stop_event.set()



class OrderListener(BaseSQSListener):
    def handle_message(self, message):
        print(f"Order Queue handling message: {message}")

class ManufactureListener(BaseSQSListener):

    def __init__(self, queue_url):
        super().__init__(queue_url)
        self.conn = sqlite3.connect("queue.db")
        self.c = self.conn.cursor()
        self.c.execute("INSERT INTO queues VALUES (?, ?)", ("Manufacture", "pick"))
        self.conn.commit()
        self.conn.close()
    def handle_message(self, message):
        message = message["Body"].split(" ")
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

class InventoryListener(BaseSQSListener):
    def __init__(self, queue_url):
        super().__init__(queue_url)
        self.conn = sqlite3.connect("queue.db")
        self.c = self.conn.cursor()
        self.c.execute("INSERT INTO queues VALUES (?, ?)", ("Inventory", "item"))
        self.c.execute("INSERT INTO queues VALUES (?, ?)", ("Inventory", "order"))
        self.c.execute("INSERT INTO queues VALUES (?, ?)", ("Inventory", "manufacture"))
        self.conn.commit()
        self.conn.close()
    def handle_message(self, message):
        from Inventory.models import Inventory, Pick
        from Items.models import Items
        message_json = json.loads(message.body)
        message_body = message_json['Message'].split(' ')
        print(message_body)
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
                inventory.typeI = "shipment"
                inventory.save()
                ManufactureHistory.objects.create(manufacture=manufacture.pk, item=manufacture.item, quantity=manufacture.quantity, is_complete=True)
                manufacture.delete()
            except Exception as e:
                print(f"Manufacture with id {message_body[2]} did not create")
                print(e)


class AccountsReceivableListener(BaseSQSListener):
    def __init__(self, queue_url):
        super().__init__(queue_url)
        self.conn = sqlite3.connect("queue.db")
        self.c = self.conn.cursor()
        self.c.execute("INSERT INTO queues VALUES (?, ?)", ("AccountsReceivable", "order"))
        self.conn.commit()
        self.conn.close()
    def handle_message(self, message):
        from Orders.models import Orders
        from AccountsReceivable.models import AccountsReceivable

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


class LogListener(BaseSQSListener):
    def handle_message(self, message):
        from Shared.models import logmessage
        print(f"Log Queue handling message: {message}")
        logmessage.objects.create(message=message["Body"])

        # Forward the message to its respective queue(s)
        # Get the sender's name from the message
        sender = message["Body"].split(" ")[0]
        # Get the queue(s) that are listening to the sender
        conn = sqlite3.connect("queue.db")
        c = conn.cursor()
        topics = c.execute("SELECT topic FROM queues WHERE listeningto=?", (sender,)).fetchall()
        conn.close()
        print(topics)
        # Send the message to each queue
        for topic in topics:
            print("Sending " + topic[0])
            self.sns.publish(TopicArn=f"arn:aws:sns:us-west-2:710141730058:{topic[0]}", Message=message["Body"])
