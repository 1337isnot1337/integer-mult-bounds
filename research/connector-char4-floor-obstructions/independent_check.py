"""Independent outside-component and cyclic charge checks from literal states."""
from itertools import combinations, product
from random import Random
from math import comb
import json
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent


def cycle_states(walk, k, start):
    state = list(start)
    states = [tuple(state)]
    for source in walk:
        state[source] = (state[source] + 1) % 4
        states.append(tuple(state))
    if states[0] != states[-1]:
        raise ArithmeticError('cycle not restored')
    return states


def component_stats(states, walk, first, last):
    bad = [0] * len(states[0])
    internal = 0
    for t in range(first, last):
        source = walk[t]
        if states[t][source] == 0:
            internal += 1
        else:
            bad[source] += 1
    if any(count not in (0, 3) for count in bad):
        raise ArithmeticError('source bad arc split between components')
    d = sum(count == 3 for count in bad)
    if d < 1 or last - first != 3 * d + internal:
        raise ArithmeticError('component length formula fails')
    seen = set()
    repeated = []
    for t in range(first, last + 1):
        parity = tuple(value % 2 for value in states[t])
        if parity in seen:
            repeated.append(t)
        seen.add(parity)
    if internal == 0 and d <= 3 and len(repeated) < 2:
        raise ArithmeticError('small component has fewer than two repeats')
    return d, internal, repeated


