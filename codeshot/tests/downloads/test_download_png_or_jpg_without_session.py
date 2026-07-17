from django.test import Client
from django.urls import reverse

def test_download_png_works_without_session_data():
    client = Client()

    response = client.get(reverse("download_png"))

    assert response.status_code == 200
    assert response["Content-Type"] == "image/png"

def test_download_jpg_works_without_session_data():
    client = Client()

    response = client.get(reverse("download_jpg"))

    assert response.status_code == 200
    assert response["Content-Type"] == "image/jpeg"

