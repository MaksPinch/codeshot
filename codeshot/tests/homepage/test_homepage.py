from rest_framework.test import APIClient
from django.urls import reverse

def test_homepage():
    client = APIClient()
    url = reverse('home')
    resp = client.get(url)

    assert resp.status_code == 200
