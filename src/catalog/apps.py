"""Django app configuration for the catalog app."""

from django.apps import AppConfig


class CatalogConfig(AppConfig):
    """Configuration for the catalog Django app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "catalog"
