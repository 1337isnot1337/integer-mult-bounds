#!/usr/bin/env python3
"""All-length three-field receiver cost floor; exact integers, no word-length cap.

Uses the credited #4470 constructor only to obtain the frozen native events.
Window extraction, dependency relaxation and dominance certificates are new.
Prepared for mihir-s-05 with substantial OpenAI Codex assistance. Apache-2.0.
"""
import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def span(basis):
    result = {0}
    for vector in basis:
        result |= {value ^ vector for value in result}
    return frozenset(result)


def dimension(space):
    need(len(space) > 0 and len(space) & (len(space) - 1) == 0,
         "binary subspace cardinality")
    return len(space).bit_length() - 1


def partition(values):
    return tuple(sorted((value for value in values if value), reverse=True))


def capped_sums(ranks):
    return tuple(sum(min(rank, k) for rank in ranks) for k in range(1, 10))


def dominates(incumbent, candidate):
    """Exact certificate for every concave rank price with f(0)=0; see README."""
    return sum(incumbent) == sum(candidate) and all(
        a <= b for a, b in zip(capped_sums(incumbent), capped_sums(candidate)))


def source_checks():
    manifest = json.loads((HERE / "SOURCES.json").read_bytes())
    checked = 0
    for row in manifest["files"]:
        if row["usage"] == "input":
            raw = (ROOT / row["path"]).read_bytes()
            need(hashlib.sha256(raw).hexdigest() == row["sha256"],
                 "changed source: " + row["path"])
            checked += 1
    need(checked == 7, "complete constructor source closure")
    return checked


def construct():
    # A private cache prevents stale bytecode from replacing authenticated source.
    code = ("import json,sys;sys.path.insert(0,sys.argv[1]);import native_joint;"
            "c,p,*_=native_joint.construct();print(json.dumps([c,p['forward']]))")
    with tempfile.TemporaryDirectory(prefix="receiver-floor-pycache-") as cache:
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-X", "pycache_prefix=" + cache,
             "-c", code, str(ROOT / "research/joint-helper-lattice")],
            capture_output=True, check=True, timeout=120)
    return json.loads(result.stdout)


def operands(event):
    if event[0] != "scalar":
        return []
    gate = event[1]
    return gate[1:3] if gate[0] in ("add", "copy") else gate[1:2]


def incumbent_profile(starts, ends, contacts):
    current, paid = list(starts), []
    for pair, frame in zip(((0, 2), (1, 2)), contacts):
        for role in pair:
            need(current[role] <= frame, "incumbent contact is monotone")
            paid.append(dimension(frame) - dimension(current[role]))
            current[role] = frame
    for a, b in zip(current, ends):
        need(a <= b, "incumbent exit is monotone")
        paid.append(dimension(b) - dimension(a))
    return partition(paid)


def extract_windows(certificate, program):
    # Frame state at a cut is after the preceding touch, before the next climb.
    # The next scalar/warp entrance (or final frame) is the fixed exit contract.
    events = [event for event in program if event[0] != "climb"]
    bases = certificate["frames"]
    need(all(type(v) is int and 0 <= v < 512 for basis in bases for v in basis),
         "frames lie in F2^9")
    frames = [span(basis) for basis in bases]
    need(all(len(frame) == 2 ** len(basis) for frame, basis in zip(frames, bases)),
         "independent input frame bases")
    state, phase, result = certificate["start"][:], None, []
    for pos, event in enumerate(events):
        if event[0] == "phase":
            phase = event[1]
        if phase in ("B", "cleanup_tail") and pos + 1 < len(events):
            second = events[pos + 1]
            if (event[0] == second[0] == "scalar"
                    and event[1][0] == second[1][0] == "add"):
                roles = operands(event) + operands(second)
                if all(kind == "L" for kind, _ in roles):
                    a, x, b, y = (role for _, role in roles)
                    ca, cb = Fraction(*event[1][3:]), Fraction(*second[1][3:])
                    if x == y and len({a, b, x}) == 3 and ca in (-1, 1) and cb in (-1, 1):
                        owners = [a, b, x]
                        start_ids = [state[role] for role in owners]
                        end_ids = []
                        for role in owners:
                            boundary = certificate["final"][role]
                            for later in events[pos + 2:]:
                                if ["L", role] in operands(later):
                                    boundary = later[2]
                                    break
                                if later[0] == "warp" and later[1] == ["L", role]:
                                    boundary = later[3]
                                    break
                            end_ids.append(boundary)
                        result.append({
                            "index": pos, "phase": phase, "roles": owners,
                            "coefficients": [int(ca), int(cb)],
                            "start_bases": [bases[i] for i in start_ids],
                            "exit_bases": [bases[i] for i in end_ids],
                            "contact_bases": [bases[event[2]], bases[second[2]]],
                        })
        if event[0] == "scalar":
            for kind, role in operands(event):
                if kind == "L":
                    state[role] = event[2]
        elif event[0] == "warp":
            state[event[1][1]] = event[4]
    need(len(result) == 128, "128 eligible adjacent windows")
    need(Counter(row["phase"] for row in result) == {"B": 123, "cleanup_tail": 5},
         "phase coverage")
    return result


