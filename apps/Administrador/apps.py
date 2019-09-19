from django.apps import AppConfig


class AdministradorConfig(AppConfig):
    name = 'Administrador'
    print("Created: ")
    def ready(self):
        import apps.Administrador.senal