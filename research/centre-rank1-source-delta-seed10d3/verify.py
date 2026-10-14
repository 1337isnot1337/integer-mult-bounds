#!/usr/bin/env python3
"""Exhaust the two-panel rank-one source-delta identity on arbitrary dirt."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SELECTED_SHA256 = "10b9e340fd8e354a37a0c4813c90e5de1dd42044b5f6aca4a3fc5a42b685fa32"
COMPLEX_A = Fraction(67018507072324140917, 40000000000000000000000)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL_SOURCE_DELTA_FANOUT: {message}")


def linear_apply(rows: tuple[int, ...], x: int) -> int:
    """Apply a binary matrix whose row masks encode output dot products."""
    y = 0
    for i, row in enumerate(rows):
        y |= ((row & x).bit_count() & 1) << i
    return y


def matrix_rank(rows: tuple[int, ...], n: int) -> int:
    basis: dict[int, int] = {}
    for value in rows:
        x = value
        while x:
            pivot = x.bit_length() - 1
            if pivot in basis:
                x ^= basis[pivot]
            else:
                basis[pivot] = x
                break
    return len(basis)


def schedule(
    rows: tuple[int, ...],
    direction: int,
    *,
    candidate: bool,
    correction_mask: int | None = None,
    correction_control: int = 3,
) -> list[tuple[int, int]]:
    """Emit a literal CNOT schedule; registers 10 and 11 are dirty scratch."""
    gates: list[tuple[int, int]] = []
    scratch = 10
    alpha_register = correction_control
    y0_base, y1_base = 4, 7

    def accumulate_to_scratch(controls: list[int]) -> None:
        for control in controls:
            gates.append((control, scratch))

    def uncompute_scratch(controls: list[int]) -> None:
        for control in reversed(controls):
            gates.append((control, scratch))

    for j, row in enumerate(rows):
        x_controls = [i for i in range(3) if (row >> i) & 1]
        direction_coefficient = (row & direction).bit_count() & 1
        correction = direction_coefficient if correction_mask is None else ((correction_mask >> j) & 1)

        if candidate:
            accumulate_to_scratch(x_controls)
            gates.append((scratch, y0_base + j))
            gates.append((scratch, y1_base + j))
            if correction:
                gates.append((alpha_register, y1_base + j))
            uncompute_scratch(x_controls)
            # Remove the arbitrary entry value of the dirty scratch bit.
            gates.append((scratch, y0_base + j))
            gates.append((scratch, y1_base + j))
        else:
            accumulate_to_scratch(x_controls)
            gates.append((scratch, y0_base + j))
            uncompute_scratch(x_controls)
            gates.append((scratch, y0_base + j))

            second_controls = x_controls + ([alpha_register] if direction_coefficient else [])
            accumulate_to_scratch(second_controls)
            gates.append((scratch, y1_base + j))
            uncompute_scratch(second_controls)
            gates.append((scratch, y1_base + j))
    return gates


def run_gates(gates: list[tuple[int, int]], state: int) -> int:
    for control, target in gates:
        if (state >> control) & 1:
            state ^= 1 << target
    return state


def expected(rows: tuple[int, ...], direction: int, state: int) -> int:
    x = state & 0b111
    alpha = (state >> 3) & 1
    y0 = (state >> 4) & 0b111
    y1 = (state >> 7) & 0b111
    common = linear_apply(rows, x)
    correction = linear_apply(rows, direction) if alpha else 0
    expected_state = state & ~(((1 << 3) - 1) << 4) & ~(((1 << 3) - 1) << 7)
    expected_state |= (y0 ^ common) << 4
    expected_state |= (y1 ^ common ^ correction) << 7
    return expected_state


def provenance() -> None:
    record = ROOT / "certificates/selected-result.json"
    digest = hashlib.sha256(record.read_bytes()).hexdigest()
    require(digest == SELECTED_SHA256, "selected-record pin changed")
    selected = json.loads(record.read_text())
    require(selected.get("review") == "docs/research/community-batch1099-review.md", "review pointer changed")
    require(selected.get("certificate") == "research/community-frontier1094-audit/ASSEMBLY.json", "certificate pointer changed")
    require(selected.get("reproduce") == "make frontier1094-verify", "reproduction pointer changed")


def main() -> None:
    provenance()

    # A nontrivial full-rank 3x3 map. v=e0, so Lv is its first column.
    rows = (0b011, 0b110, 0b111)
    n = m = 3
    v = 0b001
    require(matrix_rank(rows, n) == n, "positive map is not invertible")
    lv = linear_apply(rows, v)
    require(lv == 0b101, "wrong exact correction column")

    baseline = schedule(rows, v, candidate=False)
    candidate = schedule(rows, v, candidate=True)
    checked = 0
    for state in range(1 << 12):
        want = expected(rows, v, state)
        require(run_gates(baseline, state) == want, "separate baseline circuit is incorrect")
        require(run_gates(candidate, state) == want, "fused candidate differs on dirty input")
        checked += 1
    require(checked == 4096, "unexpected exhaustive coverage")
    require(len(baseline) == 44 and len(candidate) == 28, "literal CNOT invoice changed")

    # Meaningful negative controls: each faulty circuit has a concrete witness.
    witness = (1 << 3)  # x=0, alpha=1, y0=y1=t=q=0
    want = expected(rows, v, witness)
    omitted = schedule(rows, v, candidate=True, correction_mask=0)
    require(run_gates(omitted, witness) != want, "omitted-correction control was not rejected")
    stale = schedule(rows, v, candidate=True, correction_control=11)
    require(run_gates(stale, witness) != want, "stale-alpha control was not rejected")
    wrong_column = schedule(rows, v, candidate=True, correction_mask=lv ^ 1)
    require(run_gates(wrong_column, witness) != want, "wrong-column control was not rejected")

    saving_mass = 8 ** (1 - float(COMPLEX_A)) - 1
    require(6.9 < saving_mass < 7.1, "planning screen outside expected enclosure")
    print(
        "PASS_SOURCE_DELTA_FANOUT "
        f"states={checked} baseline_cnot={len(baseline)} candidate_cnot={len(candidate)} controls=3 rank=3 source_delta_rank=1 "
        f"selected_complex_rank_mass_margin~{saving_mass:.12f}"
    )


if __name__ == "__main__":
    main()
