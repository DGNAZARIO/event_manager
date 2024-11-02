from django.shortcuts import render, get_object_or_404
from .models import Evento

def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'events/lista_eventos.html', {'eventos': eventos})

def detalhes_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    return render(request, 'events/detalhes_evento.html', {'evento': evento})
