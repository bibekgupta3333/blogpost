from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator


def validate_phone_number(value):
    if len(value) <= 9:
        raise ValidationError('Phone numbers must not be less than 10 digits')
    return value
