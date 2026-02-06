import jsonschema

from regsim.core.simulation import load_json, load_schema, simulate
from regsim.parser import extract_from_file


def test_simulate_json_examples():
    rules = load_json("examples/rules.json")
    payload = load_json("examples/input.json")
    result = simulate(rules, payload, snapshot_date="2024-04-01")
    assert result["status"] in {"PASS", "FAIL"}
    assert "applied_rules" in result["metadata"]
    assert result["metadata"]["rule_snapshot"] == "2024-04-01"
    output_schema = load_schema("output.schema.json")
    jsonschema.validate(instance=result, schema=output_schema)


def test_simulate_messy_input_no_crash():
    rules = load_json("examples/rules.json")
    payload = load_json("examples/messy_input.json")
    result = simulate(rules, payload)
    assert result["status"] in {"PASS", "FAIL"}
    output_schema = load_schema("output.schema.json")
    jsonschema.validate(instance=result, schema=output_schema)


def test_extract_from_python_file():
    extraction = extract_from_file("examples/payout_service.py")
    assert extraction.errors == []
    assert extraction.payloads


def test_rule_schema_validation_fails_fast():
    rules = [{
        "rule_id": "BAD_RULE",
        "condition": {"field": "payment.amount", "operator": ">", "value": 1},
        "action": {"type": "FAIL", "message": "bad"},
    }]
    payload = {"payment": {"amount": 5}}

    try:
        simulate(rules, payload)
    except ValueError as exc:
        assert "schema validation failed" in str(exc)
    else:
        assert False, "Expected schema validation to fail"
