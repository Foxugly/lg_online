import re

from django.core.exceptions import ValidationError


def validate_enterprise_number(value):
    reg = re.compile("[A-Za-z]")
    reg_ok = re.compile("[0-9 -.]{9,12}")
    if len(re.findall(reg, value)):
        raise ValidationError("no character in the field")
    elif len(re.findall(reg_ok, value)):
        return value
    else:
        raise ValidationError("unknown characters")
