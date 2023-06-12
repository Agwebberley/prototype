from Shared.listener import SQSListener

from .models import AccountsReceivableHistory, AccountsReceivable
from orders.models import Orders

class AccountsReceivableListener(SQSListener):
    def handle_message(self, message):
        # split the message into a list by spaces
        message = message.split(' ')

        # if the message is an order created message
        # create an AccountsReceivable object for the order
        if message[0] == 'order' and message[1] == 'created':
            order = Orders.objects.get(id=message[2])
            order_total = float(order.get_order_total())
            AccountsReceivable.objects.create(order=order, amount=order_total)
        # if the message is an order deleted message
        # delete the AccountsReceivable object for the order if it exists
        elif message[0] == 'order' and message[1] == 'deleted':
            order = Orders.objects.get(id=message[2])
            try:
                accounts_receivable = AccountsReceivable.objects.get(order=order)
                accounts_receivable.delete()
            except AccountsReceivable.DoesNotExist:
                pass
        # if the message is an order updated message
        # update the AccountsReceivable object for the order if it exists
        elif message[0] == 'order' and message[1] == 'updated':
            order = Orders.objects.get(id=message[2])
            try:
                accounts_receivable = AccountsReceivable.objects.get(order=order)
                order_total = float(order.get_order_total())
                accounts_receivable.amount = order_total
                accounts_receivable.save()
            except AccountsReceivable.DoesNotExist:
                pass