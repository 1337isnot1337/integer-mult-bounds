#!/usr/bin/env python3
"""Independent XOR-span reconstruction of #2979's V45 frame group and invoice arithmetic.

This checks the source-bound local frame/profile arithmetic and cross-checks the
published T74 aggregate numerically. It does not rebuild stages 2/3, owners,
chronology, native admission, or the exact outer release.
"""
from collections import Counter
from copy import deepcopy
from decimal import Decimal as D, localcontext
from fractions import Fraction as Q
from functools import lru_cache
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PKG = ROOT / "research" / "rank7-joint-endframes"


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def read(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw)


@lru_cache(maxsize=100_000)
def _span(vectors):
    """Return an F2 span by explicit closure, independent of RREF implementations."""
    out = {0}
    for v in vectors:
        old = tuple(out)
        out.update(x ^ v for x in old)
    return frozenset(out)


def span(vectors):
    return _span(tuple(vectors))


def rank(vectors):
    n = len(span(vectors))
    need(n and n & (n - 1) == 0, "span cardinality is not a power of two")
    return n.bit_length() - 1


def inside(a, b):
    return span(a).issubset(span(b))


def dot_parity(a, b):
    return (a & b).bit_count() & 1


def profile(word):
    full = span([1 << i for i in range(9)])
    ends = [full] * 112
    ends += [span(z for z in range(1, 512) if not dot_parity(z, p)) for p in word["ports"]]
    ends += [full] * 480
    starts = [span([p]) for p in word["ports"]] + [frozenset()] * 592
    for r, rows in word["start_extra"].items():
        starts[int(r)] = span(rows)
    for r, rows in word["helper_final"].items():
        ends[int(r)] = span(rows)

    current = list(starts)
    paid = Counter()

    def climb(r, rows):
        rows = span(rows)
        need(inside(current[r], rows), f"nonmonotone register {r}")
        d = rank(rows) - rank(current[r])
        if d:
            paid[d] += 1
        current[r] = rows

    def step(gate):
        if gate[0] == "warp":
            need(current[gate[1]] == span(gate[3]), "warp entry frame")
            current[gate[1]] = span(gate[4])
        elif gate[0] == "add":
            climb(gate[1], gate[-1])
            climb(gate[2], gate[-1])
        elif gate[0] == "scale":
            climb(gate[1], gate[-1])
        else:
            raise AssertionError(("unknown gate", gate[0]))

    for gate in word["A"]:
        step(gate)
    for r, rows in zip(word["centers"], word["center_frames"]):
        need(current[r] == span(rows), f"center entry frame {r}")
        levels = []
        for cut in word["cut"]:
            if cut[2] == r:
                levels.append(span(word["target_levels"].get(str(cut[1] - 112), [])))
        rows = span(rows)
        for target in sorted(set(levels), key=len, reverse=True):
            if rows != target:
                paid[rank(rows) - rank(target)] += 1
            rows = target
    warps = {}
    for entry in word["warps"]:
        warps.setdefault(entry[0], []).append(entry)
    for pos in range(len(word["B"]) + 1):
        for entry in warps.get(pos, []):
            need(current[entry[1]] == span(entry[3]), "B warp entry frame")
            current[entry[1]] = span(entry[4])
        if pos < len(word["B"]):
            step(word["B"][pos])
    for gate in word["restore"]:
        step(gate)

    live = set(range(704)) - set(word["removed"])
    for r in live:
        climb(r, ends[r])
    inventory = Counter(rank(ends[r]) - rank(starts[r]) for r in live if r >= 224)
    return dict(sorted(paid.items())), dict(sorted(inventory.items()))


def roles(gate):
    return set(gate[1:3] if gate[0] == "add" else gate[1:2])


