from django.shortcuts import render, redirect, get_object_or_404
from ..models import Turma, Usuario, AlunoTurma
from ..forms import UsuarioForm
from .decorator import admin_required

# helper interno
def _salvar_estudante(request, instance=None):
    """
    helper para cadastrar ou editar
    instance=None → cadastrar; instance=aluno → editar
    """
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            est = form.save(commit=False)
            est.perfil = 'aluno'
            est.save()

            # Atualiza ou cria Turma
            turma_id = request.POST.get('turma')
            di = request.POST.get('data_inicio')
            df = request.POST.get('data_fim') or None

            # remove matrícula antiga antes de criar nova
            if instance:
                AlunoTurma.objects.filter(aluno=est).delete()
            if turma_id and di:
                AlunoTurma.objects.create(
                    aluno=est,
                    turma_id=turma_id,
                    data_inicio=di,
                    data_fim=df
                )

            return redirect('listar_estudantes')
    else:
        form = UsuarioForm(instance=instance)

    # preparações de contexto para pré-seleção
    turmas = Turma.objects.all()
    selec = None
    di = df = None
    if instance:
        ultima = AlunoTurma.objects.filter(aluno=instance).order_by('-data_inicio').first()
        if ultima:
            selec = ultima.turma.id
            di    = ultima.data_inicio
            df    = ultima.data_fim

    return render(request,
                  'regatta_id_app/estudantes/cadastroestudante.html',
                  {
                    'form': form,
                    'turmas': turmas,
                    'selected_turma': selec,
                    'data_inicio':   di,
                    'data_fim':      df,
                  })

@admin_required
def listar_estudantes(request):
    estudantes_info = []
    # pega só os alunos
    for aluno in Usuario.objects.filter(perfil='aluno'):
        # usa o related_name para economizar query
        ultima = aluno.turmas_aluno.order_by('-data_inicio').first()
        estudantes_info.append({
            'estudante':   aluno,
            'turma':       ultima.turma.nome    if ultima else None,
            'data_inicio': ultima.data_inicio   if ultima else None,
        })

    return render(request,
                  'regatta_id_app/estudantes/estudantes.html',
                  {'estudantes_info': estudantes_info})

    return _salvar_estudante(request)

@admin_required
def cadastrar_estudante(request):
    return _salvar_estudante(request)

@admin_required
def editar_estudante(request, pk):
    aluno = get_object_or_404(Usuario, pk=pk, perfil='aluno')
    return _salvar_estudante(request, instance=aluno)

@admin_required
def excluir_estudante(request, pk):
    aluno = get_object_or_404(Usuario, pk=pk, perfil='aluno')
    if request.method == 'POST':
        aluno.delete()
    return redirect('listar_estudantes')
