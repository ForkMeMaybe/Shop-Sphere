import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Shop_Sphere.settings.dev")

celery = Celery("Shop_Sphere")
celery.config_from_object("django.conf:settings", namespace="CELERY")
celery.autodiscover_tasks()
