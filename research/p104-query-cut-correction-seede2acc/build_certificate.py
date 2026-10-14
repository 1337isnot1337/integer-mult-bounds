#!/usr/bin/env python3
"""Compile the terminal P104 I-G/2 scatter certificate from pinned inputs."""
from pathlib import Path
from itertools import combinations, product
from fractions import Fraction as Q
import gzip
import hashlib
import importlib.util
import json
import sys
import argparse

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BASE = ROOT / "research/p104-native-channel"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def roots():
    out = set()
    for i, j in combinations(range(8), 2):
        for sign in (-1, 1):
            row = [0] * 8
            row[i], row[j] = 2, 2 * sign
            out.add(tuple(row))
    for signs in product((-1, 1), repeat=7):
        if signs.count(-1) % 2 == 0:
            out.add((1, *signs))
    if len(out) != 120:
        raise ValueError("E8 root count")
    return sorted(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="replace the recorded certificate")
    args = parser.parse_args()
    witness_path = BASE / "inputs/LOWRANK-WITNESS.json"
    fixture_path = BASE / "inputs/P104-FIXTURE.json"
    witness_bytes, fixture_bytes = witness_path.read_bytes(), fixture_path.read_bytes()
    witness, fixture_doc = json.loads(witness_bytes), json.loads(fixture_bytes)
    fixture = fixture_doc["section4_explicit_P104"]
    roots_all = roots()
    removed = {tuple(v) for v in fixture["F0"] + fixture["C"]}
    ports = [r for r in roots_all if r not in removed]
    if len(removed) != 16 or len(ports) != 104:
        raise ValueError("P104 port inventory")

    compiler = load_module("p104_terminal_source_compile", BASE / "compile.py")
    CE, N = compiler.CE, compiler.N
    r2, labels, physical, transform, iso = compiler.label_isometry()
    if r2 != roots_all:
        raise ValueError("compiler root order")
    frame = lambda f: compiler.canon(transform(v) for v in f)
    full_raw = witness["final_frames"]["X0"]
    full = frame(full_raw)
    additions, target_records = [], []
    for t, root_t in enumerate(ports):
        old_raw = witness["final_frames"][f"Y{t}"]
        old_physical = frame(old_raw)
        if len(old_raw) != 8 or len(old_physical) != 8 or len(full_raw) != 9:
            raise ValueError("terminal target/source frame dimensions")
        up_actual = CE.canonical_frame(9, old_physical).adjoint().then(
            CE.canonical_frame(9, full)
        )
        down_actual = CE.canonical_frame(9, full).adjoint().then(
            CE.canonical_frame(9, old_physical)
        )
        up, _ = CE.lower_child(up_actual)
        down, _ = CE.lower_child(down_actual)
        if up["rank"] != 1 or down["rank"] != 1:
            raise ValueError("terminal transition did not compile to rank one")

        target_additions = [["transport", f"Y{t}", old_raw, full_raw, 1]]
        terms = []
        for s, root_s in enumerate(ports):
            inner = sum(x * y for x, y in zip(root_t, root_s)) // 4
            coefficient = Q(t == s) - Q(inner, 2)
            if coefficient:
                terms.append([s, coefficient.numerator, coefficient.denominator])
                target_additions.append(["add", f"Y{t}", f"X{s}", str(coefficient), full_raw])
        if len(terms) != 48 or any(den != 2 or abs(num) != 1 for _, num, den in terms):
            raise ValueError("expected 48 off-diagonal half-coefficients")
        target_additions.append(["transport", f"Y{t}", full_raw, old_raw, 1])
        additions.extend(target_additions)
        target_records.append(dict(
            target=t,
            root=list(root_t),
            old_raw=old_raw,
            old_physical=list(old_physical),
            full_raw=full_raw,
            full_physical=list(full),
            terms=terms,
            up_recipe=up,
            down_recipe=down,
        ))

    corrected_program = witness["program"] + additions
    canonical_program = json.dumps(corrected_program, sort_keys=True, separators=(",", ":")).encode()
    cert = dict(
        schema_version=1,
        status="COMPILED_TERMINAL_P104_I_MINUS_G_OVER_2",
        predecessor_pr=1972,
        predecessor_head="fd82d172f46933fd253c2c6de4bd5eaff5429cfd",
        source_witness_sha256=hashlib.sha256(witness_bytes).hexdigest(),
        source_fixture_sha256=hashlib.sha256(fixture_bytes).hexdigest(),
        selected_record_sha256="10b9e340fd8e354a37a0c4813c90e5de1dd42044b5f6aca4a3fc5a42b685fa32",
        label_isometry=iso,
        port_roots=[list(v) for v in ports],
        cut_index=len(witness["program"]),
        target_records=target_records,
        added_events=len(additions),
        added_scalar_additions=sum(e[0] == "add" for e in additions),
        added_rank_profile={"1": 208},
        corrected_program_sha256=hashlib.sha256(canonical_program).hexdigest(),
        construction="append sparse (I-G/2) source scatter after source/dirty-helper restoration; each Y_t ascends to F9, receives 48 exact source terms, then returns to its endpoint hyperplane",
    )
    raw = (json.dumps(cert, sort_keys=True, indent=2) + "\n").encode()
    out = HERE / "CORRECTION.json.gz"
    packed = gzip.compress(raw, mtime=0)
    if out.exists() and not args.write:
        if out.read_bytes() != packed:
            raise ValueError("recorded certificate differs; rerun with --write after review")
        action = "MATCHES"
    else:
        out.write_bytes(packed)
        action = "WROTE"
    print(action, out.relative_to(ROOT), "targets=104 terms=4992 events=5200")


if __name__ == "__main__":
    main()
