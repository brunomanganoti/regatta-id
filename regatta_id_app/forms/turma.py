# regatta_id_app/forms/turma.py

from django import forms
from ..models import Turma

DIAS_SEMANA_CHOICES = [
    ('segunda', 'Segunda-feira'),
    ('terca', 'Terça-feira'),
    ('quarta', 'Quarta-feira'),
    ('quinta', 'Quinta-feira'),
    ('sexta', 'Sexta-feira'),
    ('sabado', 'Sábado'),
    ('domingo', 'Domingo'),
]


class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        # adicionamos o campo `codigo` antes de descrição
        fields = ['nome', 'codigo', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da turma'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código da turma (ex: TURMA-0001)'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição da turma',
                'rows': 4
            }),
        }
        dias_semana = forms.MultipleChoiceField(
            choices=DIAS_SEMANA_CHOICES,
            widget=forms.SelectMultiple(
                attrs={
                    'class': 'form-select',
                    'multiple': 'multiple',
                }
            ),
            label='Dias da Semana',
            required=True
        )
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da turma'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código da turma (ex: TURMA-0001)'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição da turma',
                'rows': 4
            }),
        }
