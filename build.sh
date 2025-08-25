#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=== Build Script Starting ==="
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

echo "=== Installing Python Dependencies ==="
pip install -r requirements.txt

echo "=== Setting Django Settings Module ==="
export DJANGO_SETTINGS_MODULE=Recipe_project.settings

echo "=== Testing Django Configuration ==="
python manage.py check

echo "=== Collecting Static Files ==="
python manage.py collectstatic --no-input

echo "=== Running Database Migrations ==="
python manage.py migrate

echo "=== Testing WSGI Import ==="
python -c "from Recipe_project.wsgi import application; print('WSGI application imported successfully')"

echo "=== Build Script Completed Successfully ==="
