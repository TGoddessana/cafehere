import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_mobile_number(value):
    regex = r"^\+[0-9]{1,4}+-[0-9]{1,14}$"
    if not re.match(regex, value):
        raise ValidationError(
            message=_("{value} is not a valid mobile number").format(value=value),
            code="invalid_mobile_number",
        )
