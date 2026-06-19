#!/bin/bash
set -e

echo "Starting Gunicorn..."
python -m gunicorn django_project.wsgi:application --bind 0.0.0.0:$PORT --workers 3
