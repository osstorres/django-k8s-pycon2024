from django.urls import path
from .views import HostView, LoadView

app_name = "hello"
urlpatterns = [
    path("host/", HostView.as_view(), name="host"),
    path("load/", LoadView.as_view(), name="load"),
]
