
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','sell_web.settings')

app = Celery('sell_import_app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

