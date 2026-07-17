import pytest
from django.urls import reverse

def upload_data_into_session(client):
    session = client.session
    session["code"] = "print('download png')"
    session["language"] = "python"
    session["filename"] = "png.py"
    session["theme"] = "default"
    session["font_size"] = 13
    session["padding"] = 24
    session.save()

@pytest.mark.django_db
def test_download_png(client):
    upload_data_into_session(client)
    response = client.get(reverse("download_png"))

    assert response.status_code == 200
    assert response["Content-Type"] == 'image/png'
    assert "attachment" in response["Content-Disposition"]
    
@pytest.mark.django_db
def test_download_jpg(client):
    upload_data_into_session(client)
    response = client.get(reverse("download_jpg"))

    assert response.status_code == 200
    assert response["Content-Type"] == "image/jpeg"
    assert "attachment" in response["Content-Disposition"]


