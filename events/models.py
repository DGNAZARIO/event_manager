# events/models.py
from django.db import models
from django.contrib.auth.models import User

# Modelo Evento
class Evento(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    local = models.CharField(max_length=255)
    organizador = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['data_inicio']

# Modelo Inscricao
class Inscricao(models.Model):
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE, related_name='inscricoes')
    nome_participante = models.CharField(max_length=200)
    email_participante = models.EmailField()
    data_inscricao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome_participante} - {self.evento.nome}"

    class Meta:
        unique_together = ('evento', 'email_participante')
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        ordering = ['data_inscricao']

# Modelo Registration (corrigido)
class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user} - {self.evento}"