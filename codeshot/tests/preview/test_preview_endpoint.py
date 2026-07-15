from django.urls import reverse
import pytest
from rest_framework.test import APIClient
from codeshot.models import ProductEvent
from codeshot.services.analytics import record_product_event

@pytest.mark.django_db
def test_preview_endpoint_returns_highlighted_payload():
    client = APIClient()
    response = client.post(
        reverse("preview"),
        {
            "code": "print('Hello test preview endpoint')",
            "language": "python",
            "filename": "test_preview.py",
            "theme": "monokai",
            "font_size": 13,
            "padding": 52,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "highlight" in payload["highlighted_code"]
    assert payload["filename"] == "test_preview.py"
    assert payload["theme"] == "monokai"
    assert payload["font_size"] == 13
    assert payload["padding"] == 52


def test_preview_endpoint_rejects_invalid_data():
    client = APIClient()
    response = client.post(reverse("preview"), {"code": ""})
    assert response.status_code == 400
    assert "code" in response.json()["errors"]


def test_preview_endpoint_rejects_get():
    client = APIClient()
    response = client.get(reverse("preview"))
    assert response.status_code == 405



@pytest.mark.django_db
def test_preview_endpoint_records_preview_event(client):
    response = client.post(
        reverse("preview"),
        {
            "code": "print('hello')",
            "language": "python",
            "filename": "hello.py",
            "theme": "dracula",
            "font_size": 14,
            "padding": 24,
        },
    )

    assert response.status_code == 200
    event = ProductEvent.objects.get(event_name=ProductEvent.PREVIEW_CREATED)
    assert event.language == "python"
    assert event.theme == "dracula"
