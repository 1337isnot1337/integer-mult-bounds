#!/usr/bin/env python3
"""Independent audit of one #2979 rank-7 group: V45.

Reconstructs the shared end frame of helpers 249, 251, 265 and 267 on both
PR2942 parent words, prices every subset against the published integer frame
surrogate, and checks the losing single-helper controls. This file does not
import research/rank7-joint-endframes/producer.py, verify.py, or
construction/STAGE-PRICES.json.

The frame profile is a separate transcription of the inherited climb rules
(Jeremy Kothe, PR #2894, as stated in that package's vendored preload_move.py):
monotone subspace climbs, warp resets, centre/target cuts, and a final climb
to each live end frame. Calibration is the parent's stored profile, which this
transcription recomputes before any edit is applied.
"""

from __future__ import annotations

import copy
import gzip
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "research" / "rank7-joint-endframes" / "data"

# Integer surrogate c_r = floor(2^40 * lo_r(b)) at the #2979 base saving.
# Not re-derived from the moment engines in this package. The break-even
# charge for one freed width unit is the published gap c_1 - 25371.
WEIGHTS = {
    1: 2116671,
    2: 4228346,
    3: 6338140,
    4: 8446713,
    5: 10554378,
    6: 12661320,
    7: 14767661,
    8: 16873488,
    9: 18978865,
}
PARTNER_ALLOWANCE = 25371
BREAK_EVEN = WEIGHTS[1] - PARTNER_ALLOWANCE
HELPERS = (249, 251, 265, 267)
NORMALS = (7, 42, 45)


def basis(vectors):
    pivot = {}
    for value in vectors:
        value = int(value)
        while value:
            bit = value.bit_length() - 1
            if bit in pivot:
                value ^= pivot[bit]
            else:
                pivot[bit] = value
                break
    for row in sorted(pivot):
        for other in list(pivot):
            if other > row and (pivot[other] >> row) & 1:
                pivot[other] ^= pivot[row]
    return tuple(pivot[row] for row in sorted(pivot, reverse=True))


def contained(small, big):
    return basis(list(big) + list(small)) == basis(list(big))


def orthogonal(normals):
    survivors = [
        vector
        for vector in range(512)
        if all((vector & normal).bit_count() % 2 == 0 for normal in normals)
    ]
    return basis(survivors)


def roles(gate):
    if gate[0] == "add":
        return gate[1:3]
    if gate[0] == "scale":
        return gate[1:2]
    raise ValueError("not a scalar gate")


def frame_report(word):
    full = basis(1 << i for i in range(9))
    ends = (
        [full] * 112
        + [
            basis(vector for vector in range(1, 512) if (vector & port).bit_count() % 2 == 0)
            for port in word["ports"]
        ]
        + [full] * 480
    )
    for register, frame in word["helper_final"].items():
        ends[int(register)] = basis(frame)
    current = [(port,) for port in word["ports"]] + [()] * (112 + 480)
    for register, frame in word["start_extra"].items():
        current[int(register)] = basis(frame)
    paid = Counter()

    def climb(register, frame):
        frame = basis(frame)
        if not contained(current[register], frame):
            raise ValueError("nonmonotone")
        rank_jump = len(frame) - len(current[register])
        if rank_jump:
            paid[rank_jump] += 1
        current[register] = frame

    def step(gate):
        if gate[0] == "warp":
            if current[gate[1]] != basis(gate[3]):
                raise ValueError("warp")
            current[gate[1]] = basis(gate[4])
            return
        for register in roles(gate):
            climb(register, gate[-1])

    for gate in word["A"]:
        step(gate)
    for register, frame in zip(word["centers"], word["center_frames"]):
        if current[register] != basis(frame):
            raise ValueError("centre")
        level = frame
        targets = sorted(
            {
                basis(word["target_levels"].get(str(gate[1] - 112), []))
                for gate in word["cut"]
                if gate[2] == register
            },
            key=len,
            reverse=True,
        )
        for target in targets:
            if basis(level) != target:
                paid[len(level) - len(target)] += 1
            level = target
    warps = {}
    for record in word["warps"]:
        warps.setdefault(record[0], []).append(record)
    for position in range(len(word["B"]) + 1):
        for record in warps.get(position, []):
            if current[record[1]] != basis(record[3]):
                raise ValueError("Bwarp")
            current[record[1]] = basis(record[4])
        if position < len(word["B"]):
            step(word["B"][position])
    for gate in word["restore"]:
        step(gate)
    live = set(range(704)) - set(word["removed"])
    for register in live:
        climb(register, ends[register])
    starts = [(port,) for port in word["ports"]] + [()] * (112 + 480)
    for register, frame in word["start_extra"].items():
        starts[int(register)] = basis(frame)
    inventory = Counter(
        len(ends[register]) - len(starts[register])
        for register in live
        if register >= 224
    )
    return (
        {str(rank): count for rank, count in sorted(paid.items())},
        {str(width): count for width, count in sorted(inventory.items())},
    )


