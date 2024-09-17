from configurations import importer
import os

importer.install()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "analytics_application.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")
