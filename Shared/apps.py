from django.apps import AppConfig


class SharedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Shared'

    def ready(self):
        pass
        #import Shared.signals
