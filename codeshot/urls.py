from django.urls import path

from .views import (
    download_jpg_view,
    download_png_view,
    health_view,
    home_view,
    preview_view,
    stats_view,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("preview/", preview_view, name="preview"),
    path("download/png", download_png_view, name="download_png"),
    path("download/jpg", download_jpg_view, name="download_jpg"),
    path("health/", health_view, name="health"),
    path("stats/", stats_view, name="stats"),
]
