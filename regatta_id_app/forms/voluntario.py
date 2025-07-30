from django import forms
from .usuario import UsuarioForm
from ..models import Usuario

class VoluntarioForm(UsuarioForm):
    class Meta(UsuarioForm.Meta):
        fields = UsuarioForm.Meta.fields + [
            "rg",
            "cargo",          # área de atuação
            "data_admissao",  # data de entrada
            "validade_fim",   # data de saída opcional
            "observacoes",
        ]
        widgets = {
            **UsuarioForm.Meta.widgets,
            "rg":            forms.TextInput(attrs={"class": "form-control"}),
            "cargo":         forms.TextInput(attrs={"class": "form-control"}),
            "data_admissao": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "validade_fim":  forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "observacoes":   forms.Textarea(attrs={"class": "form-control", "rows":3}),
        }
