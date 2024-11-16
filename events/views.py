from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.models import Registration
from .forms import EventForm, InscricaoForm, RegistrationForm
from events.models import Inscricao as Registration
import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.shortcuts import render
from .models import Inscricao, Evento
from .forms import FiltroInscricaoForm


def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'events/lista_eventos.html', {'eventos': eventos})


def detalhes_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    inscricoes = evento.inscricoes.all()  # Obter todas as inscrições do evento

    if request.method == 'POST':
        form = InscricaoForm(request.POST, evento=evento)  # Passando o evento para o formulário
        if form.is_valid():
            inscricao = form.save(commit=False)
            inscricao.evento = evento  # Associando o evento à inscrição
            inscricao.save()
            messages.success(request, "Inscrição realizada com sucesso!")
            return redirect('detalhes_evento', evento_id=evento.id)
    else:
        form = InscricaoForm(evento=evento)  # Passando o evento para o formulário

    return render(request, 'events/detalhes_evento.html', {
        'evento': evento,
        'inscricoes': inscricoes,
        'form': form,
    })

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            # Cria o evento sem salvar no banco ainda
            event = form.save(commit=False)
            # Define o organizador do evento como o usuário logado
            event.organizador = request.user
            # Agora salva o evento no banco de dados
            event.save()
            # Redireciona para a lista de eventos ou para outra página
            return redirect('lista_eventos')  # Ou para a página de detalhes do evento, conforme necessário
    else:
        form = EventForm()

    return render(request, 'events/create_event.html', {'form': form})


@login_required
def edit_event(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, organizador=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('lista_eventos')
    else:
        form = EventForm(instance=evento)
    return render(request, 'events/edit_event.html',  {'form': form, 'evento': evento})

def register_participant(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Salva a inscrição
            messages.success(request, "Inscrição realizada com sucesso!")
            return redirect('event_list')  # Redirecionar para a lista de eventos, por exemplo
    else:
        form = RegistrationForm()
    return render(request, 'events/register_participant.html', {'form': form})


@login_required
def edit_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id)
    evento = registration.evento  # Pegue o evento da inscrição
    form = RegistrationForm(instance=registration)

    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=registration)
        if form.is_valid():
            form.save()
            if evento:  # Verifique se o evento existe
                messages.success(request, "Inscrição atualizada com sucesso.")
                return redirect('detalhes_evento', evento_id=evento.id)  # Passando o evento.id correto
            else:
                messages.error(request, "Evento não encontrado para a inscrição.")
        else:
            messages.error(request, "Erro ao atualizar a inscrição. Verifique os dados fornecidos.")

    return render(request, 'events/edit_registration.html', {'form': form, 'registration': registration})


def delete_registration(request, registration_id):
    registration = get_object_or_404(Inscricao, id=registration_id)

    if request.method == 'POST':
        event_id = registration.evento.id
        registration.delete()
        messages.success(request, "Inscrição cancelada com sucesso.")
        send_confirmation_email(registration, "Sua inscrição foi cancelada com sucesso.")
        return redirect('detalhes_evento', evento_id=event_id)

    return render(request, 'events/delete_registration.html', {'registration': registration})


@login_required
def deletar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)

    if request.method == 'POST':
        evento.delete()
        return redirect('lista_eventos')  # Redireciona após exclusão

    return render(request, 'events/deletar_evento.html', {'evento': evento})


# Função auxiliar para enviar e-mail
def send_confirmation_email(registration, message):
    from django.core.mail import send_mail
    try:
        send_mail(
            subject="Confirmação de Cancelamento",
            message=message,
            from_email="seu-email@dominio.com",
            recipient_list=[registration.email_participante],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def __init__(self, *args, **kwargs):
    self.evento = kwargs.pop('evento', None)  # Recebe o evento da view
    super(InscricaoForm, self).__init__(*args, **kwargs)

def save(self, commit=True):
    evento = super().save(commit=False)
    if commit:
        evento.save()
    return evento


def listar_inscricoes(request):
    form = FiltroInscricaoForm(request.GET or None)
    inscricoes = Inscricao.objects.all()

    if form.is_valid():
        evento = form.cleaned_data.get('evento')
        data_inicio = form.cleaned_data.get('data_inicio')
        data_fim = form.cleaned_data.get('data_fim')

        if evento:
            inscricoes = inscricoes.filter(evento=evento)
        if data_inicio:
            inscricoes = inscricoes.filter(data_inscricao__date__gte=data_inicio)
        if data_fim:
            inscricoes = inscricoes.filter(data_inscricao__date__lte=data_fim)

    return render(request, 'listar_inscricoes.html', {'form': form, 'inscricoes': inscricoes})

def relatorio_inscricoes(request):
    eventos = Evento.objects.all()
    relatorio = []

    for evento in eventos:
        total_inscricoes = Inscricao.objects.filter(evento=evento).count()
        relatorio.append({'evento': evento.nome, 'total_inscricoes': total_inscricoes})

    return render(request, 'relatorio_inscricoes.html', {'relatorio': relatorio})


def exportar_inscricoes_csv(request, evento_id):
    evento = Evento.objects.get(pk=evento_id)
    inscricoes = Inscricao.objects.filter(evento=evento)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="inscricoes_{evento_id}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nome', 'Email', 'Data de Inscrição'])
    for inscricao in inscricoes:
        writer.writerow([inscricao.nome, inscricao.email, inscricao.data_inscricao])

    return response