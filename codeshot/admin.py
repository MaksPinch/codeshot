from django.contrib import admin

from codeshot.models import ProductEvent


@admin.register(ProductEvent)
class ProductEventAdmin(admin.ModelAdmin):
    list_display = ("event_name", "language", "theme", "export_format", "created_at")
    list_filter = ("event_name", "language", "theme", "export_format")
    search_fields = ("language", "theme", "export_format")
    readonly_fields = ("created_at",)
