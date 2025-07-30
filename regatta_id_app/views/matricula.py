from django.shortcuts import render, redirect, get_object_or_404
from ..models import AlunoTurma
from .decorator import admin_required

@admin_required
def listar_matriculas(request):
    # (…igual…)
    ...

@admin_required
def cadastrar_matricula(request):
    # (…igual…)
    ...

@admin_required
def editar_matricula(request, pk):
    # (…igual…)
    ...

@admin_required
def excluir_matricula(request, pk):
    # (…igual…)
    ...
