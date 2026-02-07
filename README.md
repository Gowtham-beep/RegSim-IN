# RegSim-IN 🇮🇳
**Regulatory Simulation & Failure Memory CLI for Indian Backend Systems**

PyPI package: `regsim-in` (`https://pypi.org/project/regsim-in/`)

## Why This Project Exists (Simple Explanation)

In India, when developers build fintech apps (like payment tools, invoicing systems, or lending platforms), they often discover **regulatory problems** (tax rules, RBI guidelines) **too late** — during audits, tax notices, or when something breaks in production.

These problems are usually:
- Predictable (the same mistake happens again and again)
- Repeated by many teams
- Very expensive or stressful when found late

RegSim-IN is a small command-line tool that helps developers **find these problems early** — while they are still writing code or testing locally — instead of waiting for a disaster.

It turns complicated government rules into simple, computer-checkable instructions.

## Who Should Use This Tool?

- Backend developers building anything related to money/payments in India  
- Founders or small teams creating early versions (prototypes/MVPs) of fintech products  
- Anyone who wants to avoid nasty surprises from TDS, GST, or RBI rules later

## What Is RegSim-IN? (One-Sentence Version)

**RegSim-IN** is a free command-line tool you install with `pip` that checks your code/data against Indian tax and RBI rules **before** you deploy anything to real users.

It acts like a very strict, very fast reviewer that only cares about regulations.

## The Real Problem It Solves (Plain English)

Most teams:
- Write code that looks correct  
- But forget or misunderstand some tax/RBI detail  
- Only find out when the tax department sends a notice, a payment fails, or an auditor flags it  
- Then waste weeks fixing it — and often make the **same mistake** again in another part of the app or another project

RegSim-IN helps you:
- Catch these mistakes **while you're still coding or testing**  
- See exactly **which rule** you broke and **why**  
- Stop repeating the same compliance mistakes

## What v1 Actually Does (Very Clear List)

Version 1 is simple and safe on purpose:

- You write rules in easy-to-read JSON files (like mini law statements)  
- You give it your sample data (also JSON)  
- It checks if your data follows the rules  
- It tells you **PASS** or **FAIL** — and explains exactly what went wrong  
- Everything is 100% predictable (same input = same result every time)  
- Works great in automated tests (CI/CD pipelines) — can stop a bad merge  
- Keeps a record of which rules were used and when (so you can prove "we checked on this date")

It **does not**:
- Talk to any government website
- File taxes for you
- Give legal advice
- Automatically know the latest law changes
- Check your entire running app (just data samples or code snippets)

## Real Example Everyone Can Understand

Imagine your app pays freelancers ₹45,000 but forgets to cut TDS (tax deducted at source).

**Your test data looks like this:**
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

**The tool checks against this simple rule:**
"If payment > ₹30,000 to a contractor → TDS must be deducted"

**Result from RegSim-IN:**
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

→ You fix it **before** sending real money.

## Installation (One Command)

```bash
pip install regsim-in
```

(You need Python installed — most developers already have it.)

## Quick Usage Examples

Check one file:
```bash
regsim-in simulate --rules my-rules-folder/ --input my-test-data.json
```

Check your whole source code folder:
```bash
regsim-in simulate --rules rules/ --input src/
```

In a GitHub Actions / CI pipeline (stops bad code):
```bash
regsim-in simulate --rules rules/ --input payload.json || exit 1
```

## CLI Options (Current v1)

- `regsim-in --version` prints the installed version.
- `regsim-in simulate --rules <path> --input <path>` runs a simulation.
- `--snapshot-date YYYY-MM-DD` attaches a regulatory snapshot date in output metadata (for audit trails).

## Important Safety Warnings (Please Read)

**RegSim-IN is NOT:**
- A replacement for a Chartered Accountant (CA)
- A way to file taxes or talk to the government
- Automatically up-to-date with every new RBI circular
- Giving you legal protection

It is only a **developer helper** to find obvious mistakes early.
For real money movement, always talk to qualified professionals.

**Official Disclaimer:**  
RegSim-IN is a developer simulation tool for engineering feedback only.  
It does **not** guarantee legal or regulatory compliance.  
Always consult qualified professionals for real-world decisions.

## Future Plans (Not Promises)

Later versions might add:
- Remembering past failures so you don't repeat them  
- Easier ways for people to share rules  
- Checking more complicated flows (queues, retries)

None of these are in v1. v1 is intentionally small and trustworthy.

## Core Beliefs Behind This Tool

- Simulation > pretending to be perfect  
- Clear rules > hidden assumptions  
- Predictable behavior > magic  
- Learning from mistakes > repeating them

---

Thank you for reading.

If you're a developer in India building anything fintech-related, try it and tell me what breaks (or doesn't).
Feedback → better tool.

Gowtham  
Bengaluru, 2026
