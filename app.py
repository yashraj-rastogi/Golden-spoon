"""
WSGI compatibility layer for Render deployment.
This file provides the 'app' module that Render expects.
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Recipe_project.settings')

# Create the WSGI application
application = get_wsgi_application()

# Export as 'app' for compatibility with some deployment platforms
app = application