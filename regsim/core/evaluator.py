from regsim.core.fields import get_field
from regsim.core.validators import is_invalid_gstin


def evaluate_condition(condition, payload):
    found, field_value = get_field(payload, condition["field"])
    operator = condition["operator"]
    expected = condition["value"]

    if operator == "missing":
        return not found

    if operator == "invalid_gstin":
        return not found or is_invalid_gstin(field_value)

    if not found:
        return False

    try:
        if operator == ">":
            return field_value > expected
        if operator == ">=":
            return field_value >= expected
        if operator == "==":
            return field_value == expected
    except TypeError:
        return False

    raise ValueError(f"Unsupported operator: {operator}")
