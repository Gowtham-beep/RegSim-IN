from regsim.core.fields import get_field
from regsim.core.validators import is_invalid_gstin


def _compare(found, field_value, operator, expected):
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


def _evaluate_structured_condition(condition, payload):
    if "all" in condition:
        return all(evaluate_condition(item, payload) for item in condition["all"])
    if "any" in condition:
        return any(evaluate_condition(item, payload) for item in condition["any"])
    if "not" in condition:
        return not evaluate_condition(condition["not"], payload)

    found, field_value = get_field(payload, condition["field"])
    operator = condition.get("operator")
    if operator is None and "op" in condition:
        operator = condition["op"]
    expected = condition.get("value")
    return _compare(found, field_value, operator, expected)


def evaluate_condition(condition, payload):
    if "field" in condition or "all" in condition or "any" in condition or "not" in condition:
        return _evaluate_structured_condition(condition, payload)

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

            if not _compare(found, field_value, operator, expected):
                return False

        return True
