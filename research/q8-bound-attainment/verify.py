#!/usr/bin/env python3
"""Attainment of the mixed-negative Q8 bound at t = 1 and t = 2.

The checker multiplies the retained words. It does not search a shorter word.
"""

import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = Path(__file__).resolve().parent
MARKER = "PASS_Q8_BOUND_ATTAINMENT t2=6 bound=6 no_new_kappa"
ONE, Z, ZI, ZJ = 1, 1 << 4, 1 << 5, 1 << 6


def fail(message):
    raise SystemExit("FAIL_Q8_BOUND_ATTAINMENT " + message)


def require(condition, message):
    if not condition:
        fail(message)


def group_product(left, right):
    left_i, left_j = left & 1, left >> 1 & 1
    right_i, right_j = right & 1, right >> 1 & 1
    central = (left >> 2) ^ (right >> 2) ^ (left_i & right_i) ^ (left_j & right_j) ^ (left_j & right_i)
    return central << 2 | (left_i ^ right_i) | (left_j ^ right_j) << 1


def hamilton(left, right):
    axes = ((0, 1, 2, 3), (1, 0, 3, 2), (2, 3, 0, 1), (3, 2, 1, 0))
    signs = ((0, 0, 0, 0), (0, 1, 0, 1), (0, 1, 1, 0), (0, 0, 1, 1))
    row, column = left & 3, right & 3
    return axes[row][column] + 4 * ((left >> 2) ^ (right >> 2) ^ signs[row][column])


def multiply(left, right):
    value = 0
    for i in range(8):
        if left >> i & 1:
            for j in range(8):
                if right >> j & 1:
                    value ^= 1 << group_product(i, j)
    return value


def apply(state, call):
    roles = len(state)
    label, row_mask, column_mask = call
    factor = {1: ONE | (1 << 1), 2: ONE | (1 << 2)}[label]
    selected = [0] * roles
    for row in range(roles):
        if column_mask >> row & 1:
            for column in range(roles):
                selected[column] ^= state[row][column]
    change = [multiply(factor, value) for value in selected]
    output = [list(row) for row in state]
    for row in range(roles):
        if row_mask >> row & 1:
            output[row] = [left ^ right for left, right in zip(output[row], change)]
    return tuple(tuple(row) for row in output)


def endpoint(word, roles):
    state = tuple(tuple(int(row == column) for column in range(roles)) for row in range(roles))
    for call in word:
        state = apply(state, call)
    return state


def diagonal(targets):
    roles = len(targets)
    return tuple(tuple(targets[row] if row == column else 0 for column in range(roles)) for row in range(roles))


def parity_bound(target_count):
    count = -(-11 * target_count // 5)
    if count % 2 != target_count % 2:
        count += 1
    return count


def spine(label, role):
    return [(label, 1 << role, 1 << role)] * 3


def words():
    return {
        "t1-zi": ((ZI,), spine(1, 0)),
        "t1-zj": ((ZJ,), [(1, 1, 1), (1, 1, 1), (2, 1, 1)]),
        "t2-zi-zi": ((ZI, ZI), spine(1, 0) + spine(1, 1)),
        "t2-zi-zj": ((ZI, ZJ), spine(1, 0) + spine(2, 1)),
        "t2-zj-zj": ((ZJ, ZJ), spine(2, 0) + spine(2, 1)),
        "t3-zi-zi-zi": ((ZI, ZI, ZI), spine(1, 0) + spine(1, 1) + spine(1, 2)),
        "t4-balanced": ((ZI, ZI, ZJ, ZJ), spine(1, 0) + spine(1, 1) + spine(2, 2) + spine(2, 3)),
    }


def evaluate():
    selected = ROOT / "certificates/selected-result.json"
    require(
        hashlib.sha256(selected.read_bytes()).hexdigest()
        == "bb2eaa58647b353f88d0aec2eafb9d30df1be53589231b23e12ceef3e4bad129",
        "selected record drift",
    )
    record = json.loads(selected.read_text(encoding="utf-8"))
    require(Fraction(record["kappa"]) == Fraction(836330098538459, 500000000000000000), "the selected kappa moved")
    agreements = sum(group_product(left, right) == hamilton(left, right) for left in range(8) for right in range(8))
    require(agreements == 64, "the two product tables disagree")
    require(multiply(1 << 1, multiply(1 << 1, 1 << 1)) == ZI, "the cube of i moved")
    require(multiply(1 << 2, multiply(1 << 2, 1 << 2)) == ZJ, "the cube of j moved")
    require([parity_bound(t) for t in (1, 2, 3, 4)] == [3, 6, 7, 10], "the parity bounds moved")
    attained = missed = 0
    for targets, word in words().values():
        require(endpoint(word, len(targets)) == diagonal(targets), "a witness missed its endpoint")
        bound = parity_bound(len(targets))
        if len(word) == bound:
            attained += 1
        else:
            missed += 1
            require(len(word) > bound, "a longer endpoint met the bound")
    require(attained == 5 and missed == 2, "the attainment count moved")
    return {
        "products": 64,
        "attained": 5,
        "t1_calls": 3,
        "t2_calls": 6,
        "t3_calls": 9,
        "t3_bound": 7,
        "t4_calls": 12,
        "t4_bound": 10,
        "no_new_kappa": True,
    }


def main():
    observed = evaluate()
    expected = json.loads((PACKAGE / "RESULT.json").read_text(encoding="utf-8"))
    require(observed == expected, "RESULT.json does not match the execution")
    print(MARKER)


if __name__ == "__main__":
    main()
