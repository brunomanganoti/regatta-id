-- Criação de enum para perfis de usuários
CREATE TYPE perfil_usuario AS ENUM ('aluno', 'colaborador', 'visitante', 'voluntario');

-- Usuários do sistema (alunos, colaboradores, visitantes, voluntários)
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    email TEXT,
    telefone TEXT,
    perfil perfil_usuario NOT NULL,
    foto BYTEA, -- para imagem facial
    ativo BOOLEAN DEFAULT TRUE,
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    consentimento_lgpd BOOLEAN DEFAULT FALSE
);

-- Dados de acesso facial (hash, código ou metadado do reconhecimento facial)
CREATE TABLE dados_biometricos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    facial_hash TEXT NOT NULL,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Colaboradores e seus níveis de acesso
CREATE TABLE acessos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    nivel_acesso TEXT CHECK (nivel_acesso IN ('admin')),
    autorizado BOOLEAN DEFAULT TRUE
);

-- Tabela de turmas
CREATE TABLE turmas (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    descricao TEXT
);

-- Relacionamento entre alunos e turmas
CREATE TABLE aluno_turma (
    id SERIAL PRIMARY KEY,
    aluno_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    turma_id INTEGER NOT NULL REFERENCES turmas(id) ON DELETE CASCADE,
    data_inicio DATE NOT NULL,
    data_fim DATE
);

-- Horários permitidos de entrada e saída por turma
CREATE TABLE horarios (
    id SERIAL PRIMARY KEY,
    turma_id INTEGER REFERENCES turmas(id) ON DELETE SET NULL,
    hora_entrada TIME NOT NULL,
    hora_saida TIME NOT NULL,
    dias_semana TEXT[] NOT NULL -- Ex: '{segunda,terça,quarta}'
);

-- Registros de entrada e saída
CREATE TABLE acessos_registrados (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    tipo_acesso TEXT CHECK (tipo_acesso IN ('entrada', 'saida')) NOT NULL,
    local TEXT NOT NULL,
    data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valido BOOLEAN DEFAULT TRUE,
    alerta BOOLEAN DEFAULT FALSE
);

-- Log de eventos críticos (segurança, LGPD, etc.)
CREATE TABLE eventos_criticos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    tipo_evento TEXT NOT NULL,
    descricao TEXT,
    data_evento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Histórico de sessões e tentativas inválidas
CREATE TABLE tentativas_acesso (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    sucesso BOOLEAN NOT NULL,
    ip_origem TEXT,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    motivo TEXT
);

-- Histórico de presença por sala
CREATE TABLE presencas (
    id SERIAL PRIMARY KEY,
    aluno_id INTEGER REFERENCES usuarios(id),
    turma_id INTEGER REFERENCES turmas(id),
    sala TEXT NOT NULL,
    data_presenca DATE NOT NULL,
    presente BOOLEAN DEFAULT TRUE
);

-- Registro de rotas (salas pelas quais um usuário passou)
CREATE TABLE rota_usuario (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    sala TEXT NOT NULL,
    data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
