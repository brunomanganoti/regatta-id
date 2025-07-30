from django.db import models
from .usuario import Usuario
from .turma import Turma

class Presenca(models.Model):
    aluno        = models.ForeignKey(Usuario, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name="presencas")
    turma        = models.ForeignKey(Turma, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name="presencas")
    sala         = models.CharField(max_length=255)
    data_presenca = models.DateField()
    presente     = models.BooleanField(default=True)
