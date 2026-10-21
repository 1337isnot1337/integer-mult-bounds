#!/usr/bin/env python3
"""Construct and check the terminal-helper trim of the full-identity unit.

The six immutable inputs below retain their original repository paths and
attribution.  The independent native interpreter checks arbitrary input
columns; the exact Clifford compiler checks the changed physical operators,
including absolute phase.  This module writes no files unless requested.
"""

from collections import Counter, defaultdict
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import importlib.util
import json
import sys


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CANONICAL = "research/kappa-rebuild/complex/full-identity-certificates/THREE-base-FULL-IDENTITY-CANONICAL.json.gz"
NATIVE = "research/kappa-rebuild/complex/full-identity-certificates/THREE-base-FULL-IDENTITY-NATIVE.json.gz"
CHECKER = "research/kappa-causal-continuation/buffer-borrowing/verify_buffers.py"
CLIFFORD = "research/t74-native-fast/vendor/native/new/code/borrow/vendor/clifford/clifford_exact.py"
PRUNE = "research/kappa-function-composition/complex/prune_native.py"
REBUILD = "research/kappa-rebuild/complex/rebuild_native.py"
SOURCE_SHA256 = {
    CANONICAL: "6418ec3da24d548a57f5c3fe5b9062c26c9478e638504a61c387f5cfb5f4ed61",
    NATIVE: "c54b0a3e129d28e6dbf74fa731fc3bb70fe3c6705f07256750fbecddcc842d39",
    CHECKER: "106b4d5e052427230df452f0c901d5390a0583782960b80a8af94d9a984022c7",
    CLIFFORD: "2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962",
    PRUNE: "f2b37c183a10922eabc8e0436b426a08866430e96bd0adc7e178951c7fbb5257",
    REBUILD: "f94c527cc02215de49350d477618188c4c0da48bc8fb05b4e37b24c482cad7d5",
}
TRIMMED_ROLES = (
    277, 282, 293, 298, 307, 309, 323, 325, 341, 346, 353,
    355, 357, 362, 369, 371, 373, 378, 385, 387, 389, 394,
)
EXPECTED_TARGETS = {4: 22, 5: 6, 6: 18, 7: 56, 8: 93, 9: 213}
EXPECTED_PAID = {1: 2465, 2: 713, 3: 224, 4: 102, 5: 20, 8: 8}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def canonical_bytes(value):
    """Proof-relevant representation, independent of gzip container details."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def string_keys(profile):
    return {str(rank): count for rank, count in sorted(profile.items()) if count}


def authenticate():
    actual = {relative: sha256((ROOT / relative).read_bytes()).hexdigest()
              for relative in SOURCE_SHA256}
    need(actual == SOURCE_SHA256, "An immutable native-trim input changed")
    return actual


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def read(relative):
    return json.loads(gzip.decompress((ROOT / relative).read_bytes()))


def cross_field_uses(word):
    uses = defaultdict(list)
    for index, event in enumerate(word):
        if event[0] == "scalar" and event[1][0] in ("add", "copy"):
            for role in event[1][1:3]:
                if role[0] == "L":
                    uses[role[1]].append(index)
    return uses


def helper_profile(canonical):
    frames = canonical["frames"]
    result = Counter()
    for role in range(224, 632):
        start, end = canonical["start"][role], canonical["final"][role]
        width = len(frames[end]) - len(frames[start])
        need(0 < width <= 9, "Every helper retains positive productive width")
        result[width] += 1
    need(sum(result.values()) == 408, "Complete arbitrary-helper census")
    return result


def fuse_centers(indexed_word, canonical, backward, ce, p, normalizer):
    """Replace the eight literal adjacent 5+3 center chains by rank eight.

    This is the source p7 invoice convention.  The constructor also records
    and exactly lowers the actual direct endpoint of each chain.
    """
    out = []
    certificates = []
    position = 0
    while position < len(indexed_word):
        source_index, event = indexed_word[position]
        if event[0] != "center":
            out.append(event)
            position += 1
            continue
        need(position + 1 < len(indexed_word), "Center pair has two events")
        second_index, second = indexed_word[position + 1]
        expected_ranks = (3, 5) if backward else (5, 3)
        need(second[0] == "center" and event[1] == second[1]
             and event[3] == second[2]
             and (event[4], second[4]) == expected_ranks,
             "Exactly the inherited adjacent center 5+3 chain")
        role, old, middle, new = event[1], event[2], event[3], second[3]
        expected_dimensions = (0, 3, 8) if backward else (8, 3, 0)
        need(tuple(len(canonical["frames"][f]) for f in (old, middle, new))
             == expected_dimensions, "Nested oriented center endpoint")
        physical = ce.canonical_frame(9, canonical["frames"][old]).adjoint().then(
            ce.canonical_frame(9, canonical["frames"][new]))
        if backward:
            physical = p.conjugate(ce, physical)
        recipe = normalizer.lower_exact(p, ce, physical)
        need(recipe["rank"] == 8, "Unsplit center physical rank is eight")
        certificates.append({
            "source_events": [source_index, second_index],
            "role": role, "old_frame": old, "middle_frame": middle,
            "new_frame": new, "paid_rank": 8,
            "exact_tableau_and_global_phase": True, "factorization": recipe,
        })
        out.append(["center", role, old, new, 8])
        position += 2
    need(len(certificates) == 8, "Exactly eight unsplit owned-center jobs")
    return out, certificates


def run(include_objects=False):
    """Return the deterministic receipt; optionally include the changed objects.

    Imports and source reads are the only side effects.  With include_objects
    true, ``changed_canonical`` and ``changed_words`` are added to the result.
    The outer helper normalizers are recorded in each directional receipt.
    """
    pins = authenticate()
    v = load(CHECKER, "terminal_helper_trim_independent")
    ce = load(CLIFFORD, "terminal_helper_trim_clifford")
    p = load(PRUNE, "terminal_helper_trim_prune")
    normalizer = load(REBUILD, "terminal_helper_trim_normalizer")
    canonical = read(CANONICAL)
    words = read(NATIVE)
    need(set(words) == {"forward", "backward"}, "Both source orientations")
    need(canonical["v"] == 112 and canonical["R"] == 408
         and len(canonical["start"]) == len(canonical["final"]) == 632,
         "The pinned 112-port native unit has 632 arbitrary inputs")
    old_targets = helper_profile(canonical)
    need(old_targets == {5: 28, 6: 18, 7: 56, 8: 93, 9: 213},
         "Inherited productive-helper profile")
    results = {}
    changed_words = {}
    changed_canonical = None
    new_targets = None
    new_paid = None
    for direction in ("forward", "backward"):
        word = words[direction]
        backward = direction == "backward"
        baseline = v.replay(word, canonical, [], backward, False)
        uses = cross_field_uses(word)
        trimmed = [(index, event) for index, event in enumerate(word)
                   if event[0] == "climb" and event[2] >= 224
                   and index > max(uses[event[2]])]
        need(tuple(sorted(event[2] for _, event in trimmed)) == TRIMMED_ROLES,
             "Exact source terminal-climb census")
        new_canonical = deepcopy(canonical)
        new_word = deepcopy(word)
        substitutions = []
        phases = []
        omitted = {index for index, _ in trimmed}
        changed = set()
        for index, event in trimmed:
            _, _, role, old, new, rank = event
            need(rank == 1 and role not in changed,
                 "One final rank-one climb per changed helper")
            need(canonical["final"][role] == new,
                 "Trimmed climb reaches original final frame")
            need(canonical["start"][role] == 0,
                 "Every changed helper has trivial entrance frame")
            need(len(canonical["frames"][old]) == 4
                 and len(canonical["frames"][new]) == 5,
                 "Productive helper rank decreases from five to four")
            new_canonical["final"][role] = old
            changed.add(role)
            retagged = []
            for j in range(index + 1, len(new_word)):
                following = new_word[j]
                if following[0] == "scalar" and ["L", role] in following[1][1:3]:
                    need(following[1][0] == "scale"
                         and following[1][1] == ["L", role]
                         and following[2] == new,
                         "Only scalar scaling follows terminal climb")
                    following[2] = old
                    retagged.append(j)
                elif following[0] == "warp" and following[1] == ["L", role]:
                    need(False, "No coordinate warp after trimmed climb")
                elif following[0] == "climb" and following[2] == role:
                    need(False, "No later paid helper climb")
            adapters = [j for j, e in enumerate(new_word)
                        if e[0] == "residual_adapter" and e[2] == role]
            need(len(adapters) == 2
                 and {new_word[j][1] for j in adapters} == {"pre", "post"},
                 "Replace both inherited helper residual adapters")
            omitted.update(adapters)
            physical = ce.canonical_frame(9, canonical["frames"][old])
            if backward:
                physical = p.conjugate(ce, physical)
            normal = normalizer.normal_form(p, ce, physical, 4)
            phases.append({"role": role, "new_end_frame": old,
                           "direction": direction, "normal_form": normal})
            substitutions.append({
                "source_event": index, "role": role, "old_frame": old,
                "removed_final_frame": new, "paid_rank_removed": rank,
                "old_target_rank": 5, "new_target_rank": 4,
                "last_cross_field_use": max(uses[role]),
                "retagged_scalars": retagged,
                "removed_residual_adapters": adapters,
            })
        indexed = [(j, e) for j, e in enumerate(new_word) if j not in omitted]
        new_word, centers = fuse_centers(indexed, new_canonical, backward,
                                         ce, p, normalizer)
        paid = Counter(e[-1] for e in new_word if e[0] in ("climb", "center"))
        targets = helper_profile(new_canonical)
        need(paid == EXPECTED_PAID, "Derived complete unsplit paid profile")
        need(targets == EXPECTED_TARGETS, "Derived complete productive profile")
        new_canonical["local_profile"] = string_keys(paid)
        checked = v.replay(new_word, new_canonical, [], backward, False)
        need(checked["conservative_real_scalar_primitive_allowance"]
             == baseline["conservative_real_scalar_primitive_allowance"],
             "Terminal removal adds no scalar primitive")
        need(checked["free_warp_operator_endpoint_matches"]
             and checked["independent_borrowed_input_fields"] == 632
             and checked["expected_restored_helpers"] == 408,
             "Exact endpoint on all 632 independent native inputs")
        need(checked["paid_profile"] == dict(sorted(paid.items())),
             "Independent native invoice equals derived unsplit invoice")
        if changed_canonical is not None:
            need(new_canonical == changed_canonical,
                 "Both orientations have the same changed canonical object")
            need(targets == new_targets and paid == new_paid,
                 "Both orientations have identical complete profiles")
        changed_canonical = new_canonical
        new_targets, new_paid = targets, paid
        changed_words[direction] = new_word
        results[direction] = {
            "baseline": baseline, "changed": checked, "removed": substitutions,
            "phase_normalizers": phases, "unsplit_center_pairs": centers,
        }
    need(results["forward"]["removed"] == results["backward"]["removed"],
         "Same priced trim and boundary substitutions in both orientations")
    need(sum(len(row["phase_normalizers"]) for row in results.values()) == 44,
         "All 44 changed helper operators have exact phase normalizers")

    # Controls address the two tempting unsound versions of this change:
    # deleting a transform needed by a later contact, or retaining rank five.
    mutation = deepcopy(words["forward"])
    uses = cross_field_uses(mutation)
    active = next(i for i, e in enumerate(mutation)
                  if e[0] == "climb" and e[2] >= 224 and i < max(uses[e[2]]))
    mutation.pop(active)
    rejected_active_climb = False
    try:
        v.replay(mutation, canonical, [], False, False)
    except ValueError:
        rejected_active_climb = True
    need(rejected_active_climb, "An interaction-bearing climb deletion is rejected")
    rejected_old_target_rank = False
    first = results["forward"]["removed"][0]
    try:
        normalizer.normal_form(p, ce, ce.canonical_frame(
            9, canonical["frames"][first["old_frame"]]), 5)
    except ValueError:
        rejected_old_target_rank = True
    need(rejected_old_target_rank, "Old rank-five productive credit is rejected")
    result = {
        "status": "PASS_TERMINAL_HELPER_TRIM_ALL_632_INPUTS_BOTH_ORIENTATIONS",
        "local_unsplit_targets": string_keys(new_targets),
        "local_unsplit_paid": string_keys(new_paid),
        "old_local_helper_targets": string_keys(old_targets),
        "derived_helper_count": sum(new_targets.values()),
        "derived_helper_rank_mass": sum(r * n for r, n in new_targets.items()),
        "derived_paid_rank_mass": sum(r * n for r, n in new_paid.items()),
        "changed_helper_phase_checks": 44,
        "unsplit_center_phase_checks": 16,
        "results": results,
        "negative_controls": {
            "active_climb_rejected": rejected_active_climb,
            "active_climb_source_event": active,
            "old_rank_five_credit_rejected": rejected_old_target_rank,
        },
        "source_sha256": pins,
        "changed_payload_sha256": {
            "canonical": sha256(canonical_bytes(changed_canonical)).hexdigest(),
            "native_words": sha256(canonical_bytes(changed_words)).hexdigest(),
        },
    }
    if include_objects:
        result["changed_canonical"] = changed_canonical
        result["changed_words"] = changed_words
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-result", type=Path, metavar="PATH",
                        help="write the deterministic JSON receipt to PATH")
    parser.add_argument("--include-objects", action="store_true",
                        help="include the changed canonical object and native words")
    args = parser.parse_args()
    result = run(include_objects=args.include_objects)
    if args.write_result is not None:
        args.write_result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])
    print("Targets:", result["local_unsplit_targets"])
    print("Paid:", result["local_unsplit_paid"])


if __name__ == "__main__":
    main()
