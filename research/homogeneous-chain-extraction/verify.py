"""Exact homogeneous-chain controller; Apache-2.0, OpenAI Codex assisted.

Finite checks supplement PROOF.md. No native provider or kappa is certified.
"""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

ZERO = (0, 0, 0, 0)
ONE = (1, 0, 0, 0)
Q = (0, 1, 0, 0)
P = (0, 0, 1, 0)
NATIVE_RECEIPT = 'research/one-terminal-h3-prefix/inputs/research/kappa-round3-warp-20261022/NATIVE-VALIDATION.json'
NATIVE_RECEIPT_SHA256 = 'eec3b14241430b6c9f5de3cbf0e3d45a172d8071d2dccd2b59d56a1fbac3d428'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def mul(a, b):
    out = [0] * 4
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    out[(i + j) % 4] += x * y
    return tuple(out)


def negative(a):
    return tuple(-x for x in a)


def identity(n):
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def row_add(matrix, target, source, coefficient):
    matrix[target] = [add(x, mul(coefficient, y))
                      for x, y in zip(matrix[target], matrix[source])]


def row_scale(matrix, target, coefficient):
    matrix[target] = [mul(coefficient, x) for x in matrix[target]]


def boundaries(n):
    """Chronological reversible operations, excluding the two paid oracles."""
    need(n >= 3 and n % 2 == 1, 'An odd chain length at least three is required')
    m = (n - 1) // 2
    right = [('add', 2*k, n-1, P if (m-k) % 2 else ONE) for k in range(m)]
    diagonal = [('scale', i, P) for i in range(1, n, 2)]
    correction = [('add', i, i-2, negative(P)) for i in range(n-1, 1, -1)]
    left = [('add', 2*k, 2*k-2, P) for k in range(1, m)]
    left += [('add', 2*k+1, 2*k+3, P) for k in range(m-2, -1, -1)]
    left += [('scale', 2*k+1, negative(P)) for k in range(m)]
    left += [('add', n-1, n-3, P)]
    left += [('swap', 2*k, 2*k+1) for k in range(m)]
    return right, diagonal, correction, left


def operate(matrix, operations):
    for operation in operations:
        if operation[0] == 'add':
            _, target, source, coefficient = operation
            row_add(matrix, target, source, coefficient)
        elif operation[0] == 'scale':
            _, target, coefficient = operation
            row_scale(matrix, target, coefficient)
        elif operation[0] == 'swap':
            _, a, b = operation
            matrix[a], matrix[b] = matrix[b], matrix[a]
        else:
            raise ValueError('Unknown boundary operation')


def controller(n, mutation=None):
    right, diagonal, correction, left = boundaries(n)
    if mutation == 'missing spectator injection':
        right = right[1:]
    if mutation == 'missing long-root correction':
        correction = []
    if mutation == 'wrong long-root sign':
        correction = [('add', i, j, P) for _, i, j, _ in correction]
    if mutation == 'missing Pauli conjugations':
        diagonal = []
    if mutation == 'missing spectator restoration':
        left = [op for op in left if not (op[0] == 'add' and op[1] == n-1)]
    matrix = identity(n)
    operate(matrix, right)
    operate(matrix, diagonal)
    if mutation == 'sign-only raw dual':
        # Descending rows omit all required powers q^d for d>=2.
        for i in range(n-1, 0, -1):
            row_add(matrix, i, i-1, negative(Q))
    else:
        # Ascending rows use updated predecessors: (I+q J^T)^-1.
        for i in range(1, n):
            row_add(matrix, i, i-1, negative(Q))
    operate(matrix, diagonal)
    operate(matrix, correction)
    # Ascending rows use original successors: I+q J.
    for i in range(n-1):
        row_add(matrix, i, i+1, Q)
    operate(matrix, left)
    return matrix


