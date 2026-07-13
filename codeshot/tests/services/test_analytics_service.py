import pytest

from codeshot.models import ProductEvent
from codeshot.services.analytics import record_product_event


@pytest.mark.django_db
def test_analytics_service():
    event = record_product_event(
        ProductEvent.PREVIEW_CREATED,
        editor_state={
            "code": "print('secret')",
            "language": "python",
            "theme": "dracula",
        }
    )

    assert event.event_name == ProductEvent.PREVIEW_CREATED
    assert event.language == "python"
    assert event.theme == "dracula"
    
