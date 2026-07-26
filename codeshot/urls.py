from django.urls import path

from .views import (
    download_jpg_view,
    download_png_view,
    health_view,
    home_view,
    login_user,
    not_implemented_yet,
    preview_view,
    register_user,
    stats_view,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("preview/", preview_view, name="preview"),
    path("download/png", download_png_view, name="download_png"),
    path("download/jpg", download_jpg_view, name="download_jpg"),
    path("health/", health_view, name="health"),
    path("stats/", stats_view, name="stats"),
    path("api/auth/register/", register_user, name="register"),
    path("api/auth/login/", login_user, name="login"),
    path("api/auth/logout/", not_implemented_yet, name="logout"),
    path("api/auth/me/", not_implemented_yet, name="me"),
]
