from django.contrib import admin

from codeshot.models import ProductEvent

def test_product_event_registers_in_admin():
    assert ProductEvent in admin.site._registry

