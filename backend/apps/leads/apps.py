# ==============================================================================
# Leads App Configuration
# ==============================================================================


from django.apps import AppConfig


class LeadsConfig(AppConfig):
    """Configure the leads application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.leads"
    label = "leads"
