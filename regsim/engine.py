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


def simulate(rules,payload):
    if not isinstance(payload, dict):
        raise InvalidPayloadError("Input payload must be a JSON object")
    
    return{
        # place holder logic
        "status":"PASS",
        "violations":[],
        "metadata":{
            "engine":"regsim-in",
            "version":"0.1.0"
        }
    }
