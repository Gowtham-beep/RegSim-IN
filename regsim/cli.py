# regsim/cli.py

import argparse
import json
import sys

from regsim.commands.simulate import run_simulation
from regsim.core.simulation import evaluate_rules, load_json
from regsim.engine import InvalidPayloadError
from regsim.parser import extract_from_file


def main():
    parser = argparse.ArgumentParser(prog="regsim-in")

    subparsers = parser.add_subparsers(dest="command", required=True)

    simulate_parser = subparsers.add_parser("simulate", help="Run regulatory simulation")
    simulate_parser.add_argument("--rules", required=True)
    simulate_parser.add_argument("--input", required=True)

    args = parser.parse_args()

    if args.command == "simulate":
        try:
            if args.input.endswith(".py"):
                extraction = extract_from_file(args.input)

                if extraction.errors:
                    print(json.dumps({
                        "status": "ERROR",
                        "errors": extraction.errors,
                    }))
                    sys.exit(2)

                rules = load_json(args.rules)
                all_results = []
                for payload in extraction.payloads:
                    all_results.append(evaluate_rules(rules, payload))

                print(json.dumps(all_results, indent=2))
                sys.exit(1 if any(r["status"] == "FAIL" for r in all_results) else 0)

            result = run_simulation(args.rules, args.input)
            print(json.dumps(result, indent=2))
        except InvalidPayloadError as e:
            print(json.dumps({
                "status": "ERROR",
                "violations": [],
                "metadata": {
                    "error": str(e)
                }
            }))
            sys.exit(1)
        except Exception as e:
            print(json.dumps({
                "status": "ERROR",
                "violations": [],
                "metadata": {
                    "error": str(e)
                }
            }))
            sys.exit(1)