def apply_groups(parent, record, chosen):
    out = deepcopy(parent)
    changed = []
    for name in chosen:
        W, helpers = record["groups"][name]
        W = span(W)
        for h in helpers:
            row = record["helper_final_changes"][str(h)]
            need(parent["helper_final"][str(h)] == row["old"], "helper old-frame pin")
            need(span(row["new"]) == W and rank(row["new"]) == 7, "shared rank-7 helper endpoint")
            need(inside(row["new"], row["old"]), "helper endpoint containment")
            out["helper_final"][str(h)] = list(row["new"])
    for edit in record["frame_edits"]:
        owners = [name for name, (W, _) in record["groups"].items() if inside(edit["new_frame"], W)]
        need(len(owners) == 1, ("unique frame-edit owner", edit["section"], edit["index"], owners))
        name = owners[0]
        if name not in chosen:
            continue
        section, i = edit["section"], edit["index"]
        gate = out[section][i]
        need(gate[:-1] == edit["gate"] and span(gate[-1]) == span(edit["old_frame"]), "gate preimage pin")
        need(rank(edit["new_frame"]) == rank(edit["old_frame"]) - 1, "gate codimension one")
        need(inside(edit["new_frame"], edit["old_frame"]), "gate hyperplane containment")
        need(inside(edit["new_frame"], record["groups"][name][0]), "gate is inside shared W")
        gate[-1] = list(edit["new_frame"])
        changed.append((name, section, i))
    for name in chosen:
        W = record["groups"][name][0]
        for h in record["groups"][name][1]:
            for section in ("A", "B", "restore"):
                for i, gate in enumerate(out[section]):
                    if h in roles(gate):
                        need(inside(gate[-1], W), ("lowered-helper event outside W", name, h, section, i))
    return out, changed


def price(profile_, weights):
    return sum(weights[r] * n for r, n in profile_.items())


def dec_fraction(value):
    q = Q(value)
    return D(q.numerator) / D(q.denominator)


def decimal_root(profile_, replicas):
    """High-precision numerical cross-check; intentionally not an exact certificate."""
    with localcontext() as ctx:
        ctx.prec = 90
        denominator = D(73 * 896 * replicas)

        def moment(b):
            terms = []
            for r, n in profile_.items():
                base = D(73) / D(r)
                terms.append(D(n) * D(r) * (b * base.ln()).exp())
            return sum(terms, D(0)) / denominator

        low, high = D(0), D("0.01")
        need(moment(low) < 1 < moment(high), "T74 moment root bracket")
        for _ in range(320):
            mid = (low + high) / 2
            if moment(mid) < 1:
                low = mid
            else:
                high = mid
        root = (low + high) / 2
        return root, moment(root) - 1


