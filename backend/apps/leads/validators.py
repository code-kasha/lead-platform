# ==============================================================================
# Validators for the leads app
# ==============================================================================

from django.core.exceptions import ValidationError


def validate_phone(value):

    if value and not value.replace("+", "").isdigit():

        raise ValidationError("Phone number must contain only digits.")
