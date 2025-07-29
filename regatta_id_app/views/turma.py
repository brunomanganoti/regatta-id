from django.shortcuts import render, redirect, get_object_or_404
from ..models import Turma, AlunoTurma
from ..forms import TurmaForm
from .decorator import admin_required

@admin_required
def listar_turmas(request):
    # Busca todas as turmas
    turmas = Turma.objects.all().order_by('nome')
    turmas_info = []

    # Para cada turma, conta quantos alunos estão vinculados
    for turma in turmas:
        qtd_alunos = AlunoTurma.objects.filter(turma=turma).count()
        turmas_info.append({
            'turma': turma,
            'qtd_alunos': qtd_alunos,
        })

    # Renderiza com o contexto esperado pelo template
    return render(request,
                  'regatta_id_app/turmas/turmas.html',  # ajuste o path se estiver diferente
                  {'turmas_info': turmas_info})

@admin_required
def cadastrar_turma(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_turmas')
    else:
        form = TurmaForm()
    return render(request,
                  'regatta_id_app/turmas/cadastroturmas.html',
                  {'form': form})


@admin_required
def editar_turma(request, pk):
    # (…igual…)
    ...

@admin_required
def excluir_turma(request, pk):
    # (…igual…)
    ...
