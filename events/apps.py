from django.apps import AppConfig

# Configuració de l'aplicació "events"
class EventsConfig(AppConfig):
    # Tipus de camp per defecte per a les claus primàries
    default_auto_field = 'django.db.models.BigAutoField'
    # Nom de l'aplicació
    name = 'events'
