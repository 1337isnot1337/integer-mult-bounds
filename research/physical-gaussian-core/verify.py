"""Cold entry point for the physical Gaussian compression checks."""
import argparse
import importlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gaussian_sources import opened, require


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", required=True)
    args = parser.parse_args()
    require(args.suite in ("setup", "convolution", "exponentials", "interior", "axis", "boundary"),
            "registered Gaussian suite")
    with opened():
        name = "gaussian_check_" + args.suite
        module = importlib.import_module(name)
        require(Path(module.__file__).resolve() == Path(__file__).resolve().parent / (name + ".py"),
                "package-local Gaussian checker")
        result = module.run()
    print(json.dumps({"status": "PASS_PHYSICAL_GAUSSIAN_CORE", "suite": args.suite,
                      "evidence": result}, sort_keys=True))


if __name__ == "__main__":
    main()
