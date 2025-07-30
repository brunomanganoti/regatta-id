from django import forms
from ..models import Usuario
from .usuario import UsuarioForm

class ColaboradorForm(UsuarioForm):
    class Meta(UsuarioForm.Meta):
        # acrescenta os novos campos
        fields = UsuarioForm.Meta.fields + ["cargo", "data_admissao"]
        widgets = {
            **UsuarioForm.Meta.widgets,
            "cargo": forms.TextInput(attrs={"class": "form-control"}),
            "data_admissao": forms.DateInput(attrs={"type": "date",
                                                    "class": "form-control"}),
        }
