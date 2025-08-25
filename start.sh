#!/bin/bash
echo "Starting Golden Spoon Recipe App..."
echo "Python version:"
python --version
echo "Current directory:"
pwd
echo "Directory contents:"
ls -la
echo "Python path:"
python -c "import sys; print(sys.path)"
echo "Testing WSGI import:"
python -c "from Recipe_project.wsgi import application; print('WSGI import successful')"
echo "Starting gunicorn..."
exec gunicorn Recipe_project.wsgi:application --bind 0.0.0.0:$PORT --workers 3
