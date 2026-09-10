from django.urls import path

from .views import (
    create_export_job,
    download_jpg_view,
    download_png_view,
    export_job_detail,
    health_view,
    home_view,
    login_user,
    logout_user,
    me_information,
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
    path("api/auth/logout/", logout_user, name="logout"),
    path("api/auth/me/", me_information, name="me"),
    path("api/exports/", create_export_job, name="create_export"),
    path("api/exports/<int:job_id>/", export_job_detail, name="export_detail"),
]
