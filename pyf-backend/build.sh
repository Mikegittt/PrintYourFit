#!/bin/bash
set -e

export CARGO_HOME=/tmp/cargo
export PIP_CACHE_DIR=/tmp/pip-cache

echo "Python version:"
python --version

echo "Installing dependencies..."
python -m pip install --no-cache-dir -r requirements.txt

echo "Running migrations..."
python manage.py migrate --noinput || true

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "Build complete!"
