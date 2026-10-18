"""Source-derived K column and one-bank ideal consumer oracle.

Clear1nsight, with substantial OpenAI assistance. Apache-2.0.
The authenticated PR3467 codec and PR3382 Gaussian arithmetic are reused with
credit. Independent literal.py and observable.py import none of that code.
"""

from collections import Counter, deque
from fractions import Fraction
import hashlib
import json


SIZE = 512
ZERO = (0, 0)
WATCH = (1099, 2121, 3278, 4241, 5086, 5397)
BANKS = ("Q0", "G0", "X0")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def fraction(value):
    return [value.numerator, value.denominator]


def scaled(values, factor):
    out = []
    for real, imag in values:
        parts = (factor * real, factor * imag)
        require(all(x.denominator == 1 for x in parts), "integral oracle field")
        out.append(tuple(x.numerator for x in parts))
    return out


def symbolic(word):
    """Propagate one symbolic paired input, including every late sign."""
    program = word["program"]
    state = {bank: Fraction(0) for bank in word["initial_frames"]}
    state["Y91"], state["Y90"] = Fraction(1), Fraction(-1)
    frames = {bank: list(frame) for bank, frame in word["initial_frames"].items()}
    counts, stored_denominators, product_denominators = Counter(), Counter(), Counter()
    snapshots, erasures, observed = {}, [], []
    maximum = Fraction(1)
    for event, row in enumerate(program):
        op, target = row[:2]
        counts[op] += 1
        if op == "transport":
            require(frames[target] == row[2], "symbolic source frame")
            frames[target] = list(row[3])
        elif op == "add":
            source = row[2]
            require(frames[target] == frames[source] == row[4], "symbolic common frame")
            product = Fraction(str(row[3])) * state[source]
            require(4 % product.denominator == 0, "ADD product quarter denominator")
            product_denominators[str(product.denominator)] += 1
            state[target] += product
        elif op == "sign":
            require(str(row[2]) == "-1" and frames[target] == row[3], "symbolic sign")
            state[target] = -state[target]
        elif op == "zero":
            require(target not in state, "symbolic private allocation")
            state[target], frames[target] = Fraction(0), list(row[2])
        else:
            require(op == "erase" and state[target] == 0 and frames[target] == row[2],
                    "symbolic private erasure")
            erasures.append(event)
            del state[target], frames[target]
        if target in state:
            value = state[target]
            require(4 % value.denominator == 0, "stored quarter denominator")
            stored_denominators[str(value.denominator)] += 1
            maximum = max(maximum, abs(value))
        if event == 2024:
            observed = [state[b] for b in ("D31", "D30", "D29", "D28", "D27", "Q7")]
        if event in WATCH:
            snapshots[str(event)] = {
                bank: {"coefficient": state[bank], "frame": list(frames[bank])}
                for bank in BANKS}
    require(frames == word["final_frames"], "all symbolic final frames")
    require(observed == [0] * 6, "six original collector fields vanish")
    require(state["X0"] == Fraction(-1, 2), "late signed X0 response")
    require(state["Q0"] == state["D1"] == state["G0"] == 0, "named dirty return")
    require(counts == {"transport": 2070, "add": 3104, "sign": 208, "zero": 8, "erase": 8},
            "all five actual opcode kinds")
    require(stored_denominators == {"1": 4928, "2": 390, "4": 72}
            and product_denominators == {"1": 3006, "2": 52, "4": 46},
            "complete all-u denominator certificate")
    return {"snapshots": snapshots, "final": state, "receipt": {
        "opcode_counts": dict(counts), "stored_denominators": dict(stored_denominators),
        "ADD_product_denominators": dict(product_denominators),
        "maximum_absolute_normalised_coefficient": fraction(maximum),
        "erasure_events": erasures, "six_first_collector_coefficients": [fraction(x) for x in observed],
        "final_nonzero_coefficients": {b: fraction(x) for b, x in state.items() if x},
        "scope": "One symbolic paired family, every5398 event, including all208 signs; no rank census."}}


def chart_paths(word):
    """Short source-authenticated chart paths, distinct from literal bank histories."""
    edges = {}
    for event, row in enumerate(word["program"]):
        if row[0] == "transport":
            old, new = tuple(row[2]), tuple(row[3])
            edges.setdefault(old, []).append((new, event, False))
            edges.setdefault(new, []).append((old, event, True))
    paths, queue = {(): []}, deque([()])
    while queue:
        old = queue.popleft()
        for new, event, inverse in edges.get(old, []):
            if new not in paths:
                paths[new] = paths[old] + [(event, inverse)]
                queue.append(new)
    return paths


