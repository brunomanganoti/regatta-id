#!/bin/bash

echo "Aguardando o banco de dados iniciar..."
while ! nc -z db 5432; do
  sleep 0.1
done

echo "Aplicando migrações..."
python manage.py migrate

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

exec "$@"
