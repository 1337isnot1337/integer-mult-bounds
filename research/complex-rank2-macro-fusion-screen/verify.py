#!/usr/bin/env python3
"""Screen direct rank-1-pair to rank-2 macro substitutions in the selected trace."""
from __future__ import annotations

import collections
import gzip
import hashlib
import io
import json
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "research/community-frontier1094-audit/selected-replay.tar.gz"
ARCHIVE_SHA256 = "f1da80610bf33c58527f18ad63b4350d0b864e1d4486141ee17ac9bed4d529d6"
PROGRAM_MEMBER = (
    "candidate/strict/global/base/providers/gauge44/LOCAL-PROGRAMS.json.gz"
)
PROGRAM_SHA256 = "241fde27d4e43f5a9cb6b128f9f76c5131a53d09f0371676163f914d0b0fef3a"
RECIPE_MEMBER = (
    "candidate/strict/global/base/providers/gauge44/CLIFFORD-RECIPES.json"
)
RECIPE_SHA256 = "d0768f2164d5f64a2fdbec422f1cfde4e400818792f1904ca541958377243731"
SELECTED = ROOT / "certificates/selected-result.json"
SELECTED_SHA256 = "bb2eaa58647b353f88d0aec2eafb9d30df1be53589231b23e12ceef3e4bad129"
SELECTED_KAPPA = "0.001672660197076918"
EXPECTED_TOUCH_HISTOGRAM = {1: 10, 2: 5, 5: 20}
EXPECTED_PHASE_PAIRS = {
    ("A", "A"): 20,
    ("B", "B"): 8,
    ("cleanup_tail", "final"): 7,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_sources() -> tuple[dict[str, list], list[dict], str]:
    archive_bytes = ARCHIVE.read_bytes()
    require(digest(archive_bytes) == ARCHIVE_SHA256, "selected archive pin")
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as archive:
        names = {member.name for member in archive.getmembers()}
        require(PROGRAM_MEMBER in names, "selected local program present")
        require(RECIPE_MEMBER in names, "selected child recipes present")
        program_bytes = archive.extractfile(PROGRAM_MEMBER).read()
        recipe_bytes = archive.extractfile(RECIPE_MEMBER).read()
    require(digest(program_bytes) == PROGRAM_SHA256, "local program member pin")
    require(digest(recipe_bytes) == RECIPE_SHA256, "child recipe member pin")
    programs = json.loads(gzip.decompress(program_bytes))
    recipes = json.loads(recipe_bytes)["children"]
    require(set(programs) == {"forward", "backward"}, "both orientations present")
    require(len(recipes) == 2896, "selected recipe inventory")

    keys = [(entry["old"], entry["new"], entry["rank"]) for entry in recipes]
    require(len(set(keys)) == len(keys), "child recipe transitions are unique")

    selected_bytes = SELECTED.read_bytes()
    require(digest(selected_bytes) == SELECTED_SHA256, "selected record pin")
    selected = json.loads(selected_bytes)
    require(selected["decimal"] == SELECTED_KAPPA, "selected kappa record")
    return programs, recipes, selected["decimal"]


def local_register_touched(event: list, register: int) -> bool:
    tag = event[0]
    if tag in ("climb", "adapter", "residual_adapter"):
        return event[2] == register
    if tag != "scalar":
        return False

    operation = event[1]
    kind = operation[0]
    require(kind in ("scale", "add", "copy", "clear"), "known scalar event")
    touched = {tuple(operation[1])}
    if kind in ("add", "copy"):
        touched.add(tuple(operation[2]))
    return ("L", register) in touched


def screen_orientation(
    events: list, recipe_keys: set[tuple[int, int, int]], target_rank: int = 2
) -> dict:
    last_by_register: dict[int, tuple[int, str, int, int, int, int]] = {}
    rank_one_successors = 0
    candidates = []

    for index, event in enumerate(events):
        if event[0] != "climb":
            continue
        _, phase, register, old, new, rank = event
        previous = last_by_register.get(register)
        if previous is not None and previous[4] == old:
            if previous[5] == 1 and rank == 1:
                rank_one_successors += 1
                if (previous[3], new, target_rank) in recipe_keys:
                    intervening = [
                        events[j]
                        for j in range(previous[0] + 1, index)
                        if local_register_touched(events[j], register)
                    ]
                    candidates.append({
                        "first_index": previous[0],
                        "second_index": index,
                        "first_phase": previous[1],
                        "second_phase": phase,
                        "register": register,
                        "old": previous[3],
                        "middle": old,
                        "new": new,
                        "intervening_touches": intervening,
                    })
        last_by_register[register] = (index, phase, register, old, new, rank)

    touch_histogram = collections.Counter(
        len(candidate["intervening_touches"]) for candidate in candidates
    )
    phase_pairs = collections.Counter(
        (candidate["first_phase"], candidate["second_phase"])
        for candidate in candidates
    )
    return {
        "rank_one_successors": rank_one_successors,
        "candidates": candidates,
        "touch_histogram": dict(sorted(touch_histogram.items())),
        "phase_pairs": dict(sorted(phase_pairs.items())),
        "directly_fusible": sum(not candidate["intervening_touches"]
                                 for candidate in candidates),
    }


def main() -> None:
    programs, recipes, selected_kappa = load_sources()
    recipe_keys = {
        (entry["old"], entry["new"], entry["rank"])
        for entry in recipes
    }

    receipts = {
        orientation: screen_orientation(events, recipe_keys)
        for orientation, events in programs.items()
    }
    for orientation, receipt in receipts.items():
        rank_one_climbs = sum(
            event[0] == "climb" and event[5] == 1
            for event in programs[orientation]
        )
        require(rank_one_climbs == 2412,
                orientation + " selected rank-one child count")
        require(receipt["rank_one_successors"] == 1441,
                orientation + " rank-one successor count")
        require(len(receipt["candidates"]) == 35,
                orientation + " direct rank-two recipe candidates")
        require(receipt["touch_histogram"] == EXPECTED_TOUCH_HISTOGRAM,
                orientation + " scalar-interference histogram")
        require(receipt["phase_pairs"] == EXPECTED_PHASE_PAIRS,
                orientation + " candidate phase pairs")
        require(receipt["directly_fusible"] == 0,
                orientation + " no conflict-free direct substitution")
        require(all(
            event[0] == "scalar"
            for candidate in receipt["candidates"]
            for event in candidate["intervening_touches"]
        ), orientation + " all candidate conflicts are scalar events")

    require(receipts["forward"]["touch_histogram"]
            == receipts["backward"]["touch_histogram"],
            "orientation screens agree")

    # Positive control: this exact endpoint pair has a direct rank-two recipe.
    witness = (0, 27, 2)
    require(witness in recipe_keys, "rank-two endpoint positive control")
    witness_count = sum(
        candidate["old"] == witness[0] and candidate["new"] == witness[1]
        for candidate in receipts["forward"]["candidates"]
    )
    require(witness_count == 2, "rank-two witness multiplicity in the forward trace")

    # Negative controls: wrong target rank rejects all candidates; deleting the
    # one positive-control recipe rejects exactly its two occurrences.
    wrong_rank = screen_orientation(programs["forward"], recipe_keys, target_rank=3)
    require(not wrong_rank["candidates"], "wrong-rank control rejects candidates")
    mutated_keys = recipe_keys - {witness}
    mutated = screen_orientation(programs["forward"], mutated_keys)
    require(len(mutated["candidates"]) == 33,
            "removed-recipe control rejects exactly two candidates")

    print(
        "PASS_COMPLEX_RANK2_MACRO_FUSION_SCREEN "
        "orientations=2 rank1_climbs=2412 rank1_successors=1441 "
        "direct_rank2_candidates=35 "
        "blocked_by_scalar=35 directly_fusible=0 "
        "touch_histogram=1:10,2:5,5:20 controls=3 "
        f"selected_kappa={selected_kappa} no_new_kappa"
    )


if __name__ == "__main__":
    main()
