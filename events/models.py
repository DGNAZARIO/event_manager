from django.db import models
from django.contrib.auth.models import User

class Evento(models.Model):
    nome = models.CharField(max_length=200)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    descricao = models.TextField()
    local = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Inscricao(models.Model):
    nome_participante = models.CharField(max_length=200)
    email_participante = models.EmailField()
    data_inscricao = models.DateTimeField(auto_now_add=True)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscricoes')

    class Meta:
        unique_together = ('evento', 'email_participante')  # Garantir que o email seja único por evento

    def __str__(self):
        return f"{self.nome_participante} - {self.evento.nome}"