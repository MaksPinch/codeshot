from django.db import models


class ProductEvent(models.Model):
    PREVIEW_CREATED = "preview_created"
    EXPORT_STARTED = "export_started"
    EXPORT_COMPLETED = "export_completed"
    EXPORT_FAILED = "export_failed"

    EVENT_LIST = [
        (PREVIEW_CREATED, "Preview created"),
        (EXPORT_STARTED, "Export started"),
        (EXPORT_COMPLETED, "Export completed"),
        (EXPORT_FAILED, "Export failed"),
    ]
    event_name = models.CharField(max_length=64, choices=EVENT_LIST)
    language = models.CharField(max_length=32, blank=True)
    theme = models.CharField(max_length=32, blank=True)
    export_format = models.CharField(max_length=16, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["event_name", "created_at"]),
        ]

        permissions = [
            ("export_images", "Can export images"),
            ("view_product_stats", "Can view product statistics"),
        ]

    def __str__(self):
        return f"{self.event_name} at {self.created_at:%Y-%m-%d %H:%M:%S}"
