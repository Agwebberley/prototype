from django.apps import AppConfig


class ManufactureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Manufacture'

    def ready(self):
        import Manufacture.signals
