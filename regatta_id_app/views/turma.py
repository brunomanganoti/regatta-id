from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.db.models import Min, Max
from ..models import Turma, Horario
from ..forms import TurmaForm, HorarioForm
from .decorator import admin_required


# cria o formset para Horario dentro de Turma
HorarioFormSet = inlineformset_factory(
    Turma,
    Horario,
    form=HorarioForm,
    extra=1,            # sempre mostre uma linha extra para adicionar
    can_delete=True,    # permite remover na UI
)

# ----------------------------------------------------------------------
# -------- TURMA -------------------------------------------------------
# ----------------------------------------------------------------------

@admin_required
def listar_turmas(request):
    """
    Exibe todas as turmas com:
      • primeiro horário cadastrado (hora_entrada – hora_saida)
      • data de início   → menor data de matrícula de alunos
      • data de término → maior data_fim de matrícula
      • código gerado a partir do ID
    Filtros: nome da turma e data de início.
    """
    turmas_qs = Turma.objects.all()

    # -------- filtros -----------------------------------------------------
    nome_q = request.GET.get("q", "").strip()
    if nome_q:
        turmas_qs = turmas_qs.filter(nome__icontains=nome_q)

    inicio_q = request.GET.get("data_inicio")
    if inicio_q:
        turmas_qs = turmas_qs.filter(
            alunos__data_inicio=inicio_q        # AlunoTurma FK
        )

    turmas_qs = turmas_qs.order_by("nome").distinct()

    # -------- prepara dados agregados ------------------------------------
    turmas_info = []
    for turma in turmas_qs:
        # Horário (pega o primeiro apenas p/ exibir)
        h = turma.horarios.order_by("hora_entrada").first()
        horario_str = (
            f"{h.hora_entrada.strftime('%H:%M')} - {h.hora_saida.strftime('%H:%M')}"
            if h else "—"
        )

        # Datas início / fim de matrículas
        aggs = turma.alunos.aggregate(
            inicio=Min("data_inicio"),
            fim=Max("data_fim"),
        )
        data_inicio = aggs["inicio"]
        data_fim    = aggs["fim"]

        # Código simples (ex.: TURMA-0001)
        codigo = f"TURMA-{turma.id:04d}"

        turmas_info.append(
            {
                "turma": turma,
                "horario": horario_str,
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "codigo": codigo,
            }
        )

    return render(
        request,
        "turma/turma.html",
        {
            "turmas_info": turmas_info,
            "filtro_nome": nome_q,
            "filtro_data": inicio_q,
        },
    )

@admin_required
def _crud_turma(request, instance=None):
    turma = instance or Turma()
    if request.method == "POST":
        form    = TurmaForm(request.POST, instance=turma)
        formset = HorarioFormSet(request.POST, instance=turma)
        if form.is_valid() and formset.is_valid():
            turma_salva = form.save()
            formset.instance = turma_salva
            formset.save()
            return redirect("listar_turmas")
    else:
        form    = TurmaForm(instance=turma)
        formset = HorarioFormSet(instance=turma)

    return render(request, "turma/cadastro_turma.html", {
        "form":    form,
        "formset": formset,
    })

@admin_required
def cadastrar_turma(request):
    return _crud_turma(request)

@admin_required
def editar_turma(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    return _crud_turma(request, instance=turma)


@admin_required
def excluir_turma(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    turma.delete()
    return redirect("listar_turmas")


# ----------------------------------------------------------------------
# -------- HORÁRIOS da turma -------------------------------------------
# ----------------------------------------------------------------------
@admin_required
def listar_horarios(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id)
    horarios = turma.horarios.all().order_by("hora_entrada")

    return render(
        request,
        "turma/horario_turma.html",
        {"turma": turma, "horarios": horarios},
    )


def _crud_horario(request, turma, instance=None):
    """Create / Update de Horário da turma."""
    form = HorarioForm(request.POST or None, instance=instance)

    # força campo turma oculto (não editável na interface)
    form.fields["turma"].widget = forms.HiddenInput()
    if request.method == "GET" and instance is None:
        form.initial["turma"] = turma

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("listar_horarios", turma_id=turma.id)

    return render(
        request,
        "turma/cadastro_horario.html",
        {"form": form, "turma": turma},
    )


@admin_required
def cadastrar_horario(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id)
    return _crud_horario(request, turma)


@admin_required
def editar_horario(request, pk):
    horario = get_object_or_404(Horario, pk=pk)
    return _crud_horario(request, horario.turma, horario)


@admin_required
def excluir_horario(request, pk):
    horario = get_object_or_404(Horario, pk=pk)
    turma_id = horario.turma_id
    horario.delete()
    return redirect("listar_horarios", turma_id=turma_id)


