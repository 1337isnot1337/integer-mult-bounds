#!/usr/bin/env python3
"""Exact bounded word search in the two-role F2[A5] register model."""
from collections import deque
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).with_name("CERTIFICATE.json")


def pmul(p, q):
    """Composition p after q, for image-list permutations."""
    return tuple(p[q[i]] for i in range(5))


def pinv(p):
    out = [0] * 5
    for i, image in enumerate(p):
        out[image] = i
    return tuple(out)


def all_group():
    ident = tuple(range(5))
    a = (1, 2, 3, 4, 0)       # (1 2 3 4 5)
    b = (1, 2, 0, 3, 4)       # (1 2 3)
    gens = (a, pinv(a), b, pinv(b))
    elements = [ident]
    index = {ident: 0}
    for x in elements:
        for g in gens:
            y = pmul(x, g)
            if y not in index:
                index[y] = len(elements)
                elements.append(y)
    assert len(elements) == 60
    assert all(sum(x[i] > x[j] for i in range(5) for j in range(i + 1, 5)) % 2 == 0
               for x in elements)
    return elements, index, gens


def matrix_multiply(a, b, ring_multiply):
    out = [0, 0, 0, 0]
    for i in range(2):
        for j in range(2):
            value = 0
            for k in range(2):
                value ^= ring_multiply(a[2 * i + k], b[2 * k + j])
            out[2 * i + j] = value
    return tuple(out)


def encode_matrix(m):
    return b"".join(x.to_bytes(8, "little") for x in m)


