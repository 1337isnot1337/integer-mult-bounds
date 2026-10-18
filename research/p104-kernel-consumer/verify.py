#!/usr/bin/env python3
"""Authenticate, compare and replay the bounded P104 consumer audit.

Clear1nsight, with substantial OpenAI assistance. Apache-2.0.
Normal replay reads its receipt and never regenerates source or output files.
"""

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys
from types import ModuleType


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]
OWN = ("primary.py", "literal.py", "observable.py", "verify.py", "PROOF.md", "COSTS.md")
PREDECESSORS = {
    "source": "research/p104-stagewise-entrance/source.py",
    "classifier": "research/p104-stagewise-entrance/classifier.py",
    "admission": "research/p104-stagewise-entrance/admission.py",
    "model": "research/p104-stagewise-entrance/inputs/pr3382_model.py",
}
WORD = "research/p104-rounded-collector/inputs/WORD.json"
NATIVE = "research/p104-rounded-collector/inputs/NATIVE.json.gz"
COMPLETION = "research/p104-omitted-completion/CERTIFICATE.json"
ADAPTERS = "research/p104-omitted-frame-adapters/ADAPTERS.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def strict_json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key " + key)
            result[key] = value
        return result

    def invalid(value):
        raise ValueError("noninteger JSON token " + value)

    return json.loads(data, object_pairs_hook=pairs, parse_float=invalid, parse_constant=invalid)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def same(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(same(left[k], right[k]) for k in left)
    if isinstance(left, (list, tuple)):
        return len(left) == len(right) and all(same(a, b) for a, b in zip(left, right))
    return left == right


def read_regular(path):
    require(not any(part.is_symlink() for part in (path, *path.parents)),
            "symbolic link in source path " + str(path))
    require(path.is_file(), "regular source missing " + str(path))
    with path.open("rb") as stream:
        data = stream.read(32 * 1024 * 1024 + 1)
    require(len(data) <= 32 * 1024 * 1024, "source size limit")
    return data


def module(data, path, name):
    value = ModuleType(name)
    value.__file__ = str(path)
    exec(compile(data, str(path), "exec"), value.__dict__)
    return value


def capture():
    raw_manifest = read_regular(PACKAGE / "SOURCES.json")
    manifest = strict_json(raw_manifest)
    require(type(manifest.get("schema_version")) is int and manifest["schema_version"] == 1,
            "source manifest schema")
    raw = {}
    for row in manifest["files"]:
        if row["usage"] != "input":
            continue
        name = row["path"]
        require(type(name) is str and not name.startswith("/")
                and all(part not in ("", ".", "..") for part in name.split("/")), "canonical input path")
        require(name not in raw, "duplicate input")
        data = read_regular(ROOT / name)
        require(sha(data) == row["sha256"], "source manifest mismatch " + name)
        raw[name] = data
    require(all(name in raw for name in (*PREDECESSORS.values(), WORD, NATIVE, COMPLETION, ADAPTERS)),
            "all executable scientific inputs declared")
    own = {name: read_regular(PACKAGE / name) for name in OWN}
    return raw_manifest, raw, own


def compare_arrays(primary, literal):
    require(primary["p"] == literal["arrays"]["derived_p"], "full independently prepared p")
    unscaled = literal["receipt"]["unscaled"]
    failure = unscaled["first_literal_failure"]
    require(unscaled["status"] == "EXACT_LITERAL_FAILURE"
            and unscaled["counts"]["events_completed"] == 1099
            and unscaled["first_completed_event_outside_B9"] is None, "exact first-failure boundary")
    expected = {"kind": "nonintegral_fractional_addend", "event": 1099,
                "source": "Y90", "target": "D1", "address": 10,
                "component": "real", "coefficient": "1/4", "exact_increment": "-1/2"}
    require(type(failure) is dict and all(same(failure.get(k), v) for k, v in expected.items()),
            "specific unscaled admission counterexample")
    require(same(failure["source_value"], (-2, 0)) and failure["actual_word_event"] ==
            ["add", "D1", "Y90", "1/4", [381, 241, 2]], "actual failed physical read")
    strong = literal["arrays"]["strong"]
    require(primary["expected_checkpoints"] == strong["checkpoints"],
            "all complete Q0/G0/X0 arrays against separate scalar/chart oracle")
    require(primary["expected_final_Y"]["Y90"] == strong["final_Y90"]
            and primary["expected_final_Y"]["Y91"] == strong["final_Y91"],
            "both returned physical Y arrays")
    require(strong["final_Q0"] == [(0, 0)] * 512, "final Q0 zero")
    require(strong["final_X0"] == primary["expected_checkpoints"]["5397"]["X0"]["values"]
            and any(z != (0, 0) for z in strong["final_X0"]), "physical -2 A_F p endpoint")
    expected_nonzero = sorted(primary["receipt"]["symbolic"]["final_nonzero_coefficients"])
    x_nonzero = set(expected_nonzero) - {"Y90", "Y91"}
    require({"Y90", "Y91"} <= set(expected_nonzero) and len(x_nonzero) == 52
            and all(bank.startswith("X") and bank[1:].isdigit() for bank in x_nonzero),
            "symbolic endpoint support is exactly52 X banks and two Y banks")
    require(sorted(literal["receipt"]["strong"]["nonzero_final_banks"]) == expected_nonzero,
            "literal endpoint support equals the complete symbolic bank list")
    return {"full_p_coordinates": 512, "strong_checkpoint_banks": 18,
            "strong_checkpoint_Gaussian_coordinates": 9216,
            "returned_Y_Gaussian_coordinates": 1024,
            "comparison": "Complete arrays and frames compared before hashes, not hashes alone.",
            "original_failure_checked": expected, "final_query_restored": True,
            "final_required_X0_nonzero": True}


def calculate():
    manifest, raw, own = capture()
    modules = {name: module(raw[path], ROOT / path, "p104_retained_" + name)
               for name, path in PREDECESSORS.items()}
    executable = {name: module(own[name + ".py"], PACKAGE / (name + ".py"), "p104_consumer_" + name)
                  for name in ("primary", "literal", "observable")}
    word = strict_json(raw[WORD])
    native = strict_json(gzip.decompress(raw[NATIVE]))
    primary = executable["primary"].analyze(word, native, modules)
    literal = executable["literal"].run_literal(word, native, primary["p"])
    observable = executable["observable"].analyze(raw[WORD], raw[COMPLETION], raw[ADAPTERS])
    comparisons = compare_arrays(primary, literal)
    require(observable["completion"]["X0_pair_coefficient"] == [-1, 2]
            and observable["rho5_pair_response"] == [[0, 1]] * 5,
            "independent reverse row and five-readout oracle")
    require(not same({"schema_version": 1}, {"schema_version": True}), "typed receipt control")
    for path, original in raw.items():
        require(read_regular(ROOT / path) == original, "input changed during replay " + path)
    for path, original in own.items():
        require(read_regular(PACKAGE / path) == original, "implementation changed during replay " + path)
    require(read_regular(PACKAGE / "SOURCES.json") == manifest, "manifest changed during replay")
    receipt = {"schema_version": 1, "status": "PASS_P104_KERNEL_CONSUMER",
               "SOURCES_sha256": sha(manifest), "input_sha256": {p: sha(b) for p, b in raw.items()},
               "implementation_and_proof_sha256": {p: sha(b) for p, b in own.items()},
               "primary": primary["receipt"], "literal": literal["receipt"],
               "observable": observable, "full_array_comparison": comparisons,
               "typed_receipt_control": "Boolean true is distinct from integer1",
               "scope": "A source-bound consumer/caller audit with two finite fixtures and a written all-B9 paired-family implication. No paid caller, supplier, enlarged-domain advantage or kappa claim."}
    return strict_json(canonical(receipt))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-receipt", action="store_true",
                        help="explicitly regenerate this package's owned RECEIPT.json")
    args = parser.parse_args()
    result = calculate()
    path = PACKAGE / "RECEIPT.json"
    if args.write_receipt:
        require(not path.is_symlink(), "receipt output must not be a link")
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        expected = strict_json(read_regular(path))
        require(same(result, expected), "typed deterministic receipt mismatch")
    print("PASS_P104_KERNEL_CONSUMER receipt=" + sha(read_regular(path))
          + " p=" + result["primary"]["coefficient_column"]["p_sha256"])


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print("FAIL_P104_KERNEL_CONSUMER: " + str(error), file=sys.stderr)
        raise SystemExit(1) from error
