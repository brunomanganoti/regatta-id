from django.db import models
from .usuario import Usuario  # referência cruzada

class Turma(models.Model):
    nome       = models.CharField(max_length=255)
    descricao  = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class AlunoTurma(models.Model):
    aluno       = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="turmas_aluno")
    turma       = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="alunos")
    data_inicio = models.DateField()
    data_fim    = models.DateField(blank=True, null=True)
