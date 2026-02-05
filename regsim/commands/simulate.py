# regsim/commands/simulate.py

import json
from datetime import datetime
from pathlib import Path


def load_json(path: str):
    raw = Path(path).read_text().strip()
    if not raw:
        raise ValueError(f"{path} is empty")
    return json.loads(raw)


def evaluate_condition(condition: dict, facts: dict) -> bool:
    for key, expected in condition.items():
        if key.endswith("_gt"):
            fact_key = key.replace("_gt", "")
            if facts.get(fact_key, 0) <= expected:
                return False
        else:
            if facts.get(key) != expected:
                return False
    return True


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
                "authority": rule["authority"],
                "severity": rule["severity"],
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
