import pytest

from codeshot.models import ProductEvent


@pytest.mark.django_db
def test_product_event_can_be_created():
    event = ProductEvent.objects.create(
        event_name=ProductEvent.PREVIEW_CREATED,
        language="python",
        theme="dracula",
    )
    assert event.id is not None
    assert event.event_name == ProductEvent.PREVIEW_CREATED
    assert event.created_at is not None
