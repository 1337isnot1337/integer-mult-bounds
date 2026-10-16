#!/usr/bin/env python3
"""Exact target-scale screen for the selected complex local word.

At kappa = 1/10 the retained planning transfer requires primitive saving
a = 1/9.  This checker lower-bounds the local-word moment at that point using
integer ninth-root inequalities only.  Any idle, hosting or centre charges
are nonnegative additions to this local bill.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = Path(__file__).resolve().parent
SCALE = 10**30
TARGET_A = Q(1, 9)
EXPECTED_WORD = {1: 2412, 2: 418, 3: 432, 4: 142, 5: 82, 8: 8}


def require(ok: bool, label: str) -> None:
    if not ok:
        raise ValueError(label)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ast_assignments(path: Path) -> dict[str, object]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: dict[str, object] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        value = ast.literal_eval(node.value)
        for target in node.targets:
            if isinstance(target, ast.Name):
                found[target.id] = value
            elif isinstance(target, ast.Tuple):
                names = [x.id for x in target.elts if isinstance(x, ast.Name)]
                if len(names) == len(target.elts) and isinstance(value, tuple):
                    found.update(zip(names, value))
    return found


def source_profile() -> tuple[int, int, int, dict[int, int]]:
    source = ROOT / "research/complex-local-word-ceiling/levers.py"
    values = ast_assignments(source)
    require((values.get("M"), values.get("FAM"), values.get("ST")) == (73, 896, 9),
            "selected local-word dimensions drifted")
    word = values.get("WORD")
    require(isinstance(word, dict), "selected local word is missing")
    word = {int(r): int(n) for r, n in word.items()}
    require(word == EXPECTED_WORD, "selected local profile differs from the audited source")
    return 73, 896, 9, word


def root_enclosure(rank: int, width: int) -> tuple[int, int, bool]:
    """Enclose (rank/width)^(8/9) in multiples of 1/SCALE.

    The comparison k/SCALE <= y is equivalent to
    k^9 * width^8 <= rank^8 * SCALE^9, so every step is integer arithmetic.
    """
    require(0 < rank < width, "rank must lie strictly inside the width")
    rhs = rank**8 * SCALE**9
    width_factor = width**8
    lo, hi = 0, SCALE
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid**9 * width_factor <= rhs:
            lo = mid
        else:
            hi = mid - 1
    exact = lo**9 * width_factor == rhs
    upper = lo if exact else lo + 1
    require(lo**9 * width_factor <= rhs, "root lower endpoint failed")
    require(upper**9 * width_factor >= rhs, "root upper endpoint failed")
    return lo, upper, exact


def local_bill_interval(word: dict[int, int], width: int, families: int, stages: int):
    per_call_families = Q(families, stages)
    lower = upper = Q(0)
    terms = []
    for rank, count in sorted(word.items()):
        lo, hi, exact = root_enclosure(rank, width)
        lower += count * Q(lo, SCALE)
        upper += count * Q(hi, SCALE)
        terms.append({
            "rank": rank,
            "count": count,
            "root_lower_numerator": str(lo),
            "root_upper_numerator": str(hi),
            "exact_root": exact,
        })
    return lower / per_call_families, upper / per_call_families, terms


def rank_mass_bill_interval(unpaid: int, centre: Q, width: int, families: int, stages: int, cap: int):
    """Most favorable moment for a fixed total rank mass and cap: put all at cap."""
    per_call_families = Q(families, stages)
    total_mass = (width - unpaid) * per_call_families + centre
    lo, hi, _ = root_enclosure(cap, width)
    lower = total_mass * Q(lo, SCALE) / (cap * per_call_families)
    upper = total_mass * Q(hi, SCALE) / (cap * per_call_families)
    return lower, upper


def result_record() -> dict[str, object]:
    selected_path = ROOT / "certificates/selected-result.json"
    assembly_path = ROOT / "research/community-frontier1094-audit/ASSEMBLY.json"
    word_path = ROOT / "research/complex-local-word-ceiling/levers.py"
    selected = read_json(selected_path)
    assembly = read_json(assembly_path)
    width, families, stages, word = source_profile()

    selected_kappa = str(selected["kappa"])
    require(selected_kappa == str(assembly["kappa"]), "selected record and assembly kappa differ")
    require(assembly["binding"] == "complex", "source assembly is no longer complex-bound")

    local_mass = sum(rank * count for rank, count in word.items())
    lower, upper, terms = local_bill_interval(word, width, families, stages)
    rank_cap = 51
    require(2 * rank_cap**2 < width**2 <= 2 * (rank_cap + 1) ** 2,
            "rank cap is no longer the largest rank allowed by the selected halving guard")
    # Positive control: at a=0 this local bill is exactly rank mass/(m W).
    zero_saving_bill = Q(local_mass * stages, width * families)
    require(zero_saving_bill < 1, "positive control at a=0 failed")
    require(lower > 1, "the selected local word does not exclude a=1/9")

    coverage_cases = []
    for label, unpaid, centre in (
        ("selected_coverage", 1, Q(64)),
        ("two_unpaid_centre_free", 2, Q(0)),
        ("three_unpaid_centre_free", 3, Q(0)),
        ("three_unpaid_selected_centre", 3, Q(64)),
        ("four_unpaid_selected_centre", 4, Q(64)),
    ):
        b_lo, b_hi = rank_mass_bill_interval(unpaid, centre, width, families, stages, rank_cap)
        coverage_cases.append({
            "label": label,
            "unpaid_coordinates": unpaid,
            "centre_mass": str(centre),
            "all_mass_at_rank_cap": rank_cap,
            "bill_lower": str(b_lo),
            "bill_upper": str(b_hi),
            "bill_upper_decimal": f"{float(b_hi):.15f}",
            "strictly_below_one": b_hi < 1,
        })
    case = {item["label"]: item for item in coverage_cases}
    require(Q(case["selected_coverage"]["bill_lower"]) > 1,
            "selected coverage does not fail even under ideal rank-cap repacking")
    require(Q(case["two_unpaid_centre_free"]["bill_lower"]) > 1,
            "two-unpaid centre-free necessity control failed")
    require(case["three_unpaid_centre_free"]["strictly_below_one"],
            "three-unpaid centre-free ideal positive control failed")
    require(Q(case["three_unpaid_selected_centre"]["bill_lower"]) > 1,
            "three-unpaid selected-centre necessity control failed")
    require(case["four_unpaid_selected_centre"]["strictly_below_one"],
            "four-unpaid selected-centre ideal positive control failed")

    # At a=1/9, kappa=a/(1+a)=1/10.  The retained outer transfer has strict
    # reservations, so any kappa>1/10 needs a primitive a>1/9.
    return {
        "status": "PASS_KAPPA01_SELECTED_COMPLEX_WORD_FLOOR",
        "scope": "fixed selected complex local word, width, family count and stage count; no idle credit",
        "target": {"kappa": "1/10", "primitive_saving": "1/9"},
        "selected": {
            "kappa": selected_kappa,
            "binding": assembly["binding"],
            "selected_record_sha256": sha256(selected_path),
            "assembly_sha256": sha256(assembly_path),
            "local_word_source_sha256": sha256(word_path),
        },
        "model": {
            "width": width,
            "live_families_per_replica": families,
            "stages": stages,
            "live_families_per_call": f"{families}/{stages}",
            "local_profile": {str(r): n for r, n in sorted(word.items())},
            "local_rank_mass": local_mass,
            "idle_mass_assumed": 0,
            "centre_charge_assumed": 0,
            "maximum_child_rank": rank_cap,
            "root_scale": str(SCALE),
        },
        "certificate": {
            "rank_terms": terms,
            "bill_lower": str(lower),
            "bill_upper": str(upper),
            "bill_lower_decimal": f"{float(lower):.15f}",
            "bill_upper_decimal": f"{float(upper):.15f}",
            "margin_lower": str(lower - 1),
            "positive_control_a_zero_bill": str(zero_saving_bill),
            "strict_rejection": lower > 1,
            "coverage_relaxations": coverage_cases,
            "necessary_unpaid_coordinates_at_target": {
                "with_centre_fully_removed": 3,
                "with_selected_centre_charge_64": 4,
                "scope": "uniform coverage law, fixed width 73, nine stages, and rank cap 51; idealized rank-mass distribution only",
            },
        },
        "interpretation": (
            "The local paid word alone costs more than one normalized unit at a=1/9. "
            "Separately, the selected coverage law fails even if all rank mass is "
            "ideally repacked at rank 51 and local work is free. Thus this word and "
            "this coverage law each need structural change; passing relaxed cases "
            "are budget thresholds, not constructions."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    args = parser.parse_args()
    record = result_record()
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    if args.write:
        args.write.write_text(rendered, encoding="utf-8")
    else:
        expected = read_json(PACKAGE / "RESULT.json")
        require(record == expected, "RESULT.json differs from exact replay")
    print("PASS_KAPPA01_SELECTED_COMPLEX_WORD_FLOOR bill_lower=" + record["certificate"]["bill_lower_decimal"])


if __name__ == "__main__":
    main()
