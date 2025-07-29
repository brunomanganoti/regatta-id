from django.shortcuts import render, redirect, get_object_or_404
from ..models import Horario
from ..forms import HorarioForm
from .decorator import admin_required

DIAS_SEMANA = [d[0] for d in HorarioForm.base_fields['dias_semana'].choices]

@admin_required
def listar_horarios(request):
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
    # (…igual…)
    ...

@admin_required
def excluir_horario(request, horario_id):
    # (…igual…)
    ...
