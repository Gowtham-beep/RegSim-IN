# regsim/cli.py

import argparse
import json
import sys

from regsim.commands.simulate import run_simulation
from regsim.engine import InvalidPayloadError


def main():
    parser = argparse.ArgumentParser(prog="regsim-in")

    subparsers = parser.add_subparsers(dest="command", required=True)

    simulate_parser = subparsers.add_parser("simulate", help="Run regulatory simulation")
    simulate_parser.add_argument("--rules", required=True)
    simulate_parser.add_argument("--input", required=True)

    args = parser.parse_args()

    if args.command == "simulate":
        try:
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
