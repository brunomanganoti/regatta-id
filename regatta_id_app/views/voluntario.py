from django.shortcuts import render, redirect, get_object_or_404
from ..models import Usuario
from ..forms.voluntario import VoluntarioForm
from .decorator import admin_required

VOLUNT = Usuario.PerfilUsuario.VOLUNTARIO

@admin_required
def listar_voluntarios(request):
    """
    Lista voluntários com filtros por nome e data de entrada (`data_admissao`).
    `cargo` é exibido na tabela como “Área de atuação”.
    """
    voluntarios = Usuario.objects.filter(perfil=VOLUNT)

    # filtros ---------------------------------------------------------------
    nome_q = request.GET.get("q", "").strip()
    if nome_q:
        voluntarios = voluntarios.filter(nome__icontains=nome_q)

    data_q = request.GET.get("data_admissao")
    if data_q:
        voluntarios = voluntarios.filter(data_admissao=data_q)

    voluntarios = voluntarios.order_by("nome")

    return render(
        request,
        "voluntario/voluntario.html",
        {
            "voluntarios": voluntarios,
            "filtro_nome": nome_q,
            "filtro_data": data_q,
        },
    )

# ---------------------- helper -------------------------------------------
def _salvar_voluntario(request, instance=None):
    """Cria ou edita um voluntário."""
    if request.method == "POST":
        form = VoluntarioForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            vol = form.save(commit=False)
            vol.perfil = VOLUNT
            vol.save()
            return redirect("listar_voluntarios")
    else:
        form = VoluntarioForm(instance=instance)

    return render(
        request,
        "voluntario/cadastro_voluntario.html",
        {"form": form},
    )

# ---------------------- criar --------------------------------------------
@admin_required
def cadastrar_voluntario(request):
    return _salvar_voluntario(request)

# ---------------------- editar -------------------------------------------
@admin_required
def editar_voluntario(request, pk):
    vol = get_object_or_404(Usuario, pk=pk, perfil=VOLUNT)
    return _salvar_voluntario(request, instance=vol)

# ---------------------- excluir ------------------------------------------
@admin_required
def excluir_voluntario(request, pk):
    vol = get_object_or_404(Usuario, pk=pk, perfil=VOLUNT)
    vol.delete()
    return redirect("listar_voluntarios")
