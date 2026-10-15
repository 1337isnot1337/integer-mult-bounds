"""Replay distinct executable boundaries of the fixed-role caller argument."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import loader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", choices=("frame", "continuation", "nested"), required=True)
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    loader.activate()
    if args.suite == "frame":
        import frame_checks
        result = frame_checks.run()
    elif args.suite == "continuation":
        import continuation_checks as checks
        result = dict(cursor=checks.cursor_checks(), roles=checks.nested_roles(),
                      transfer=checks.transfer_checks())
    else:
        import nested_bank_checks
        result = nested_bank_checks.run()
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    receipt = sha256(encoded).hexdigest()
    if not args.emit:
        expected = json.loads((HERE / "RESULT.json").read_text())[args.suite]["sha256"]
        if receipt != expected:
            raise ValueError("complete suite receipt differs: " + args.suite + ": " + receipt)
        print("PASS_SELECTED_BIT_PHYSICAL_CALLER_" + args.suite.upper())
    print(json.dumps(dict(suite=args.suite, sha256=receipt, result=result), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
