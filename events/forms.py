from django import forms
from .models import Inscricao

class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['nome_participante', 'email_participante']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email_participante")
        evento = self.instance.evento  # O evento associado deve ser passado ao formulário

        if Inscricao.objects.filter(evento=evento, email_participante=email).exists():
            raise forms.ValidationError("Este e-mail já está inscrito para este evento.")
