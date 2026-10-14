"""Direct SAT (S1's open item): is there any Hurwitz decoder with n <= C terms and sum of exact costs <= C?
Terms (w_j, u_j) arbitrary; cost_j from the exact formula (checked in hurwitz_floor.py); cost-0 terms are useless
(they touch only free entries) so n <= C.  Symmetry: terms sorted by (cost desc) not imposed; lex order on w_j words."""
import sys, itertools; sys.path.insert(0, sys.path[0])
from lines import *
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153
C = int(sys.argv[1])
S = views()['Hurwitz']; v = S.v
rel = [(T, U_) for T in range(v) for U_ in range(v) if T == U_ or S.NO[T, U_]]
pool = IDPool(); cl = []
W = [[pool.id(('w', j, T)) for T in range(v)] for j in range(C)]
U = [[pool.id(('u', j, T)) for T in range(v)] for j in range(C)]
P = {}
for j in range(C):
    for T, S_ in rel:
        p = pool.id(('p', j, T, S_)); P[j, T, S_] = p
        cl += [[-p, W[j][T]], [-p, U[j][S_]], [p, -W[j][T], -U[j][S_]]]
def xor_eq(lits, target):
    # chain xor with aux vars
    acc = lits[0]
    for l in lits[1:]:
        z = pool.id(('x', len(cl), acc, l))
        cl.extend([[-z, acc, l], [-z, -acc, -l], [z, -acc, l], [z, acc, -l]]); acc = z
    cl.append([acc] if target else [-acc])
for T, S_ in rel:
    xor_eq([P[j, T, S_] for j in range(C)], 1 if T == S_ else 0)
costlits = []
for j in range(C):
    r1 = pool.id(('r1', j)); r2 = pool.id(('r2', j))
    for T, S_ in rel: cl.append([-P[j, T, S_], r1])
    # r2 >= (|R|>=2 & |A|>=2 & relevant): any 2 rows, 2 cols -> relevant automatically (each line orth to one other)
    for T1, T2 in itertools.combinations(range(v), 2):
        for S1, S2 in itertools.combinations(range(v), 2):
            cl.append([-W[j][T1], -W[j][T2], -U[j][S1], -U[j][S2], r2])
    costlits += [r1, r2]
enc = CardEnc.atmost(lits=costlits, bound=C, vpool=pool, encoding=EncType.seqcounter)
s = Cadical153(bootstrap_with=cl + enc.clauses)
print('C', C, 'SAT' if s.solve() else 'UNSAT', flush=True)