def collector_inventory(word, plans):
    rows = word["program"][2114:2129]
    counts = Counter(row[0] for row in rows)
    require(counts == {"zero": 1, "add": 11, "transport": 2, "erase": 1},
            "actual eighth collector shape")
    wrapper_rows, phases = [], Counter()
    for event in (2120, 2122):
        require(plans[event]["rank"] == 7, "actual eighth collector rank")
        for side in ("right", "left"):
            plan = plans[event][side]
            permutation = [x for x, _ in plan]
            require(sorted(permutation) == list(range(SIZE)), "wrapper permutation")
            visited, cycles = set(), 0
            for start in range(SIZE):
                if start in visited:
                    continue
                cycles += 1
                current = start
                while current not in visited:
                    visited.add(current)
                    current = permutation[current]
            wrapper_phases = Counter(str(p) for _, p in plan)
            require(wrapper_phases == {str(i): 128 for i in range(4)},
                    "each actual wrapper has all four phase classes")
            phases.update(wrapper_phases)
            wrapper_rows.append({"event": event, "side": side, "cycles": cycles,
                                 "Gaussian_SWAP": SIZE - cycles,
                                 "phase_histogram": dict(wrapper_phases)})
    require([r["cycles"] for r in wrapper_rows] == [64, 64, 128, 48], "wrapper cycle inventory")
    require(phases == {str(i): 512 for i in range(4)}, "wrapper phase inventory")
    return {"events": [2114, 2128], "counts": dict(counts), "native_rank_mass": 14,
            "completed_native_pairs": 3584, "real_ADD_SUB_before_SWAP_phase_lowering": 39936,
            "native_floor_halves": 14336, "native_Gaussian_quarter_turns": 3584,
            "wrappers": wrapper_rows, "wrapper_Gaussian_SWAPs": 1744,
            "wrapper_phase_histogram": dict(phases), "owned_zero_Gaussian_banks": 1,
            "scope": "Existing eighth collector only. Both transports, all four wrappers and cleanup included; no physical or recursive price inferred."}


def analyze(word, native, modules):
    source, classifier, admission, model = [modules[n] for n in ("source", "classifier", "admission", "model")]
    structure = source.structure(word, native)
    paths = chart_paths(word)
    path_events = {e for path in paths.values() for e, _ in path}
    plans = source.native_plans(word, native, sorted(path_events | set(structure["selected"]) | {2120, 2122}), model)
    parameters = [[ZERO] * SIZE for _ in range(52)]
    parameters[44][15] = (1, 0)
    initial_y = admission.encode_sources(structure, plans, model, source, classifier, parameters)
    recovered = admission.decode_sources(structure, plans, model, source, classifier, initial_y)
    require(recovered == parameters, "exact K column and return")
    p = initial_y["Y91"]
    require(initial_y["Y90"] == [(-r, -i) for r, i in p], "opposite prepared Y sources")
    require({b for b, value in initial_y.items() if any(z != ZERO for z in value)} == {"Y90", "Y91"},
            "complete K column support")
    require(model.member(p), "p belongs to B9")
    require(any(x % 4 for z in model.decode(p) for x in z), "p outside4B9")
    gap = structure["gaps"][44]
    require(gap["kind"] == "zero" and gap["event"] == 1817 and gap["next_event"] == 1819,
            "exact inherited coefficient meaning")
    profile = source.apply_path(p, gap["path_to_read"], plans, model)
    require(profile == [(-4, 0) if k & 15 == 15 else ZERO for k in range(SIZE)], "E9 delta15 profile")
    scalar = symbolic(word)
    images = {(): p}

    def image(frame):
        key = tuple(frame)
        if key not in images:
            require(key in paths, "reachable canonical chart")
            values = p
            for event, inverse in paths[key]:
                values = source.apply_native(values, event, plans, model, inverse=inverse)
            require(model.member(values), "oracle frame image is in B9")
            images[key] = values
        return images[key]

    arrays = {cut: {bank: {"frame": item["frame"], "values": scaled(image(item["frame"]), 4 * item["coefficient"])}
                     for bank, item in row.items()}
              for cut, row in scalar["snapshots"].items()}
    final_ys = {bank: scaled(image(word["final_frames"][bank]), 4 * scalar["final"][bank])
                for bank in ("Y90", "Y91")}
    return {"p": p, "expected_checkpoints": arrays, "expected_final_Y": final_ys,
            "receipt": {"coefficient_column": {"slot": 44, "mask": 15, "source_support": ["Y91", "Y90"],
                            "p_sha256": digest(p), "nonzero_coordinates": sum(z != ZERO for z in p),
                            "component_height": max(abs(x) for z in p for x in z), "in_B9": True,
                            "in_4B9": False, "K_inverse_returns_coefficients": True, "gap": gap},
                        "symbolic": scalar["receipt"], "collector": collector_inventory(word, plans),
                        "chart_oracle_paths": {str(list(k)): paths[k] for k in images},
                        "strong_checkpoint_hashes": {cut: {b: digest(item["values"]) for b, item in row.items()}
                                                      for cut, row in arrays.items()}}}
