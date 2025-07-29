from django.shortcuts import render, redirect, get_object_or_404
from ..models import AcessoRegistrado
from ..forms import TurmaForm
from .decorator import admin_required

@admin_required
def relatorio_view(request):
    # usamos o mesmo nome de variável que o template espera
    eventos = AcessoRegistrado.objects.order_by('-data_hora')
    return render(request,
                  'regatta_id_app/relatorio/relatorio.html',
                  {'eventos': eventos})