def main():
    selected = read(ROOT / "certificates/selected-result.json")
    record = read(PKG / "data/STAGE1-FRAME-EDITS.json")
    prices = read(PKG / "construction/STAGE-PRICES.json")
    claim = read(PKG / "CLAIM.json")
    cap = read(PKG / "certificates/RELAX-CAP.json")
    allocation = {int(k): int(v) for k, v in read(PKG / "allocation/PROFILE.json").items()}
    weights = {int(k): int(v) for k, v in prices["weights"]["c"].items()}
    break_even = int(prices["weights"]["break_even"])

    rows = {}
    for variant in ("base", "extra"):
        parent = read(PKG / f"data/PARENT-{variant}.json.gz")
        parent_profile, parent_inventory = profile(parent)
        need(parent_profile == {int(k): v for k, v in parent["report"]["local_profile"].items()}, "independent parent profile")
        need(parent_inventory == {int(k): v for k, v in parent["report"]["width_inventory"].items()}, "independent parent inventory")

        stage1, edits = apply_groups(parent, record, list(record["groups"]))
        stage1_profile, stage1_inventory = profile(stage1)
        need(len(edits) == 139, "all five groups account for 139 frame edits")
        need(stage1_profile == {int(k): v for k, v in record["declared_local_profile"].items()}, "five-group local profile")
        need(stage1_inventory == {int(k): v for k, v in record["declared_width_inventory"].items()}, "five-group width inventory")

        v45, v45_edits = apply_groups(parent, record, ["V45"])
        joint_profile, joint_inventory = profile(v45)
        need(len(v45_edits) == 61, "V45 frame edit count")
        only_one = deepcopy(v45)
        v45_helpers = record["groups"]["V45"][1]
        for h in v45_helpers[1:]:
            only_one["helper_final"][str(h)] = deepcopy(parent["helper_final"][str(h)])
        one_profile, one_inventory = profile(only_one)
        delta = lambda newer: price(newer, weights) - price(parent_profile, weights)
        joint_delta, one_delta = delta(joint_profile), delta(one_profile)
        joint_margin = -joint_delta - len(v45_helpers) * break_even
        one_margin = -one_delta - break_even
        need((joint_delta, joint_margin) == (-8_388_172, 22_972), "V45 coordinated price and margin")
        need((one_delta, one_margin) == (-2_038_159, -53_141), "V45 losing single-helper control")
        rows[variant] = {
            "parent_profile": parent_profile,
            "stage1_profile": stage1_profile,
            "stage1_inventory": stage1_inventory,
            "v45_profile": joint_profile,
            "v45_inventory": joint_inventory,
            "v45_edit_count": len(v45_edits),
            "v45_delta_units": joint_delta,
            "v45_margin_units": joint_margin,
            "single_helper": v45_helpers[0],
            "single_delta_units": one_delta,
            "single_margin_units": one_margin,
            "single_inventory": one_inventory,
        }
    need(rows["base"] == rows["extra"], "provider profile agreement")

    final_rows = {}
    for variant in ("base", "extra"):
        final = read(PKG / f"data/WORD-{variant}.json.gz")
        final_profile, final_inventory = profile(final)
        need(final_profile == {int(k): v for k, v in final["report"]["local_profile"].items()}, "independent final-word profile")
        need(final_inventory == {int(k): v for k, v in final["report"]["width_inventory"].items()}, "independent final-word inventory")
        final_rows[variant] = (final_profile, final_inventory)
    need(final_rows["base"] == final_rows["extra"], "final provider profile agreement")
    final_profile, final_inventory = final_rows["base"]

    total_delta = price(final_profile, weights) - price(rows["base"]["parent_profile"], weights)
    stage_delta_sum = sum(int(prices[f"stage{i}"]["literal_price_units"]) for i in (1, 2, 3))
    need(total_delta == stage_delta_sum == -56_726_747, "final frame-price delta equals three published stage deltas")
    need(final_inventory == {int(k): v for k, v in claim["width_inventory"].items()}, "claim width inventory matches independently profiled final word")
    need(final_profile == {int(k): v for k, v in claim["local_profile"].items()}, "claim local profile matches independently profiled final word")

    calls, replicas = int(claim["calls"]), int(claim["replicas"])
    idle = dict(allocation)
    for r, n in final_profile.items():
        idle[r] = idle.get(r, 0) - calls * n
    need(all(n >= 0 for n in idle.values()), "T74 profile pays all 666 complete local calls")
    idle = {r: n for r, n in sorted(idle.items()) if n}
    need(sum(r * n for r, n in allocation.items()) == replicas * 65_088, "complete T74 rank-mass identity")
    need(sum(r * n for r, n in final_profile.items()) * calls + sum(r * n for r, n in idle.items()) == replicas * 65_088,
         "local plus idle profile closes T74 rank mass")
    need(allocation == {int(k): v for k, v in claim["profile"].items()}, "T74 profile matches claim")

    root, root_residual = decimal_root(allocation, replicas)
    selected_kappa = Q(selected["kappa"])
    claimed_kappa = Q(claim["kappa"])
    cap_lower = dec_fraction(cap["cap_lower"])
    cap_upper = dec_fraction(cap["cap_upper"])
    need(claimed_kappa > selected_kappa, "claimed candidate kappa strictly exceeds selected kappa")
    need(root > dec_fraction(claim["complex_lower"]), "numerical T74 root exceeds claimed conservative complex lower bound")
    need(root < cap_lower < cap_upper, "numerical T74 root lies below the fixed-inventory cap bracket")
    need(D(0) < root - dec_fraction(claimed_kappa) < D("1e-24"), "claim is a conservative floor of the numerical T74 root")

    print(json.dumps({
        "status": "PASS_V45_INDEPENDENT_LOCAL_PROFILE_AND_T74_AGGREGATE_ARITHMETIC",
        "v45": rows["base"],
        "final_local_profile": final_profile,
        "final_width_inventory": final_inventory,
        "local_stage_delta_units": total_delta,
        "sum_of_stage_deltas_units": stage_delta_sum,
        "t74_profile": allocation,
        "t74_idle_profile_after_666_calls": idle,
        "t74_rank_mass": sum(r * n for r, n in allocation.items()),
        "root_decimal_crosscheck_only": str(root),
        "root_moment_residual_decimal": str(root_residual),
        "claimed_kappa_minus_selected_exact": str(claimed_kappa - selected_kappa),
        "limitations": [
            "Stages 2 and 3 are not independently reconstructed from their transform/rewrite records.",
            "T74 ownership chronology, physical admission, native admission, and outer release are not independently audited here.",
            "The Decimal root is a numeric cross-check, not an exact root certificate."
        ]
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
