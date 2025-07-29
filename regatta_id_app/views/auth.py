from django.shortcuts import render, redirect
from ..models import Usuario
from .decorator import login_required_custom, admin_required

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

        if not u.acessos.filter(nivel_acesso='admin', autorizado=True).exists():
            return render(request, 'regatta_id_app/sistema/login.html',
                          {'error': 'Acesso permitido apenas para administradores.'})

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
