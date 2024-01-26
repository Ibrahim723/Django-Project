from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Create a Celery instance
app = Celery('project')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()



