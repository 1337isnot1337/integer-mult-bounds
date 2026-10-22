#!/usr/bin/env python3
"""PR4633 endpoint audit and boundary-only repair obstruction.

Apache-2.0. Prepared with substantial OpenAI Codex assistance.
Run from any directory; standard library only. --require-supplier exits nonzero
on the submitted artifact, rather than treating its logical replay as admission.
Frozen predecessor files are read, never rewritten.
"""
import argparse
from collections import Counter
from copy import deepcopy
import gzip
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import struct
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SUBJECT = "b390d64abfcdba1a3816b86fc763cbc95d43c12c"
SOURCE = "research/kappa-rebuild/bit/sources/pr589-regenerated/"
PINS = {
    SOURCE + "WORD.json.gz": "e3e301e62bc2b41dbf1ceac0acf3d35824ebeab1848c5a2142d4577b109da52f",
    SOURCE + "records/frames.json": "d006b3bfe0c04afecfea7aecfa59dfe4298b99501c70da3938e40289bc2f5010",
    SOURCE + "records/249-records.bin": "ea44aa047a2a9cf034de8b56b2166c49cf2dbdf9cd9ed6a20299a4f2b05ef09a",
    "research/bit-ambient-quotient/build.py": "1d6601e57f4d8809065ed6821b1bda35621fb6a08a8fd48cc3fdf95ed59e19c7",
    "research/bit-ambient-quotient/verify.py": "d60e8db9aea2dbee786432143aac8c18996bf491b513b57d1729a4bbb3f7464e",
    "research/bit-ambient-quotient/QUOTIENT-BIT-WORD.json.gz": "a1b9555b38d234e3921cdabd280e6a754619e26dd620a069a2a85a93efa31b2c",
    "research/bit-ambient-quotient/RESULT.json": "fdb1059a80c345004259eea514585a7ac2f199b1825af46477b9dc0bff8aaf90",
    "research/complex-ambient-quotient/QUOTIENT-WORD.json.gz": "10155f81100e9cd6283f1d9dfd071bc0c3e0e89dc3794a66e4129a1f34d99dc4",
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    raw = (ROOT / path).read_bytes()
    return json.loads(gzip.decompress(raw) if path.endswith(".gz") else raw)


def span(basis):
    out = {0}
    for v in basis:
        out |= {x ^ v for x in out}
    return frozenset(out)


def dim(space):
    need(len(space) > 0 and len(space) & (len(space) - 1) == 0, "Subspace size")
    return len(space).bit_length() - 1


def dot(x, y):
    return (x & y).bit_count() & 1


def reduced_frame(frame):
    rows = [sum((x & 1) << j for j, x in enumerate(row)) for row in frame["A"]]
    return frozenset(x for x in range(256) if all(dot(x, r) == 0 for r in rows))


def check_transports(artifact):
    """The missing rank/geometry guard, independent of the logical replay."""
    frames = [span(b) for b in artifact["frame_bases"]]
    dims = {int(k): v for k, v in artifact["frame_dims"].items()}
    need(set(dims) == set(range(len(frames))), "Frame table indices")
    for i, frame in enumerate(frames):
        need(dim(frame) == dims[i], "Frame basis dimension")
    for op, _, old, new, rank, _ in artifact["records"]:
        if op == 0:
            need(frames[old] <= frames[new], "MOVE frames are not nested")
            need(rank == dims[new] - dims[old], "MOVE rank is not derived from its frames")
    return frames, dims


def port_census(frames, start, final, pairs, ambient):
    cases, bad = Counter(), []
    for p in range(pairs):
        a, b = frames[start[p]], frames[final[pairs + p]]
        row = (dim(a), dim(b), dim(a & b))
        cases[row] += 1
        valid = (dim(frames[final[p]]) - dim(a) == ambient - 1
                 and dim(b) - dim(frames[start[pairs + p]]) == ambient - 1
                 and row == (1, ambient - 1, 0)
                 and dim(frames[final[p]]) == ambient
                 and dim(frames[start[pairs + p]]) == 0)
        if not valid:
            bad.append(p)
    return {"cases_dim_P_dim_H_intersection": [
        {"dimensions": list(k), "ports": n} for k, n in sorted(cases.items())],
        "invalid_ports": bad, "valid_ports": pairs - len(bad)}


def require_supplier(artifact):
    """Necessary interface checks only; passing would not prove admission."""
    frames, _ = check_transports(artifact)
    need(artifact["ambient_dim"] == 8, "BIT ambient")
    need(len(artifact["start"]) == len(artifact["final"]) == 661, "BIT role count")
    for r in range(222, 661):
        need(dim(frames[artifact["start"][r]]) == 0
             and dim(frames[artifact["final"][r]]) == 8, "Helper boundary")
    census = port_census(frames, artifact["start"], artifact["final"], 111, 8)
    need(not census["invalid_ports"],
         f"BIT supplier endpoint contract fails on {len(census['invalid_ports'])}/111 ports")


def optimistic_boundary_repair(a, b):
    """Minimize every capped rank moment over ALL complementary P', H'.

    The initial X frame a is zero or a line, X ends at the full ambient,
    Y starts at zero and ends at b. Choose ANY new line P' and hyperplane H'
    avoiding P'. Distances of preimage frames are dim U + dim V - 2dim(U cap V).
    The model even allows a general complementary pair without checking its
    exact representatives implement the controller's common stage multiplier.
    """
    da, db = dim(a), dim(b)
    need(da in (0, 1), "Boundary repair scope: X entrance zero or line")
    if db == 8:
        best = (1 - da, 1)
    elif da == 0:
        best = (1, 7 - db)
    elif a <= b:
        best = (0, 9 - db)
    else:
        best = (0, 7 - db)

    # Every hyperplane is ker(n dot -), n != 0. For a fixed hyperplane,
    # the cheapest admissible P' is a itself if it is outside H', any other
    # outside line otherwise. Enumerating n therefore covers all 32640 pairs.
    for normal in range(1, 256):
        dh_intersection = dim(frozenset(x for x in b if dot(x, normal) == 0))
        y_rank = db + 7 - 2 * dh_intersection
        x_rank = 1 if da == 0 else (2 if all(dot(x, normal) == 0 for x in a) else 0)
        for cap in range(1, 9):
            need(min(x_rank, cap) + min(y_rank, cap)
                 >= sum(min(r, cap) for r in best), "Boundary optimum counterexample")
    return [r for r in best if r]


def audit():
    for path, digest in PINS.items():
        need(sha256((ROOT / path).read_bytes()).hexdigest() == digest, "Source pin: " + path)
    artifact = read("research/bit-ambient-quotient/QUOTIENT-BIT-WORD.json.gz")
    frames, dims = check_transports(artifact)
    census = port_census(frames, artifact["start"], artifact["final"], 111, 8)
    need(census["valid_ports"] == 0, "Expected current-head endpoint failure")

    word = read(SOURCE + "WORD.json.gz")
    source_frames = read(SOURCE + "records/frames.json")["frames"]
    binary = {int(k): reduced_frame(f) for k, f in source_frames.items()}
    rational_good, binary_bad = 0, []
    for p in range(111):
        entrance, terminal = word["start"][p], word["final"][111 + p]
        u = source_frames[str(entrance)]["B"][0]
        normal = source_frames[str(terminal)]["A"][0]
        rational_good += int(sum(x * y for x, y in zip(u, normal)) != 0)
        if dim(binary[entrance] & binary[terminal]) != 0:
            binary_bad.append(p)
    need(rational_good == 111 and len(binary_bad) == 103, "Source field-change control")
    need(source_frames["10"]["B"][0] == [0, 1, 1, 0, 1, 0, 0, 1], "Port 8 witness")
    need(word["start"][8] == 10 and word["final"][119] == 533, "Port 8 frame IDs")

    spec = importlib.util.spec_from_file_location("pr4633_original_verifier",
        ROOT / "research/bit-ambient-quotient/verify.py")
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    profiles = [verifier.replay(artifact["records"], artifact["start"],
                artifact["final"], dims, reverse)[0] for reverse in (False, True)]
    need(profiles[0] == profiles[1] and verifier.rank_mass(profiles[0]) == 4842,
         "Submitted logical replay")
    records = list(struct.iter_unpack("<6i", (ROOT / SOURCE / "records/249-records.bin").read_bytes()))
    need(len(records) == len(artifact["records"]), "Record count")
    longer = [(old, new) for old, new in zip(records, artifact["records"])
              if old[0] == 0 and new[4] > old[4]]
    need(len(longer) == 557, "Re-padding lengthens 557 MOVEs")
    source_dims = {int(k): f["dim"] for k, f in source_frames.items()}
    for reverse in (False, True):
        original = verifier.replay(records, word["start"], word["final"], source_dims, reverse)[0]
        need(original == verifier.LOCAL, "Pinned source replay")

    # The original replay accepts false ranks, including zero for every MOVE.
    tampered = deepcopy(artifact)
    for record in tampered["records"]:
        if record[0] == 0:
            record[4] = 0
    for reverse in (False, True):
        cheap = verifier.replay(tampered["records"], tampered["start"],
                                tampered["final"], dims, reverse)[0]
        need(verifier.rank_mass(cheap) == 36, "False-rank negative control")
    try:
        check_transports(tampered)
    except ValueError:
        pass
    else:
        raise ValueError("Transport guard accepted false ranks")

    repair = Counter()
    for p in range(111):
        repair.update(optimistic_boundary_repair(frames[artifact["start"][p]],
                                               frames[artifact["final"][111 + p]]))
    need(repair == Counter({1: 49, 3: 41, 5: 62}), "Boundary repair profile")
    targets, paid, surplus, _ = verifier.invoice({8: 439}, profiles[0] + repair)
    cap_gaps = {cap: sum(min(r, cap) * n for r, n in paid.items())
                     - sum(min(r, cap) * n for r, n in targets.items())
                for cap in range(1, max(max(targets), max(paid)) + 1)}
    need(surplus == -2757 and min(cap_gaps.values()) == 2757, "Exact concave-moment obstruction")

    complex_word = read("research/complex-ambient-quotient/QUOTIENT-WORD.json.gz")
    complex_frames = [span(b) for b in complex_word["frames"]]
    complex_census = port_census(complex_frames, complex_word["start"],
                                 complex_word["final"], 112, 9)
    need(complex_census["valid_ports"] == 0, "Complex block-8 endpoint failure")
    result = {
        "status": "PASS_AUDIT_REJECTS_UNSUPPORTED_KAPPA",
        "reviewed_head": SUBJECT, "source_sha256": PINS,
        "bit_ports": census, "complex_ports": complex_census,
        "source_rational_complementary_ports": rational_good,
        "source_ports_broken_before_any_quotient": binary_bad,
        "logical_replay_both_directions": True, "arbitrary_columns": 661,
        "adds": 24305, "owned_copy_episodes": 9,
        "source_paid_mass": 5129, "submitted_paid_mass": 4842,
        "main_rank_mass_loss": 1554 - artifact["main_rank_mass"],
        "copy_rank_mass_loss": 63 - 36,
        "moves_lengthened_by_repadding": len(longer),
        "extra_rank_on_lengthened_moves": sum(new[4] - old[4] for old, new in longer),
        "false_move_ranks_original_replay_paid_mass": 36,
        "false_move_ranks_rejected_by_new_guard": True,
        "minimum_boundary_repair_profile": dict(sorted(repair.items())),
        "minimum_boundary_repair_rank_mass": verifier.rank_mass(repair),
        "repaired_local_paid_mass": verifier.rank_mass(profiles[0] + repair),
        "repaired_global_rank_surplus": surplus,
        "minimum_capped_paid_minus_target": min(cap_gaps.values()),
        "capped_paid_minus_target": cap_gaps,
        "boundary_only_repair_fails_all_kappa_between_zero_and_one": True,
        "scope": "Submitted GF(2) preimage-frame model and per-port endpoint adapters; no barrier to new constructions or joint rewrites.",
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-supplier", action="store_true")
    parser.add_argument("--write", action="store_true", help="Write this audit's RESULT.json only")
    args = parser.parse_args()
    result = audit()
    if args.write:
        (HERE / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])
    print("BIT: 0/111 valid ports; complex: 0/112 valid block-8 ports")
    print("Boundary repair: +482 local ranks, paid mass 5324, surplus -2757")
    print("All capped paid-minus-target gaps >= 2757: first screen fails for 0 < kappa < 1")
    if args.require_supplier:
        require_supplier(read("research/bit-ambient-quotient/QUOTIENT-BIT-WORD.json.gz"))


if __name__ == "__main__":
    main()
