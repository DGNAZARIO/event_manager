from django.shortcuts import render
from .models import Evento

def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'events/lista_eventos.html', {'eventos': eventos})


def detalhes_evento():
    return None