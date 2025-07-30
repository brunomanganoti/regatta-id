from django.shortcuts import render, redirect, get_object_or_404
from ..models import Usuario
from ..forms.visitante import VisitanteForm
from .decorator import admin_required

VISIT = Usuario.PerfilUsuario.VISITANTE

@admin_required
def listar_visitantes(request):
    """
    Exibe a tabela de visitantes com filtros simples
    (nome e data de admissão).
    """
    visitantes = Usuario.objects.filter(perfil=VISIT)

    # ---- filtros ---------------------------------------------------------
    nome_q = request.GET.get("q", "").strip()
    if nome_q:
        visitantes = visitantes.filter(nome__icontains=nome_q)

    data_q = request.GET.get("data_admissao")
    if data_q:
        visitantes = visitantes.filter(data_admissao=data_q)

    visitantes = visitantes.order_by("nome")

    return render(
        request,
        "visitante/visitante.html",
        {
            "visitantes": visitantes,
            "filtro_nome": nome_q,
            "filtro_data": data_q,
        },
    )

# ---------- helper --------------------------------------------------------
def _salvar_visitante(request, instance=None):
    if request.method == "POST":
        form = VisitanteForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            vis = form.save(commit=False)
            vis.perfil = VISIT
            vis.save()
            return redirect("listar_visitantes")
    else:
        form = VisitanteForm(instance=instance)

    return render(
        request,
        "visitante/cadastro_visitante.html",
        {"form": form},
    )

# ---------- criar ---------------------------------------------------------
@admin_required
def cadastrar_visitante(request):
    return _salvar_visitante(request)

# ---------- editar --------------------------------------------------------
@admin_required
def editar_visitante(request, pk):
    vis = get_object_or_404(Usuario, pk=pk, perfil=VISIT)
    return _salvar_visitante(request, instance=vis)

# ---------- excluir -------------------------------------------------------
@admin_required
def excluir_visitante(request, pk):
    vis = get_object_or_404(Usuario, pk=pk, perfil=VISIT)
    vis.delete()
    return redirect("listar_visitantes")
