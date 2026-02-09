import ast
import json

from regsim.utils import extract_call_args, extract_dict, get_func_name


class ExtractionResult:
    def __init__(self):
        self.payloads = []
        self.errors = []


def _add_unique_payload(result: ExtractionResult, payload, seen):
    if not payload:
        return
    key = json.dumps(payload, sort_keys=True, default=str)
    if key in seen:
        return
    seen.add(key)
    result.payloads.append(payload)


def extract_from_file(file_path):
    result = ExtractionResult()
    seen = set()

    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())
    except Exception as e:
        result.errors.append(str(e))
        return result

    for node in ast.walk(tree):
        # Detect dict literals assigned to variables
        if isinstance(node, ast.Assign):
            if isinstance(node.value, ast.Dict):
                payload = extract_dict(node.value)
                _add_unique_payload(result, payload, seen)
        if isinstance(node, ast.AnnAssign) and isinstance(node.value, ast.Dict):
            payload = extract_dict(node.value)
            _add_unique_payload(result, payload, seen)

        # Detect function calls with literal keyword args.
        if isinstance(node, ast.Call):
            func_name = get_func_name(node)
            if func_name:
                payload = extract_call_args(node)
                _add_unique_payload(result, payload, seen)

    return result
