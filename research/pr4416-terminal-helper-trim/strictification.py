#!/usr/bin/env python3
"""Charged higher-moment strictification of the terminal-trim native unit.

1337isnot1337 with substantial OpenAI Codex assistance. Apache-2.0.
Native construction: zxv, PR4359; tensor completion: PR4416;
higher-moment tail and exact interval engine: zxv, PR4433.
"""
from fractions import Fraction as Q
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C = Q('0.002696355')
KAPPA = Q('0.00269635')
V, CUTOFF, FLOOR = 180, 10, 15
U = Q(3, 10)
TARGETS = {4:330, 5:90, 6:270, 7:840, 8:1395, 9:3195,
           25:448, 41:448, 57:448, 121:224}
PAID = {1:36975, 2:10695, 3:3360, 4:1530, 5:300,
        8:1464, 16:448, 32:448, 48:448}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def intervals():
    return module('credited_pr4433_intervals',
                  ROOT/'research/higher-moment-strictification/verify.py')


def run(native):
    T = {int(k): v for k, v in native['targets'].items()}
    P = {int(k): v for k, v in native['paid'].items()}
    need(T == TARGETS and P == PAID, 'Bind the actual reconstructed native invoice')
    need(native['dimension'] == 121 and native['productive_fields'] == 7688,
         'Bind ambient dimension and distinct productive fields')
    t = 1-C
    B, T1, P1 = sum(T.values()), sum(k*n for k,n in T.items()), sum(k*n for k,n in P.items())
    need((T1, P1, T1-P1) == (131393, 130785, 608), 'Complete rank-one masses')
    need(0 < C < U and 1 < CUTOFF < FLOOR < 121 and t+U >= 1,
         'Higher-moment and strict-rank hypotheses')
    E = intervals()
    target, paid = E.moment(T,t), E.moment(P,t)
    alpha = E.divide(paid,target)
    gamma = E.divide(E.moment(P,t+U), E.mul(E.power(CUTOFF,U),target))
    delta = E.divide((Q(B*FLOOR),)*2,E.mul(E.power(CUTOFF,C),target))
    limits = (1-Q(1,10**9), Q(181,200), Q(881,1000))
    for name, bounds, limit in zip(('alpha','gamma','delta'),(alpha,gamma,delta),limits):
        need(0 < bounds[0] <= bounds[1] < limit < 1, name+' has a strict rational upper bound')
    a,g,d = limits
    bound = 1/(1+V*(1-a))+2*g**V+2*d**V
    need(bound < 1, 'Charge every original paid tail and productive completion')
    need(1/(1+160*(1-a))+2*g**160+2*d**160 > 1,
         'The same rounded certificate rejects power160')
    old_gamma = E.divide((Q(P1),)*2,E.mul(E.power(CUTOFF,C),target))
    need(alpha[0]**V+2*old_gamma[0]**V > 1,
         'Rank-one-tail estimate cannot certify this chosen small power')
    old_T = dict(T); old_T.pop(4); old_T[5] += 330
    old_P = dict(P); old_P[1] += 330
    need(E.moment(old_T,t)[1] < E.moment(old_P,t)[0],
         'The predecessor invoice fails at the new tested saving')
    ceiling = Q('0.002696357')
    need(E.moment(T,1-ceiling)[1] < E.moment(P,1-ceiling)[0],
         'Reject an unsupported raw saving above the new bracket')
    gain = E.moment(T,t)[0]-E.moment(P,t)[1]
    need(gain > 0, 'Exact positive raw mixed surplus')
    return {'status':'PASS_EXACT_TRIMMED_HIGHER_MOMENT_STRICTIFICATION',
            'tested_saving':C, 'tensor_power':V, 'cutoff_base':CUTOFF, 'floor_base':FLOOR,
            'tail_offset':U, 'paid_tail_exponent':t+U, 'targets':T, 'paid':P,
            'productive_fields':B, 'target_rank_one_moment':T1, 'paid_rank_one_moment':P1,
            'rank_one_surplus':608, 'raw_moment_margin':E.display((target[0]-paid[1],target[1]-paid[0])),
            'alpha':E.display(alpha), 'gamma':E.display(gamma), 'delta':E.display(delta),
            'rational_limits':limits, 'normalized_paid_upper':bound,
            'strict_moment_gap':E.display((1-bound,)*2),
            'ambient':'121^180', 'minimum_target':'15^180', 'maximum_paid':'10^180',
            'rank_one_surplus_encoding':'131393^180-130785^180',
            'raw_moment_sign_change_bracket':[C,ceiling],
            'controls':{'predecessor_at_new_saving_rejected':True,
                        'unsupported_raw_saving_rejected':True,
                        'power160_under_same_limits_rejected':True,
                        'rank_one_tail_at_power180_rejected':True},
            'materialized_product_or_uniform_word':False}
