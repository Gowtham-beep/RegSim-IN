from regsim.core.simulation import load_json, simulate
from regsim.parser import extract_from_file


def test_simulate_json_examples():
    rules = load_json("examples/rules.json")
    payload = load_json("examples/input.json")
    result = simulate(rules, payload, snapshot_date="2024-04-01")
    assert result["status"] in {"PASS", "FAIL"}
    assert "applied_rules" in result["metadata"]
    assert result["metadata"]["rule_snapshot"] == "2024-04-01"


def test_simulate_messy_input_no_crash():
    rules = load_json("examples/rules.json")
    payload = load_json("examples/messy_input.json")
    result = simulate(rules, payload)
    assert result["status"] in {"PASS", "FAIL"}


def test_extract_from_python_file():
    extraction = extract_from_file("examples/payout_service.py")
    assert extraction.errors == []
    assert extraction.payloads
