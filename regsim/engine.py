def get_field(payload, field_path):
    """
    Fetch nested fields like payment.amount.
    Returns a tuple: (found, value)
    """
    parts = field_path.split(".")
    current = payload

    for part in parts:
        if not isinstance(current, dict):
            return False, None
        if part not in current:
            return False, None
        current = current[part]

    return True, current


class InvalidPayloadError(Exception):
    pass


REQUIRED_RULE_FIELDS = [
    "rule_id",
    "rule_version",
    "effective_from",
    "condition",
    "action",
]


def validate_rules(rules):
    for rule in rules:
        for field in REQUIRED_RULE_FIELDS:
            if field not in rule:
                raise ValueError(
                    f"Rule missing required field: {field} ({rule.get('rule_id')})"
                )


def simulate(rules,payload):
    if not isinstance(payload, dict):
        raise InvalidPayloadError("Input payload must be a JSON object")

    validate_rules(rules)
    
    return{
        # place holder logic
        "status":"PASS",
        "violations":[],
        "metadata":{
            "engine":"regsim-in",
            "version":"0.1.0"
        }
    }
