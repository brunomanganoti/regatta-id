from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import Usuario, Turma, AlunoTurma, AcessoRegistrado, Horario
from .forms import TurmaForm, UsuarioForm, HorarioForm

# —– substitua @login_required do Django por um decorator que verifica sessão —–
def login_required_custom(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped

def admin_required(view_func):
    @login_required_custom
    def _wrapped(request, *args, **kwargs):
        u = Usuario.objects.get(pk=request.session['usuario_id'])
        if not u.acessos.filter(nivel_acesso='admin', autorizado=True).exists():
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped

def root_redirect_view(request):
    if request.session.get('usuario_id'):
        return redirect('dashboard')
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('password')
        try:
            u = Usuario.objects.get(email=email, senha=senha, ativo=True)
        except Usuario.DoesNotExist:
            request.session.flush()
            return render(request, 'regatta_id_app/sistema/login.html',
                          {'error': 'Email ou senha inválidos.'})

        # verifica se tem acesso ADMIN
        if not u.acessos.filter(nivel_acesso='admin', autorizado=True).exists():
            return render(request, 'regatta_id_app/sistema/login.html',
                          {'error': 'Acesso permitido apenas para administradores.'})

        # tudo OK: guarda o usuário na sessão
        request.session['usuario_id']   = u.id
        request.session['usuario_nome'] = u.nome
        return redirect('dashboard')

    return render(request, 'regatta_id_app/sistema/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

@admin_required
def dashboard_view(request):
    return render(request, 'regatta_id_app/sistema/dashboard.html')

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

@admin_required
def cadastrar_estudante(request):
    return _salvar_estudante(request)

@admin_required
def editar_estudante(request, pk):
    aluno = get_object_or_404(Usuario, pk=pk, perfil='aluno')
    # usa o mesmo helper mas passa instance e contexto extra
    return _salvar_estudante(request, instance=aluno)

@admin_required
def excluir_estudante(request, pk):
    aluno = get_object_or_404(Usuario, pk=pk, perfil='aluno')
    if request.method == 'POST':
        aluno.delete()
    return redirect('listar_estudantes')


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
def relatorio_view(request):
    # usamos o mesmo nome de variável que o template espera
    eventos = AcessoRegistrado.objects.order_by('-data_hora')
    return render(request,
                  'regatta_id_app/relatorio/relatorio.html',
                  {'eventos': eventos})

@admin_required
def listar_horarios(request):
    from .models import Horario
    horarios = Horario.objects.select_related('turma').all()
    return render(request, 'regatta_id_app/horarios/horarios.html', {'horarios': horarios})

DIAS_SEMANA = [dia[0] for dia in HorarioForm.base_fields['dias_semana'].choices]

@admin_required
def cadastrar_horarios(request):
    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('horarios')
    else:
        form = HorarioForm()

    context = {
        'form': form,
        'dias_da_semana': DIAS_SEMANA,
        'dias_selecionados': request.POST.getlist('dias_semana') if request.method == 'POST' else [],
    }
    return render(request, 'regatta_id_app/horarios/cadastrohorarios.html', context)
    
@admin_required
def editar_horarios(request, horario_id):
    horario = get_object_or_404(Horario, pk=horario_id)

    if request.method == 'POST':
        form = HorarioForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
            return redirect('horarios')
    else:
        form = HorarioForm(instance=horario)

    context = {
        'form': form,
        'dias_da_semana': DIAS_SEMANA,
        'dias_selecionados': horario.dias_semana if horario.dias_semana else [],
    }
    return render(request, 'regatta_id_app/horarios/cadastrohorarios.html', context)