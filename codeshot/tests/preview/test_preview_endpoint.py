from django.urls import reverse
import pytest
from rest_framework.test import APIClient

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
