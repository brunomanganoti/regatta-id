from django.db import models
from django.contrib.postgres.fields import ArrayField

class Usuario(models.Model):
    class PerfilUsuario(models.TextChoices):
        ALUNO = 'aluno', 'Aluno'
        COLABORADOR = 'colaborador', 'Colaborador'
        VISITANTE = 'visitante', 'Visitante'
        VOLUNTARIO = 'voluntario', 'Voluntário'

    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(blank=True, null=True)
    senha = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=50, blank=True, null=True)
    perfil = models.CharField(max_length=20, choices=PerfilUsuario.choices)
    foto = models.ImageField(upload_to='fotos/', blank=True, null=True)
    ativo = models.BooleanField(default=True)
    observacoes = models.TextField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    consentimento_lgpd = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} ({self.perfil})"

class DadosBiometricos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='biometrias')
    facial_hash = models.TextField()
    data_registro = models.DateTimeField(auto_now_add=True)

class Acesso(models.Model):
    class NivelAcesso(models.TextChoices):
        ADMIN = 'admin', 'Admin'

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='acessos')
    nivel_acesso = models.CharField(max_length=20, choices=NivelAcesso.choices)
    autorizado = models.BooleanField(default=True)

class Turma(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class AlunoTurma(models.Model):
    aluno = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='turmas_aluno')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='alunos')
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)

class Horario(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, blank=True, related_name='horarios')
    hora_entrada = models.TimeField()
    hora_saida = models.TimeField()
    dias_semana = ArrayField(models.CharField(max_length=20), blank=False)

class AcessoRegistrado(models.Model):
    class TipoAcesso(models.TextChoices):
        ENTRADA = 'entrada', 'Entrada'
        SAIDA = 'saida', 'Saída'

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='acessos_registrados')
    tipo_acesso = models.CharField(max_length=20, choices=TipoAcesso.choices)
    local = models.CharField(max_length=255)
    data_hora = models.DateTimeField(auto_now_add=True)
    valido = models.BooleanField(default=True)
    alerta = models.BooleanField(default=False)

class EventoCritico(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='eventos_criticos')
    tipo_evento = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(auto_now_add=True)

class TentativaAcesso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='tentativas_acesso')
    sucesso = models.BooleanField()
    ip_origem = models.CharField(max_length=100, blank=True, null=True)
    data_hora = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField(blank=True, null=True)

class Presenca(models.Model):
    aluno = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='presencas')
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, blank=True, related_name='presencas')
    sala = models.CharField(max_length=255)
    data_presenca = models.DateField()
    presente = models.BooleanField(default=True)

class RotaUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='rotas')
    sala = models.CharField(max_length=255)
    data_hora = models.DateTimeField(auto_now_add=True)
