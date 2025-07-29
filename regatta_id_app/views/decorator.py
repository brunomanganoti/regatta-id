from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from ..models import Usuario

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
