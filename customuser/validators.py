from django.core.exceptions import ValidationError
import re


def validate_enterprise_numberl(value):
    reg = re.compile("[A-Za-z]")
    reg_ok = re.compile("[0-9 -.]{9,12}")
    if len(re.findall(reg, value)):
        raise ValidationError("no character in the field")
    elif len(re.findall(reg_ok, value)):
        return value
    else:
        raise ValidationError("unknown characters")
