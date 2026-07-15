import pytest
from django.test import Client
from django.urls import reverse
from codeshot.services.exports import ExportError
from codeshot.models import ProductEvent
from codeshot.services.analytics import record_product_event

@pytest.mark.django_db
def test_failed_to_load_png_file_with_error_500(monkeypatch):
    client = Client()

    def failed_generate_image(editor_state, image_format):
        raise ExportError("failed")

    monkeypatch.setattr("codeshot.views.generate_image", failed_generate_image)
    response = client.get(reverse("download_png"))

    assert response.status_code == 500
    assert b"Could not generate image export." in response.content


@pytest.mark.django_db
def test_failed_to_load_png_or_jpg_with_the_record_of_it(client, monkeypatch):
    def test_failed_to_generate_image(editor_state, format):
        raise ExportError("failed")

    monkeypatch.setattr("codeshot.views.generate_image", test_failed_to_generate_image)
    response = client.get(reverse("download_png"))

    assert response.status_code == 500

    started_event = ProductEvent.objects.get(event_name=ProductEvent.EXPORT_STARTED)

    assert started_event.event_name == "export_started"

    failed_event = ProductEvent.objects.get(event_name=ProductEvent.EXPORT_FAILED)

    assert failed_event.event_name == "export_failed"





