from django import forms
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.shortcuts import redirect
from ..models import Usuario

def root_redirect_view(request):
    if request.session.get('usuario_id'):
        return redirect('dashboard')
    return redirect('login')

class LoginForm(forms.Form):
    """
    Formulário simples para autenticação por e-mail e senha.
    """
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Entre com seu E-mail",
                "required": "required",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Entre com sua senha",
                "required": "required",
            }
        )
    )

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("email")
        senha = cleaned.get("password")

        try:
            user = Usuario.objects.get(email=email, senha=senha, ativo=True)
        except Usuario.DoesNotExist:
            raise forms.ValidationError("Email ou senha inválidos.")

        # exige permissão de administrador
        if not user.acessos.filter(nivel_acesso="admin", autorizado=True).exists():
            raise forms.ValidationError("Acesso permitido apenas para administradores.")

        cleaned["user"] = user
        return cleaned
class LoginView(FormView):
    """
    View de autenticação usando `FormView` para separar regras de negócio
    da apresentação e aproveitar validação de formulário.
    """
    template_name = "sistema/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("dashboard")

    # evita que usuário logado veja novamente a tela de login
    def dispatch(self, request, *args, **kwargs):
        if request.session.get("usuario_id"):
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.cleaned_data["user"]
        # popula sessão
        self.request.session["usuario_id"] = user.id
        self.request.session["usuario_nome"] = user.nome
        return super().form_valid(form)


def logout_view(request):
    request.session.flush()
    return redirect('login')