def inspect(walk, k, origin):
    states = cycle_states(walk, k, origin)
    inside = [all(value <= 1 for value in state) for state in states]
    if not any(inside):
        return 0
    pivot = inside.index(True)
    rotated = walk[pivot:] + walk[:pivot]
    states = cycle_states(rotated, k, states[pivot])
    inside = [all(value <= 1 for value in state) for state in states]
    vertices = [t for t, ok in enumerate(inside) if ok]
    components = [(a, b) for a, b in zip(vertices, vertices[1:]) if b - a > 1]
    stats = [component_stats(states, rotated, a, b) for a, b in components]
    s = len(vertices) - 1
    small = sum(h == 0 and d <= 3 for d, h, repeats in stats)
    internal_outside = sum(h for d, h, repeats in stats)
    if sum(d for d, h, repeats in stats) != k or s != k - internal_outside + len(stats):
        raise ArithmeticError('global edge/component accounting fails')
    global_seen, global_repeats = set(), set()
    for t, state in enumerate(states[:-1]):
        value = tuple(v % 2 for v in state)
        if value in global_seen:
            global_repeats.add(t)
        global_seen.add(value)
    r = len(global_repeats)
    charges = set()
    for d, h, repeats in stats:
        if h == 0 and d <= 3:
            for t in repeats:
                if t in charges or (t < len(walk) and t not in global_repeats):
                    raise ArithmeticError('duplicate or invalid parity charge')
                charges.add(t)
    capital_s = min(k, (r + 1) // 2)
    bound = k + capital_s + (k - capital_s) // 4
    if 2 * small > len(charges) or len(charges) > r + 1 or s > bound:
        raise ArithmeticError('component charge/intersection bound fails')
    return 1


def compare_certificate(result):
    certificate = json.loads((HERE / "CERTIFICATE.json").read_text())
    actual = [(r["r"], r["H"], r["upper"]) for r in result["rows"]]
    expected = [(r["r"], r["cube_intersection"], r["mask_upper"]) for r in certificate["rows"]]
    if actual != expected or result["max_k19_upper"] != certificate["max_mask_upper"]:
        raise ArithmeticError("independent cube table differs from certificate")
    if result["component_cases"] != 21120 or result["nonempty_cases"] != 20976:
        raise ArithmeticError("independent component family incomplete")


def check_catalog():
    rows = json.loads((HERE / "MAXIMIZERS.json").read_text())["canonical_maximizers"]
    if len(rows) != 4:
        raise ArithmeticError("unexpected catalog size")
    words = set()
    for row in rows:
        word = row["walk"]
        if len(word) != 20 or any(word.count(j) != 4 for j in range(5)):
            raise ArithmeticError("invalid catalog word")
        order = list(dict.fromkeys(word))
        if order != list(range(5)) or tuple(word) in words:
            raise ArithmeticError("catalog is noncanonical or duplicated")
        words.add(tuple(word))
        q = cycle_states(word, 5, [0]*5)
        masks = set()
        for a, b in combinations(range(21), 2):
            value = tuple((x+y) % 4 for x, y in zip(q[a], q[b]))
            if max(value) <= 1:
                masks.add(sum(x << j for j, x in enumerate(value)))
        for a in range(21):
            value = tuple(2*x % 4 for x in q[a])
            if max(value) <= 1:
                masks.add(sum(x << j for j, x in enumerate(value)))
        if len(masks) != 29 or [m for m in range(1, 32) if m not in masks] != row["missing"]:
            raise ArithmeticError("independent catalog coverage differs")
        if not all(set(word[t:t+5]) == set(range(5)) for t in range(0, 20, 5)):
            raise ArithmeticError("catalog word lacks four permutation rounds")


def receipt():
    digest = hashlib.sha256()
    names = ('CERTIFICATE.json', 'CUBE-SHARPNESS.json', 'README.md', 'SOURCES.json', 'TASK.json', 'VERIFY.json', 'DEPTH2.md', 'MAXIMIZERS.json', 'depth_two.py', 'independent_depth2.c', 'independent_check.py', 'verify.py')
    for name in names:
        digest.update(name.encode() + b"\0" + hashlib.sha256((HERE / name).read_bytes()).digest())
    return digest.hexdigest()


def check_sharpness():
    data = json.loads((HERE / "CUBE-SHARPNESS.json").read_text())
    word = data["word"]
    if len(word) != 72 or any(word.count(j) != 4 for j in range(18)):
        raise ArithmeticError("sharpness word multiplicities")
    states = cycle_states(word, 18, [0]*18)[:-1]
    parity = {tuple(v % 2 for v in q) for q in states}
    inside = [t for t, q in enumerate(states) if all(v <= 1 for v in q)]
    if len(parity) != 72 or len(inside) != 22 or inside != data["valid_boundaries"]:
        raise ArithmeticError("independent sharpness check failed")


def main():
    checked = nonempty = 0
    for zero in combinations(range(8), 4):
        walk = [0 if t in zero else 1 for t in range(8)]
        for origin in product(range(4), repeat=2):
            nonempty += inspect(walk, 2, origin)
            checked += 1
    rng = Random(102052)
    for k in (3, 4, 9, 19):
        for _ in range(100):
            walk = [j for j in range(k) for _ in range(4)]
            rng.shuffle(walk)
            q = cycle_states(walk, k, [0] * k)
            for _ in range(50):
                point = rng.choice(q[:-1])
                origin = tuple((rng.randrange(2) - value) % 4 for value in point)
                nonempty += inspect(walk, k, origin)
                checked += 1
    rows = []
    for r in range(76):
        capital_s = min(19, (r + 1) // 2)
        h = 19 + capital_s + (19 - capital_s) // 4
        cube = comb(76, 3) * h // 4 + comb(76, 2) + 1
        n = 76 - r
        parity = 1 + comb(n, 2) + comb(n, 4) if n >= 4 else 1 + comb(n, 2)
        rows.append({'r': r, 'H': h, 'cube_bound': cube, 'parity_bound': parity,
                     'upper': min(cube, parity)})
    if max(row['upper'] for row in rows) >= 1 << 19:
        raise ArithmeticError('nineteen-source exclusion fails')
    result = {'component_cases': checked, 'nonempty_cases': nonempty,
              'max_k19_upper': max(row['upper'] for row in rows), 'rows': rows}
    compare_certificate(result)
    check_catalog()
    check_sharpness()
    print(json.dumps({key: value for key, value in result.items() if key != 'rows'}, sort_keys=True))
    print('receipt_sha256', receipt())
    print('PASS_INDEPENDENT_CUBE_COMPONENTS N4<=18')


if __name__ == '__main__':
    main()
