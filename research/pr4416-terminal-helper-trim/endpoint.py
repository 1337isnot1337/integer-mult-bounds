#!/usr/bin/env python3
"""Explicit conditional ordinary/outer endpoint for the terminal trim.

1337isnot1337 with substantial OpenAI Codex assistance. Apache-2.0.
The integer source/exit compiler is Jacob Alan Sussman's Theorem1G;
logarithmic majorants and higher-moment transfer follow PR4411/PR4433.
"""
from fractions import Fraction as Q
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def module(name, path):
    spec = importlib.util.spec_from_file_location(name,path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def uniform_rank(strict, C, KAPPA):
    E = module('pr4433_logarithmic_intervals', ROOT/'research/higher-moment-strictification/verify.py')
    v, t, theta = strict['tensor_power'], 1-C, Q(6,7)
    gap = (C-KAPPA)/7
    need(strict['cutoff_base'] == 10 and strict['floor_base'] == 15,
         'Use the actual complete separated mixed unit')
    need(10**7 < 15**6 and 2*(10**v)**7 <= (121**v)**6,
         'Strict exit exponent and shifted logarithm bound')
    eta = E.scale(E.exp_interval(E.scale(E.log_bounds(121),-v*C)),t)
    base = E.exp_interval(E.scale(E.log_bounds(121),v*C))
    p = 1
    while eta[0] <= theta**p or base[1] >= 2**p:
        p += 1
    need(eta[0] > theta**p and base[1] < 2**p,
         'Logarithmic majorant covers exits and ordinary base cases')
    need(gap > 0 and gap.numerator == 1, 'Exact reciprocal integer grid')
    step = gap.denominator
    def passes(j):
        return (step*j+1)**p < 2**j
    lo,hi = 1,2
    while not passes(hi):
        lo,hi = hi,2*hi
    while hi-lo > 1:
        mid = (lo+hi)//2
        if passes(mid): hi = mid
        else: lo = mid
    H = step*hi
    need(H > 7*v and passes(hi) and not passes(hi-1),
         'Explicit finite winning rank and neighboring rejection')
    need(eta[1] < theta**(p-1) or base[0] > 2**(p-1),
         'One lower logarithm power cannot meet these sufficient bounds')
    return {'tensor_power':v, 'uniform_saving':C-gap, 't':t, 'theta_upper':theta,
            'gap':gap, 'logarithm_power':p, 'eta':E.display(eta),
            'm_to_saving':E.display(base), 'H':H, 'N':'2^'+str(H),
            'integer_test':{'left_base':H+1,'left_exponent':p,'right_base':2,'right_exponent':hi},
            'grid_step':step, 'previous_grid_point_rejected':True,
            'lower_logarithm_power_rejected':True,
            'materialized_uniform_word':False}


def run(strict):
    S = module('trim_constants',HERE/'strictification.py')
    C,K = S.C,S.KAPPA
    need(Q(strict['tested_saving']) == C and Q(strict['normalized_paid_upper']) < 1,
         'Bind the fully charged strict mixed moment')
    compiler = uniform_rank(strict,C,K)
    d = (C-K)/7
    params = {'kappa':K,'tested_saving':C,'complex_uniform_saving':C-d,
              'b':K+5*d,'a':K+4*d,'q':K+3*d,'bit_saving':Q('.0027'),
              'epsilon':1-d,'beta':1-3*d,'r0':d/10,'stop':d,'layout':d,'d':d}
    E = module('credited_pr4405_outer_ledger',
               ROOT/'research/pr4359-p7-padding/dependencies/compiler-refill/endpoint.py')
    outer = E.ledger(params)
    need(len(outer['strict_checks']) == 54 and len(outer['functional_checks']) == 3,
         'Retain every source outer admission predicate')
    need(all(v > 0 for group in ('strict_checks','functional_checks') for v in outer[group].values()),
         'Every strict and functional admission inequality holds')
    need(len(outer['margins']) == 9 and min(outer['margins'].values()) > K,
         'Every one of the nine complete cost rows beats kappa')
    controls = {}
    for name,updates in [('closed_epsilon',{'epsilon':Q(1)}),
                         ('closed_uniform_gap',{'complex_uniform_saving':params['b']}),
                         ('unfunded_outer_point',{'kappa':C}),
                         ('insufficient_BIT',{'bit_saving':Q('.0023')})]:
        row = E.ledger(dict(params,**updates))
        failed = {k:v for k,v in row['strict_checks'].items() if v <= 0}
        need(failed,'Reject '+name)
        controls[name] = failed
    return {'status':'PASS_CONDITIONAL_TRIMMED_OUTER_POINT', 'kappa':K,
            'tested_saving':C, 'gain_over_PR4416':K-Q('.00268647'),
            'relative_gain_over_PR4416':(K-Q('.00268647'))/Q('.00268647'),
            'compiler':compiler, 'outer':outer,
            'minimum_outer_margin_above_kappa':min(outer['margins'].values())-K,
            'negative_controls':controls,
            'scope':'Conditional all-column native construction, exact finite moment and outer arithmetic. Inherited analytic, precision, fixed-tape, storage and recovery premises remain separate. No selected-frontier promotion or formal full multiplication theorem.'}
