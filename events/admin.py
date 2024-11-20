# events/admin.py
from django.contrib import admin
from .models import Evento, Inscricao

# Registre os modelos no Django Admin para gerenciá-los
admin.site.register(Evento)
admin.site.register(Inscricao)
