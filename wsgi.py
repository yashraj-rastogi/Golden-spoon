import os
from django.core.wsgi import get_wsgi_application

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Recipe_project.settings')

# Create the WSGI application
application = get_wsgi_application()

# For debugging
if __name__ == "__main__":
    print("WSGI application created successfully")
    print(f"Using settings: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
