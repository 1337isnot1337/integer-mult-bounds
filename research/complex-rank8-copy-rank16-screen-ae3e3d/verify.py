#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact zero-overhead ceiling screen for the rank-8 copy block."""
import hashlib
import importlib.util
import argparse
import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PACKAGE = HERE.relative_to(ROOT).as_posix()
CEILING_PATH = "research/complex-local-word-ceiling/ceiling.py"
CEILING_SHA256 = "86a1432870b3b21d8454106ec9162fddc0471472d9214c590a1420f2426cedfc"
BASE = "0fdd7d82de03e43c9e5a1000dfbcd380d1b687d2"
SELECTED_SHA256 = "10b9e340fd8e354a37a0c4813c90e5de1dd42044b5f6aca4a3fc5a42b685fa32"
CATALOGUE_SHA256 = "d46eb6d5b3e279428753d770653663fbdf1063e55c255ea073d768f344927ef7"
GRID = Fraction(1, 10**12)
THRESHOLD = Fraction(1, 20)
WORD = {1: 2412, 2: 418, 3: 432, 4: 142, 5: 82, 8: 8}
M, FAMILIES, STAGES, CENTRE, UNPAID = 73, 896, 9, 64, 1


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def load_engine():
    sources = json.loads((HERE / "SOURCES.json").read_text(encoding="utf-8"))
    pins = {row["path"]: row["sha256"] for row in sources["files"]}
    need(pins[CEILING_PATH] == CEILING_SHA256, "ceiling.py manifest pin mismatch")
    engine_path = ROOT / CEILING_PATH
    need(sha256(engine_path.read_bytes()) == CEILING_SHA256,
         "pinned ceiling engine SHA-256 mismatch")
    need(pins["certificates/selected-result.json"] == SELECTED_SHA256,
         "selected-record manifest pin mismatch")
    need(pins["docs/research/agent-task-catalog.json"] == CATALOGUE_SHA256,
         "task-catalogue manifest pin mismatch")
    spec = importlib.util.spec_from_file_location("rank_shape_ceiling", engine_path)
    need(spec is not None and spec.loader is not None, "cannot load pinned ceiling engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def cap(engine, profile, centre=CENTRE):
    return engine.ceiling(profile, M, FAMILIES, STAGES, centre,
                          grid=GRID, unpaid=UNPAID)


def mass(profile):
    return sum(Fraction(rank) * Fraction(count)
               for rank, count in profile.items())


def ratio_interval(candidate, baseline):
    return (candidate[0] / baseline[1] - 1,
            candidate[1] / baseline[0] - 1)


def as_pair(interval):
    return [str(interval[0]), str(interval[1])]


def encode_profile(profile):
    return {str(rank): (count if isinstance(count, int) else str(count))
            for rank, count in sorted(profile.items())}


def build_report():
    engine = load_engine()
    baseline = cap(engine, WORD)
    need(baseline == (Fraction(1690054109, 10**12),
                      Fraction(169005411, 10**11)),
         "selected baseline ceiling bracket changed")
    need(mass(WORD) == 5586, "selected local profile mass changed")

    candidate = dict(WORD)
    del candidate[8]
    candidate[16] = 4
    need(mass(candidate) == mass(WORD), "rank-8/rank-16 replacement changed paid mass")
    candidate_cap = cap(engine, candidate)
    need(candidate_cap == (Fraction(1693625547, 10**12),
                           Fraction(423406387, 250_000_000_000)),
         "candidate ceiling bracket changed")
    gain = ratio_interval(candidate_cap, baseline)
    need(gain == (Fraction(1190479, 563351370),
                  Fraction(3571439, 1_690_054_109)),
         "relative-gain interval changed")
    need(gain[1] < THRESHOLD,
         "zero-overhead rank-8 copy regrouping unexpectedly clears the 5% gate")

    # Positive budget control: the all-mass rank-16 relaxation is known to
    # clear the threshold, but is not a decoder construction.
    all_rank16 = {16: Fraction(mass(WORD), 16)}
    ideal_cap = cap(engine, all_rank16)
    ideal_gain = ratio_interval(ideal_cap, baseline)
    need(ideal_gain[0] > THRESHOLD,
         "all-mass rank-16 sensitivity control no longer clears the 5% gate")

    # Negative accounting control: append four rank-16 children without
    # removing the eight source children. This overcharges by 64 mass.
    overcharged = dict(WORD)
    overcharged[16] = 4
    overcharged_cap = cap(engine, overcharged)
    need(mass(overcharged) == 5650, "overcharge control mass")
    need(overcharged_cap[1] < candidate_cap[0],
         "extra paid rank mass failed to lower the relaxed ceiling")

    rank1_ideal = {1: 12, 2: 418, 3: 432, 4: 142, 5: 82, 8: 8, 16: 150}
    need(mass(rank1_ideal) == mass(WORD), "rank-1 sensitivity mass")
    rank1_cap = cap(engine, rank1_ideal)

    return {
        "schema_version": 1,
        "kind": "scoped zero-overhead rank-shape screen",
        "base_commit": BASE,
        "selected_record_sha256": SELECTED_SHA256,
        "catalogue_sha256": CATALOGUE_SHA256,
        "ceiling_engine_path": CEILING_PATH,
        "ceiling_engine_sha256": CEILING_SHA256,
        "model": {
            "ports": M, "families": FAMILIES, "stages": STAGES,
            "centre_charge": CENTRE, "unpaid_coordinates_per_family": UNPAID,
            "grid": str(GRID), "target_relative_gain": str(THRESHOLD),
        },
        "baseline": {
            "profile": encode_profile(WORD),
            "paid_mass": str(mass(WORD)),
            "ceiling_bracket": as_pair(baseline),
        },
        "candidate": {
            "hypothesis": "replace all eight rank-8 private-temporary copy children by four rank-16 block children",
            "profile": encode_profile(candidate),
            "paid_mass": str(mass(candidate)),
            "moved_mass": 64,
            "added_gather_copy_frame_restore_host_precision_cost": 0,
            "ceiling_bracket": as_pair(candidate_cap),
            "relative_gain_interval": as_pair(gain),
            "clears_five_percent_gate": False,
            "interpretation": "Even the zero-overhead relaxation is below the task gate; no block identity was synthesized.",
        },
        "controls": {
            "all_mass_rank16_ideal_only": {
                "profile": encode_profile(all_rank16),
                "ceiling_bracket": as_pair(ideal_cap),
                "relative_gain_interval": as_pair(ideal_gain),
                "clears_five_percent_gate": True,
                "is_construction": False,
            },
            "rank1_mass_rank16_sensitivity_only": {
                "profile": encode_profile(rank1_ideal),
                "ceiling_bracket": as_pair(rank1_cap),
                "relative_gain_interval": as_pair(ratio_interval(rank1_cap, baseline)),
                "is_construction": False,
            },
            "append_without_removing_control": {
                "profile": encode_profile(overcharged),
                "paid_mass": str(mass(overcharged)),
                "ceiling_bracket": as_pair(overcharged_cap),
                "rejected_as_undercharged_candidate": True,
            },
        },
        "scope_limit": "Only regrouping the eight existing rank-8 children; rank-1 through rank-5 changes, actual decoder identity, altered coverage, and full supplier assembly are not covered.",
        "claim_status": "No advance claim posted; finding is reported after the exact first-step budget screen.",
        "no_new_kappa": True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    path = HERE / "CERTIFICATE.json"
    payload = json.dumps(build_report(), indent=2, sort_keys=True) + "\n"
    if args.write_certificate:
        path.write_text(payload, encoding="utf-8")
    else:
        need(path.is_file(), "missing CERTIFICATE.json")
        need(path.read_text(encoding="utf-8") == payload,
             "certificate differs from deterministic exact replay")
    print("PASS_COMPLEX_RANK8_COPY_RANK16_SCREEN moved_mass=64 paid_mass=5586 "
          "gain_upper=0.002113210 below_5pct=1 ideal_control=1 no_new_kappa")


if __name__ == "__main__":
    main()
