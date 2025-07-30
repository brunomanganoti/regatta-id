from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Auth & Home
    path('',                 views.root_redirect_view, name='root'),
    path('login/',           views.LoginView.as_view(),  name='login'),
    path('logout/',          views.logout_view,        name='logout'),
    path('dashboard/',       views.dashboard,          name='dashboard'),

    # Estudantes
    path('estudantes/',                      views.listar_estudantes,    name='listar_estudantes'),
    path('estudantes/novo/',                 views.cadastrar_estudante,  name='cadastrar_estudante'),
    path('estudantes/<int:pk>/editar/',      views.editar_estudante,     name='editar_estudante'),
    path('estudantes/<int:pk>/excluir/',     views.excluir_estudante,    name='excluir_estudante'),

    # Colaboradores
    path('colaboradores/',                   views.listar_colaboradores,      name='listar_colaboradores'),
    path('colaboradores/novo/',              views.cadastrar_colaborador,     name='cadastrar_colaborador'),
    path('colaboradores/<int:pk>/editar/',   views.editar_colaborador,        name='editar_colaborador'),
    path('colaboradores/<int:pk>/excluir/',  views.excluir_colaborador,       name='excluir_colaborador'),

    # Visitantes
    path('visitantes/',                      views.listar_visitantes,        name='listar_visitantes'),
    path('visitantes/novo/',                 views.cadastrar_visitante,      name='cadastrar_visitante'),
    path('visitantes/<int:pk>/editar/',      views.editar_visitante,         name='editar_visitante'),
    path('visitantes/<int:pk>/excluir/',     views.excluir_visitante,        name='excluir_visitante'),

    # Voluntários
    path('voluntarios/',                     views.listar_voluntarios,       name='listar_voluntarios'),
    path('voluntarios/novo/',                views.cadastrar_voluntario,     name='cadastrar_voluntario'),
    path('voluntarios/<int:pk>/editar/',     views.editar_voluntario,        name='editar_voluntario'),
    path('voluntarios/<int:pk>/excluir/',    views.excluir_voluntario,       name='excluir_voluntario'),

    # Relatório
    path('relatorio/',        views.relatorio_view,      name='relatorio'),

    # Turmas
    path("turmas/",                      views.listar_turmas,   name="listar_turmas"),
    path("turmas/novo/",                  views.cadastrar_turma, name="cadastrar_turma"),
    path("turmas/<int:pk>/editar/",       views.editar_turma,    name="editar_turma"),
    path("turmas/<int:pk>/excluir/",      views.excluir_turma,   name="excluir_turma"),

    # Horários da turma
    path("turmas/<int:turma_id>/horarios/",             views.listar_horarios,   name="listar_horarios"),
    path("turmas/<int:turma_id>/horarios/novo/",        views.cadastrar_horario, name="cadastrar_horario"),
    path("horarios/<int:pk>/editar/",                   views.editar_horario,    name="editar_horario"),
    path("horarios/<int:pk>/excluir/",                  views.excluir_horario,   name="excluir_horario"),

    # Matrículas (AlunoTurma)
    path('matriculas/',                   views.listar_matriculas,      name='listar_matriculas'),
    path('matriculas/novo/',              views.cadastrar_matricula,    name='cadastrar_matricula'),
    path('matriculas/<int:pk>/editar/',   views.editar_matricula,       name='editar_matricula'),
    path('matriculas/<int:pk>/excluir/',  views.excluir_matricula,      name='excluir_matricula'),

    # Acessos Registrados
    path('acessos/',                       views.listar_acessos,     name='listar_acessos'),
    path('acessos/novo/',                  views.cadastrar_acesso,   name='cadastrar_acesso'),
    path('acessos/<int:pk>/editar/',       views.editar_acesso,      name='editar_acesso'),
    path('acessos/<int:pk>/excluir/',      views.excluir_acesso,     name='excluir_acesso'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
