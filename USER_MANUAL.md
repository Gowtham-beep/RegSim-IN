# RegSim-IN User Manual

This guide shows how to integrate RegSim-IN into real development workflows: local testing, CI, and rule authoring. It assumes you already installed the CLI via `pip install regsim-in` and can run `regsim-in` from your terminal.

## What RegSim-IN Does

- Validates JSON input against your regulatory rules.
- Emits a clear `PASS` or `FAIL` with structured details.
- Provides metadata for audit trails (rules applied, snapshot date).

It does not fetch live regulations, file taxes, or provide legal advice.

## Core Concepts

- Rules: JSON files that describe regulatory conditions and actions.
- Payloads: JSON objects (or extracted test payloads from Python files) that represent the data you want checked.
- Simulation: Running rules against payloads to surface violations.

## Basic Workflow

1. Write rules in JSON.
2. Save example payloads (JSON) or embed payloads in Python code (see “Python source input”).
3. Run `regsim-in simulate` during local development and in CI.
4. Inspect `PASS`/`FAIL` output and fix violations early.

## CLI Overview

- `regsim-in --version` prints the installed version.
- `regsim-in simulate --rules <path> --input <path>` runs a simulation.
- `--snapshot-date YYYY-MM-DD` attaches a regulatory snapshot date in output metadata.

## Quickstart

Create a minimal rule file `rules/tds.json`:

```json
{
  "rule_id": "TDS_194C_THRESHOLD",
  "rule_version": "1.0",
  "effective_from": "2024-04-01",
  "source_reference": "Income Tax Act 1961, Section 194C",
  "condition": {
    "all": [
      { "field": "payment.amount", "op": ">", "value": 30000 },
      { "field": "payment.vendor_type", "op": "==", "value": "contractor" },
      { "field": "payment.tds_deducted", "op": "==", "value": false }
    ]
  },
  "action": {
    "type": "FAIL",
    "severity": "HIGH",
    "message": "TDS must be deducted under section 194C"
  }
}
```

Create a payload `payload.json`:

```json
{
  "payment": {
    "id": "pay_1029",
    "amount": 45000,
    "vendor_type": "contractor",
    "tds_deducted": false
  }
}
```

Run:

```bash
regsim-in simulate --rules rules/ --input payload.json
```

You will get `PASS` or `FAIL` plus a list of violations and metadata.

## Using a Rules Folder

RegSim-IN loads all `.json` rules from a folder (recursively). This is the recommended approach for real projects.

```bash
regsim-in simulate --rules rules/ --input payload.json
```

Tips:
- Keep one rule per file for clarity and change tracking.
- Use consistent `rule_id` and `rule_version` fields.

## Using Multiple Payloads

You can run the CLI on different payload files as part of your test suite. Example using a shell loop:

```bash
for file in tests/payloads/*.json; do
  regsim-in simulate --rules rules/ --input "$file" || exit 1
done
```

## Python Source Input (Optional)

If you pass a Python file or a folder containing `.py` files, RegSim-IN attempts to extract embedded payloads and simulate them. This is useful when your test data is inside fixtures or inline examples.

```bash
regsim-in simulate --rules rules/ --input src/
```

If extraction errors occur, RegSim-IN will return a structured `ERROR` response.

## Snapshot Date for Audit Trails

Use `--snapshot-date` to record the regulatory snapshot date you are testing against. This value is echoed in the output metadata and can be stored alongside build artifacts.

```bash
regsim-in simulate --rules rules/ --input payload.json --snapshot-date 2025-04-01
```

## CI/CD Integration

Add a step that fails the build when any simulation fails.

GitHub Actions example:

```bash
regsim-in simulate --rules rules/ --input payload.json || exit 1
```

You can add multiple payloads or run across your test fixtures.

## Understanding Output

Successful output:

```json
{
  "status": "PASS",
  "violations": [],
  "metadata": {
    "engine": "regsim-in",
    "engine_version": "0.1.0",
    "rule_snapshot": "2025-04-01",
    "applied_rules": [
      {
        "rule_id": "TDS_194C_THRESHOLD",
        "rule_version": "1.0",
        "effective_from": "2024-04-01",
        "source_reference": "Income Tax Act 1961, Section 194C"
      }
    ]
  }
}
```

Failure output (example):

```json
{
  "status": "FAIL",
  "violations": [
    {
      "rule_id": "TDS_194C_THRESHOLD",
      "rule_version": "1.0",
      "severity": "HIGH",
      "message": "TDS must be deducted under section 194C",
      "risk": null,
      "source_reference": "Income Tax Act 1961, Section 194C"
    }
  ],
  "metadata": {
    "engine": "regsim-in",
    "engine_version": "0.1.0",
    "rule_snapshot": "2025-04-01",
    "applied_rules": [
      {
        "rule_id": "TDS_194C_THRESHOLD",
        "rule_version": "1.0",
        "effective_from": "2024-04-01",
        "source_reference": "Income Tax Act 1961, Section 194C"
      }
    ]
  }
}
```

## Rule Authoring Guidelines

- Keep rules small and focused.
- Use meaningful `rule_id` values and increment `rule_version` when logic changes.
- Always include `effective_from` and `source_reference` for traceability.
- Prefer `FAIL` actions for regulatory violations; extend rules only when needed.

## Troubleshooting

- `Input payload must be a JSON object`: Your input JSON is not an object at the top level.
- `Rules must be a JSON array`: Your rules file must contain a JSON array or a single JSON object (which will be wrapped).
- `Rule schema validation failed`: Check required fields like `rule_id`, `condition`, `action`.

## Safety and Disclaimer

RegSim-IN is a developer simulation tool for engineering feedback only. It does not guarantee legal or regulatory compliance. Always consult qualified professionals for real-world decisions.
