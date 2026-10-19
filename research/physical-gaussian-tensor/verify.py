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
    require(args.suite in ("moves", "router", "gather"), "declared tensor check")
    with opened():
        name = "tensor_check_" + args.suite
        module = importlib.import_module(name)
        require(Path(module.__file__).resolve() == Path(__file__).resolve().parent / (name + ".py"),
                "package-local tensor checker")
        print(json.dumps({"status": "PASS_PHYSICAL_GAUSSIAN_TENSOR", "suite": args.suite,
                          "evidence": module.run()}, sort_keys=True))


if __name__ == "__main__":
    main()
