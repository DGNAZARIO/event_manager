from events.models import Registration
from .forms import EventForm, InscricaoForm, RegistrationForm
from events.models import Inscricao as Registration
import csv
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Inscricao
from .forms import FiltroInscricaoForm
from .forms import LoginForm
from .models import Usuario
from django.contrib.auth.hashers import check_password
from django.shortcuts import  redirect
from django.contrib import messages
from .forms import RegistroForm
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Evento, Relatorio

@login_required
def lista_eventos(request):
    eventos = Evento.objects.filter(organizador=request.user)
    return render(request, 'events/lista_eventos.html', {'eventos': eventos})

@login_required
def detalhes_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    inscricoes = evento.inscricoes.all()

    if request.method == 'POST':
        form = InscricaoForm(request.POST, evento=evento)
        if form.is_valid():
            inscricao = form.save(commit=False)
            inscricao.evento = evento
            inscricao.save()
            messages.success(request, "Inscrição realizada com sucesso!")
            return redirect('detalhes_evento', evento_id=evento.id)
    else:
        form = InscricaoForm(evento=evento)

    return render(request, 'events/detalhes_evento.html', {
        'evento': evento,
        'inscricoes': inscricoes,
        'form': form,
    })

@login_required
def create_event(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Você precisa estar logado para criar eventos.")
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizador = request.user
            event.save()
            return redirect('lista_eventos')
    else:
        form = EventForm()

    return render(request, 'events/create_event.html', {'form': form})


@login_required
def edit_event(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, organizador=request.user)

    if evento.organizador != request.user:
        return HttpResponseForbidden("Você não tem permissão para editar este evento.")

    if request.method == 'POST':
        form = EventForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('lista_eventos')
    else:
        form = EventForm(instance=evento)
    return render(request, 'events/edit_event.html',  {'form': form, 'evento': evento})

@login_required
def register_participant(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscrição realizada com sucesso!")
            return redirect('event_list')
    else:
        form = RegistrationForm()
    return render(request, 'events/register_participant.html', {'form': form})


@login_required
def edit_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id)
    evento = registration.evento
    form = RegistrationForm(instance=registration)

    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=registration)
        if form.is_valid():
            form.save()
            if evento:
                messages.success(request, "Inscrição atualizada com sucesso.")
                return redirect('detalhes_evento', evento_id=evento.id)
            else:
                messages.error(request, "Evento não encontrado para a inscrição.")
        else:
            messages.error(request, "Erro ao atualizar a inscrição. Verifique os dados fornecidos.")

    return render(request, 'events/edit_registration.html', {'form': form, 'registration': registration})

@login_required
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
        return redirect('lista_eventos')

    return render(request, 'events/deletar_evento.html', {'evento': evento})



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

def is_admin(user):
    return user.is_superuser


@login_required
def relatorio_inscricoes(request):
    if request.user.is_staff:
        relatorios = Relatorio.objects.all()
    else:

        relatorios = Relatorio.objects.filter(usuario=request.user)

    eventos = Evento.objects.filter(organizador=request.user).annotate(total_inscricoes=Count('inscricoes')) if not request.user.is_staff else Evento.objects.annotate(total_inscricoes=Count('inscricoes'))

    relatorio = [{'evento': evento.nome, 'total_inscricoes': evento.total_inscricoes} for evento in eventos]

    if request.GET.get('exportar') == '1':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio_inscricoes.csv"'

        writer = csv.writer(response)
        writer.writerow(['Evento', 'Total de Inscrições'])
        for item in relatorio:
            writer.writerow([item['evento'], item['total_inscricoes']])

        return response

    return render(request, 'events/relatorio_inscricoes.html', {'relatorio': relatorio})

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


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                usuario = Usuario.objects.get(username=username)
                if check_password(password, usuario.password):
                    request.session['usuario_id'] = usuario.id
                    return redirect('home')
                else:
                    form.add_error(None, "Senha incorreta.")
            except Usuario.DoesNotExist:
                form.add_error(None, "Usuário não encontrado.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def home_view(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)
        return render(request, 'home.html', {'usuario': usuario})
    else:
        return redirect('login')

def logout_view(request):
    try:
        del request.session['usuario_id']
    except KeyError:
        pass
    return redirect('login')


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = RegistroForm()

    return render(request, 'registration/registro.html', {'form': form})