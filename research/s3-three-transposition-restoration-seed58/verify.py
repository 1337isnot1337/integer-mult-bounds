#!/usr/bin/env python3
"""Exact regular-S3 boundary replay with explicit signed-ADD row swaps."""

from itertools import permutations, product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL_S3_THREE_TRANSPOSITION_BOUNDARY: " + message)


E = (0, 1, 2)
A = (1, 0, 2)  # (12)
B = (0, 2, 1)  # (23)
C = (2, 1, 0)  # (13)
GENERATORS = (A, B, C)
LETTERS = {A: "a", B: "b", C: "c"}
ROWS = tuple(permutations(range(3)))
ROW_INDEX = {g: i for i, g in enumerate(ROWS)}


def compose(p, q):
    """Function composition p after q."""
    return tuple(p[q[i]] for i in range(3))


def word_product(word):
    out = E
    for h in word:
        out = compose(out, h)
    return out


def right_map(h):
    """Old row g moves to new row g*h."""
    return tuple(ROW_INDEX[compose(g, h)] for g in ROWS)


def cycles(mapping):
    seen, result = set(), []
    for start in range(len(mapping)):
        if start in seen:
            continue
        cycle, at = [], start
        while at not in seen:
            seen.add(at)
            cycle.append(at)
            at = mapping[at]
        result.append(tuple(cycle))
    return tuple(result)


def cycle_lengths(mapping):
    return tuple(sorted(len(cycle) for cycle in cycles(mapping)))


def minimum_swaps(mapping):
    # Exact transposition distance: m points minus the number of cycles.
    return len(mapping) - len(cycles(mapping))


def signed_add_swap(state, i, j):
    """3 signed ADDs and one NEG implement (x_i,x_j)->(x_j,x_i)."""
    out = list(state)
    out[i] += out[j]
    out[j] -= out[i]
    out[i] += out[j]
    out[j] = -out[j]
    return tuple(out)


def apply_right_reference(state, h):
    out = [None] * len(state)
    for old, new in enumerate(right_map(h)):
        out[new] = state[old]
    return tuple(out)


def apply_right(state, h):
    """Emit the cycle transpositions using the explicit signed-ADD swap."""
    out = tuple(state)
    for cycle in cycles(right_map(h)):
        pivot = cycle[0]
        for other in cycle[1:]:
            out = signed_add_swap(out, pivot, other)
    return out


def run_macro(state, word):
    outputs, at = [], tuple(state)
    for h in word:
        outputs.append(sum(at))
        at = apply_right(at, h)
        require(sum(at) == outputs[-1], "trivial-character reader changed")
    return tuple(outputs), at


def run_schedule(state, macros, eager):
    outputs, at = [], tuple(state)
    for word in macros:
        word_outputs, at = run_macro(at, word)
        outputs.extend(word_outputs)
        if eager:
            # Each macro endpoint is c, and c is its own inverse.
            at = apply_right(at, word_product(word))
    return tuple(outputs), at


def parity(p):
    inversions = sum(
        1 for i in range(3) for j in range(i + 1, 3) if p[i] > p[j]
    )
    return -1 if inversions % 2 else 1


def sign_character(state):
    return sum(parity(g) * state[i] for i, g in enumerate(ROWS))


def enumerate_reduced_words(max_length=4):
    by_length, checked = {}, 0
    for length in range(1, max_length + 1):
        count, identities = 0, []
        for word in product(GENERATORS, repeat=length):
            if any(word[i] == word[i - 1] for i in range(1, length)):
                continue
            count += 1
            checked += 1
            if word_product(word) == E:
                identities.append(word)
        by_length[length] = count, tuple(identities)
    return checked, by_length


def name_word(word):
    return "".join(LETTERS[h] for h in word)


