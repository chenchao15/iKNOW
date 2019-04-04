"""
WSGI config for iKNOW project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""
import sys
sys.path.append('.venv/lib/python3.5/site-packages')  
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iKNOW.settings")

application = get_wsgi_application()
