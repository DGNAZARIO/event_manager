from django import forms
from .models import Inscricao, Evento
from events.models import Registration
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['nome_participante', 'email_participante']

    def __init__(self, *args, **kwargs):
        # Permitir a passagem do evento no momento da criação ou edição
        self.evento = kwargs.pop('evento', None)
        super(InscricaoForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email_participante")

        # Verificar se o evento foi passado corretamente
        if not self.evento:
            raise forms.ValidationError("O evento não foi associado corretamente.")

        # Validar se o email já está inscrito para o evento
        if Inscricao.objects.filter(evento=self.evento, email_participante=email).exists():
            raise forms.ValidationError("Este e-mail já está inscrito para este evento.")

        return cleaned_data


class EventForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nome', 'descricao', 'data_inicio', 'data_fim', 'local', 'organizador']

    data_inicio = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local'
        })
    )
    data_fim = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local'
        })
    )

    def save(self, commit=True):
        evento = super().save(commit=False)
        if commit:
            evento.save()
        return evento


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['nome_participante', 'email_participante', 'evento']


class FiltroInscricaoForm(forms.Form):
    evento = forms.ModelChoiceField(queryset=Evento.objects.all(), required=False, label="Evento")
    data_inicio = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Data Inicial")
    data_fim = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Data Final")

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())


class RegistroForm(UserCreationForm):
    username = forms.CharField(
        label=_('Usuário'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Digite seu usuário')}),
        error_messages={
            'required': _('Por favor, insira um nome de usuário.'),
            'unique': _('Este nome de usuário já está em uso.'),
        }
    )
    email = forms.EmailField(
        label=_('E-mail'),
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Digite seu e-mail')}),
        error_messages={
            'required': _('Por favor, insira um e-mail.'),
            'invalid': _('Por favor, insira um e-mail válido.'),
        }
    )
    password1 = forms.CharField(
        label=_('Senha'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Digite sua senha')}),
        error_messages={
            'required': _('Por favor, insira uma senha.'),
        }
    )
    password2 = forms.CharField(
        label=_('Confirmação de Senha'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Confirme sua senha')}),
        error_messages={
            'required': _('Por favor, confirme sua senha.'),
            'password_mismatch': _('As senhas não coincidem.'),
        }
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        # Remove textos de ajuda padrão
        for field in self.fields.values():
            field.help_text = None