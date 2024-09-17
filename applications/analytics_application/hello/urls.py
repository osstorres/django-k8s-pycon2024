from django.urls import path
from .views import HostView

app_name = "hello"
urlpatterns = [
    path("host/", HostView.as_view(), name="host"),
]
