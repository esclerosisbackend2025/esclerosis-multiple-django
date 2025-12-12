from django.apps import AppConfig

class EsclerosisappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EsclerosisApp'

    def ready(self):
        import EsclerosisApp.signals

