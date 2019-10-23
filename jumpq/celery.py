from __future__ import absolute_import

import os

from celery import Celery

from django.conf import settings


mode = os.getenv('DJANGO_MODE', 'devel')

if mode == 'devel':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jumpq.devel")
elif mode == 'staging':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jumpq.staging")
elif mode == 'prod':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jumpq.prod")

# Celery app setup: the app instance is told where the Django configuration
# lives and is made to autodiscover tasks from all our INSTALLED_APPS. This
# captures tasks living in tasks.py submodules from each app. Tasks which live
# in helpers.py submodules for each app are captured by the CELERY_IMPORTS
# setting.
celery_app = Celery('jumpq')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