def relaxed_profiles(starts, ends, *, dependency=True, intersections=True, exits=True):
    """Finite acyclic overapproximation of ALL finite scalar words.

    A bit records possible dependence on initial x, never its exact coefficient.
    Frame subspaces are relaxed to dimensions plus static necessary pair bounds.
    Toggles weaken specific premises for rejection controls only.
    """
    need(all(a <= b for a, b in zip(starts, ends)), "monotone boundaries")
    initial = tuple(map(dimension, starts))
    final = tuple(map(dimension, ends))
    pairs = []
    for i in range(3):
        for j in range(3):
            if i == j or not (starts[i] <= ends[j] and starts[j] <= ends[i]):
                continue
            lower = dimension({a ^ b for a in starts[i] for b in starts[j]})
            upper = (dimension(ends[i] & ends[j]) if intersections
                     else min(final[i], final[j]))
            pairs.append((i, j, lower, upper))

    @lru_cache(None)
    def visit(dims, mask):
        terminal = mask == 7 or not dependency
        gap = partition(final[i] - dims[i] for i in range(3)) if exits else ()
        profiles = {gap} if terminal else set()
        for i, j, lower, upper in pairs:
            for common in range(max(dims[i], dims[j], lower), upper + 1):
                after = list(dims)
                after[i] = after[j] = common
                after = tuple(after)
                mask_after = mask | ((1 << i) if mask & (1 << j) else 0)
                if (after, mask_after) == (dims, mask):
                    # Every such edge has zero charge. Removing it cannot change
                    # any future transition or terminal condition in this graph.
                    continue
                need(sum(after) + mask_after.bit_count() > sum(dims) + mask.bit_count(),
                     "strict acyclic potential")
                added = (common - dims[i], common - dims[j])
                for suffix in visit(after, mask_after):
                    profiles.add(partition((*added, *suffix)))
        return frozenset(profiles)

    profiles = visit(initial, 4)
    if exits:
        mass = sum(final) - sum(initial)
        need(all(sum(p) == mass for p in profiles), "all terminal rank mass charged")
    return profiles, visit.cache_info().currsize


def evaluate_window(row):
    starts = [span(b) for b in row["start_bases"]]
    ends = [span(b) for b in row["exit_bases"]]
    contacts = [span(b) for b in row["contact_bases"]]
    old = incumbent_profile(starts, ends, contacts)
    profiles, states = relaxed_profiles(starts, ends)
    need(old in profiles, "incumbent admitted at window " + str(row["index"]))
    need(all(dominates(old, p) for p in profiles),
         "all-length floor failed at window " + str(row["index"]))
    return {**row, "incumbent": old, "reachable_states": states,
            "terminal_profiles": sorted(profiles)}


def failure_controls(windows):
    by_index = {row["index"]: row for row in windows}
    cases = [
        ("drop_directed_dependency", 10557, {"dependency": False}, (2, 1)),
        ("drop_exit_intersection", 11078, {"intersections": False}, (2, 2)),
        ("drop_terminal_charge", 10554, {"exits": False}, ()),
    ]
    output = {}
    for name, index, weakening, false_gain in cases:
        row = by_index[index]
        starts = [span(b) for b in row["start_bases"]]
        ends = [span(b) for b in row["exit_bases"]]
        profiles, _ = relaxed_profiles(starts, ends, **weakening)
        need(false_gain in profiles, "negative control actually exposes its false gain")
        need(false_gain not in row["terminal_profiles"], "normal model excludes the false gain")
        need(not dominates(row["incumbent"], false_gain), "false gain rejected")
        output[name] = {"index": index, "incumbent": row["incumbent"],
                        "falsely_admitted": false_gain}
    return output


