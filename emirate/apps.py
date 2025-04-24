from django.apps import AppConfig


class EmirateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emirate'


    def ready(self):
        import emirate.signals  # Assurez-vous de charger vos signaux lors du chargement de l'application
   






