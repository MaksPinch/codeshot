from django.test import Client
from django.urls import reverse

def test_health(client):
    client = Client()
    response = client.get(reverse("health"))

    assert response.status_code == 200
    assert response["Content-Type"] == "application/json"
    assert b'{"status": "ok"}' in response.content
