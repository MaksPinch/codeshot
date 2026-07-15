import pytest
from django.urls import reverse
from codeshot.models import ProductEvent
from codeshot.services.analytics import record_product_event

def upload_data_into_session(client):
    session = client.session
    session["code"] = "print('download png')"
    session["language"] = "python"
    session["filename"] = "png.py"
    session["theme"] = "default"
    session["font_size"] = 13
    session["padding"] = 24
    session.save()


def get_streaming_bytes(response):
    return b"".join(response.streaming_content)


@pytest.mark.django_db
def test_download_png(client):
    upload_data_into_session(client)
    response = client.get(reverse("download_png"))
    file_bytes = get_streaming_bytes(response)

    assert response.status_code == 200
    assert response["Content-Type"] == "image/png"
    assert "attachment" in response["Content-Disposition"]
    assert file_bytes.startswith(b"\x89PNG")


@pytest.mark.django_db
def test_download_jpg(client):
    upload_data_into_session(client)
    response = client.get(reverse("download_jpg"))
    file_bytes = get_streaming_bytes(response)

    assert response.status_code == 200
    assert response["Content-Type"] == "image/jpeg"
    assert "attachment" in response["Content-Disposition"]
    assert file_bytes.startswith(b"\xff\xd8\xff")


@pytest.mark.django_db
def test_download_png_or_jpg_with_records_of_events(client):
    upload_data_into_session(client)
    response = client.get(reverse("download_png"))

    assert response.status_code == 200

    started_event = ProductEvent.objects.get(event_name=ProductEvent.EXPORT_STARTED)

    assert started_event.event_name == "export_started"
    assert started_event.language == "python"
    assert started_event.theme == "default"

    completed_event = ProductEvent.objects.get(event_name=ProductEvent.EXPORT_COMPLETED)

    assert completed_event.event_name == "export_completed"
    assert completed_event.language == "python"
    assert completed_event.theme == "default"
