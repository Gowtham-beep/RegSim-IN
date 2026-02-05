import re

GSTIN_REGEX = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")


def is_invalid_gstin(value):
    if not isinstance(value, str):
        return True
    return not bool(GSTIN_REGEX.match(value))
