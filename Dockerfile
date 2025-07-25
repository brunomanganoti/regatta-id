# Usando imagem oficial Python
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Atualiza e instala dependências
RUN apt-get update \
    && apt-get install -y libpq-dev gcc netcat-openbsd \
    && apt-get clean

# Cria diretório de trabalho
WORKDIR /code

# Copia os arquivos
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

# Entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
