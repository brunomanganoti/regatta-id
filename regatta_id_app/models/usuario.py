from django.db import models
from django.contrib.postgres.fields import ArrayField  # se precisar em outro lugar

class Usuario(models.Model):
    class PerfilUsuario(models.TextChoices):
        ALUNO        = "aluno",       "Aluno"
        COLABORADOR  = "colaborador", "Colaborador"
        VISITANTE    = "visitante",   "Visitante"
        VOLUNTARIO   = "voluntario",  "Voluntário"

    nome              = models.CharField(max_length=255)
    cpf               = models.CharField(max_length=14, unique=True)
    email             = models.EmailField(blank=True, null=True)
    senha             = models.CharField(max_length=255, blank=True, null=True)
    telefone          = models.CharField(max_length=50, blank=True, null=True)
    perfil            = models.CharField(max_length=20, choices=PerfilUsuario.choices)
    foto              = models.ImageField(upload_to="fotos/", blank=True, null=True)
    ativo             = models.BooleanField(default=True)
    observacoes       = models.TextField(blank=True, null=True)
    data_cadastro     = models.DateTimeField(auto_now_add=True)
    consentimento_lgpd = models.BooleanField(default=False)
    cargo          = models.CharField(max_length=120, blank=True, null=True)
    data_admissao  = models.DateField(blank=True, null=True)
    rg               = models.CharField("RG", max_length=20, blank=True, null=True)
    validade_inicio  = models.DateField(blank=True, null=True)
    validade_fim     = models.DateField(blank=True, null=True)

    class TurnoEntrada(models.TextChoices):
        MANHA = "manha", "Manhã"
        TARDE = "tarde", "Tarde"
        DIA   = "dia",   "Dia inteiro"

    turno_entrada    = models.CharField(
        max_length=10,
        choices=TurnoEntrada.choices,
        blank=True,
        null=True,
    )
    visitado         = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.perfil})"


class DadosBiometricos(models.Model):
    usuario       = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="biometrias")
    facial_hash   = models.TextField()
    data_registro = models.DateTimeField(auto_now_add=True)


class Acesso(models.Model):
    class NivelAcesso(models.TextChoices):
        ADMIN = "admin", "Admin"

    usuario     = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="acessos")
    nivel_acesso = models.CharField(max_length=20, choices=NivelAcesso.choices)
    autorizado  = models.BooleanField(default=True)
