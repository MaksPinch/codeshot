import pytest

from codeshot.models import ProductEvent
from codeshot.services.analytics import get_product_event_summary

@pytest.mark.django_db
def test_product_event_summary_counts_events():
    ProductEvent.objects.create(
        event_name=ProductEvent.PREVIEW_CREATED, language="python"
    )
    ProductEvent.objects.create(
        event_name=ProductEvent.EXPORT_COMPLETED,
        language="python",
        export_format="png"
    )

    summary = get_product_event_summary()

    assert summary["total_event"] == 2
    assert {"event_name": "preview_created", "count": 1} in summary["by_event_name"]
    assert {"export_format": "png", "count": 1} in summary["export_by_format"]
    
