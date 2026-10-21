#!/usr/bin/env python3
"""Exact scoped upper bound for the frozen fixed-window native packing model.

This proof uses no optimizer. The linear dual is displayed symbolically and
each nontrivial inequality is certified throughout the mixed-root interval.
Apache-2.0; native source construction: PR4359 and its retained credits.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import importlib.util
import json

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE_ROOT = HERE.parents[1]
ENGINE_HASH = "4a51eea1d796224e4a8bb6e2031146ba743e63ed88b2e7e241093a7025a063de"
NATIVE_PRODUCER_HASH = "9edf27738981b58c2bf8ca03bb70631c200aad0ca9948372f1c58fc445894da0"
NATIVE_RECEIPT_HASH = "5c8cc831151aa7147e6c3dd2a6832d19026aecc660955131149bdc54f0b26878"
LOW = Q("0.002312854665364207351198238279")
HIGH = Q("0.002312854665364207351198238280")
STOCK = {5: 28, 6: 18, 7: 56, 8: 93, 9: 213}
WIDTHS = (0, 5, 6, 7, 8, 9)
TARGETS = {5: 140, 6: 52, 7: 56, 8: 93, 9: 1229, 25: 448, 57: 224}
PAID = {1: 17559, 2: 5027, 3: 1738, 4: 714, 5: 254}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def clean(p):
    return {int(r): Q(v) for r, v in sorted(p.items()) if v}


def plus(*parts):
    out = Counter()
    for coefficient, polynomial in parts:
        for rank, value in polynomial.items():
            out[rank] += Q(coefficient)*value
    return clean(out)


def h(rank):
    return {rank: Q(1)} if rank else {}


def split(rank):
    out = {5: rank//5}
    if rank % 5:
        out[rank % 5] = out.get(rank % 5, 0)+1
    return clean(out)


def gain(capacity, pattern):
    return plus((1, split(capacity)), (-1, split(capacity-sum(pattern))),
                *((-1, h(rank)) for rank in pattern if rank))


def build(source_root):
    native_path = HERE.parent/"kappa-4359-native-packing/verify.py"
    receipt_path = native_path.with_name("CERTIFICATE.json")
    require(sha256(native_path.read_bytes()).hexdigest() == NATIVE_PRODUCER_HASH
            and sha256(receipt_path.read_bytes()).hexdigest() == NATIVE_RECEIPT_HASH,
            "immutable native source and attainable construction certificate")
    native_spec = importlib.util.spec_from_file_location("fixed_window_native_source", native_path)
    native_module = importlib.util.module_from_spec(native_spec)
    native_spec.loader.exec_module(native_module)
    native_engine, original, previous, helpers, source_pins = native_module.load_predecessor(source_root)
    receipt = json.loads(receipt_path.read_text())
    replayed_native, _ = native_module.build(source_root)
    require(json.loads(json.dumps(replayed_native)) == receipt,
            "the entire frozen native certificate is reproduced from authenticated source bytes")
    require({int(rank): count for rank, count in receipt["new_profile"]["targets"].items()} == TARGETS
            and {int(rank): count for rank, count in receipt["new_profile"]["paid"].items()} == PAID,
            "the attained polynomial is exactly the frozen native invoice")
    require(list(map(Q, receipt["root_bracket"])) == [LOW, HIGH], "the same exact attained mixed-root interval")
    require(Counter(row["width"] for row in helpers["recipes"]) == STOCK,
            "complete actual per-stage native helper stock")
    native_word = native_engine.read_json(source_root/native_module.NATIVE)
    local_paid = {1: 2487, 2: 713, 3: 232, 4: 102, 5: 28}
    for direction in ("forward", "backward"):
        require(Counter(event[-1] for event in native_word[direction] if event[0] in ("climb", "center"))
                == local_paid, "the entire actual oriented local paid word is fixed")
    families = defaultdict(list)
    for row in previous["windows"]:
        families[row["family"]].append(row)
    require(set(families) == {0, 1, 2, 3}
            and all(len(rows) == 224 for rows in families.values()), "actual fixed owner counts")
    require({family: {tuple(row["stages"]) for row in rows} for family, rows in families.items()}
            == {0: {(0, 1)}, 1: {(2,)}, 2: {(4,)}, 3: {(5, 6)}},
            "the four family resource stages are disjoint")
    require(all(len(row["axes"]) == (16 if family in (0, 3) else 8)
                for family, rows in families.items() for row in rows), "actual fixed window capacities")
    path = HERE.parent/"kappa-4359-outer-endpoint/verify.py"
    require(sha256(path.read_bytes()).hexdigest() == ENGINE_HASH, "reviewed rational interval engine")
    spec = importlib.util.spec_from_file_location("fixed_window_interval_engine", path)
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    powers = {}

    def enclose(polynomial):
        low = high = Q(0)
        for rank, coefficient in polynomial.items():
            if rank not in powers:
                # Each rank^(1-C) decreases in C, giving a simultaneous
                # enclosure for every C in the entire closed root bracket.
                powers[rank] = (engine.rank_power(rank, HIGH)[0],
                                engine.rank_power(rank, LOW)[1])
            a, b = powers[rank]
            low += coefficient*(a if coefficient >= 0 else b)
            high += coefficient*(b if coefficient >= 0 else a)
        return low, high

    def encode_poly(polynomial):
        return {rank: str(value) for rank, value in polynomial.items()}

    def certify(polynomial, message):
        interval = enclose(polynomial)
        require((not polynomial and interval == (0, 0)) or interval[0] > 0, message)
        return {"polynomial": encode_poly(polynomial),
                "interval": engine.encode(interval), "identically_zero": not polynomial}

    # Per-wide-window dual: one price for a physical owner, plus nonnegative
    # prices for the limited width-seven and width-eight helper inventories.
    owner_price = gain(16, (6, 9))
    seven_price = plus((1, gain(16, (7, 9))), (-1, owner_price))
    eight_price = plus((Q(1, 2), gain(16, (8, 8))), (-Q(1, 2), owner_price))
    prices = {
        "owner": certify(owner_price, "nonnegative per-owner dual price"),
        "width7": certify(seven_price, "nonnegative width-seven resource dual price"),
        "width8": certify(eight_price, "nonnegative width-eight resource dual price"),
    }
    wide_rows = []
    for pattern in product(WIDTHS, repeat=2):
        if sum(pattern) > 16:
            continue
        bound = plus((1, owner_price), (pattern.count(7), seven_price),
                     (pattern.count(8), eight_price))
        gap = plus((1, bound), (-1, gain(16, pattern)))
        wide_rows.append({"pattern": pattern,
                          "dual_gap": certify(gap, "valid wide-pattern dual inequality "+str(pattern))})
    require(len(wide_rows) == 33, "complete fixed-window pattern enumeration")
    wide_upper = plus((224, owner_price), (112, seven_price), (186, eight_price))
    wide_attained = plus((93, gain(16, (8, 8))), (56, gain(16, (7, 9))),
                         (56, gain(16, (9, 7))), (18, gain(16, (6, 9))),
                         (1, gain(16, (9, 6))))
    require(wide_upper == wide_attained, "the integral published assignment attains the dual bound identically")
    # All nonzero-price resources are fully used. There is enough actual
    # width-six/nine stock for the displayed tight patterns at each stage.
    selected = {(8, 8): 93, (7, 9): 56, (9, 7): 56, (6, 9): 18, (9, 6): 1}
    for stage in (0, 1):
        used = Counter()
        for pattern, count in selected.items():
            used[pattern[stage]] += count
        require(all(used[rank] <= count for rank, count in STOCK.items()), "actual stage inventory is feasible")
        require(used[7] == STOCK[7] and used[8] == STOCK[8], "every priced stock constraint is saturated")

    # A rank-eight window has only one helper slot, and widths nine do not
    # fit. Gains for zero and width five vanish identically; every other
    # eligible width has positive gain, and all are already hosted.
    middle_rows = []
    for rank in (0, 5, 6, 7, 8):
        middle_rows.append({"pattern": [rank], "gain": certify(gain(8, (rank,)),
                                                                  "nonnegative single-window gain")})
    middle_upper = plus(*((STOCK[rank], gain(8, (rank,))) for rank in (5, 6, 7, 8)))
    require(sum(STOCK[rank] for rank in (5, 6, 7, 8)) == 195 <= 224,
            "all nonnegative eligible stocks fit the exact middle-window owner count")

    # Start with every helper on a fresh native-width field and every idle
    # window paid in full. The exact gain upper bounds reconstruct precisely
    # the published mixed polynomial, so no hidden rank credit is introduced.
    initial_targets = {25: 448, 57: 224, **{rank: 7*count for rank, count in STOCK.items()}}
    initial_paid = plus((7, local_paid), (448, split(16)), (448, split(8)))
    base_moment = plus((1, initial_targets), (-1, initial_paid))
    optimal_moment = plus((1, base_moment), (2, wide_upper), (2, middle_upper))
    published_moment = plus((1, TARGETS), (-1, PAID))
    require(optimal_moment == published_moment, "exact full-invoice upper bound equals the published polynomial")
    low_margin = engine.mixed_margin(TARGETS, PAID, LOW)
    high_margin = engine.mixed_margin(TARGETS, PAID, HIGH)
    require(low_margin[0] > 0 and high_margin[1] < 0,
            "the unique published root lies in the interval")
    require(min(STOCK) == max(local_paid) == 5 and all(rank > 5 for rank in (25, 57)),
            "all variable source ranks are at least five, paid ranks are at most five, and fixed sources exceed five")
    require(sum(rank*count for rank, count in initial_targets.items())
            - sum(rank*count for rank, count in initial_paid.items()) == 224,
            "every packing retains the exact positive rank surplus because every hosted axis removes one paid axis")
    require(sum(initial_targets.values()) < sum(local_paid.values())*7,
            "even the maximum possible source count is smaller than the unchanged local paid count")
    strict_count = sum(not row["dual_gap"]["identically_zero"] for row in wide_rows)
    tight_patterns = [row["pattern"] for row in wide_rows if row["dual_gap"]["identically_zero"]]
    return {
        "schema": "fixed-native-window-packing-dual-limit/1",
        "status": "PASS_EXACT_SCOPED_DUAL_UPPER_BOUND_AT_ENTIRE_ROOT_INTERVAL",
        "interval_engine_sha256": ENGINE_HASH,
        "native_producer_sha256": NATIVE_PRODUCER_HASH,
        "native_receipt_sha256": NATIVE_RECEIPT_HASH,
        "native_replay_status": replayed_native["status"],
        "source_sha256": source_pins,
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE/"PROOF.md").read_bytes()).hexdigest(),
        "saving_interval": [str(LOW), str(HIGH)],
        "root_endpoint_margins": [engine.encode(low_margin), engine.encode(high_margin)],
        "native_stock_per_stage": STOCK,
        "local_paid_word_per_stage": local_paid,
        "fixed_main_targets": {25: 448, 57: 224},
        "fixed_window_families": [
            {"family": family, "stages": rows[0]["stages"],
             "owners": len(rows), "capacity": len(rows[0]["axes"])}
            for family, rows in sorted(families.items())
        ],
        "owner_and_resource_prices": prices,
        "wide_patterns": wide_rows, "strict_wide_inequalities": strict_count,
        "identically_tight_wide_patterns": tight_patterns,
        "middle_patterns": middle_rows,
        "wide_upper": encode_poly(wide_upper), "middle_upper": encode_poly(middle_upper),
        "complete_optimal_moment": encode_poly(optimal_moment),
        "root_comparison": {
            "scaled_moment": "M(t)/5^t",
            "strictly_increasing_in_t": True,
            "reason": "Every source rank is at least 5, every paid rank is at most 5, and fixed rank-57 sources have positive multiplicity.",
            "all_profile_rank_surpluses": 224,
            "maximum_possible_productive_fields": sum(initial_targets.values()),
            "unchanged_local_paid_calls": sum(local_paid.values())*7,
            "conclusion": "Every admitted packing has a unique mixed root in (0,1), no greater than the attained root inside the certified bracket.",
        },
        "no_optimizer_used": True,
        "scope": [
            "The original four idle families, stages, 224 owners per family, and exact per-stage helper-width inventories are fixed.",
            "Each rank16 window hosts at most one helper in each of its two native stage slots, on disjoint slices of its original 16 axes.",
            "Each rank8 window hosts at most one helper, on a slice of its original eight axes.",
            "All remaining helpers are independent fresh outputs at their native widths; all residual axes use the existing maximal-rank-five split.",
            "The native local words, complete local paid invoice, and main productive endpoints remain fixed.",
            "Assignments can be asymmetric between stages or families; any native role may be exchanged within its actual stage inventory, with its fresh owner set rebuilt.",
            "The symbolic nonnegative dual prices bound every integral packing in this model, even its fractional relaxation, throughout the root interval.",
            "The published integral construction attains the bound identically; its exact native feasibility is established in its separate frozen certificate.",
            "This is a scoped mathematical upper bound. It is not an assertion of solver optimality or of global optimality over other controllers, native words, or compiler interfaces.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--out", type=Path)
    action.add_argument("--check", "--check-only", action="store_true")
    args = parser.parse_args()
    result = build(args.source_root.resolve())
    text = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.out:
        args.out.write_text(text)
    else:
        require((HERE/"CERTIFICATE.json").read_text() == text,
                "committed scoped packing-limit receipt differs from exact replay")
    print(json.dumps({key: result[key] for key in ("status", "strict_wide_inequalities",
                                                "identically_tight_wide_patterns", "complete_optimal_moment")}, sort_keys=True))


if __name__ == "__main__":
    main()
