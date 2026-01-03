#!/bin/bash

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate --noinput

# Start Gunicorn server
gunicorn config.wsgi --log-file -