"""Exact width-73 optimizer for residual ranks 4, 5, 7, 8 and 9.

The optimum is for the bank-dependent paid moment, including fallback,
with a fixed residual inventory. This does not validate a multiplication
supplier or optimize its local program. See PROOF.md for the exact domain.
"""
from collections import Counter
from math import gcd, lcm
from pathlib import Path
import argparse
import json

RANKS = (4, 5, 7, 8, 9)


class NoSaturatingPacking(ValueError):
    """The inventory cannot attain this dual bound at any replication."""


def validate(inventory):
    if any(type(r) is not int or r not in RANKS or type(n) is not int or n < 0
           for r, n in inventory.items()):
        raise ValueError('Expected nonnegative integer counts at ranks 4, 5, 7, 8, 9')
    return Counter({r: inventory.get(r, 0) for r in RANKS})


def minimum_replicas(inventory):
    """Smallest positive replication admitting an exact dual-saturating packing."""
    n = validate(inventory)
    K = sum(n.values())
    W = sum((r-1)*count for r, count in n.items())
    if n[8] < n[4]:
        raise NoSaturatingPacking('Each rank-4 item needs at least one rank-8 item')
    if n[8] + 2*n[7] < 3*n[4]:
        raise NoSaturatingPacking('Insufficient rank-7/rank-8 capacity around rank-4 items')
    if 9*W < 64*K:
        raise NoSaturatingPacking('The equality equations require a negative padding count')
    return 64 // gcd(W, 64)


def _pair(blocks):
    """Pair an even number of equally weighted blocks, using compressed counts."""
    result, carry = [], None
    for pattern, count in blocks:
        if not count:
            continue
        if carry is not None:
            result.append((carry + pattern, 1))
            count -= 1
            carry = None
        if count // 2:
            result.append((Counter({r: 2*n for r, n in pattern.items()}), count // 2))
        if count % 2:
            carry = pattern
    if carry is not None:
        raise ArithmeticError('Nonintegral block pairing')
    return result


def construct(inventory, replicas=None, replica_multiple=1):
    """Return an optimal packing as the existing bank emitter's pattern list.

    Default to the smallest replication that reaches the exact lower bound.
    Work uses a bounded number of integer operations, independent of counts;
    large multiplicities remain compressed.
    """
    base = validate(inventory)
    least = minimum_replicas(base)
    if type(replica_multiple) is not int or replica_multiple <= 0:
        raise ValueError('The architecture replica multiple must be a positive integer')
    admissible = lcm(least, replica_multiple)
    if replicas is None:
        replicas = admissible
    if type(replicas) is not int or replicas <= 0 or replicas % admissible:
        raise ValueError(f'Replicas must be a positive multiple of {admissible}')
    n = Counter({r: count*replicas for r, count in base.items()})
    K = sum(n.values())
    W = sum((r-1)*count for r, count in n.items())
    banks, pads = W//64, 9*(W//64)-K

    # Deficits 9-r are 5,4,2,1,0. Complete every deficit-5 item first.
    x = min(n[4], n[7])
    y = n[4]-x
    full = [(Counter({4:1,7:1,8:1}),x), (Counter({4:1,8:3}),y)]
    ones = n[8]-x-3*y
    if ones < 0 or ones % 2:
        raise ArithmeticError('Invalid remaining deficit-one count')
    twos = [(Counter({7:1}),n[7]-x), (Counter({8:2}),ones//2)]
    fours = [(Counter({5:1}),n[5])] + _pair(twos)
    full += _pair(fours)

    packed = Counter()
    for pattern, count in full:
        if not count:
            continue
        pattern[9] = 9-sum(pattern.values())
        key = tuple(pattern.get(r,0) for r in RANKS)+(0,)
        packed[key] += count
    if pads:
        packed[(0,0,0,0,8,1)] += pads
    patterns = [dict(count=count, **{f'r{r}':v for r,v in zip(RANKS,key) if v},
                     padding=key[-1]) for key,count in sorted(packed.items())]
    certificate = check(patterns, n)
    if certificate['banks'] != banks or certificate['padding'] != pads:
        raise ArithmeticError('Construction missed the equality count')
    certificate.update(replicas=replicas, minimum_replicas=least,
                       minimum_admissible_replicas=admissible, replica_multiple=replica_multiple,
                       inventory_per_replica=dict(base))
    return patterns, certificate


def check(patterns, inventory):
    """Independent integer census of a purported equality witness."""
    expected = validate(inventory)
    found, banks, pads = Counter(), 0, 0
    for p in patterns:
        if set(p)-{'count','padding',*(f'r{r}' for r in RANKS)}:
            raise ValueError('Unknown pattern field')
        count, pad = p['count'], p['padding']
        if type(count) is not int or count <= 0 or type(pad) is not int or pad not in (0,1):
            raise ValueError('Invalid pattern multiplicity or padding')
        items = {r:p.get(f'r{r}',0) for r in RANKS}
        if any(type(v) is not int or v < 0 for v in items.values()):
            raise ValueError('Invalid item count')
        if sum(r*v for r,v in items.items())+pad != 73:
            raise ValueError('Bank width differs from 73')
        if sum(items.values()) != 9-pad:
            raise ValueError('Pattern does not attain the exact bank bound')
        found.update({r:count*v for r,v in items.items()})
        banks += count
        pads += count*pad
    if found != expected:
        raise ValueError('Packing inventory does not match')
    K = sum(found.values())
    W = sum((r-1)*n for r,n in found.items())
    if W != 64*banks or pads != 9*banks-K:
        raise ValueError('Packing does not attain the inventory bound')
    return dict(banks=banks, padding=pads, items=K, weighted_inventory=W)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inventory',type=Path,help='JSON object mapping ranks to counts per replica')
    parser.add_argument('--replicas',type=int)
    parser.add_argument('--replica-multiple',type=int,default=1,
                        help='Required architecture multiple, e.g. 8 for the existing E8 expander')
    parser.add_argument('--output',type=Path,required=True,help='New patterns JSON file')
    args=parser.parse_args()
    raw=json.loads(args.inventory.read_text())
    patterns,certificate=construct({int(r):n for r,n in raw.items()},args.replicas,args.replica_multiple)
    with args.output.open('x') as stream:
        stream.write(json.dumps(patterns,indent=2)+'\n')
    print(json.dumps(certificate,indent=2))


if __name__ == '__main__':
    main()
