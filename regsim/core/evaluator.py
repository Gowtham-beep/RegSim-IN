from regsim.core.fields import get_field
from regsim.core.validators import is_invalid_gstin


def evaluate_condition(condition, payload):
    if "field" not in condition:
        for raw_key, expected in condition.items():
            if raw_key.endswith("_gt"):
                field = raw_key[:-3]
                operator = ">"
            elif raw_key.endswith("_gte"):
                field = raw_key[:-4]
                operator = ">="
            elif raw_key.endswith("_eq"):
                field = raw_key[:-3]
                operator = "=="
            else:
                field = raw_key
                operator = "=="

            found, field_value = get_field(payload, field)
            if not found:
                return False

            try:
                if operator == ">":
                    if not field_value > expected:
                        return False
                elif operator == ">=":
                    if not field_value >= expected:
                        return False
                elif operator == "==":
                    if not field_value == expected:
                        return False
                else:
                    raise ValueError(f"Unsupported operator: {operator}")
            except TypeError:
                return False

        return True

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
