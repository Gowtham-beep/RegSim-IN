# regsim/cli.py

import argparse
import json
import os
import sys

from regsim.commands.simulate import run_simulation
from regsim.core.simulation import load_json, simulate
from regsim.engine import InvalidPayloadError
from regsim.parser import extract_from_file


def main():
    parser = argparse.ArgumentParser(prog="regsim-in")

    subparsers = parser.add_subparsers(dest="command", required=True)

    simulate_parser = subparsers.add_parser("simulate", help="Run regulatory simulation")
    simulate_parser.add_argument("--rules", required=True)
    simulate_parser.add_argument("--input", required=True)
    simulate_parser.add_argument(
        "--snapshot-date",
        help="Regulatory snapshot date (YYYY-MM-DD)",
        required=False,
    )

    args = parser.parse_args()

    if args.command == "simulate":
        try:
            rules = load_json(args.rules)

            if os.path.isdir(args.input):
                all_results = []
                extraction_errors = []

                for root, dirs, files in os.walk(args.input):
                    dirs.sort()
                    for filename in sorted(files):
                        if not filename.endswith(".py"):
                            continue
                        file_path = os.path.join(root, filename)
                        extraction = extract_from_file(file_path)
                        if extraction.errors:
                            extraction_errors.extend(extraction.errors)
                            continue
                        for payload in extraction.payloads:
                            all_results.append(
                                simulate(rules, payload, snapshot_date=args.snapshot_date)
                            )

                if extraction_errors:
                    print(json.dumps({
                        "status": "ERROR",
                        "errors": extraction_errors,
                    }))
                    sys.exit(2)

                print(json.dumps(all_results, indent=2))
                sys.exit(1 if any(r["status"] == "FAIL" for r in all_results) else 0)

            if args.input.endswith(".py"):
                extraction = extract_from_file(args.input)

                if extraction.errors:
                    print(json.dumps({
                        "status": "ERROR",
                        "errors": extraction.errors,
                    }))
                    sys.exit(2)

                all_results = []
                for payload in extraction.payloads:
                    all_results.append(
                        simulate(rules, payload, snapshot_date=args.snapshot_date)
                    )

                print(json.dumps(all_results, indent=2))
                sys.exit(1 if any(r["status"] == "FAIL" for r in all_results) else 0)

            payload = load_json(args.input)
            result = simulate(rules, payload, snapshot_date=args.snapshot_date)
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
