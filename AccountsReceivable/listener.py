from Shared.listener import SQSListener

class AccountsReceivableListener(SQSListener):
    def handle_message(self, message):
        return super().handle_message(message)