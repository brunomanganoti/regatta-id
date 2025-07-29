from django.db import models
from django.contrib.postgres.fields import ArrayField
from .turma import Turma

class Horario(models.Model):
    turma        = models.ForeignKey(Turma, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name="horarios")
    hora_entrada = models.TimeField()
    hora_saida   = models.TimeField()
    dias_semana  = ArrayField(models.CharField(max_length=20))
