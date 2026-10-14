#!/usr/bin/env python3
"""Independent replay of the terminal P104 I-G/2 side correction."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import argparse
import gzip
import hashlib
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
NATIVE_PATH = ROOT / "research/p104-native-channel/vendor/native_verify.py"
CEILING_PATH = ROOT / "research/complex-local-word-ceiling/ceiling.py"
WITNESS_PATH = ROOT / "research/p104-native-channel/inputs/LOWRANK-WITNESS.json"
FIXTURE_PATH = ROOT / "research/p104-native-channel/inputs/P104-FIXTURE.json"
SELECTED_PATH = ROOT / "certificates/selected-result.json"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def root_lines():
    out = set()
    for i, j in combinations(range(8), 2):
        for sign in (-1, 1):
            row = [0] * 8
            row[i], row[j] = 2, 2 * sign
            out.add(tuple(row))
    for signs in product((-1, 1), repeat=7):
        if signs.count(-1) % 2 == 0:
            out.add((1, *signs))
    need(len(out) == 120, "E8 root inventory")
    return sorted(out)


def inner(a, b):
    value = sum(x * y for x, y in zip(a, b))
    need(value % 4 == 0, "doubled root inner product is not integral")
    return value // 4


def canon(values):
    pivots = {}
    for value in values:
        reduced = value
        while reduced:
            j = reduced.bit_length() - 1
            if j in pivots:
                reduced ^= pivots[j]
            else:
                pivots[j] = reduced
                break
    for j in sorted(pivots):
        for k in pivots:
            if k > j and (pivots[k] >> j) & 1:
                pivots[k] ^= pivots[j]
    return tuple(pivots[j] for j in sorted(pivots, reverse=True))


@lru_cache(maxsize=None)
def frame_key(values):
    return canon(values)


def mv(rows, vector):
    return sum(((row & vector).bit_count() & 1) << i for i, row in enumerate(rows))


def inverse_binary(rows):
    n = len(rows)
    work = [row | (1 << (n + i)) for i, row in enumerate(rows)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if (work[r] >> col) & 1), None)
        need(pivot is not None, "compressed pairing matrix is singular")
        work[col], work[pivot] = work[pivot], work[col]
        for r in range(n):
            if r != col and ((work[r] >> col) & 1):
                work[r] ^= work[col]
    need([r & ((1 << n) - 1) for r in work] == [1 << i for i in range(n)],
         "compressed pairing inverse")
    return tuple(r >> n for r in work)


def physical_isometry(roots, iso):
    gram_rows = [sum(((inner(a, b) + 1) & 1) << j for j, b in enumerate(roots))
                 for a in roots]
    pivots = iso["pivot_root_indices"]
    need(len(pivots) == len(set(pivots)) == 9, "nine distinct root pivots")
    compressed = [sum(((row >> j) & 1) << k for k, j in enumerate(pivots))
                  for row in gram_rows]
    gram = [compressed[i] for i in pivots]
    need(gram == iso["compressed_gram"], "compressed Gram matrix")
    dual = inverse_binary(tuple(gram))
    need(list(dual) == iso["compressed_dual_gram"], "compressed Gram inverse")
    dot = lambda a, b: (a & mv(dual, b)).bit_count() & 1
    orthogonal = iso["orthonormal_basis_compressed"]
    need(len(orthogonal) == 9 and all(
        dot(a, b) == int(i == j)
        for i, a in enumerate(orthogonal) for j, b in enumerate(orthogonal)
    ), "orthonormal physical basis")
    transform = lambda x: sum(dot(x, v) << j for j, v in enumerate(orthogonal))
    physical = [transform(x) for x in compressed]
    need(physical == iso["physical_root_labels"] and len(set(physical)) == 120,
         "physical root images")
    for i in range(120):
        for j in range(120):
            need(((physical[i] & physical[j]).bit_count() & 1) == ((gram_rows[i] >> j) & 1),
                 "all 14,400 physical pairings")
    return compressed, physical, transform, dot, gram_rows


def roots_and_ports(fixture):
    roots = root_lines()
    removed = {tuple(x) for x in fixture["F0"] + fixture["C"]}
    need(len(removed) == 16, "fixture removes sixteen root lines")
    ports = [r for r in roots if r not in removed]
    need(len(ports) == 104, "P104 port count")
    return roots, ports


def correction_terms(ports, t):
    terms = []
    for s, root_s in enumerate(ports):
        coefficient = Q(int(t == s)) - Q(inner(ports[t], root_s), 2)
        if coefficient:
            terms.append([s, coefficient.numerator, coefficient.denominator])
    return terms


def exact_rational_rank(matrix):
    work = [[Q(x) for x in row] for row in matrix]
    if not work:
        return 0
    rows, cols, pivot_row = len(work), len(work[0]), 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if work[r][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [x / scale for x in work[pivot_row]]
        for r in range(rows):
            if r != pivot_row and work[r][col]:
                scale = work[r][col]
                work[r] = [x - scale * y for x, y in zip(work[r], work[pivot_row])]
        pivot_row += 1
    return pivot_row


def dirty_query_cut(witness):
    program = witness["program"]
    full = witness["final_frames"]["X0"]
    is_cleanup = lambda e: (e[0] == "add" and e[1].startswith("Q") and e[2].startswith("X")
                            and e[4] == full)
    start = len(program)
    while start and is_cleanup(program[start - 1]):
        start -= 1
    suffix = program[start:]
    need(len(suffix) == 416 and all(is_cleanup(e) for e in suffix),
         "pinned final query-restoration suffix")
    rows = {r: {r: Q(1)} for r in witness["initial_frames"]}
    for event in program[:start]:
        if event[0] == "add":
            _, dst, src, coefficient, _ = event
            factor = Q(coefficient)
            for name, value in list(rows[src].items()):
                total = rows[dst].get(name, Q(0)) + factor * value
                if total:
                    rows[dst][name] = total
                else:
                    rows[dst].pop(name, None)
        elif event[0] == "zero":
            rows[event[1]] = {}
        elif event[0] == "copy":
            rows[event[1]] = dict(rows[event[2]])
        elif event[0] == "erase":
            del rows[event[1]]
    for k in range(8):
        row = rows[f"Q{k}"]
        need(row.get(f"Q{k}") == 1, "dirty query keeps its independent initial value")
        need(sum(name.startswith("X") and value != 0 for name, value in row.items()) == 52,
             "gathered query source support")
        need(all(name == f"Q{k}" or name.startswith("X") for name in row),
             "query cut has only its own dirty input and source terms")
    return start


def append_events(witness, ports):
    full_raw = witness["final_frames"]["X0"]
    events, expected_terms = [], []
    for t in range(len(ports)):
        old_raw = witness["final_frames"][f"Y{t}"]
        need(len(frame_key(tuple(old_raw))) == 8, "target hyperplane rank")
        need(len(frame_key(tuple(full_raw))) == 9, "source full-frame rank")
        events.append(["transport", f"Y{t}", old_raw, full_raw, 1])
        terms = correction_terms(ports, t)
        need(len(terms) == 48 and all(den == 2 and abs(num) == 1 for _, num, den in terms),
             "48 exact off-diagonal half-coefficients per target")
        expected_terms.append(terms)
        for s, num, den in terms:
            events.append(["add", f"Y{t}", f"X{s}", str(Q(num, den)), full_raw])
        events.append(["transport", f"Y{t}", full_raw, old_raw, 1])
    return witness["program"] + events, events, expected_terms


def replay(program, witness, ports, wanted):
    frames = {r: list(f) for r, f in witness["initial_frames"].items()}
    rows = {r: {r: Q(1)} for r in frames}
    profile, scalar = Counter(), Counter()
    max_l1 = max(sum(abs(x) for x in row.values()) for row in rows.values())
    for index, event in enumerate(program):
        op = event[0]
        if op == "transport":
            _, reg, old, new, rank = event
            need(reg in frames and frame_key(tuple(frames[reg])) == frame_key(tuple(old)),
                 f"transport start at event {index}")
            old_key, new_key = frame_key(tuple(old)), frame_key(tuple(new))
            old_rank, new_rank = len(old_key), len(new_key)
            need(rank == abs(old_rank - new_rank) and rank > 0,
                 f"transport rank at event {index}")
            large, small = (new_key, old_key) if new_rank >= old_rank else (old_key, new_key)
            need(all(_in_span(v, large) for v in small), f"nested transport at event {index}")
            frames[reg] = list(new)
            profile[rank] += 1
        elif op == "add":
            _, dst, src, coefficient, chart = event
            need(dst in rows and src in rows, f"ADD register at event {index}")
            key = frame_key(tuple(chart))
            need(frame_key(tuple(frames[dst])) == key == frame_key(tuple(frames[src])),
                 f"ADD common chart at event {index}")
            factor = Q(coefficient)
            for name, value in list(rows[src].items()):
                total = rows[dst].get(name, Q(0)) + factor * value
                if total:
                    rows[dst][name] = total
                else:
                    rows[dst].pop(name, None)
            scalar["add"] += 1
            max_l1 = max(max_l1, sum(abs(x) for x in rows[dst].values()))
        elif op == "zero":
            _, reg, chart = event
            need(reg not in rows, f"private allocation at event {index}")
            rows[reg], frames[reg] = {}, list(chart)
            scalar["zero"] += 1
        elif op == "copy":
            _, dst, src, chart = event
            key = frame_key(tuple(chart))
            need(dst in rows and src in rows and not rows[dst], f"private copy at event {index}")
            need(frame_key(tuple(frames[dst])) == key == frame_key(tuple(frames[src])),
                 f"copy chart at event {index}")
            rows[dst] = dict(rows[src])
            scalar["copy"] += 1
            max_l1 = max(max_l1, sum(abs(x) for x in rows[dst].values()))
        elif op == "erase":
            _, reg, chart = event
            need(reg in rows and frame_key(tuple(frames[reg])) == frame_key(tuple(chart)),
                 f"private erase at event {index}")
            del rows[reg], frames[reg]
            scalar["erase"] += 1
        else:
            raise ValueError("unknown event type " + str(op))
    need(set(rows) == set(witness["initial_frames"]), "private storage lifetime")
    need(set(frames) == set(witness["final_frames"]), "frame lifetime")
    for reg, final_frame in witness["final_frames"].items():
        need(frame_key(tuple(frames[reg])) == frame_key(tuple(final_frame)), "final frame " + reg)
        expected = {reg: Q(1)}
        if wanted == "G/2" and reg.startswith("Y"):
            t = int(reg[1:])
            for s, root_s in enumerate(ports):
                c = Q(inner(ports[t], root_s), 2)
                if c:
                    expected[f"X{s}"] = c
        elif wanted == "identity" and reg.startswith("Y"):
            expected[f"X{int(reg[1:])}"] = Q(1)
        need(rows[reg] == expected, "arbitrary-input endpoint " + reg)
    return dict(profile=dict(sorted(profile.items())), scalar=dict(sorted(scalar.items())),
                rank_mass=sum(r * n for r, n in profile.items()), max_prefix_l1=str(max_l1))


def _in_span(value, frame):
    reduced = value
    pivots = {v.bit_length() - 1: v for v in frame if v}
    while reduced:
        pivot = reduced.bit_length() - 1
        if pivot not in pivots:
            return False
        reduced ^= pivots[pivot]
    return True


def check_certificate(cert, witness, fixture_bytes, ports, expected_events, expected_terms):
    witness_bytes = WITNESS_PATH.read_bytes()
    need(cert["source_witness_sha256"] == hashlib.sha256(witness_bytes).hexdigest(),
         "predecessor witness pin")
    need(cert["source_fixture_sha256"] == hashlib.sha256(fixture_bytes).hexdigest(),
         "fixture pin")
    selected_bytes = SELECTED_PATH.read_bytes()
    need(hashlib.sha256(selected_bytes).hexdigest() == cert["selected_record_sha256"],
         "selected-record pin")
    need(cert["predecessor_head"] == "fd82d172f46933fd253c2c6de4bd5eaff5429cfd",
         "PR1972 head")
    need(cert["port_roots"] == [list(x) for x in ports], "certificate port roots")
    need(cert["cut_index"] == len(witness["program"]), "terminal cut index")
    need(cert["added_events"] == len(expected_events) == 5200, "added event count")
    need(cert["added_scalar_additions"] == 4992, "added ADD count")
    need(cert["added_rank_profile"] == {"1": 208}, "added transition histogram")
    records = cert["target_records"]
    need(len(records) == len(ports), "104 native target recipes")
    for t, record in enumerate(records):
        need(record["target"] == t and record["root"] == list(ports[t]), "target/root binding")
        need(record["terms"] == expected_terms[t] and len(record["terms"]) == 48,
             "exact sparse I-G/2 row")
        need(record["old_raw"] == witness["final_frames"][f"Y{t}"], "target source frame")
        need(record["full_raw"] == witness["final_frames"]["X0"], "common full frame")


def check_native(cert, roots, witness):
    N = load_module("p104_side_correction_native", NATIVE_PATH)
    iso = cert["label_isometry"]
    compressed, physical, transform, dot, _ = physical_isometry(roots, iso)
    by_root = dict(zip(roots, compressed))
    physical_by_root = dict(zip(roots, physical))
    fixture = json.loads(FIXTURE_PATH.read_bytes())["section4_explicit_P104"]
    removed = {tuple(x) for x in fixture["F0"] + fixture["C"]}
    ports = [r for r in roots if r not in removed]
    for s, root in enumerate(ports):
        need(witness["initial_frames"][f"X{s}"] == [by_root[root]], "source label binding")
    full_physical = canon(transform(x) for x in witness["final_frames"]["X0"])
    need(len(full_physical) == 9, "physical full frame")
    total = 0
    for t, record in enumerate(cert["target_records"]):
        old_physical = canon(transform(x) for x in witness["final_frames"][f"Y{t}"])
        need(list(old_physical) == record["old_physical"], "physical target frame")
        need(list(full_physical) == record["full_physical"], "physical full-frame record")
        normal = physical_by_root[ports[t]]
        need(len(old_physical) == 8 and all(((x & normal).bit_count() & 1) == 0
                                            for x in old_physical),
             "physical target is the root hyperplane")
        for name, native_record, old, new in (
            ("up", record["up_recipe"], old_physical, full_physical),
            ("down", record["down_recipe"], full_physical, old_physical),
        ):
            need(native_record["rank"] == 1, "native rank-one recipe")
            N.equal(N.recipe(native_record), N.adjoint(N.frame(old, 9)) + N.frame(new, 9),
                    f"target {t} {name} transition including phase")
            total += 1
    need(total == 208, "all native correction transitions")
    return total


def build_expected(witness, ports):
    corrected, events, terms = append_events(witness, ports)
    digest = hashlib.sha256(json.dumps(corrected, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return corrected, events, terms, digest


def controls(cert, program, witness, ports, expected_terms):
    out = {}
    bad = deepcopy(cert)
    bad["target_records"][0]["terms"][0][1] *= -1
    try:
        check_certificate(bad, witness, FIXTURE_PATH.read_bytes(), ports,
                          append_events(witness, ports)[1], expected_terms)
    except ValueError:
        out["wrong_correction_coefficient"] = "REJECTED"
    else:
        raise ValueError("accepted wrong correction coefficient")

    bad_program = deepcopy(program)
    descent = next(i for i in range(len(witness["program"]), len(bad_program))
                   if bad_program[i][0] == "transport" and bad_program[i][1] == "Y0"
                   and bad_program[i][2] == witness["final_frames"]["X0"])
    del bad_program[descent]
    try:
        replay(bad_program, witness, ports, "identity")
    except ValueError:
        out["missing_target_descent"] = "REJECTED"
    else:
        raise ValueError("accepted missing target descent")

    N = load_module("p104_side_correction_native_control", NATIVE_PATH)
    bad_recipe = deepcopy(cert["target_records"][0]["up_recipe"])
    bad_recipe["left"]["phase"] = (bad_recipe["left"]["phase"] + 1) % 4
    try:
        t = cert["target_records"][0]
        N.equal(N.recipe(bad_recipe), N.adjoint(N.frame(t["old_physical"], 9))
                + N.frame(t["full_physical"], 9), "mutated native phase")
    except ValueError:
        out["wrong_native_phase"] = "REJECTED"
    else:
        raise ValueError("accepted wrong native phase")
    need(len(out) == 3, "all negative controls")
    return out


def run():
    witness_bytes, fixture_bytes = WITNESS_PATH.read_bytes(), FIXTURE_PATH.read_bytes()
    witness = json.loads(witness_bytes)
    fixture_doc = json.loads(fixture_bytes)
    roots, ports = roots_and_ports(fixture_doc["section4_explicit_P104"])
    coordinate_rank = exact_rational_rank(ports)
    gram_rank = exact_rational_rank([[inner(a, b) for b in ports] for a in ports])
    need(coordinate_rank == gram_rank == 8,
         "exact rational rank-eight P104 coordinates and Gram matrix")
    query_cut = dirty_query_cut(witness)
    cert = json.loads(gzip.decompress((HERE / "CORRECTION.json.gz").read_bytes()))
    program, events, terms, digest = build_expected(witness, ports)
    check_certificate(cert, witness, fixture_bytes, ports, events, terms)
    need(cert["corrected_program_sha256"] == digest, "complete corrected-program digest")

    # The first replay binds the source construction at its declared G/2 endpoint.
    base = replay(witness["program"], witness, ports, "G/2")
    corrected = replay(program, witness, ports, "identity")
    need(base["max_prefix_l1"] == "106", "pinned base prefix L1")
    need(corrected["max_prefix_l1"] == "106", "correction preserves prefix L1 ceiling")
    need(corrected["profile"] == {1: 1282, 2: 58, 3: 86, 4: 104, 5: 48, 6: 24, 7: 8, 8: 8},
         "corrected transport profile")
    need(corrected["rank_mass"] == 2576, "corrected rank mass")
    need(corrected["scalar"].get("add") == 7616, "base plus correction ADD count")
    need(len(events) == 5200 and sum(e[0] == "add" for e in events) == 4992,
         "correction event invoice")

    native_transitions = check_native(cert, roots, witness)
    full_key = frame_key(tuple(witness["final_frames"]["X0"]))
    target_path_floor = 0
    for t in range(104):
        target_key = frame_key(tuple(witness["final_frames"][f"Y{t}"]))
        need(len(full_key) - len(target_key) == 1 and all(_in_span(v, full_key) for v in target_key),
             "rank-one terminal target/full nesting")
        need(correction_terms(ports, t), "each target requires a nonzero correction")
        # A source ADD can share a chart with Y_t only at the full source frame.
        # Any path from rank 8 to rank 9 and back has total paid rank at least 2.
        target_path_floor += 2 * (len(full_key) - len(target_key))
    need(target_path_floor == native_transitions == 208,
         "rank-one excursions attain the exact per-target terminal path floor")

    ceiling = load_module("p104_candidate_ceiling", CEILING_PATH)
    selected = json.loads(SELECTED_PATH.read_bytes())
    selected_kappa = Q(selected["kappa"])
    selected_a = selected_kappa / (1 - selected_kappa)
    local_profile = corrected["profile"]
    moment = ceiling.relax(local_profile, 73, 896, 9, 64, selected_a)
    need(moment[1] < 1, "optimistic local relaxation clears selected saving parameter")
    a_lo, a_hi = ceiling.ceiling(local_profile, 73, 896, 9, 64)
    model = ceiling.model(local_profile, 73, 896, 9, 64)
    kappa_cap = a_hi / (1 + a_hi)

    mutation_controls = controls(cert, program, witness, ports, terms)
    return dict(
        status="PASS_TERMINAL_P104_SIDE_CORRECTION_FRAME_MODEL",
        provenance=dict(predecessor_pr=1972, predecessor_head=cert["predecessor_head"],
                        source_witness_sha256=hashlib.sha256(witness_bytes).hexdigest(),
                        source_fixture_sha256=hashlib.sha256(fixture_bytes).hexdigest(),
                        selected_record_sha256=hashlib.sha256(SELECTED_PATH.read_bytes()).hexdigest()),
        geometry=dict(roots=120, ports=104, coordinate_rank=coordinate_rank, gram_rank=gram_rank,
                      off_diagonal_nonzeros_per_row=48, correction_nonzeros=4992,
                      all_exact_coefficients="+/-1/2"),
        cut=dict(index=cert["cut_index"], source_frame_rank=9, target_frame_rank=8,
                 helpers_restored_before_correction=True,
                 excluded_dirty_query_cut_index=query_cut,
                 each_query_retains_its_independent_initial_input=True),
        correction=dict(scalar_additions=4992, target_transitions=native_transitions,
                        terminal_frame_path_floor=target_path_floor,
                        path_floor_reason="Every nonzero source ADD needs the common rank-9 source frame; each rank-8 target starts and ends at rank 8, so its nested transport path has paid rank at least 1+1.",
                        added_rank_profile={"1": 208}, new_helpers=0, new_copies=0,
                        new_helper_restoration=0, corrected_program_events=len(program),
                        corrected_program_sha256=digest),
        replay=dict(base=base, corrected=corrected, controls=mutation_controls),
        optimistic_selected_coverage_screen=dict(
            model=dict(m=73, live_families="896/9", stages=9, centre_per_call=64,
                       idle_rank_cap=model["R"], idle_mass=str(model["idle_mass"])),
            selected_kappa=str(selected_kappa), selected_a=str(selected_a),
            moment_at_selected_a=[str(x) for x in moment],
            a_ceiling=[str(a_lo), str(a_hi)],
            kappa_ceiling=str(kappa_cap),
            limitation="Same coverage-law substitution with fractionally repacked rank-<=51 idle mass; not a realized owner map, global supplier, precision proof, all-size lift or new kappa."),
        scope="Exact finite 104-port terminal I-G/2 correction appended after the pinned G/2 channel. The sparse output correction adds only rank-one target frame excursions; complete multiplication admission remains open.",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run()
    text = json.dumps(result, sort_keys=True, indent=2) + "\n"
    result_path = HERE / "RESULT.json"
    if args.write:
        result_path.write_text(text)
    else:
        need(result_path.read_text() == text, "RESULT.json differs; run verify.py --write after a reviewed change")
    print("PASS_TERMINAL_P104_SIDE_CORRECTION_FRAME_MODEL",
          "targets=104 terms=4992 rank1=208 rank_mass=2576",
          "a_ceiling=" + str(float(Q(result["optimistic_selected_coverage_screen"]["a_ceiling"][1]))))


if __name__ == "__main__":
    try:
        main()
    except (KeyError, IndexError, TypeError, ValueError, OSError) as error:
        print("FAIL:", error)
        raise SystemExit(1)
