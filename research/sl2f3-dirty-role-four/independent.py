#!/usr/bin/env python3
"""Independent frozenset F2[SL2(F3)] replay; imports no primary engine."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CERT_PATH = HERE / "CERTIFICATE.json"
ROLES = 4


def need(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit(f"FAIL_INDEPENDENT_SL2F3_DIRTY_ROLE_FOUR: {message}")


def load_json_reject_duplicates(path: Path):
    def hook(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError(f"duplicate JSON key {key!r} in {path}")
            out[key] = value
        return out

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=hook)


def mat2_mul(a, b):
    return tuple(
        sum(a[2 * r + k] * b[2 * k + c] for k in range(2)) % 3
        for r in range(2)
        for c in range(2)
    )


def build_group():
    # Enumerate in a different order (row-major a,b then c,d) then reindex.
    raw = [
        (a, b, c, d)
        for a in range(3)
        for b in range(3)
        for c in range(3)
        for d in range(3)
        if (a * d - b * c) % 3 == 1
    ]
    # Sort by flattened tuple descending — deliberately not the primary sort.
    elements = sorted(raw, key=lambda t: (-t[0], -t[1], -t[2], -t[3]))
    need(len(elements) == 24, "group order")
    index = {g: i for i, g in enumerate(elements)}
    e = index[(1, 0, 0, 1)]
    table = [[index[mat2_mul(a, b)] for b in elements] for a in elements]
    inv = [
        next(j for j in range(24) if table[i][j] == e and table[j][i] == e)
        for i in range(24)
    ]
    return elements, index, e, table, inv


ELEMENTS, INDEX, E, TABLE, INV = build_group()
I2 = INDEX[(0, 1, 2, 0)]
W = INDEX[(0, 2, 1, 2)]
IW = INV[W]
C = TABLE[TABLE[IW][I2]][W]
GENS = (I2, INV[I2], W, IW)


def algebra_mul(left: frozenset, right: frozenset) -> frozenset:
    out: set[int] = set()
    for g in left:
        for h in right:
            prod = TABLE[g][h]
            if prod in out:
                out.remove(prod)
            else:
                out.add(prod)
    return frozenset(out)


def algebra_add(left: frozenset, right: frozenset) -> frozenset:
    return left.symmetric_difference(right)


def identity_matrix():
    one = frozenset({E})
    zero = frozenset()
    return tuple(one if r == c else zero for r in range(ROLES) for c in range(ROLES))


def matrix_mul(a, b):
    out = []
    for r in range(ROLES):
        for c in range(ROLES):
            acc = frozenset()
            for k in range(ROLES):
                acc = algebra_add(acc, algebra_mul(a[ROLES * r + k], b[ROLES * k + c]))
            out.append(acc)
    return tuple(out)


def factor(g: int, x: int, y: int):
    """I + ([g]+[e]) x y^T as a frozenset matrix."""
    one = frozenset({E})
    ge = frozenset({g, E})
    out = list(identity_matrix())
    for r in range(ROLES):
        if not ((x >> r) & 1):
            continue
        for c in range(ROLES):
            if (y >> c) & 1:
                out[ROLES * r + c] = algebra_add(out[ROLES * r + c], ge)
    return tuple(out)


def target_matrix(diag):
    out = [frozenset() for _ in range(ROLES * ROLES)]
    for r, g in enumerate(diag):
        out[ROLES * r + r] = frozenset({g})
    return tuple(out)


def pack_state(matrix) -> tuple[int, ...]:
    """Pack frozenset supports into the primary 24-bit mask encoding."""
    out = []
    for entry in matrix:
        mask = 0
        for g in entry:
            mask |= 1 << g
        out.append(mask)
    return tuple(out)


def make_calls():
    calls = []
    for g in GENS:
        for x in range(1, 1 << ROLES):
            for y in range(1, 1 << ROLES):
                if (bin(x & y).count("1") & 1) == 1:
                    calls.append((g, x, y))
    need(len(calls) == 480, "480 factors")
    return tuple(calls)


def main() -> None:
    cert = load_json_reject_duplicates(CERT_PATH)
    need(cert["result_minimum"] == 5, "certificate minimum")
    need(cert["dirty_role_lowers_minimum"] is False, "dirty flag")
    need(cert["no_new_kappa"] is True, "kappa flag")

    calls = make_calls()
    gates = tuple(factor(g, x, y) for g, x, y in calls)
    call_index = {call: i for i, call in enumerate(calls)}

    # Direct five-call word.
    def at(g, role):
        e = 1 << role
        return call_index[(g, e, e)]

    direct = (at(I2, 0), at(W, 1), at(IW, 2), at(I2, 2), at(W, 2))
    state = identity_matrix()
    for idx in direct:
        state = matrix_mul(state, gates[idx])
    target = target_matrix((I2, W, C, E))
    need(state == target, "independent direct word misses target")

    # Omission controls.
    for drop in range(5):
        reduced = direct[:drop] + direct[drop + 1 :]
        st = identity_matrix()
        for idx in reduced:
            st = matrix_mul(st, gates[idx])
        need(st != target, f"independent omission {drop} unexpectedly hits")

    # Two-call pair census digest (independent encoding).
    pair_states = set()
    for a, gate in enumerate(gates):
        for b in range(len(calls)):
            pair_states.add(pack_state(matrix_mul(gate, gates[b])))
    need(len(pair_states) == cert["two_call_distinct_states"], "pair state count")

    digest = hashlib.sha256()
    for packed in sorted(pair_states):
        for support in packed:
            digest.update(support.to_bytes(3, "little"))
    need(
        digest.hexdigest() == cert["two_call_state_sha256"],
        "independent pair-state digest mismatch",
    )

    # Depth-4 MITM with frozenset→packed interface, no primary import.
    one_words = {pack_state(gates[i]): (i,) for i in range(len(calls))}
    pair_words = {}
    for a, gate in enumerate(gates):
        for b in range(len(calls)):
            pair_words.setdefault(pack_state(matrix_mul(gate, gates[b])), (a, b))

    def left_translate_mask(mask: int, g: int) -> int:
        out = 0
        while mask:
            bit = mask & -mask
            a = bit.bit_length() - 1
            out |= 1 << TABLE[g][a]
            mask ^= bit
        return out

    def left_diagonal(packed, diagonal):
        return tuple(
            left_translate_mask(packed[ROLES * r + c], diagonal[r])
            for r in range(ROLES)
            for c in range(ROLES)
        )

    call_inverse = tuple(call_index[(INV[g], x, y)] for g, x, y in calls)

    def pair_from_indices(a, b):
        return pack_state(matrix_mul(gates[a], gates[b]))

    target_packed = pack_state(target)
    found = None
    if target_packed in one_words:
        found = one_words[target_packed]
    elif target_packed in pair_words:
        found = pair_words[target_packed]
    else:
        diag = (I2, W, C, E)
        for _s, (a, b) in pair_words.items():
            inv_suffix = pair_from_indices(call_inverse[b], call_inverse[a])
            need_prefix = left_diagonal(inv_suffix, diag)
            if need_prefix in one_words:
                found = one_words[need_prefix] + (a, b)
                break
        if found is None:
            for _s, (a, b) in pair_words.items():
                inv_suffix = pair_from_indices(call_inverse[b], call_inverse[a])
                need_prefix = left_diagonal(inv_suffix, diag)
                if need_prefix in pair_words:
                    found = pair_words[need_prefix] + (a, b)
                    break
    need(found is None, "independent search found a length≤4 witness")

    print(
        "PASS_INDEPENDENT_SL2F3_DIRTY_ROLE_FOUR "
        f"group=24 roles={ROLES} calls=480 target_minimum=5 "
        f"distinct_pair_states={len(pair_states)} dirty_lowers=false no_new_kappa"
    )


if __name__ == "__main__":
    main()
