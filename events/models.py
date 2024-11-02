# events/models.py

from django.db import models

class Evento(models.Model):
    nome = models.CharField(max_length=200)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    descricao = models.TextField()
    local = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