def target(n):
    jobs = 2*((n-1)//2)
    return [[(Q if i < jobs else ONE) if i == j else ZERO
             for j in range(n)] for i in range(n)]


def even_boundaries(n):
    """The cyclic middle boundary attains n-2 jobs for every even n."""
    need(n >= 2 and n % 2 == 0, 'An even chain length is required')
    if n == 2:
        return [], [], [('swap', 0, 1)], [('swap', 0, 1)]
    m = n//2
    right = [('swap', i, i-1) for i in range(n-2, 0, -1)]
    right += [('add', 2*k, 0, P if k % 2 else ONE) for k in range(1, m)]
    right += [('add', 2*k+1, n-1, P if (m-1-k) % 2 else ONE)
              for k in range(m-1)]
    correction = [('add', i, i-2, negative(P)) for i in range(n-1, 1, -1)]
    middle = [('swap', i, i+1) for i in range(n-1)]
    middle += [('scale', i, P) for i in range(1, n-1, 2)]
    if (m-1) % 2:
        middle += [('scale', n-1, P)]
    left = [('add', 2*k, 2*k-2, P) for k in range(1, m-1)]
    left += [('add', 2*k+1, 2*k+3, P) for k in range(m-3, -1, -1)]
    left += [('add', n-2, n-4, P)]
    left += [('scale', i, negative(P) if i % 2 else P) for i in range(n-2)]
    if (m-1) % 2:
        left += [('scale', n-1, P)]
    left += [('swap', 2*k, 2*k+1) for k in range(m)]
    return right, correction, middle, left


def even_controller(n, mutation=None):
    right, correction, middle, left = even_boundaries(n)
    if mutation == 'missing spectator injection':
        right = right[1:]
    if mutation == 'missing long-root correction':
        correction = []
    if mutation == 'wrong long-root sign':
        correction = [('add', i, j, P) for _, i, j, _ in correction]
    if mutation == 'missing middle Pauli scales':
        middle = [op for op in middle if op[0] != 'scale']
    if mutation == 'wrong cyclic wrap weight':
        middle += [('scale', n-1, P)]
    if mutation == 'missing spectator restoration':
        left = [op for op in left if not (op[0] == 'add' and op[1] == n-2)]
    matrix = identity(n)
    operate(matrix, right)
    indices = range(n-1, 0, -1) if mutation == 'sign-only raw dual' else range(1, n)
    for i in indices:
        row_add(matrix, i, i-1, negative(Q))
    operate(matrix, correction)
    operate(matrix, middle)
    for i in range(n-1):
        row_add(matrix, i, i+1, Q)
    operate(matrix, left)
    return matrix


def modular_rank(matrix, prime):
    a = [[x % prime for x in row] for row in matrix]
    rank = 0
    for column in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = pow(a[rank][column], -1, prime)
        a[rank] = [x * inverse % prime for x in a[rank]]
        for i in range(rank+1, len(a)):
            coefficient = a[i][column]
            a[i] = [(x-coefficient*y) % prime for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


def lower_bound_fixtures():
    """Finite corroboration with dirty roles; the general bound is proved."""
    prime = 65537
    count = 0
    for n in range(2, 10):
        for scratch in range(4):
            width = n + scratch
            b = [[int(i == j) for j in range(width)] for i in range(width)]
            # Elementary operations give invertible arbitrary-input mixing.
            for k in range(3*width):
                i, j = k % width, (k+1) % width
                b[i] = [(x+(k+1)*y) % prime for x, y in zip(b[i], b[j])]
            need(modular_rank(b, prime) == width, 'Invertible dirty mixing')
            for transpose_first in (False, True):
                for transpose_second in (False, True):
                    for sign in (-1, 1):
                        e = [row[:] for row in b]
                        for i in range(n-1):
                            r, a = (i+1, i) if transpose_first else (i, i+1)
                            for j in range(n-1):
                                c, d = (j, j+1) if transpose_second else (j+1, j)
                                e[r][c] = (e[r][c]+sign*b[a][d]) % prime
                        need(modular_rank(e, prime) >= width-(n-1),
                             'Even-coefficient rank bound with dirty fields')
                        count += 1
    return count


def faithful_gaussian_check():
    # C has eigenvalues 1,i. Three columns contain all four cyclic roots.
    prime, imaginary = 65537, 256
    need(imaginary**2 % prime == prime-1, 'Exact fourth root over F_65537')
    ranks = []
    for columns in (1, 2, 3, 4):
        eigenvalues = [pow(imaginary, k.bit_count(), prime)
                       for k in range(1 << columns)]
        evaluation = [[pow(x, j, prime) for j in range(4)] for x in eigenvalues]
        ranks.append(modular_rank(evaluation, prime))
    need(ranks == [2, 3, 4, 4], 'Width qualification for a faithful q-ring model')
    return ranks


def cut_certificate(paid, targets, margin):
    knots = sorted(set(paid) | set(targets) | {1})
    cuts = {str(z): sum(n*min(r, z) for r, n in paid.items())
            - sum(n*min(r, z) for r, n in targets.items()) - margin*min(1, z)
            for z in knots}
    need(all(x >= 0 for x in cuts.values()), 'Nonnegative complete concave-moment cuts')
    return cuts


def native_reuse_budget():
    """Read a pinned source receipt, not a fresh native operator replay."""
    raw = (Path(__file__).resolve().parents[2] / NATIVE_RECEIPT).read_bytes()
    need(sha256(raw).hexdigest() == NATIVE_RECEIPT_SHA256, 'Exact native paid/helper receipt')
    source = json.loads(raw)
    paid = {int(r): 2*n for r, n in source['paid'].items()}
    helpers = {int(r): n for r, n in source['helpers'].items()}
    need(helpers[9] >= 112, 'Sufficient H9 slots in the optimistic reused-owner policy')
    remaining = {r: 2*(n-(112 if r == 9 else 0)) for r, n in helpers.items()}
    cases = []
    for third_rank, margin in ((16, 128), (17, 16)):
        targets = Counter(remaining)
        targets[17] += 224
        targets[third_rank] += 112
        cuts = cut_certificate(paid, targets, margin)
        cases.append({'third_rank': third_rank, 'paid_minus_target_lower_bound': margin,
                      'targets': {str(r): n for r, n in sorted(targets.items())},
                      'cut_residuals': cuts})
    optimistic = Counter(remaining)
    optimistic[17] += 336
    wrong = [
        (paid, optimistic, 17),  # The claimed uniform margin is exactly too large.
        (paid, optimistic + Counter({9: 224}), 16),  # Alias owners counted twice.
        ({r: n for r, n in paid.items() if r != 8}, optimistic, 16),
    ]
    for bad_paid, bad_target, margin in wrong:
        try:
            cut_certificate(bad_paid, bad_target, margin)
        except ValueError:
            pass
        else:
            raise ValueError('False native reused-owner budget accepted')
    return {'source_receipt_sha256': NATIVE_RECEIPT_SHA256,
            'two_call_paid': {str(r): n for r, n in sorted(paid.items())},
            'reused_H9_owners': 112, 'cases': cases,
            'budget_controls': ['excess margin', 'double-counted aliased helper jobs',
                                'unpaid omitted centers'],
            'scope': 'Both hypothetical full-capacity policies lose for every 0<=C<1; no prefix capacity or native replay claimed'}


def check():
    lengths = list(range(2, 33))
    rows = []
    for n in lengths:
        if n % 2:
            actual = controller(n)
            right, diagonal, correction, left = boundaries(n)
            operations = right + diagonal + diagonal + correction + left
            m = (n-1)//2
            expected = (5*m-2, m, 3*m)
        else:
            actual = even_controller(n)
            right, correction, middle, left = even_boundaries(n)
            operations = right + correction + middle + left
            m = n//2
            expected = (3*n-7, 5*m-3, 3*m-3+2*((m-1) % 2)) if n >= 4 else (0, 2, 0)
        need(actual == target(n), f'Exact all-column cyclic identity n={n}')
        adds = sum(op[0] == 'add' for op in operations)
        swaps = sum(op[0] == 'swap' for op in operations)
        scales = sum(op[0] == 'scale' for op in operations)
        need((adds, swaps, scales) == expected, 'Complete boundary inventory')
        rows.append({'n': n, 'Q_jobs': 2*((n-1)//2), 'calls': 2, 'scalar_ADDs': adds,
                     'swaps': swaps, 'signed_P_scales': scales})
    mutations = ['missing spectator injection', 'missing long-root correction',
                 'wrong long-root sign', 'missing Pauli conjugations',
                 'missing spectator restoration', 'sign-only raw dual']
    for mutation in mutations:
        need(controller(5, mutation) != target(5), 'Rejected mutation: '+mutation)
    even_mutations = [x.replace('missing Pauli conjugations', 'missing middle Pauli scales')
                      for x in mutations]
    even_mutations += ['wrong cyclic wrap weight']
    for mutation in even_mutations:
        need(even_controller(6, mutation) != target(6), 'Rejected even mutation: '+mutation)
    try:
        boundaries(4)
    except ValueError:
        pass
    else:
        raise ValueError('Even lengths must not enter the odd construction')
    return {
        'status': 'PASS_HOMOGENEOUS_CHAIN_EXTRACTION',
        'scope': 'Conditional cyclic-ring identity and restricted two-call optimum; no new kappa',
        'lengths': lengths,
        'independent_input_columns': sum(lengths),
        'coefficient_slots': sum(4*n*n for n in lengths),
        'boundary_profiles': rows,
        'rejected_controller_mutations': mutations,
        'rejected_even_controller_mutations': even_mutations,
        'dirty_workspace_rank_fixtures': lower_bound_fixtures(),
        'tensor_evaluation_ranks_f1_through_f4': faithful_gaussian_check(),
        'native_reused_helper_budget': native_reuse_budget(),
        'proof': 'PROOF.md',
        'native_embedding': 'unknown',
        'selected_kappa_changed': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = check()
    path = Path(__file__).with_name('RESULT.json')
    if args.write:
        path.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    else:
        need(json.loads(path.read_text(encoding='utf-8')) == result, 'Committed receipt matches replay')
    print(result['status'])


if __name__ == '__main__':
    main()
