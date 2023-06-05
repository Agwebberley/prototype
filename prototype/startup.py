"""
import threading

# The URLListener class dynamically imports a specified class and starts a listener thread for it.
class URLListener:
    def __init__(self, url, class_name):
        self.url = url
        self.class_name = class_name

    def start(self):
        # Import the class dynamically
        module = __import__('Customers.listener', fromlist=[self.class_name])
        class_ = getattr(module, self.class_name)

        # Create an instance of the class and start the listener
        listener = class_(self.url)
        thread = threading.Thread(target=listener.start)
        thread.daemon = True
        thread.start()



if __name__ == "__main__":
    urls = {"https://sqs.us-west-2.amazonaws.com/710141730058/CustomerLog": "LogListener"}
    for class_name, url in urls.items():
        print("Starting listener for " + class_name + " on " + url)
        Listener = URLListener(url, class_name)
        thread = threading.Thread(target=Listener.start)
        thread.daemon = True
        thread.start()
        print("Started listener for " + class_name + " on " + url)
"""
"""
import asyncio
from Customers.listener import LogListener

async def async_listeners():
    print('Starting SQS listeners...')
    LogListenerUrl = 'https://sqs.us-west-2.amazonaws.com/710141730058/CustomerLog'

    LogListenerTask = LogListener(LogListenerUrl)

    await LogListenerTask.start()
    print('Started SQS listeners... ASYNC')

if __name__ == "prototype.startup":
    urls = {"https://sqs.us-west-2.amazonaws.com/710141730058/CustomerLog": "LogListener"}
    for class_name, url in urls.items():
        print("Starting listener for " + class_name + " on " + url)
        asyncio.run(async_listeners())
        print("Started listener for " + class_name + " on " + url)
"""