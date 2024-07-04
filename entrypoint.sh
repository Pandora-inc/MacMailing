#!/bin/bash

# Comandos que necesitas ejecutar antes de iniciar tu aplicación
echo "Preparando ambiente..."

python manage.py collectstatic --noinput
python manage.py migrate

# Iniciar gunicorn u otro servidor WSGI si es necesario
gunicorn macmail.wsgi:application --bind 0.0.0.0:8000
