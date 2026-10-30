import os
import sys

# Agrega el proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evaluacion_ing_de_software.settings')

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()


from core.wsgi import application
app = application