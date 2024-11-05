from .models import Evento
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from .forms import EventForm

def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'events/lista_eventos.html', {'eventos': eventos})


def detalhes_evento():
    return None

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm()
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # Associa o evento ao organizador logado
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user)  # Apenas o organizador pode editar
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/edit_event.html', {'form': form})


def event_detail():
    return None


def event_list():
    return None