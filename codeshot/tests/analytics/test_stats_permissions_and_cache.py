import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.cache import cache
from django.test import Client, override_settings
from django.urls import reverse

from codeshot.models import ProductEvent
from codeshot.services.analytics import (
    EVENT_SUMMARY_CACHE_KEY,
    get_product_event_summary,
    record_product_event,
)


TEST_CACHE = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "codeshot-tests",
    }
}


@pytest.mark.django_db
def test_regular_user_cannot_get_stats():
    client = Client()
    user = get_user_model().objects.create_user(
        username="ivan", password="secure_password"
    )
    client.force_login(user)

    response = client.get(reverse("stats"))

    assert response.status_code == 403
    assert response.json() == {"error": "Permission denied"}


@pytest.mark.django_db
@override_settings(CACHES=TEST_CACHE)
def test_analyst_can_get_stats():
    cache.clear()
    client = Client()
    user = get_user_model().objects.create_user(
        username="anna", password="secure_password"
    )
    group = Group.objects.create(name="Analysts")
    permission = Permission.objects.get(
        codename="view_product_stats",
        content_type__app_label="codeshot",
    )
    group.permissions.add(permission)
    user.groups.add(group)
    client.force_login(user)

    response = client.get(reverse("stats"))

    assert response.status_code == 200
    assert response.json()["total_events"] == 0


@pytest.mark.django_db
@override_settings(CACHES=TEST_CACHE)
def test_product_event_summary_uses_cache(django_assert_num_queries):
    cache.clear()
    ProductEvent.objects.create(event_name=ProductEvent.PREVIEW_CREATED)

    first_summary = get_product_event_summary()

    with django_assert_num_queries(0):
        second_summary = get_product_event_summary()

    assert second_summary == first_summary


@pytest.mark.django_db
@override_settings(CACHES=TEST_CACHE)
def test_record_product_event_clears_cache():
    cache.clear()
    cache.set(EVENT_SUMMARY_CACHE_KEY, {"total_events": 100}, timeout=60)

    record_product_event(ProductEvent.PREVIEW_CREATED)

    assert cache.get(EVENT_SUMMARY_CACHE_KEY) is None
