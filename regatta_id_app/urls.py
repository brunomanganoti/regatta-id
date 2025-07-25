from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',     views.root_redirect_view, name='root'),
    path('login/',        views.login_view,       name='login'),
    path('logout/',       views.logout_view,      name='logout'),
    path('dashboard/',    views.dashboard_view,   name='dashboard'),
    path('estudantes/',   views.listar_estudantes, name='listar_estudantes'),
    path('estudantes/novo/', views.cadastrar_estudante, name='cadastrar_estudante'),
    path('estudantes/<int:pk>/editar/',  views.editar_estudante,    name='editar_estudante'),
    path('estudantes/<int:pk>/excluir/', views.excluir_estudante,   name='excluir_estudante'),
    path('turmas/',       views.listar_turmas,    name='listar_turmas'),
    path('turmas/novo/',  views.cadastrar_turma,  name='cadastrar_turma'),
    path('relatorio/',    views.relatorio_view,   name='relatorio'),
    path('horarios/',     views.listar_horarios,  name='horarios'),
    path('horarios/novo',     views.cadastrar_horarios,  name='cadastrar_horarios'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
