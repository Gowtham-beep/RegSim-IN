# RegSim-IN

**Regulatory Simulation & Failure Memory CLI for Indian Backend Systems**

---

## What is RegSim-IN?

**RegSim-IN** is a **developer-first CLI** that simulates Indian regulatory rules (TDS, GST, RBI-style constraints) against backend data flows **before production**.

It helps backend teams **detect, explain, and remember regulatory failures** early — during development, testing, and CI — instead of discovering them during audits or incidents.

RegSim-IN treats regulation as **executable rules**, not PDFs.

---

## What Problem Does This Solve?

Backend teams frequently:

* Ship compliant-looking code that fails under real regulatory edge cases
* Discover issues late (audits, settlements, reversals)
* Repeat the *same regulatory mistakes* across services and teams

RegSim-IN exists to:

* Shift regulatory failures **left**
* Make rules **explicit and testable**
* Prevent **repeat regulatory incidents**

---

## What RegSim-IN v1 Does 

Version 1 focuses on **deterministic rule simulation**.

RegSim-IN v1 can:

* Load regulatory rules defined in **JSON**
* Run those rules against input payloads (also JSON)
* Evaluate pass/fail conditions
* Emit **machine-readable JSON output**
* Explain *why* a rule failed

This makes RegSim-IN suitable for:

* Local development checks
* CI/CD gates
* Backend design validation
* Regulatory edge-case exploration

---

## Example: Detecting a Missed TDS Deduction

Consider a backend payout flow where a contractor payment is executed without deducting TDS.

**Input payload:**
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

**Simulation result:**

```json
{
  "status": "FAIL",
  "violations": [
    {
      "rule_id": "TDS_194C_THRESHOLD",
      "severity": "HIGH",
      "message": "TDS must be deducted under section 194C"
    }
  ]
}
```

This allows teams to catch deduction timing and threshold violations **before** payouts reach production systems.

---

## What RegSim-IN Explicitly Does NOT Do 

To avoid misuse or false confidence, RegSim-IN v1 does **not**:

*  Provide legal, tax, or regulatory advice
*  File or generate GST / TDS / RBI reports
*  Integrate with government, bank, or tax APIs
*  Automatically update rules from circulars
*  Fully simulate async systems (queues, retries, persistent state)

**This is a simulation tool, not a compliance authority.**

---

## Supported Languages

* **Python** (v1)

The CLI is language-agnostic, but rule evaluation currently targets Python-style backend data models.

---

## Rule Format

Rules are defined in **JSON**.

Design goals:

* Explicit structure
* Deterministic evaluation
* Easy diffing & review
* CI/CD friendliness

### Example Rule

```json
{
  "rule_id": "TDS_194C_THRESHOLD",
  "rule_version": "1.0",
  "effective_from": "2024-04-01",
  "description": "TDS applies if contractor payment exceeds threshold",
  "condition": {
    "field": "payment.amount",
    "operator": ">",
    "value": 30000
  },
  "action": {
    "type": "FAIL",
    "message": "TDS must be deducted under section 194C"
  },
  "source_reference": "Income Tax Act - Section 194C"
}
```

---

## Input Format

Inputs represent **backend payloads or traces**, also in JSON.

---

## Output Format

All outputs are **JSON only**.

Example failure output:

```json
{
  "status": "FAIL",
  "violations": [
    {
      "rule_id": "TDS_194C_THRESHOLD",
      "severity": "HIGH",
      "message": "TDS must be deducted under section 194C"
    }
  ],
  "metadata": {
    "snapshot_date": "2024-04-01"
  }
}
```

This makes RegSim-IN suitable for automation and tooling.

---

## Installation (Early Prototype)

```bash
pip install regsim-in
```

>  RegSim-IN is under active development.

---

## Usage (v1)

```bash
regsim-in simulate \
  --rules rules.json \
  --input input.json
```

Current v1 behavior:

* CLI initializes correctly
* Rules are parsed and validated
* Simulation runs deterministically
* JSON output is emitted

---

## Project Layout (Current)

```
regsim/
  cli.py
  commands/
    simulate.py
  core/
    evaluator.py
    fields.py
    simulation.py
    validators.py
  schemas/
```

The CLI stays thin, while core rule evaluation lives under `regsim/core/`.

---

## Rule Versioning & Regulatory Drift

RegSim-IN v1 supports **explicit rule versioning**:

* Rules declare:

  * `rule_version`
  * `effective_from`
  * `source_reference`
* No rule updates happen implicitly
* Simulations are always tied to a known regulatory snapshot

This ensures:

* Reproducibility
* Reviewability
* Trust

---

## CI/CD Usage Example

```bash
regsim-in simulate --rules rules.json --input payload.json || exit 1
```

A failing rule causes a non-zero exit code.

---

## Roadmap (Explicit, Not Promised)

Planned future directions include:

* Regulatory failure memory & correlation
* Safer rule authoring workflows
* Async system modeling hooks
* Community-contributed rule sets

These are **not part of v1**.

---

## Philosophy

* Simulation over certification
* Explicit rules over implicit assumptions
* Deterministic behavior over magic
* Memory over repetition

---

## Disclaimer 

RegSim-IN is a **developer simulation tool**.
It does **not** guarantee legal or regulatory compliance.

Always consult qualified professionals for real-world compliance decisions
