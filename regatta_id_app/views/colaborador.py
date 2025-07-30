from django.shortcuts import render, redirect, get_object_or_404
from ..models import Usuario
from ..forms import ColaboradorForm 
from .decorator import admin_required

COLAB = Usuario.PerfilUsuario.COLABORADOR

@admin_required
def listar_colaboradores(request):
    """Tabela com filtros por nome e data de admissão."""
    colaboradores = Usuario.objects.filter(perfil=COLAB)

    # — filtros simples —
    nome_q = request.GET.get("q", "").strip()
    if nome_q:
        colaboradores = colaboradores.filter(nome__icontains=nome_q)

    admissao_q = request.GET.get("data_admissao")
    if admissao_q:
        # Se usar o modelo auxiliar, troque para colaborador_info__data_admissao
        colaboradores = colaboradores.filter(data_admissao=admissao_q)

    colaboradores = colaboradores.order_by("nome")

    return render(
        request,
        "colaborador/colaborador.html",
        {
            "colaboradores": colaboradores,
            "filtro_nome": nome_q,
            "filtro_data": admissao_q,
        },
    )

# ---------- helper interno -----------------------------------------------
def _salvar_colaborador(request, instance=None):
    """
    Renderiza o formulário (GET) e salva (POST).
    • instance=None  ➜  criação
    • instance=obj   ➜  edição
    """
    if request.method == "POST":
        form = ColaboradorForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            colab = form.save(commit=False)
            colab.perfil = COLAB          # garante o perfil correto
            colab.save()
            return redirect("listar_colaboradores")
    else:
        form = ColaboradorForm(instance=instance)

    return render(
        request,
        "colaborador/cadastro_colaborador.html",
        {"form": form},
    )

# ---------- criação -------------------------------------------------------
@admin_required
def cadastrar_colaborador(request):
    return _salvar_colaborador(request)


# ---------- edição (nova função) -----------------------------------------
@admin_required
def editar_colaborador(request, pk: int):
    colab = get_object_or_404(Usuario, pk=pk, perfil=COLAB)
    return _salvar_colaborador(request, instance=colab)


# ---------- exclusão ------------------------------------------------------
@admin_required
def excluir_colaborador(request, pk: int):
    """
    Remove o colaborador e redireciona sem tela intermediária.
    A exclusão pode ser feita por GET ou POST —  
    utilize POST se chamar a partir de um formulário/JS.
    """
    colab = get_object_or_404(Usuario, pk=pk, perfil=COLAB)
    colab.delete()
    return redirect("listar_colaboradores")