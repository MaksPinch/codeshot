import pytest
from django.test import Client
from django.urls import reverse
from codeshot.services.exports import ExportError

@pytest.mark.django_db
def test_failed_to_load_png_file_with_error_500(monkeypatch):
    client = Client()

    def failed_generate_image(editor_state, image_format):
        raise ExportError("failed")

    monkeypatch.setattr("codeshot.views.generate_image", failed_generate_image)
    response = client.get(reverse("download_png"))

    assert response.status_code == 500
    assert b"Could not generate image export." in response.content
