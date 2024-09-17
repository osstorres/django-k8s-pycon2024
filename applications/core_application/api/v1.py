from django.urls import path, include


urlpatterns = [
    # Monitoring
    # ==========================================
    path("monitor/", include("monitor.urls", namespace="monitor")),
    # Example
    # ==========================================
    path("hello/", include("hello.urls", namespace="hello")),
]
