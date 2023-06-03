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
        thread.start()
