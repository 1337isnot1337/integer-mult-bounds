# SPDX-License-Identifier: Apache-2.0
"""PR3605 staged helpers 644/660: emitted native residual binding and separate-kernel check."""

import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import native
from common import HELPERS, PACKAGE, authenticate, decode, require


def compute():
    blobs = authenticate()
    with tempfile.TemporaryDirectory(prefix="staged-pair-native-") as work:
        record = native.audit(blobs, Path(work))
    result = {"schema_version": 1, "status": "PASS_STAGED_644_660_NATIVE_BINDING",
              "native": record}
    for tag, row in record["providers"].items():
        widths = [row["residuals"][row["bindings"][str(h)]["forward"]["recipe_key"]]["rank"]
                  for h in HELPERS]
        require(widths == [7, 7], "emitted residual widths 7/7: " + tag)
        require(row["parent_residual"]["rank"] == 8, "parent residual width 8: " + tag)
        require(row["changed_helpers"] == list(HELPERS), "single-change control: " + tag)
        require(len(row["controls"]) == 7, "seven residual controls: " + tag)
        for h in HELPERS:
            ranks = [c["rank"] for c in row["bindings"][str(h)]["forward"]["climbs"]]
            parent = row["parent_bindings"][str(h)]["climb_ranks"]
            require(sum(ranks) == 7 and sum(parent) == 8 and ranks[1:] == parent[1:] and
                    ranks[0] + 1 == parent[0], "only the first native climb changes: " + tag)
    require(authenticate() == blobs, "source stability during replay")
    return decode(json.dumps(result).encode())


def main():
    require(sys.argv[1:] in ([], ["--emit"]), "usage: verify.py [--emit]")
    result = compute()
    if sys.argv[1:]:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        require(decode((PACKAGE / "RESULT.json").read_bytes()) == result, "deterministic receipt")
        base = result["native"]["providers"]["base"]
        key = base["bindings"]["644"]["forward"]["recipe_key"]
        print(result["status"]
              + " providers=2 helpers=644,660 entrance=span(429,30) terminal=FULL"
              + f" residual_width=7 parent_width=8 shared_key={key}"
              + f" climb_recipes={len(result['native']['climb_recipes'])}"
              + " controls=7x2 single_change=2 both_orientations no_new_kappa")


if __name__ == "__main__":
    main()
