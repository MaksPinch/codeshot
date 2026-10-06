from django.core.cache import cache
from django.db.models import Count

from codeshot.models import ProductEvent

EVENT_SUMMARY_CACHE_KEY = "analytics:event-summary:v1"


def record_product_event(event_name, editor_state=None, export_format=""):
    if editor_state is None:
        editor_state = {}

    record = ProductEvent.objects.create(
        event_name=event_name,
        language=editor_state.get("language", ""),
        theme=editor_state.get("theme", ""),
        export_format=export_format,
    )

    cache.delete(EVENT_SUMMARY_CACHE_KEY)
    return record


def get_product_event_summary():
    cached_summary = cache.get(EVENT_SUMMARY_CACHE_KEY)
    if cached_summary is not None:
        return cached_summary
    summary = {
        "total_events": ProductEvent.objects.count(),
        "by_event_name": list(
            ProductEvent.objects.values("event_name")
            .annotate(count=Count("id"))
            .order_by("event_name")
        ),
        "exports_by_format": list(
            ProductEvent.objects.exclude(export_format="")
            .values("export_format")
            .annotate(count=Count("id"))
            .order_by("export_format")
        ),
    }
    cache.set(EVENT_SUMMARY_CACHE_KEY, summary, timeout=60)
    return summary
