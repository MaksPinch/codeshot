from django.urls import path

from .views import home_view, preview_view

urlpatterns = [
    path("", home_view, name="home"),
    path("preview/", preview_view, name="preview"),
]
