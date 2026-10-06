from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client
from django.urls import reverse

from codeshot.models import ExportJob


def test_create_export_requires_authentication():
    client = Client()
    url = reverse("create_export")
    response = client.post(url, data={"export_format": "png"})

    assert response.status_code == 401
    assert response.json() == {"error": "Authentication required"}


@pytest.mark.django_db
def test_create_export_without_permission_returns_403():
    client = Client()
    User = get_user_model()
    user = User.objects.create_user(
        username="ivan", email="ivan@example.com", password="secure_password"
    )
    url = reverse("create_export")

    client.force_login(user)
    response = client.post(url, data={"export_format": "png"})

    assert response.status_code == 403
    assert response.json() == {"error": "Permission denied"}
    assert ExportJob.objects.count() == 0


@pytest.mark.django_db
def test_create_export_with_permission_returns_202():
    client = Client()
    User = get_user_model()
    user = User.objects.create_user(
        username="ivan", email="ivan@example.com", password="secure_password"
    )
    url = reverse("create_export")

    client.force_login(user)
    permission = Permission.objects.get(
        codename="export_images",
        content_type__app_label="codeshot",
    )
    user.user_permissions.add(permission)

    with patch("codeshot.views.export_image_task.delay") as delay_mock:
        response = client.post(url, data={"export_format": "png"})

    assert response.status_code == 202
    assert user.has_perm("codeshot.export_images")

    export_job = ExportJob.objects.get()
    assert response.json() == {
        "id": export_job.id,
        "status": ExportJob.PENDING_STATUS,
    }
    assert export_job.user_id == user.id
    assert export_job.export_format == ExportJob.PNG_FORMAT
    delay_mock.assert_called_once_with(export_job.id)


@pytest.mark.django_db
def test_export_job_owner_can_get_status():
    client = Client()
    User = get_user_model()
    user = User.objects.create_user(
        username="ivan", email="ivan@example.com", password="secure_password"
    )
    client.force_login(user)
    job = ExportJob.objects.create(
        user=user,
        export_format=ExportJob.PNG_FORMAT,
    )
    url = reverse("export_detail", args=[job.id])

    response = client.get(url)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == job.id
    assert data["export_format"] == "png"
    assert data["status"] == ExportJob.PENDING_STATUS
    assert data["file_name"] == ""
    assert data["error"] == ""


@pytest.mark.django_db
def test_export_job_other_user_returns_403():
    client = Client()
    User = get_user_model()

    first_user = User.objects.create_user(
        username="ivan", email="ivan@example.com", password="secure_password"
    )
    second_user = User.objects.create_user(
        username="petor", email="petor@example.com", password="secure_password_1"
    )
    job = ExportJob.objects.create(
        user=first_user,
        export_format=ExportJob.PNG_FORMAT,
    )

    url = reverse("export_detail", args=[job.id])
    client.force_login(second_user)

    response = client.get(url)

    assert response.status_code == 403
    assert response.json() == {"error": "Permission denied"}


@pytest.mark.django_db
def test_export_job_not_found_returns_404():
    client = Client()
    User = get_user_model()
    user = User.objects.create_user(
        username="ivan", email="ivan@example.com", password="secure_password"
    )
    client.force_login(user)

    url = reverse("export_detail", args=[999999])
    response = client.get(url)

    assert response.status_code == 404
