from django import forms
from ..models import Horario

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
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'multiple': 'multiple',
        }),
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
