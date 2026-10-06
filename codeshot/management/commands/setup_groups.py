from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        group_export_users, _ = Group.objects.get_or_create(name="Export users")
        group_analysts_users, _ = Group.objects.get_or_create(name="Analysts")

        export_perm = Permission.objects.get(
            content_type__app_label="codeshot", codename="export_images"
        )

        stats_perm = Permission.objects.get(
            content_type__app_label="codeshot", codename="view_product_stats"
        )

        group_export_users.permissions.add(export_perm)
        group_analysts_users.permissions.add(stats_perm)

