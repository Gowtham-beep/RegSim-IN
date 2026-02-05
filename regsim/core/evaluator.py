from regsim.core.fields import get_field
from regsim.core.validators import is_invalid_gstin


def evaluate_condition(condition, payload):
    field_value = get_field(payload, condition["field"])
    operator = condition["operator"]
    expected = condition["value"]

    if operator == "missing":
        return field_value is None

    if operator == "invalid_gstin":
        return is_invalid_gstin(field_value)

    if field_value is None:
        return False

    if operator == ">":
        return field_value > expected
    if operator == ">=":
        return field_value >= expected
    if operator == "==":
        return field_value == expected

    raise ValueError(f"Unsupported operator: {operator}")
