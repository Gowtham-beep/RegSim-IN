import argparse
import json
import sys
import regsim.engine as simulate

def main():
    parser = argparse.ArgumentParser(
        description="RegSim-IN - Regulatory Simulation CLI"
    )
    
    parser.add_argument(
        "simulate",
        nargs="?",
        help=" Run regulatory simulation",
    )
    
    parser.add_argument("--rules",required=True,help="Path to rules JSON")
    parser.add_argument("--input",required=True,help="Path to input JSON")
    
    args = parser.parse_args()
    
    try:
        with open(args.rules) as f:
            rules = json.load(f)
            
        with open(args.input) as f:
            payload = json.load(f)
            
        result = simulate(rules,payload)
        print(json.dumps(result,indent=2))
        
        if result["status"] == "FAIL":
            sys.exit(1)
            
    except Exception as e:
        print(json.dumps({
            "status":"ERROR",
            "message":str(e),
        }))
        sys.exit(2)