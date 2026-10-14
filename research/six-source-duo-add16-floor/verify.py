#!/usr/bin/env python3
"""Rebuild both complete six-source censuses, then audit all hidden boundaries.

Requires Python 3.12 and a C++17 compiler (g++ or clang++). No downloads, network,
Git calls, producer imports, or writes to the package during default replay.
Tairitsu-Aya, substantial OpenAI Codex assistance. Apache-2.0.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def authenticate():
    sources = json.loads((PACKAGE / "SOURCES.json").read_text(encoding="utf-8"))
    for entry in sources["files"]:
        if entry["usage"] == "input":
            raw = (ROOT / entry["path"]).read_bytes()
            require(hashlib.sha256(raw).hexdigest() == entry["sha256"], "source SHA256: " + entry["path"])


def execute(args, timeout=120):
    proc = subprocess.run(list(map(str, args)), cwd=PACKAGE, capture_output=True,
                          text=True, encoding="utf-8", timeout=timeout)
    require(proc.returncode == 0, "command failed: " + str(args[0]) + "\n" + proc.stdout + proc.stderr)
    lines = proc.stdout.strip().splitlines()
    require(lines, "missing native receipt")
    result = json.loads(lines[-1])
    require(result.get("status") == "EXHAUSTED", "incomplete native census cannot certify absence")
    return result


def audit_module():
    spec = importlib.util.spec_from_file_location("duo_add16_literal_audit", PACKAGE / "audit.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run():
    authenticate()
    compiler = shutil.which(os.environ.get("CXX", "c++"))
    require(compiler is not None, "A C++17 compiler is required: set CXX to the g++ or clang++ executable. audit.py alone does not rebuild the complete census.")
    old = json.loads((ROOT / "research/universal-connector-six-source/EXPECTED.json").read_bytes())
    expected_controls = {(row["sources"], row["length"]): row for row in old["censuses"]}
    module = audit_module()
    saved_table = (PACKAGE / "FULL-COVERS.bin").read_bytes()
    with tempfile.TemporaryDirectory(prefix="duo-add16-") as directory:
        temp = Path(directory).resolve()
        require(temp.is_relative_to(Path(tempfile.gettempdir()).resolve()), "isolated temporary build root")
        binaries = []
        for filename in ("enumerate_rgs.cpp", "enumerate_partitions.cpp"):
            target = temp / (filename[:-4] + (".exe" if os.name == "nt" else ""))
            compiled = subprocess.run([compiler, "-std=c++17", "-O3", "-Wall", "-Wextra", "-Werror",
                                       "-Wpedantic", str(PACKAGE / filename), "-o", str(target)],
                                      capture_output=True, text=True, encoding="utf-8", timeout=60)
            require(compiled.returncode == 0, "C++17 compilation failed:\n" + compiled.stdout + compiled.stderr)
            binaries.append(target)
        records = []
        for n, width, target_calls in ((5, 10, 10), (6, 12, 12), (6, 14, 14), (6, 16, 13)):
            first = temp / f"rgs-{n}-{width}.bin"
            second = temp / f"partitions-{n}-{width}.bin"
            mode = "search" if width == 16 else "unit"
            a = execute([binaries[0], n, width, target_calls, 0, 1, 120, mode, first])
            b = execute([binaries[1], n, width, second])
            keys = ("n", "unit_steps", "unit_words", "full_coverage_unit_words", "max_unit_coverage",
                    "profile_max_four", "profile_max_six")
            require(all(a[key] == b[key] for key in keys), "independent census counts disagree")
            table = first.read_bytes()
            require(table == second.read_bytes(), "independent full-cover word tables disagree")
            record = {key: a[key] for key in keys}
            record["full_cover_table_sha256"] = hashlib.sha256(table).hexdigest()
            if width < 16:
                reference = expected_controls[n, width]
                require(a["unit_words"] == reference["words"] and a["max_unit_coverage"] == reference["max_coverage"],
                        "predecessor census control")
            else:
                six = math.factorial(16) // (math.factorial(6) * 2**5 * math.factorial(5))
                four = math.factorial(16) // (math.factorial(4)**2 * 2**4 * math.factorial(2) * math.factorial(4))
                require(a["profile_max_six"] == six and a["profile_max_four"] == four,
                        "independent exact even-partition cardinalities")
                require(a["unit_words"] == six + four == 54864810, "complete 16-add domain")
                require(table == saved_table, "complete rebuild differs from the saved certificate")
                require(not a["witness_steps"] and a["max_screened_retained_coverage"] == 63,
                        "primary hidden-boundary exclusion")
                record["primary_individually_removable_triples_checked"] = a["tested_deletion_sets"]
                record["primary_retained_coverage_maximum"] = a["max_screened_retained_coverage"]
            records.append(record)
        # An incomplete but well-formed native receipt must not be accepted.
        interrupted = temp / "interrupted.bin"
        try:
            execute([binaries[0], 6, 16, 13, 0, 1, "0.000000001", "search", interrupted])
        except ValueError as error:
            require("incomplete native census" in str(error), "deadline control failed for the wrong reason")
        else:
            raise ValueError("deadline-truncated census was incorrectly accepted")
    duo = json.loads((ROOT / "research/duo-toggle-connector/CERTIFICATE.json").read_bytes())
    tiny = {}
    for n, walk in ((3, duo["n3"]["witness_walk"]), (4, duo["n4_side_row"]["witness_walk"]),
                    (5, duo["n5_witness"]["walk"])):
        stats = module.word_stats(walk, n)
        require(stats["coverage"] == 1 << n, "retained small DUO positive control")
        tiny[str(n)] = {key: stats[key] for key in ("calls", "adds", "coverage")}
    return {
        "schema_version": 1,
        "status": "PASS_SIX_SOURCE_DUO_ADD16_MINIMUM",
        "domain": "six read-only sources; singleton/DUO complete calls; one restored dirty connector; paired readouts",
        "censuses": records,
        "small_duo_positive_controls": tiny,
        "deadline_control_rejected": True,
        "audit": module.compute(saved_table),
        "conclusions": {
            "minimum_source_adds_for_universality": 16,
            "minimum_source_calls_with_at_most_16_adds": 14,
            "excluded_cells": [[12, 14], [12, 16], [13, 14], [13, 16]],
            "minimum_all_63_row_batch_adds": 142,
            "minimum_batch_queries_at_142_adds": 140,
            "higher_add_pareto_cells_settled": False,
            "physical_supplier_or_kappa_claim": False,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="write a complete receipt exclusively instead of comparing RESULT")
    args = parser.parse_args()
    result = run()
    if args.out:
        with args.out.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(result, indent=2) + "\n")
    else:
        require(result == json.loads((PACKAGE / "RESULT.json").read_text(encoding="utf-8")), "exact complete result receipt")
    print("PASS_SIX_SOURCE_DUO_ADD16_MINIMUM: 54864810 unit words, 7480 covers, 251 orbits; k_min=14 at W<=16")
    print("Both complete native enumerations, unpruned orbit deletions, full dirty columns and controls passed.")


if __name__ == "__main__":
    main()