def main():
    elements, group_index, (a, a_inv, b, b_inv) = all_group()
    identity_group = elements[0]
    label_elements = {"a": a, "A": a_inv, "b": b, "B": b_inv}
    labels = tuple(label_elements)
    label_index = {name: group_index[g] for name, g in label_elements.items()}

    # Multiplication in F2[A5] XORs left translates. Cache each translate
    # through five 12-bit chunks so one term costs five table lookups.
    chunk_bits = 12
    chunk_size = 1 << chunk_bits
    chunk_count = (len(elements) + chunk_bits - 1) // chunk_bits
    translations = []
    for g in elements:
        g_tables = []
        images = [group_index[pmul(g, h)] for h in elements]
        for chunk in range(chunk_count):
            start = chunk * chunk_bits
            width = min(chunk_bits, len(elements) - start)
            table = [0] * chunk_size
            for pattern in range(1, 1 << width):
                low = pattern & -pattern
                bit = low.bit_length() - 1
                table[pattern] = table[pattern ^ low] ^ (1 << images[start + bit])
            g_tables.append(table)
        translations.append(g_tables)

    def translate(g, y):
        result = 0
        for chunk, table in enumerate(translations[g]):
            result |= table[(y >> (chunk * chunk_bits)) & (chunk_size - 1)]
        return result

    def ring_multiply(x, y):
        result = 0
        while x:
            low = x & -x
            result ^= translate(low.bit_length() - 1, y)
            x ^= low
        return result

    def slow_ring_multiply(x, y):
        result = 0
        while x:
            gx = x & -x
            gi = gx.bit_length() - 1
            x ^= gx
            rest = y
            while rest:
                hy = rest & -rest
                hi = hy.bit_length() - 1
                rest ^= hy
                result ^= 1 << group_index[pmul(elements[gi], elements[hi])]
        return result

    # Basis-pair coverage proves the bilinear product table; dense controls
    # independently exercise the chunked coefficient translation path.
    for gi in range(60):
        for hi in range(60):
            left, right = 1 << gi, 1 << hi
            expected = 1 << group_index[pmul(elements[gi], elements[hi])]
            assert ring_multiply(left, right) == expected
    dense_masks = []
    full = (1 << 60) - 1
    for k in range(32):
        x = (0x9E3779B97F4A7C15 * (k + 1) ^ (1 << ((7 * k + 11) % 60))) & full
        y = (0xD1B54A32D192ED03 * (k + 3) ^ (1 << ((13 * k + 5) % 60))) & full
        dense_masks.append((x, y))
        assert ring_multiply(x, y) == slow_ring_multiply(x, y)

    one = 1 << group_index[identity_group]
    I = (one, 0, 0, one)

    def f2_matrix_product(x, y):
        return tuple((x[2 * i] * y[j] ^ x[2 * i + 1] * y[2 + j])
                     for i in range(2) for j in range(2))

    # All rank-one idempotents uv^T with v^T u=1 over F2.
    projectors = []
    for u in (1, 2, 3):
        for v in (1, 2, 3):
            dot = ((u & 1) & (v & 1)) ^ (((u >> 1) & 1) & ((v >> 1) & 1))
            if dot:
                projectors.append(tuple(((u >> i) & 1) * ((v >> j) & 1)
                                        for i in range(2) for j in range(2)))
    projectors = tuple(sorted(set(projectors)))
    assert len(projectors) == 6
    for n in projectors:
        assert f2_matrix_product(n, n) == n
        assert any(n)
        assert (n[0] * n[3] ^ n[1] * n[2]) == 0
    projector_index = {n: i for i, n in enumerate(projectors)}
    brute_projectors = set()
    for mask in range(16):
        candidate = tuple((mask >> k) & 1 for k in range(4))
        determinant = candidate[0] * candidate[3] ^ candidate[1] * candidate[2]
        if any(candidate) and determinant == 0 and f2_matrix_product(candidate, candidate) == candidate:
            brute_projectors.add(candidate)
    assert brute_projectors == set(projectors)

    def factor(n, g):
        entries = []
        for i in range(2):
            for j in range(2):
                if n[2 * i + j]:
                    value = (1 << g) ^ one
                    if i == j:
                        value ^= one
                else:
                    value = one if i == j else 0
                entries.append(value)
        return tuple(entries)

    inverse_label = {"a": "A", "A": "a", "b": "B", "B": "b"}
    calls = []
    for n in projectors:
        for label in labels:
            calls.append((projector_index[n], label,
                          factor(n, label_index[label]),
                          factor(n, label_index[inverse_label[label]])))
    assert len(calls) == 24
    assert len({call[2] for call in calls}) == 24

    # Every paid call is invertible with the inverse label on the same projector.
    for call in calls:
        assert matrix_multiply(call[2], call[3], ring_multiply) == I
        assert matrix_multiply(call[3], call[2], ring_multiply) == I

    # Check the scalar conjugation normalization for every S in GL2(F2).
    gl2 = []
    for x in range(16):
        mat = tuple((x >> k) & 1 for k in range(4))
        if any(f2_matrix_product(mat, tuple((z >> k) & 1 for k in range(4))) == (1, 0, 0, 1)
               and f2_matrix_product(tuple((z >> k) & 1 for k in range(4)), mat) == (1, 0, 0, 1)
               for z in range(16)):
            gl2.append(mat)
    assert len(gl2) == 6
    scalar_identity = (1, 0, 0, 1)
    gl2_inverse = {}
    for s in gl2:
        gl2_inverse[s] = next(t for t in gl2
                              if f2_matrix_product(s, t) == scalar_identity
                              and f2_matrix_product(t, s) == scalar_identity)
    pset = set(projectors)
    for s in gl2:
        for n in projectors:
            sn = f2_matrix_product(s, n)
            conjugate = f2_matrix_product(sn, gl2_inverse[s])
            assert conjugate in pset

    # c=aba^-1b^-1 is an order-three noncentral commutator in A5.
    c = pmul(pmul(pmul(a, b), a_inv), b_inv)
    c_inv = pinv(c)
    assert c != identity_group and pmul(c, c) != identity_group and pmul(pmul(c, c), c) == identity_group
    assert pmul(c, a) != pmul(a, c)

    # Generator word distances in A5 provide the direct eight-call upper bound.
    distance = {identity_group: (0, "")}
    queue = deque([identity_group])
    while queue:
        x = queue.popleft()
        d, w = distance[x]
        for label in labels:
            y = pmul(x, label_elements[label])
            if y not in distance:
                distance[y] = (d + 1, w + label)
                queue.append(y)
    assert distance[c][0] == distance[c_inv][0] == 4

    target = (1 << group_index[c], 0, 0, 1 << group_index[c_inv])
    calls_by_name = {(ni, label): call for call in calls for ni, label in [call[:2]]}
    e11 = projector_index[(1, 0, 0, 0)]
    e22 = projector_index[(0, 0, 0, 1)]
    direct = [(e11, x) for x in "abAB"] + [(e22, x) for x in "baBA"]

    def product_of(word):
        result = I
        for ni, label in word:
            result = matrix_multiply(result, calls_by_name[(ni, label)][2], ring_multiply)
        return result

    assert product_of(direct) == target
    assert len(direct) == 8

    # Exact radius-three prefix ball with one shortest witness per matrix.
    prefix = {I: (0, ())}
    layer = [I]
    prefix_counts = [1]
    for depth in range(1, 4):
        next_layer = []
        for state in layer:
            word = prefix[state][1]
            for ci, call in enumerate(calls):
                nxt = matrix_multiply(state, call[2], ring_multiply)
                if nxt not in prefix:
                    prefix[nxt] = (depth, word + (ci,))
                    next_layer.append(nxt)
        layer = next_layer
        prefix_counts.append(len(layer))
    assert prefix[I][0] == 0

    # Negative control: c cannot be produced on one role in <=3 calls.
    one_role_target = (1 << group_index[c], 0, 0, one)
    assert one_role_target not in prefix

    prefix_hash = hashlib.sha256(b"".join(encode_matrix(m) for m in sorted(prefix))).hexdigest()
    suffix_hash = hashlib.sha256()
    suffix_nodes_by_depth = [0] * 5
    match_count = 0
    best = (99, None)

    def visit(suffix, inverse_suffix, word, depth):
        nonlocal match_count, best
        suffix_nodes_by_depth[depth] += 1
        suffix_hash.update(bytes([depth]) + encode_matrix(suffix))
        wanted_prefix = matrix_multiply(target, inverse_suffix, ring_multiply)
        entry = prefix.get(wanted_prefix)
        if entry is not None:
            match_count += 1
            total = entry[0] + depth
            if total < best[0]:
                prefix_word = entry[1]
                full = tuple(calls[i][:2] for i in prefix_word) + tuple(word)
                best = (total, full)
        if depth == 4:
            return
        for ci, call in enumerate(calls):
            next_suffix = matrix_multiply(suffix, call[2], ring_multiply)
            next_inverse = matrix_multiply(call[3], inverse_suffix, ring_multiply)
            visit(next_suffix, next_inverse, word + (call[:2],), depth + 1)

    visit(I, I, (), 0)
    if best[1] is not None:
        assert product_of(best[1]) == target
        assert best[0] == len(best[1])
    else:
        assert best[0] == 99

    certificate = {
        "result": "SEVEN_CALL_WORD_FOUND" if best[1] is not None else "NO_WORD_OF_LENGTH_AT_MOST_SEVEN",
        "minimum_paid_calls": best[0] if best[1] is not None else 8,
        "base_commit": "0b1cccf86e2f5132ed286a26ef0a681a495740ea",
        "seed": "105bdc7c008d8e95710ae18653b8a901",
        "selected_record_sha256": "10b9e340fd8e354a37a0c4813c90e5de1dd42044b5f6aca4a3fc5a42b685fa32",
        "model": {
            "group_order": len(elements), "group": "A5",
            "a_image_list_zero_based": list(a), "b_image_list_zero_based": list(b),
            "commutator_image_list_zero_based": list(c), "commutator_order": 3,
            "commutator_noncentral_witness": "ca != ac",
            "commutator_shortest_word": distance[c][1],
            "inverse_shortest_word": distance[c_inv][1],
            "roles": 2, "rank_one_idempotents": [list(x) for x in projectors],
            "paid_labels": list(labels), "paid_call_alphabet_size": len(calls),
            "formal_ring": "F2[A5]", "free_scalar_GL2_normalized_by_conjugating_projectors": True
        },
        "cost": {"direct_upper_bound": 8, "tested_threshold": 7,
                 "saving_target_calls": 1, "saving_fraction": "1/8"},
        "search": {
            "method": "exact radius-3 prefix-state set against every radius-4 suffix word",
            "prefix_unique_state_counts_by_exact_minimum_depth": prefix_counts,
            "prefix_unique_states_total": len(prefix),
            "prefix_state_sha256_sorted_matrix_bytes": prefix_hash,
            "suffix_ordered_words_visited_by_depth": suffix_nodes_by_depth,
            "suffix_nodes_total": sum(suffix_nodes_by_depth),
            "suffix_matrix_stream_sha256": suffix_hash.hexdigest(),
            "prefix_suffix_matches": match_count,
            "best_word": [[ni, label] for ni, label in best[1]] if best[1] is not None else None,
            "direct_eight_call_word": [[e11, x] for x in "abAB"] + [[e22, x] for x in "baBA"],
            "negative_control_one_role_target_in_radius3": False
        },
        "arithmetic": "Each group-algebra element is a 60-bit coefficient vector. Multiplication XORs left translates; matrices use exact 2x2 multiplication over F2[A5].",
        "arithmetic_controls": {
            "group_basis_products_checked": 60 * 60,
            "dense_products_checked_against_slow_convolution": len(dense_masks),
            "binary_2x2_matrices_exhaustively_checked_for_projectors": 16,
            "rank_one_idempotents_found": len(brute_projectors),
            "distinct_paid_operations": len({call[2] for call in calls}),
            "two_sided_inverse_products_checked": 2 * len(calls),
            "GL2_F2_elements_checked_for_conjugation_closure": len(gl2)
        }
    }
    OUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(certificate["result"], "minimum", certificate["minimum_paid_calls"])
    print("prefix_states", len(prefix), "suffix_nodes", sum(suffix_nodes_by_depth), "matches", match_count)
    print("certificate", OUT)


if __name__ == "__main__":
    main()
