import logging

from celery import shared_task
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .models import ExportJob
from .services.exports import generate_image

logger = logging.getLogger(__name__)


@shared_task
def ping_task():
    return "pong"


@shared_task
def export_image_task(job_id):
    export_job = ExportJob.objects.get(id=job_id)
    export_job.status = ExportJob.PROCESSING_STATUS
    export_job.save()

    try:
        image_format = export_job.export_format
        image_bytes = generate_image({}, image_format)

        file_content = ContentFile(image_bytes)
        file_name = default_storage.save(
            f"exports/export_{export_job.id}.{image_format}", file_content
        )

        export_job.file_name = file_name
        export_job.status = ExportJob.COMPLETED_STATUS
        export_job.error = ""
        export_job.save()

    except Exception:
        export_job.status = ExportJob.FAILED_STATUS
        export_job.file_name = ""
        export_job.error = "Could not generate image export."
        export_job.save()

        logger.exception("Export job %s failed", job_id)
        raise