def main():
    require(len(ROWS) == 6, "S3 regular row count")
    require(word_product((A, B, A)) == C, "aba must equal c")
    require(word_product((A, B, A, C)) == E, "AB must close")
    require(word_product((C, A, B, A)) == E, "BA must close")

    # Validate the actual 3-ADD/1-NEG word on basis columns. All operations
    # are linear over the integers, so this proves the exact two-row map.
    for i in range(2):
        basis2 = tuple(1 if j == i else 0 for j in range(2))
        require(signed_add_swap(basis2, 0, 1) == basis2[::-1],
                "signed-add coordinate swap")

    right_costs = {}
    for h in GENERATORS:
        mapping = right_map(h)
        lengths = cycle_lengths(mapping)
        swaps = minimum_swaps(mapping)
        require(lengths == (2, 2, 2) and swaps == 3,
                "right-transposition must be three disjoint swaps")
        right_costs[LETTERS[h]] = {
            "cycle_lengths": list(lengths),
            "logical_swaps": swaps,
            "add_ops": 3 * swaps,
            "neg_ops": swaps,
        }
        for i in range(6):
            basis6 = tuple(1 if j == i else 0 for j in range(6))
            require(apply_right(basis6, h) == apply_right_reference(basis6, h),
                    "emitted signed-add word must equal right translation")

    three_cycle = compose(A, B)
    require(cycle_lengths(right_map(three_cycle)) == (3, 3),
            "regular action of a three-cycle")
    three_cycle_swaps = minimum_swaps(right_map(three_cycle))
    require(three_cycle_swaps == 4, "three-cycle repair distance")

    checked, census = enumerate_reduced_words()
    require(checked == 45, "reduced-word domain")
    require([census[i][0] for i in range(1, 5)] == [3, 6, 12, 24],
            "all reduced words through length four")
    require([len(census[i][1]) for i in range(1, 5)] == [0, 0, 0, 12],
            "shortest relation census")
    require(all(set(w) == set(GENERATORS) for w in census[4][1]),
            "all length-four identities use all three generators")
    require((A, B, A, C) in census[4][1], "shortest witness abac")

    macro_a, macro_b = (A, B, A), (C,)
    echo = (macro_a, macro_b, macro_b, macro_a)
    require(all(word_product(w) == C for w in echo),
            "every macro endpoint is c")
    require(word_product(tuple(h for w in echo for h in w)) == E,
            "complete echo endpoint")

    # Bounded semantic replay; the group/sum proof covers arbitrary integers.
    vectors = 0
    for state in product((-1, 0, 1), repeat=6):
        vectors += 1
        for pair in ((macro_a, macro_b), (macro_b, macro_a)):
            eager_out, eager_end = run_schedule(state, pair, eager=True)
            carry_out, carry_end = run_schedule(state, pair, eager=False)
            require(eager_out == carry_out and eager_end == state and carry_end == state,
                    "paired call output or endpoint")
        eager_out, eager_end = run_schedule(state, echo, eager=True)
        carry_out, carry_end = run_schedule(state, echo, eager=False)
        require(eager_out == carry_out and eager_end == state and carry_end == state,
                "full echo output or endpoint")
        require(all(y == sum(state) for y in carry_out),
                "every emitted value must be the invariant sum")
    require(vectors == 729, "workspace-vector domain")

    # Negative controls: non-invariant readers and wrong frame endpoints.
    basis = tuple(1 if g == E else 0 for g in ROWS)
    moved = apply_right(basis, A)
    coordinate_changes = basis[ROW_INDEX[E]] != moved[ROW_INDEX[E]]
    require(coordinate_changes, "single-coordinate reader control")
    require(sign_character(moved) == -sign_character(basis),
            "sign-character reader control")

    identity_b_pair = word_product(macro_a)
    identity_b_repair_swaps = minimum_swaps(right_map(identity_b_pair))
    require(identity_b_pair == C and identity_b_repair_swaps == 3,
            "identity-B leaves a transposition repair")
    require(identity_b_repair_swaps == 3,
            "identity-B eager and terminal repairs tie")

    wrong_b = word_product(macro_a + (B,))
    require(wrong_b in (three_cycle, compose(B, A)),
            "wrong-B control leaves a three-cycle")
    wrong_b_repair_swaps = minimum_swaps(right_map(wrong_b))
    require(wrong_b_repair_swaps == 4, "wrong-B terminal repair price")

    # Unit invoice: COPY, signed ADD, NEG and dispatch each cost one.
    leaf_dispatch = macro_dispatch = root_dispatch = 1
    reader_copy, reader_adds = 1, 5
    row_swaps_per_transposition = 3
    adds_per_swap, negs_per_swap = 3, 1
    frame_adds = row_swaps_per_transposition * adds_per_swap
    frame_negs = row_swaps_per_transposition * negs_per_swap
    leaf_cost = reader_copy + reader_adds + frame_adds + frame_negs + leaf_dispatch
    cost_a = 3 * leaf_cost + macro_dispatch
    cost_b = leaf_cost + macro_dispatch
    pair_dispatch = 4 * leaf_dispatch + 2 * macro_dispatch + root_dispatch
    echo_dispatch = 8 * leaf_dispatch + 4 * macro_dispatch + root_dispatch

    pair_carried = {
        "copy": 4 * reader_copy,
        "add": 4 * (reader_adds + frame_adds),
        "neg": 4 * frame_negs,
        "dispatch": pair_dispatch,
    }
    pair_eager = dict(pair_carried)
    pair_eager["add"] += 2 * frame_adds
    pair_eager["neg"] += 2 * frame_negs
    echo_carried = {
        "copy": 8 * reader_copy,
        "add": 8 * (reader_adds + frame_adds),
        "neg": 8 * frame_negs,
        "dispatch": echo_dispatch,
    }
    echo_eager = dict(echo_carried)
    echo_eager["add"] += 4 * frame_adds
    echo_eager["neg"] += 4 * frame_negs

    def total(cost):
        return sum(cost.values())

    require((cost_a, cost_b, total(pair_eager), total(pair_carried)) ==
            (58, 20, 103, 79), "paired recurrence")
    require((total(echo_eager), total(echo_carried)) == (205, 157),
            "two-direction echo recurrence")

    result = {
        "schema_version": 1,
        "base_commit": "bce54fb3f895cbe5cd4c0eb477c3afeed100190f",
        "assignment_seed": 58,
        "model": {
            "group": "S3",
            "row_order": ["".join(str(i) for i in g) for g in ROWS],
            "generators": {"a_(12)": list(A), "b_(23)": list(B), "c_(13)": list(C)},
            "reader": "sum of the six current workspace rows",
            "call": "COPY one row; ADD the other five; right-translate by a transposition",
            "coordinate_swap_word": "3 signed ADD + 1 NEG",
        },
        "short_word_census": {
            "max_length": 4,
            "reduced_words_checked": checked,
            "reduced_words_by_length": [census[i][0] for i in range(1, 5)],
            "identity_words_by_length": [len(census[i][1]) for i in range(1, 5)],
            "length_four_identity_words": sorted(name_word(w) for w in census[4][1]),
            "shortest_witness": "abac",
            "all_length_four_identities_use_all_three_generators": True,
        },
        "regular_action_cost": {
            "right_transposition": right_costs["a"],
            "right_three_cycle": {
                "cycle_lengths": list(cycle_lengths(right_map(three_cycle))),
                "logical_swaps": three_cycle_swaps,
                "add_ops": 3 * three_cycle_swaps,
                "neg_ops": three_cycle_swaps,
            },
        },
        "invoice": {
            "dispatch": {
                "leaf": leaf_dispatch,
                "macro": macro_dispatch,
                "root": root_dispatch,
                "pair_count": pair_dispatch,
                "echo_count": echo_dispatch,
            },
            "macro_A": {"word": "aba", "endpoint": "c", "local_cost": cost_a},
            "macro_B": {"word": "c", "endpoint": "c", "local_cost": cost_b},
            "pair_A_B": {
                "eager": {**pair_eager, "total": total(pair_eager)},
                "carried": {**pair_carried, "total": total(pair_carried)},
                "saved_primitives": total(pair_eager) - total(pair_carried),
            },
            "two_direction_echo_A_B_B_A": {
                "eager": {**echo_eager, "total": total(echo_eager)},
                "carried": {**echo_carried, "total": total(echo_carried)},
                "saved_primitives": total(echo_eager) - total(echo_carried),
            },
        },
        "controls": {
            "workspace_vectors_checked": vectors,
            "single_coordinate_reader_changes": coordinate_changes,
            "sign_character_multiplier_under_transposition": -1,
            "identity_B_terminal_repair": {
                "logical_swaps": identity_b_repair_swaps,
                "add_ops": 3 * identity_b_repair_swaps,
                "neg_ops": identity_b_repair_swaps,
                "eager_and_terminal_prices_tie": True,
            },
            "wrong_B_three_cycle_terminal_repair": {
                "logical_swaps": wrong_b_repair_swaps,
                "add_ops": 3 * wrong_b_repair_swaps,
                "neg_ops": wrong_b_repair_swaps,
            },
        },
        "scope": "Exact six-row typed interface only; no supplier admission and no new kappa.",
    }
    certificate = json.loads(Path(__file__).with_name("CERTIFICATE.json").read_text())
    require(result == certificate, "certificate differs from exact reconstruction")
    print(
        "PASS_S3_THREE_TRANSPOSITION_BOUNDARY reduced_words=45 length4_relations=12 "
        "pair=103_vs79 echo=205_vs157 saved=24_and_48 "
        "workspace_vectors=729 no_new_kappa"
    )


if __name__ == "__main__":
    main()
