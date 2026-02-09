import ast


def _literal_or_none(node):
    try:
        return ast.literal_eval(node)
    except Exception:
        return None


def extract_dict(node):
    value = _literal_or_none(node)
    if isinstance(value, dict):
        return value
    return None
