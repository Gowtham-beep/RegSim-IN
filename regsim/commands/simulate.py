# regsim/commands/simulate.py

import json
from datetime import datetime
from pathlib import Path
import re

GSTIN_REGEX = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")

def is_invalid_gstin(value):
    if not isinstance(value, str):
        return True
    return not bool(GSTIN_REGEX.match(value))

def get_field(payload, field_path: str):
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



def load_json(path: str):
    raw = Path(path).read_text().strip()
    if not raw:
        raise ValueError(f"{path} is empty")
    return json.loads(raw)


def evaluate_condition(condition, payload):
    field_value = get_field(payload, condition["field"])
    operator = condition["operator"]
    expected = condition["value"]

    if operator == "missing":
        return field_value is None

    if operator == "invalid_gstin":
        return is_invalid_gstin(field_value)

    if field_value is None:
        return False

    if operator == ">":
        return field_value > expected
    if operator == ">=":
        return field_value >= expected
    if operator == "==":
        return field_value == expected

    raise ValueError(f"Unsupported operator: {operator}")



def run_simulation(rules_path: str, input_path: str) -> dict:
    rules = load_json(rules_path)
    facts = load_json(input_path)

    violations = []

    for rule in rules:
        if evaluate_condition(rule["condition"], facts):
            evidence = {
                f: facts.get(f)
                for f in rule["action"].get("evidence_fields", [])
            }

            violations.append({
                "rule_id": rule["rule_id"],
                "rule_version": rule["rule_version"],
                "authority": rule.get("authority"),
                "severity": rule.get("severity"),
                "message": rule["action"]["message"],
                "source_reference": rule.get("source_reference"),
                "risk": rule["action"].get("risk"),
                "evidence": evidence
            })

    return {
        "status": "FAIL" if violations else "PASS",
        "violations": violations,
        "metadata": {
            "evaluated_at": datetime.now().isoformat() + "Z",
            "engine_version": "0.1.0"
        }
    }
