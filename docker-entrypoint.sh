#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py seed_shelter

exec gunicorn server_adoption.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 60
