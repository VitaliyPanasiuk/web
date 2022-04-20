import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings



# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luxon.settings')

app = Celery('luxon')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)

# Load task modules from all registered Django apps.
# app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add_new_currency': {
        'task': 'accounts.tasks.add_currency',
        'schedule': crontab(hour='15', minute='00')
    },
    'check_confirmation': {
        'task': 'accounts.tasks.check_confirmation',
        'schedule': crontab(minute='*/30')
    }
}
