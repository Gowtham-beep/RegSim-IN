import ast

def extract_dict(node):
    payload = {}

    for key, value in zip(node.keys, node.values):
        if isinstance(key, ast.Constant):
            if isinstance(value, ast.Constant):
                payload[key.value] = value.value

    return payload if payload else None
