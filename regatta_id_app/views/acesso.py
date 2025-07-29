from django.shortcuts import render, redirect, get_object_or_404
from ..models import AcessoRegistrado
from ..forms import AcessoRegistradoForm
from .decorator import admin_required

@admin_required
def listar_acessos(request):
    # (…igual…)
    ...

@admin_required
def cadastrar_acesso(request):
    # (…igual…)
    ...

@admin_required
def editar_acesso(request, pk):
    # (…igual…)
    ...

@admin_required
def excluir_acesso(request, pk):
    # (…igual…)
    ...
