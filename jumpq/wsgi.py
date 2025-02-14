"""
WSGI config for jumpq project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
from decouple import config

from django.core.wsgi import get_wsgi_application

if config('ENV') == 'devel':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jumpq.devel')

application = get_wsgi_application()