def cost(profile):
    return sum(WEIGHTS[int(rank)] * count for rank, count in profile.items())


def group_owners(record, frame):
    return [
        name
        for name, payload in record["groups"].items()
        if contained(frame, payload[0])
    ]


def apply_v45(parent, record, edits, helpers):
    word = copy.deepcopy(parent)
    subspace = list(record["groups"]["V45"][0])
    for helper in helpers:
        change = record["helper_final_changes"][str(helper)]
        if change["old"] != word["helper_final"][str(helper)] or change["new"] != subspace:
            raise ValueError("end-frame preimage")
        word["helper_final"][str(helper)] = list(subspace)
    for edit in edits:
        gate = word[edit["section"]][edit["index"]]
        if gate[:-1] != edit["gate"] or gate[-1] != edit["old_frame"]:
            raise ValueError("gate preimage")
        gate[-1] = list(edit["new_frame"])
    profile, inventory = frame_report(word)
    return word, profile, inventory


def margin(delta, freed):
    return -delta - freed * BREAK_EVEN


def gates_outside(word, helpers, subspace):
    outside = 0
    for helper in helpers:
        for section in ("A", "B", "restore"):
            for gate in word[section]:
                if gate[0] in ("add", "scale") and helper in roles(gate) and not contained(gate[-1], subspace):
                    outside += 1
    return outside


def expect_nonmonotone(parent, record, edits, helpers):
    try:
        apply_v45(parent, record, edits, helpers)
    except ValueError as error:
        if str(error) != "nonmonotone":
            raise SystemExit("control rejected for the wrong reason: " + str(error))
        return
    raise SystemExit("control accepted a nonmonotone mutant")


