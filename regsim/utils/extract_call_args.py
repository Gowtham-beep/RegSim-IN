import ast


def _literal_or_none(node):
    try:
        return ast.literal_eval(node)
    except Exception:
        return None


def extract_call_args(call_node):
    payload = {}

    for kw in call_node.keywords:
        if kw.arg is None:
            continue
        value = _literal_or_none(kw.value)
        if value is not None:
            payload[kw.arg] = value

    return payload if payload else None
