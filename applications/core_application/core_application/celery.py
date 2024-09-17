import os

from celery import Celery
from configurations import importer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core_application.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

importer.install()
app = Celery("core_application")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