def audit_provider(tag, record, edits):
    with gzip.open(DATA / f"PARENT-{tag}.json.gz", "rt", encoding="utf-8") as handle:
        parent = json.load(handle)
    parent_profile, parent_inventory = frame_report(parent)
    if parent_profile != parent["report"]["local_profile"]:
        raise SystemExit(tag + " parent profile was not reproduced")
    if parent_inventory != parent["report"]["width_inventory"]:
        raise SystemExit(tag + " parent width inventory was not reproduced")
    subspace = record["groups"]["V45"][0]
    if list(orthogonal((7, 42))) != list(subspace):
        raise SystemExit("V45 is not E_7 intersect E_42")
    if (7 ^ 42) != 45 or any((vector & normal).bit_count() % 2 for vector in subspace for normal in NORMALS):
        raise SystemExit("V45 normal identity failed")
    for helper in HELPERS:
        old = parent["helper_final"][str(helper)]
        if len(basis(old)) != 8 or len(basis(subspace)) != 7 or not contained(subspace, old):
            raise SystemExit("lowered end frame is not a hyperplane of the old end frame")

    base = cost(parent_profile)
    subset_margins = {}
    joint_word = None
    joint_profile = None
    joint_inventory = None
    for size in range(5):
        found = set()
        for subset in combinations(HELPERS, size):
            word, profile, inventory = apply_v45(parent, record, edits, subset)
            found.add(margin(cost(profile) - base, size))
            if size == 4:
                joint_word, joint_profile, joint_inventory = word, profile, inventory
            if size == len(subset) and gates_outside(word, subset, subspace):
                raise SystemExit("a lowered helper is touched outside W")
        subset_margins[size] = found
    expected = {
        0: {-78512},
        1: {-53141},
        2: {-27770},
        3: {-2399},
        4: {22972},
    }
    if subset_margins != expected:
        raise SystemExit(tag + " subset margins " + str(subset_margins))
    joint_delta = cost(joint_profile) - base
    if joint_delta != -8388172 or margin(joint_delta, 4) != 22972:
        raise SystemExit(tag + " joint price mismatch")
    overhead = joint_delta + 4 * WEIGHTS[1]
    if overhead != 78512 or 4 * PARTNER_ALLOWANCE - overhead != 22972:
        raise SystemExit(tag + " overhead decomposition mismatch")
    if joint_word["cleanup"] != parent["cleanup"] or len(joint_word["helper_final"]) != 86:
        raise SystemExit(tag + " cleanup or buffer count changed")
    if any(
        before[:-1] != after[:-1]
        for section in ("A", "B", "restore")
        for before, after in zip(parent[section], joint_word[section])
    ):
        raise SystemExit(tag + " a scalar or operator changed")
    width_delta = {
        key: joint_inventory.get(key, 0) - parent_inventory.get(key, 0)
        for key in sorted(set(joint_inventory) | set(parent_inventory), key=int)
    }
    if width_delta != {"4": 0, "5": 0, "7": 4, "8": -4, "9": 0}:
        raise SystemExit(tag + " width inventory " + str(width_delta))
    sections = Counter(edit["section"] for edit in edits)
    if set(sections) != {"B", "restore"}:
        raise SystemExit(tag + " V45 edits are not confined to B and restore")

    touching = [edit for edit in edits if set(roles(edit["gate"])) & set(HELPERS)]
    omitted = [edit for edit in edits if edit is not touching[0]]
    expect_nonmonotone(parent, record, omitted, HELPERS)
    stale = copy.deepcopy(edits)
    for edit in stale:
        if edit["section"] == touching[0]["section"] and edit["index"] == touching[0]["index"]:
            edit["new_frame"] = list(edit["old_frame"])
            break
    expect_nonmonotone(parent, record, stale, HELPERS)
    return {
        "joint_delta": joint_delta,
        "joint_margin": 22972,
        "sections": dict(sections),
        "edits": len(edits),
    }


def main():
    if BREAK_EVEN != 2091300:
        raise SystemExit("break-even identity failed")
    record = json.loads((DATA / "STAGE1-FRAME-EDITS.json").read_text(encoding="utf-8"))
    if record["groups"]["V45"][1] != list(HELPERS):
        raise SystemExit("V45 helper list changed")
    edits = [
        edit
        for edit in record["frame_edits"]
        if group_owners(record, edit["new_frame"]) == ["V45"]
    ]
    if len(edits) != 61:
        raise SystemExit("expected 61 V45-only frame edits")
    reports = {tag: audit_provider(tag, record, edits) for tag in ("base", "extra")}
    if reports["base"] != reports["extra"]:
        raise SystemExit("providers disagree: " + str(reports))
    report = reports["base"]
    print(
        "PASS_RANK7_V45_GROUP_AUDIT"
        f" providers=2 edits={report['edits']}"
        f" sections={report['sections']['B']}+{report['sections']['restore']}"
        " joint_delta=-8388172 joint_margin=22972"
        " single_margin=-53141 pair_margin=-27770 triple_margin=-2399"
        " frame_only_margin=-78512 overhead=78512"
        " width_8_to_7=4 buffers=86 cleanup_unchanged=yes"
        " controls=omit-edit,stale-frame"
    )


if __name__ == "__main__":
    main()
