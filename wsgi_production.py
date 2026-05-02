import os
import sys

# Add your project directory to the sys.path
path = "/home/your-username/cmsn_college_website"  # Replace with your PythonAnywhere username
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ["DJANGO_SETTINGS_MODULE"] = "csnursing.settings_production"

# Activate your virtual environment
activate_this = "/home/your-username/.virtualenvs/cmsn_env/bin/activate_this.py"  # Replace with your username
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import Django
import django
from django.core.wsgi import get_wsgi_application

# Initialize Django
django.setup()

# Get the WSGI application
application = get_wsgi_application()
