from django.template.context_processors import request

from .models import Evento
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Inscricao
from .forms import InscricaoForm
from django.core.mail import send_mail

def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'events/lista_eventos.html', {'eventos': eventos})


def detalhes_evento():
    evento = get_object_or_404(Evento, id=id)
    inscricoes = evento.inscricoes.all()  # Inscrições já feitas para o evento

    if request.method == 'POST':
        form = InscricaoForm(request.POST)
        if form.is_valid():
            inscricao = form.save(commit=False)
            inscricao.evento = evento

            if Inscricao.objects.filter(email_participante=inscricao.email_participante, evento=evento).exists():
                messages.error(request, "Este e-mail já foi usado para se inscrever neste evento.")
            else:
                inscricao.save()
                messages.success(request, "Inscrição realizada com sucesso!")
                return redirect('event_detail', id=evento.id)
    else:
        form = InscricaoForm()

        return render(request, 'detalhes_evento.html', {'evento': evento, 'form': form, 'inscricoes': inscricoes})

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



def edit_registration(request, registration_id):
    registration = get_object_or_404(Inscricao, id=registration_id)

    if request.method == 'POST':
        form = InscricaoForm(request.POST, instance=registration)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscrição atualizada com sucesso.")
            # (Opcional) Envio de e-mail de confirmação de atualização
            send_mail(
                'Confirmação de Atualização de Inscrição',
                'Sua inscrição foi atualizada com sucesso.',
                'seu_email@example.com',
                [registration.email],
                fail_silently=False,
            )
            return redirect('event_detail', event_id=registration.event.id)
    else:
        form = InscricaoForm(instance=registration)
    return render(request, 'events/edit_registration.html', {'form': form, 'registration': registration})


def delete_registration(request, registration_id):
    registration = get_object_or_404(Inscricao, id=registration_id)

    if request.method == 'POST':
        event_id = registration.event.id  # Salva o ID do evento para redirecionamento
        registration.delete()
        messages.success(request, "Inscrição cancelada com sucesso.")
        # (Opcional) Envio de e-mail de confirmação de cancelamento
        send_mail(
            'Confirmação de Cancelamento de Inscrição',
            'Sua inscrição foi cancelada com sucesso.',
            'seu_email@example.com',
            [registration.email],
            fail_silently=False,
        )
        return redirect('event_detail', event_id=event_id)

    return render(request, 'events/delete_registration.html', {'registration': registration})