def small_geometric_control():
    """Exhaust all legal common frames on exact endpoint words through length 4.

    This is a finite semantic control for the abstraction, not the all-length proof.
    F2^2, zero entrances, full exits; integer scalar matrices track arbitrary inputs.
    """
    spaces = [span(b) for b in ((), (1,), (2,), (3,), (1, 2))]
    zero, full = spaces[0], spaces[-1]
    abstract, _ = relaxed_profiles([zero] * 3, [full] * 3)
    identity = (1, 0, 0, 0, 1, 0, 0, 0, 1)
    target = (1, 0, 1, 0, 1, 1, 0, 0, 1)
    gates = [(i, j, s) for i in range(3) for j in range(3) if i != j for s in (-1, 1)]
    matched = paths = 0

    def frame_paths(word, current, paid):
        nonlocal paths
        if not word:
            p = partition((*paid, *(2 - dimension(frame) for frame in current)))
            need(p in abstract, "legal geometric path absent from relaxation")
            paths += 1
            return
        i, j, _ = word[0]
        for frame in spaces:
            if current[i] <= frame and current[j] <= frame:
                after = list(current)
                added = (dimension(frame) - dimension(current[i]),
                         dimension(frame) - dimension(current[j]))
                after[i] = after[j] = frame
                frame_paths(word[1:], after, (*paid, *added))

    def words(matrix, word):
        nonlocal matched
        if matrix == target:
            matched += 1
            frame_paths(word, [zero] * 3, ())
        if len(word) == 4:
            return
        for i, j, s in gates:
            after = list(matrix)
            for k in range(3):
                after[3 * i + k] += s * matrix[3 * j + k]
            words(tuple(after), (*word, (i, j, s)))

    words(identity, ())
    need(matched == 84 and paths > 0, "exact dirty-input endpoint control")
    # The cone identity used in the written proof is also checked for every
    # generator f(r)=min(r,k) on ranks 0..9, entirely over integers.
    for k in range(1, 10):
        f = [min(r, k) for r in range(10)]
        delta = [f[r] - f[r - 1] for r in range(1, 10)]
        for r in range(10):
            reconstructed = delta[-1] * r + sum(
                (delta[j - 1] - delta[j]) * min(r, j) for j in range(1, 9))
            need(reconstructed == f[r], "discrete concave-price identity")
    return {"endpoint_words": matched, "geometric_paths": paths,
            "concave_basis_checks": 90}


def run():
    source_count = source_checks()
    certificate, program = construct()
    windows = [evaluate_window(row) for row in extract_windows(certificate, program)]
    controls = failure_controls(windows)
    small = small_geometric_control()
    return {"schema": "receiver-window-all-length-floor/v1",
            "status": "PASS_ALL_LENGTH_RECEIVER_FLOOR",
            "source_base": "f626db5c3a3d781d8f7695038776c621651f75e1",
            "source_files_checked": source_count,
            "window_count": len(windows),
            "reachable_states": sum(w["reachable_states"] for w in windows),
            "window_profile_pairs": sum(len(w["terminal_profiles"]) for w in windows),
            "profile_count_histogram": dict(sorted(Counter(len(w["terminal_profiles"]) for w in windows).items())),
            "failure_controls": controls, "geometric_control": small,
            "new_kappa": False, "windows": windows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="author the deterministic receipt")
    args = parser.parse_args()
    result = run()
    raw = json.dumps(result, indent=2, sort_keys=True) + "\n"
    path = HERE / "RESULT.json"
    if args.write:
        path.write_text(raw, encoding="utf-8", newline="\n")
    else:
        need(path.read_text(encoding="utf-8") == raw, "complete deterministic receipt mismatch")
    print(json.dumps({key: value for key, value in result.items() if key != "windows"}, sort_keys=True))


if __name__ == "__main__":
    main()
