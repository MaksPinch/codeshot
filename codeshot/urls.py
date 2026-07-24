from django.urls import path

from .views import (
    download_jpg_view,
    download_png_view,
    health_view,
    home_view,
    preview_view,
    stats_view,
    not_implemented_yet
)

urlpatterns = [
    path("", home_view, name="home"),
    path("preview/", preview_view, name="preview"),
    path("download/png", download_png_view, name="download_png"),
    path("download/jpg", download_jpg_view, name="download_jpg"),
    path("health/", health_view, name="health"),
    path("stats/", stats_view, name="stats"),
    path("api/auth/register/", not_implemented_yet, name="register"),
    path("api/auth/login/", not_implemented_yet, name="login"),
    path("api/auth/logout/", not_implemented_yet, name="logout"),
    path("api/auth/me/", not_implemented_yet, name="me"),
]
