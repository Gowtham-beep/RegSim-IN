import json
import sys

import jsonschema
import pytest

from regsim.cli import main as cli_main
from regsim.core.simulation import load_json, load_rules, load_schema, simulate
from regsim.engine import simulate as legacy_engine_simulate
from regsim.parser import extract_from_file


def test_simulate_json_examples():
    rules = load_rules("rules/tds/194C_threshold.json")
    payload = load_json("examples/input.json")
    result = simulate(rules, payload, snapshot_date="2024-04-01")
    assert result["status"] in {"PASS", "FAIL"}
    assert "applied_rules" in result["metadata"]
    assert result["metadata"]["rule_snapshot"] == "2024-04-01"
    output_schema = load_schema("output.schema.json")
    jsonschema.validate(instance=result, schema=output_schema)


def test_simulate_messy_input_no_crash():
    rules = load_rules("rules/tds/194C_threshold.json")
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


def test_structured_all_condition_with_op_alias():
    rules = [{
        "rule_id": "TDS_194C_THRESHOLD",
        "rule_version": "1.0",
        "effective_from": "2024-04-01",
        "condition": {
            "all": [
                {"field": "payment.amount", "op": ">", "value": 30000},
                {"field": "payment.vendor_type", "op": "==", "value": "contractor"},
                {"field": "payment.tds_deducted", "op": "==", "value": False},
            ]
        },
        "action": {
            "type": "FAIL",
            "severity": "HIGH",
            "message": "TDS must be deducted under section 194C",
        },
    }]
    payload = {
        "payment": {
            "amount": 45000,
            "vendor_type": "contractor",
            "tds_deducted": False,
        }
    }

    result = simulate(rules, payload)
    assert result["status"] == "FAIL"
    assert len(result["violations"]) == 1


def test_rbi_rules_validate_against_output_schema():
    rules = load_rules("rules/rbi/pa_fund_flow.json")
    payload = load_json("examples/rbi_input.json")
    result = simulate(rules, payload)
    output_schema = load_schema("output.schema.json")
    jsonschema.validate(instance=result, schema=output_schema)


def test_extract_from_python_file_handles_nested_literals_and_generic_calls(tmp_path):
    source = tmp_path / "service.py"
    source.write_text(
        "payload = {'payment': {'amount': 45000, 'vendor_type': 'contractor'}}\n"
        "def process():\n"
        "    create_transfer(amount=45000, vendor_type='contractor', tags=['vip'])\n"
    )

    extraction = extract_from_file(str(source))
    assert extraction.errors == []
    assert any("payment" in payload for payload in extraction.payloads)
    assert any(payload.get("amount") == 45000 for payload in extraction.payloads)


def test_cli_errors_on_python_input_with_no_extractable_payloads(monkeypatch, tmp_path, capsys):
    source = tmp_path / "empty.py"
    source.write_text("def noop():\n    return 1\n")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "regsim-in",
            "simulate",
            "--rules",
            "rules/tds/194C_threshold.json",
            "--input",
            str(source),
        ],
    )

    with pytest.raises(SystemExit) as exc:
        cli_main()

    assert exc.value.code == 2
    output = capsys.readouterr().out
    response = json.loads(output)
    assert response["status"] == "ERROR"
    assert "No payloads extracted" in response["message"]


def test_engine_simulate_delegates_to_core_behavior():
    rules = load_rules("rules/tds/194C_threshold.json")
    payload = load_json("examples/input.json")

    result = legacy_engine_simulate(rules, payload, snapshot_date="2024-04-01")
    assert result["metadata"]["engine_version"] == "0.1.0"
