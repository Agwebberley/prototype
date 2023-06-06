from django.apps import AppConfig

class CustomersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Customers'

    def ready(self):
        # Start the listener
        #t = threading.Thread(target=self.start_listener)
        #t.daemon = True
        #t.start()
        # Import signals after starting the listener
        import Customers.signals
        #import prototype.startup
        
