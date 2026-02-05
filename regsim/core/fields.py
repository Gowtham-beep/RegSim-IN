from typing import Any


def get_field(payload: Any, field_path: str):
    if field_path is None or field_path == "":
        return payload

    current = payload
    for part in field_path.split("."):
        if isinstance(current, dict):
            if part in current:
                current = current[part]
            else:
                return None
            continue

        if isinstance(current, list):
            if part.isdigit():
                idx = int(part)
                if 0 <= idx < len(current):
                    current = current[idx]
                else:
                    return None
                continue
            return None

        return None

    return current
