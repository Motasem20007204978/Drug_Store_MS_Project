from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class NameValidator(RegexValidator):
    regex = r"^[A-Z][A-Za-z_]{5,}"
    message = (
        "enter name begins with capital letter and A-Z, a-z or _"
        " between 5 and 50 characters"
    )
    flags = 0


name_validator = NameValidator()


def integer_length(value):
    if value > 10000:
        raise ValidationError("the quantity of a drug cannot be more than 10000")
