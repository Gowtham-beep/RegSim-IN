import ast

def extract_call_args(call_node):
    payload = {}

    for kw in call_node.keywords:
        if isinstance(kw.value, ast.Constant):
            payload[kw.arg] = kw.value.value

    return payload if payload else None
