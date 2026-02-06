import json
from pathlib import Path

from regsim.core.evaluator import evaluate_condition
from regsim.engine import InvalidPayloadError, validate_rules


def load_json(path: str):
    raw = Path(path).read_text().strip()
    if not raw:
        raise ValueError(f"{path} is empty")
    return json.loads(raw)


def simulate(rules, payload, snapshot_date=None) -> dict:
    if not isinstance(payload, dict):
        raise InvalidPayloadError("Input payload must be a JSON object")

    validate_rules(rules)

    violations = []
    applied_rules = []

    for rule in rules:
        applied_rules.append({
            "rule_id": rule.get("rule_id"),
            "rule_version": rule.get("rule_version"),
            "effective_from": rule.get("effective_from"),
            "source_reference": rule.get("source_reference"),
        })

        condition = rule["condition"]
        action = rule["action"]

        if evaluate_condition(condition, payload):
            if action["type"] == "FAIL":
                violations.append({
                    "rule_id": rule["rule_id"],
                    "rule_version": rule.get("rule_version"),
                    "severity": action.get("severity", "HIGH"),
                    "message": action["message"],
                    "risk": action.get("risk"),
                    "source_reference": rule.get("source_reference"),
                })

    status = "FAIL" if violations else "PASS"

    return {
        "status": status,
        "violations": violations,
        "metadata": {
            "engine": "regsim-in",
            "engine_version": "0.1.0",
            "rule_snapshot": snapshot_date,
            "applied_rules": applied_rules,
        },
    }


def run_simulation(rules_path: str, input_path: str) -> dict:
    rules = load_json(rules_path)
    payload = load_json(input_path)

    return simulate(rules, payload)
