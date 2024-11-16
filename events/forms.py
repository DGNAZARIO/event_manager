from django import forms
from .models import Inscricao, Evento
from events.models import Registration

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