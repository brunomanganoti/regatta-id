from django.shortcuts import render, redirect, get_object_or_404
from ..models import Usuario
from ..forms import UsuarioForm
from .decorator import admin_required

def _crud_generico(request, perfil, template_dir, instance=None):
    # usado por cadastrar/editar
    ...

# ----------------- Colaboradores -----------------
COLAB = Usuario.PerfilUsuario.COLABORADOR
@admin_required
def listar_colaboradores(request):
    colaboradores = Usuario.objects.filter(perfil=COLAB)
    return render(request, 'regatta_id_app/colaboradores/colaboradores.html',
                  {'colaboradores': colaboradores})

@admin_required
def cadastrar_colaborador(request):
    return _crud_generico(request, COLAB, 'colaboradores')

@admin_required
def editar_colaborador(request, pk):
    inst = get_object_or_404(Usuario, pk=pk, perfil=COLAB)
    return _crud_generico(request, COLAB, 'colaboradores', inst)

@admin_required
def excluir_colaborador(request, pk):
    # (…igual…)
    ...

# Faça o mesmo bloco para Visitantes e Voluntários,
# mudando a constante de perfil e pasta de templates.
