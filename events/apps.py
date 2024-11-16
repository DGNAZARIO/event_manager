# events/apps.py
from django.apps import AppConfig

class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Usado em Django 3.2+ para gerar IDs automaticamente
    name = 'events'  # Nome do app
    verbose_name = 'Eventos'  # Nome legível para o app
