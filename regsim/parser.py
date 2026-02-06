import ast

from regsim.utils import extract_call_args, extract_dict, get_func_name

class ExtractionResult:
    def __init__(self):
        self.payloads = []
        self.errors = []

def extract_from_file(file_path):
    result = ExtractionResult()

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
                if payload:
                    result.payloads.append(payload)

        # Detect function calls like payout(...)
        if isinstance(node, ast.Call):
            func_name = get_func_name(node)
            if func_name and "payout" in func_name.lower():
                payload = extract_call_args(node)
                if payload:
                    result.payloads.append(payload)

    return result
