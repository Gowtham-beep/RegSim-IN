import json
from datetime import datetime
from pathlib import Path

from regsim.core.evaluator import evaluate_condition
from regsim.engine import InvalidPayloadError


def load_json(path: str):
    raw = Path(path).read_text().strip()
    if not raw:
        raise ValueError(f"{path} is empty")
    return json.loads(raw)


def evaluate_rules(rules, facts) -> dict:
    if not isinstance(facts, dict):
        raise InvalidPayloadError("Input payload must be a JSON object")

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
                "evidence": evidence,
            })

    status = "PASS"
    for v in violations:
        if v.get("severity") == "BLOCKER":
            status = "FAIL"
            break
        status = "FAIL"

    return {
        "status": status,
        "violations": violations,
        "metadata": {
            "engine": "regsim-in",
            "version": "0.1.0",
            "payload_keys": list(facts.keys()),
        },
    }


def run_simulation(rules_path: str, input_path: str) -> dict:
    rules = load_json(rules_path)
    facts = load_json(input_path)

    return evaluate_rules(rules, facts)
