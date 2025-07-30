from django.db import models
from .usuario import Usuario

class AcessoRegistrado(models.Model):
    class TipoAcesso(models.TextChoices):
        ENTRADA = "entrada", "Entrada"
        SAIDA   = "saida",   "Saída"

    usuario    = models.ForeignKey(Usuario, on_delete=models.CASCADE,
                                   related_name="acessos_registrados")
    tipo_acesso = models.CharField(max_length=20, choices=TipoAcesso.choices)
    local      = models.CharField(max_length=255)
    data_hora  = models.DateTimeField(auto_now_add=True)
    valido     = models.BooleanField(default=True)
    alerta     = models.BooleanField(default=False)


class TentativaAcesso(models.Model):
    usuario   = models.ForeignKey(Usuario, on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name="tentativas_acesso")
    sucesso   = models.BooleanField()
    ip_origem = models.CharField(max_length=100, blank=True, null=True)
    data_hora = models.DateTimeField(auto_now_add=True)
    motivo    = models.TextField(blank=True, null=True)


class RotaUsuario(models.Model):
    usuario   = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="rotas")
    sala      = models.CharField(max_length=255)
    data_hora = models.DateTimeField(auto_now_add=True)
