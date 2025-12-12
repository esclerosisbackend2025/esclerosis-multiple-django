from django.apps import AppConfig


class EsclerosisappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EsclerosisApp'

    def ready(self):
        # Importar dentro para evitar AppRegistryNotReady
        from django.contrib.auth.models import Group

        grupos = ["Administradores", "Usuarios"]

        for g in grupos:
            Group.objects.get_or_create(name=g)
