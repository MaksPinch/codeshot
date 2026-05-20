import pytest
from django.urls import reverse
from rest_framework.test import APIClient


def test_homepage():
    client = APIClient()
    url = reverse("home")
    response = client.get(url)

    assert response.status_code == 200
    assert b"CodeShot" in response.content
    assert b'name="code"' in response.content
    assert b'name="language"' in response.content
    assert b'name="filename"' in response.content
    assert b"Generate preview" in response.content


@pytest.mark.django_db
def test_valid_post_saves_code_input_in_session():
    client = APIClient()

    response = client.post(
        reverse("home"),
        {
            "code": "print('saved')",
            "language": "python",
            "filename": "saved.py",
        },
    )
    
    assert response.status_code == 200
    session = client.session
    assert session["code"] == "print('saved')"
    assert session["language"] == "python"
    assert session["filename"] == "saved.py"


@pytest.mark.django_db
def test_get_restores_form_values_from_session():
    client = APIClient()

    session = client.session
    session["code"] = "print('restored')"
    session["language"] = "python"
    session["filename"] = "restored.py"
    session.save()

    response = client.get(reverse("home"))

    assert response.status_code == 200
    assert b"print(&#x27;restored&#x27;)" in response.content
    assert b"restored.py" in response.content
