from django.apps import AppConfig
from django.contrib.auth.models import Group

class EsclerosisappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EsclerosisApp'

    def ready(self):
        try:
            grupos = ["Administradores", "Usuarios"]

            for g in grupos:
                Group.objects.get_or_create(name=g)

        except Exception:
            pass
