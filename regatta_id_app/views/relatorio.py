from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q

from ..models import AcessoRegistrado, Usuario
from .decorator import admin_required


@admin_required
def relatorio_view(request):
    """
    Lista acessos (entradas/saídas) com filtros por tipo de usuário,
    nome e intervalo de datas.  Opcionalmente exporta em CSV.
    """
    eventos = AcessoRegistrado.objects.select_related("usuario").order_by("-data_hora")

    # -------- filtros ---------------------------------------------------
    tipo  = request.GET.get("tipo")        # aluno | turma | colaborador | …
    busca = request.GET.get("q", "").strip()
    di    = request.GET.get("di")          # data início   (YYYY-MM-DD)
    df    = request.GET.get("df")          # data fim

    if tipo:
        eventos = eventos.filter(usuario__perfil=tipo)

    if busca:
        eventos = eventos.filter(usuario__nome__icontains=busca)

    if di:
        eventos = eventos.filter(data_hora__date__gte=di)
    if df:
        eventos = eventos.filter(data_hora__date__lte=df)

    # -------- exporta CSV ----------------------------------------------
    if request.GET.get("export") == "csv":
        lines = ["id,nome,perfil,data_hora,evento"]
        for e in eventos:
            lines.append(
                f"{e.id},{e.usuario.nome},{e.usuario.get_perfil_display()},"
                f"{e.data_hora:%Y-%m-%d %H:%M:%S},{e.evento}"
            )
        csv_data = "\n".join(lines)
        resp = HttpResponse(csv_data, content_type="text/csv")
        resp["Content-Disposition"] = "attachment; filename=relatorio.csv"
        return resp

    # -------- página HTML ----------------------------------------------
    return render(
        request,
        "relatorio/relatorio.html",
        {
            "eventos": eventos,
            "filtro_tipo":  tipo,
            "filtro_q":     busca,
            "filtro_di":    di,
            "filtro_df":    df,
        },
    )
