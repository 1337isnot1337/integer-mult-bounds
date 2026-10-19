"""Cold entry point for complete physical Gaussian tensor checks."""
import argparse
import importlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tensor_sources import opened, require


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", required=True)
    args = parser.parse_args()
    require(args.suite in ("moves", "router", "gather", "windows", "plan", "word", "catalogue", "twiddles", "counts", "full", "full_opposite", "consumer", "consumer_opposite"), "declared tensor check")
    with opened():
        name = "tensor_check_" + ("full" if args.suite in ("full_opposite", "consumer", "consumer_opposite") else args.suite)
        module = importlib.import_module(name)
        require(Path(module.__file__).resolve() == Path(__file__).resolve().parent / (name + ".py"),
                "package-local tensor checker")
        if args.suite in ("consumer", "consumer_opposite"):
            from tensor_fixture import prepared_catalogue
            evidence = module.run(opposite=args.suite == "consumer_opposite", prepared=prepared_catalogue())
        else:
            evidence = module.run(opposite=True) if args.suite == "full_opposite" else module.run()
        print(json.dumps({"status": "PASS_PHYSICAL_GAUSSIAN_TENSOR", "suite": args.suite,
                          "evidence": evidence}, sort_keys=True))


if __name__ == "__main__":
    main()
