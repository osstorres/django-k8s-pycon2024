from django.urls import path
from .views import HealthView

app_name = "monitor"
urlpatterns = [
    path("health_check/", HealthView.as_view(), name="health_check"),
]
