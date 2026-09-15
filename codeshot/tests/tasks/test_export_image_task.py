import pytest
from django.contrib.auth import get_user_model

from codeshot.models import ExportJob
from codeshot.tasks import export_image_task


@pytest.mark.django_db
def test_export_image_task_completes(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path
    user = get_user_model().objects.create_user(
        username="ivan", password="secure_password"
    )
    job = ExportJob.objects.create(
        user=user,
        export_format=ExportJob.PNG_FORMAT,
    )

    result = export_image_task.apply(args=[job.id])
    job.refresh_from_db()

    assert result.successful()
    assert job.status == ExportJob.COMPLETED_STATUS
    assert job.file_name.endswith(".png")
    assert job.error == ""
    assert (tmp_path / job.file_name).exists()


@pytest.mark.django_db
def test_export_image_task_fails_for_invalid_format():
    user = get_user_model().objects.create_user(
        username="ivan", password="secure_password"
    )
    job = ExportJob.objects.create(
        user=user,
        export_format="txt",
    )

    result = export_image_task.apply(args=[job.id])
    job.refresh_from_db()

    assert result.failed()
    assert job.status == ExportJob.FAILED_STATUS
    assert job.file_name == ""
    assert job.error == "Could not generate image export."
