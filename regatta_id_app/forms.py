from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario, Turma, Horario
import re

def validar_cpf(cpf: str):
    """
    Valida um CPF brasileiro:
    - Deve ter 11 dígitos
    - Não pode ser sequência de dígitos iguais
    - Deve validar dígitos verificadores
    """
    # Remove tudo que não for dígito
    cpf_num = re.sub(r'\D', '', cpf)

    if len(cpf_num) != 11:
        raise ValidationError('CPF deve conter 11 dígitos numéricos.')

    # Rejeita CPFs com todos os dígitos iguais (ex. 111.111.111-11)
    if cpf_num == cpf_num[0] * 11:
        raise ValidationError('CPF inválido.')

    # Calcula dígitos verificadores
    def calc_digito(seq):
        s = sum(int(a) * b for a, b in zip(seq, range(len(seq)+1, 1, -1)))
        resto = (s * 10) % 11
        return '0' if resto == 10 else str(resto)

    dv1 = calc_digito(cpf_num[:9])
    dv2 = calc_digito(cpf_num[:9] + dv1)

    if cpf_num[-2:] != dv1 + dv2:
        raise ValidationError('CPF inválido.')

    return cpf_num  # opcional: retorna somente números

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nome',
            'email',
            'cpf',
            'telefone',
            'foto',
        ]
        widgets = {
            'nome':     forms.TextInput(attrs={'class':'form-control'}),
            'email':    forms.EmailInput(attrs={'class':'form-control'}),
            'cpf':      forms.TextInput(attrs={'class':'form-control', 'placeholder':'000.000.000-00'}),
            'telefone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'(00) 90000-0000'}),
            'foto':     forms.ClearableFileInput(attrs={'class':'form-control', 'accept':'image/*'}),
        }


    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf', '')
        cpf_num = validar_cpf(cpf)

        # Se estamos editando e o CPF não mudou, permite salvar
        if self.instance and self.instance.pk:
            instance_cpf = re.sub(r'\D', '', self.instance.cpf or '')
            if instance_cpf == cpf_num:
                return cpf_num

        # Verifica se há outro usuário com o mesmo CPF
        if Usuario.objects.filter(cpf=cpf_num).exists():
            raise ValidationError('Este CPF já está cadastrado em outro usuário.')

        return cpf_num


    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone', '')
        # remove tudo que não for dígito
        tel_num = re.sub(r'\D', '', telefone)

        # Telefones brasileiros: DDD (2) + 8 ou 9 dígitos
        if not re.fullmatch(r'\d{10,11}', tel_num):
            raise ValidationError('Telefone inválido. Informe DDD + número (10 ou 11 dígitos).')

        return tel_num  # opcional: armazena somente números

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da turma'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição da turma',
                'rows': 4
            }),
        }

DIAS_SEMANA_CHOICES = [
    ('segunda', 'Segunda-feira'),
    ('terca', 'Terça-feira'),
    ('quarta', 'Quarta-feira'),
    ('quinta', 'Quinta-feira'),
    ('sexta', 'Sexta-feira'),
    ('sabado', 'Sábado'),
    ('domingo', 'Domingo'),
]

class HorarioForm(forms.ModelForm):
    dias_semana = forms.MultipleChoiceField(
        choices=DIAS_SEMANA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Dias da Semana',
        required=True
    )

    class Meta:
        model = Horario
        fields = ['turma', 'hora_entrada', 'hora_saida', 'dias_semana']
        widgets = {
            'hora_entrada': forms.TimeInput(attrs={'type': 'time'}),
            'hora_saida': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        entrada = cleaned_data.get('hora_entrada')
        saida = cleaned_data.get('hora_saida')

        if entrada and saida and entrada >= saida:
            self.add_error('hora_saida', 'A hora de saída deve ser depois da hora de entrada.')
