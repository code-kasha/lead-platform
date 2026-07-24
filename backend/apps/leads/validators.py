# ==============================================================================
# Validators for the leads app
# ==============================================================================

from django.core.exceptions import ValidationError


def validate_phone(value):
    """Ensure phone numbers contain only digits and an optional plus sign."""

    if value and not value.replace("+", "").isdigit():

        raise ValidationError("Phone number must contain only digits.")
