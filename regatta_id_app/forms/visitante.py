from django import forms
from .usuario import UsuarioForm
from ..models import Usuario

class VisitanteForm(UsuarioForm):
    class Meta(UsuarioForm.Meta):
        fields = UsuarioForm.Meta.fields + [
            "rg",
            "validade_inicio",
            "validade_fim",
            "turno_entrada",
            "visitado",
            "observacoes",
        ]
        widgets = {
            **UsuarioForm.Meta.widgets,
            "rg": forms.TextInput(attrs={"class": "form-control"}),
            "validade_inicio": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "validade_fim":    forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "turno_entrada":   forms.Select(attrs={"class": "form-select"}),
            "visitado":        forms.TextInput(attrs={"class": "form-control"}),
            "observacoes":     forms.Textarea(attrs={"class": "form-control", "rows":3}),
        }
