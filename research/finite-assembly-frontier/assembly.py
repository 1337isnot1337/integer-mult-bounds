"""Construct a finite witness for a rational target below the assembly ceiling.

George Lydakis, with OpenAI Codex assistance. Apache-2.0.
Supplier bounds and the inherited bootstrap/analytic interfaces are premises.
"""
from fractions import Fraction as Q
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

if not __debug__:
    raise RuntimeError('Assertions must remain enabled')

INITIAL = Q(384599, 10**10)
BRIDGE = {
    'semantic': {'C0': {'base': 2, 'exponent': 210000}, 'strict_literal_gap': 1},
    'rows': {'degree_gap': Q(10**6) - Q(51*20161, 25)},
}


def load_outer():
    spec = spec_from_file_location('retained_outer', Path(__file__).parent/'vendor/outer.py')
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ceiling(bit, complex_):
    """Supremum of this assembly family for the supplied rational caps."""
    bit, complex_ = Q(bit), Q(complex_)
    if not INITIAL < min(bit, complex_) < Q(1, 32) or complex_ >= Q(1, 32):
        raise ValueError('Require INITIAL < min(bit, complex) and complex < 1/32')
    u = min(bit, complex_)
    return u/(1+u)


def greatest_grid_target(bit, complex_, grid):
    """Greatest positive multiple of grid strictly below the supremum."""
    grid = Q(grid)
    if grid <= 0:
        raise ValueError('Grid must be positive')
    ticks = ceiling(bit, complex_)/grid
    target = ((ticks.numerator-1)//ticks.denominator)*grid
    if target <= 0:
        raise ValueError('No positive grid point below the supremum')
    return target


def ceilq(x):
    return -((-x.numerator)//x.denominator)


def construct(bit, complex_, target, coefficient_bits=512, initial=INITIAL):
    """Return finite rational parameters and all 47 retained outer margins.

    coefficient_bits is a supplied charge C <= 2**coefficient_bits, not a
    supplier admission. No numerical search, zero backoff or limit is used.
    """
    bit, complex_, target, initial = map(Q, (bit, complex_, target, initial))
    limit = ceiling(bit, complex_)
    u = min(bit, complex_)
    if initial != INITIAL:
        raise ValueError('The inherited initial bound must remain unchanged')
    if not 0 < target < limit:
        raise ValueError('Target must be strictly between zero and the supremum')
    if not isinstance(coefficient_bits, int) or isinstance(coefficient_bits, bool) or coefficient_bits < 1:
        raise ValueError('A positive integer finite coefficient charge is required')

    threshold = target/(1-target)
    seed = (u + max(initial, threshold))/2
    beta = (complex_-seed)/(2*complex_)
    assert initial < seed < bit and seed < (1-beta)*complex_
    assert 0 < beta < 1
    chain = [initial]
    cutoffs = []
    # Every pass shrinks the distance to seed by seed < 1/32. The positive
    # target distance proves termination; PROOF.md gives a finite step bound.
    while chain[-1] <= threshold:
        old = chain[-1]
        value = (1-seed)*seed + seed*old
        gaps = [seed-value, 1-value-seed, 1-value-seed*(1-old), 1-seed]
        gap = min(gaps)
        assert old < value < seed < 1-value and gap > 0
        cutoff = max(1, ceilq(36/gap**2), ceilq(2*(4+coefficient_bits)/gap))
        assert cutoff*gap**2 >= 36
        assert cutoff*gap >= 2*(4+coefficient_bits)
        cutoffs.append({'gap': gap, 'cutoff_log2': cutoff})
        chain.append(value)

    value = chain[-1]
    remaining = value/(1+value)-target
    eta = min(Q(1, 16), remaining/(6*value))
    assert 0 < eta <= Q(1, 16)
    outer = load_outer().assembly(value, complex_, BRIDGE, target, eta=eta, beta=beta)
    assert len(outer['strict_constraints']) == 47
    assert outer['minimum_margin'] > target
    assert value == seed-(seed-initial)*seed**(len(chain)-1)
    return {
        'status': 'PASS_FINITE_ASSEMBLY_FROM_SUPPLIED_CAPS',
        'bit_cap': bit, 'complex_cap': complex_, 'supremum': limit,
        'target': target, 'seed': seed, 'eta': eta, 'beta': beta,
        'coefficient_bits': coefficient_bits, 'bootstrap_chain': chain,
        'cutoffs': cutoffs, 'strict_constraints': outer['strict_constraints'],
        'minimum_margin': outer['minimum_margin'],
        'scope': 'Conditional assembly witness. Supplier admission and inherited all-size interfaces are premises.',
    }


def jsonable(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {key: jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [jsonable(item) for item in value]
    return value


if __name__ == '__main__':
    import argparse
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bit', type=Q, required=True)
    parser.add_argument('--complex', type=Q, required=True, dest='complex_')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--target', type=Q)
    group.add_argument('--grid', type=Q)
    parser.add_argument('--coefficient-bits', type=int, default=512)
    args = parser.parse_args()
    target = args.target if args.target is not None else greatest_grid_target(args.bit, args.complex_, args.grid)
    print(json.dumps(jsonable(construct(args.bit, args.complex_, target, args.coefficient_bits)), indent=2))
