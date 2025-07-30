from django.shortcuts import render
from regatta_id_app.models.usuario import Usuario
from regatta_id_app.models.evento import EventoCritico

def dashboard(request):
    usuarios_ativos = Usuario.objects.filter(ativo=True).count()
    visitas_ativas = Usuario.objects.filter(perfil='visitante', ativo=True).count()
    credenciais_ativas = usuarios_ativos  # ajuste se necessário

    eventos = EventoCritico.objects.select_related('usuario').order_by('-data_evento')[:10]

    return render(request, 'sistema/dashboard.html', {
        'usuarios_ativos': usuarios_ativos,
        'visitas_ativas': visitas_ativas,
        'credenciais_ativas': credenciais_ativas,
        'eventos': eventos
    })
