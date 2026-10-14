"""Hurwitz E8 (10 quaternionic lines in H^2, w = 2): every decoder on the pattern costs >= 10 = v (exact).

Model: decoder B = sum_j w_j u_j^T over F2 (R_j = supp w_j readers, A_j = supp u_j sources), B_TT = 1, B_TS = 0 on
H-non-orthogonal pairs, free on orthogonal pairs; cost_j = Theorem-C pairing rank of span(R_j) x span(A_j) in H-units.
Checks:
 1. structure: v = 10, w = 2, every line is H-orthogonal to exactly one other (5 orthogonal pairs), any two distinct
    lines span H^2.
 2. cost formula, exact for all |R|,|A| <= 2 and implied for larger sets (span saturates):
    cost = 0 if R x A has no equal-or-non-orthogonal pair; else 2 if |R| >= 2 and |A| >= 2; else 1.
 3. Proof (argued, README): split terms into cost-2 'general' terms X (2 per term >= 2 rank X), cost-1 single-row /
    single-column terms (rho, gamma), cost-0 terms (absorbed in free entries).  B + X vanishes off rows rho and columns
    gamma, so on rho' x gamma' (complements) X equals the pattern; its C x C principal part (C = rho' & gamma') is block
    diagonal with blocks [1] / [[1,*],[*,1]] (non-orthogonal pairs are 0), so rank X >= |C|/2 and
    cost >= |C| + 20 - |rho'| - |gamma'| >= 10.
 4. SAT cross-check of the reduced form: no (X of rank <= g, rho, gamma) with 2g + |rho| + |gamma| <= 9 (CaDiCaL).
 5. Attained: the 5 orthogonal pairs as frames, cost 5 x 2 = 10.
"""
import sys, itertools; sys.path.insert(0, sys.path[0])
from lines import *
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153

def formula(S, R, A):
    if not any(T == U_ or S.NO[T, U_] for T in R for U_ in A): return 0
    return 2 if len(R) >= 2 and len(A) >= 2 else 1

def main():
    S = views()['Hurwitz']; v = S.v
    assert v == 10 and S.w == 2
    orth = ~S.NO & ~np.eye(v, dtype=bool)
    assert (orth.sum(1) == 1).all()
    assert all(S.arank([a, b]) == 2 for a, b in itertools.combinations(range(v), 2))
    print('PASS hurwitz.structure: v 10, w 2, 5 orthogonal pairs (perfect matching), any two lines span H^2')
    small = [c for k in (1, 2) for c in itertools.combinations(range(v), k)]
    for R in small:
        for A in small:
            assert S.pair_rank(R, A) == formula(S, R, A)
    print(f'PASS hurwitz.costformula: exact pairing rank == formula on all {len(small)**2} (R,A) with |R|,|A| <= 2')
    # 4. reduced SAT: B + X supported on rows rho / cols gamma; X = sum_{k<g} a_k b_k^T
    cons = [(T, U_) for T in range(v) for U_ in range(v) if T == U_ or S.NO[T, U_]]
    for g in range(0, 5):
        cap = 9 - 2 * g
        pool = IDPool(); cl = []
        a = [[pool.id(('a', k, T)) for T in range(v)] for k in range(g)]
        b = [[pool.id(('b', k, T)) for T in range(v)] for k in range(g)]
        rho = [pool.id(('r', T)) for T in range(v)]; gam = [pool.id(('c', T)) for T in range(v)]
        for T, U_ in cons:
            # if T not in rho and U_ not in gamma: X_TU = [T==U_]
            prods = []
            for k in range(g):
                p = pool.id(('p', k, T, U_)); prods.append(p)
                cl += [[-p, a[k][T]], [-p, b[k][U_]], [p, -a[k][T], -b[k][U_]]]
            target = 1 if T == U_ else 0
            # xor(prods) == target, guarded by (~rho_T & ~gam_U)
            for bits in itertools.product((0, 1), repeat=len(prods)):
                if sum(bits) % 2 != target:
                    cl.append([rho[T], gam[U_]] + [(-p if bt else p) for p, bt in zip(prods, bits)])
        enc = CardEnc.atmost(lits=rho + gam, bound=cap, vpool=pool, encoding=EncType.seqcounter)
        s = Cadical153(bootstrap_with=cl + enc.clauses); res = s.solve(); s.delete()
        assert not res, g
    print('PASS hurwitz.sat: 2g + |rho| + |gamma| <= 9 is UNSAT for every g = 0..4 (CaDiCaL, no proof log)')
    pairs = sorted({tuple(sorted((T, int(np.nonzero(orth[T])[0][0])))) for T in range(v)})
    cost = sum(S.pair_rank(p, p) for p in pairs)
    N = np.zeros((v, v), int)
    for p in pairs:
        for T in p:
            for U_ in p: N[T, U_] += 1
    assert all(N[T, T] % 2 == 1 for T in range(v)) and all(N[T, U_] % 2 == 0 for T, U_ in cons if T != U_)
    assert cost == 10
    print('PASS hurwitz.attained: frame decoder (5 orthogonal pairs) is a valid decoder of cost 10')
    print('RESULT hurwitz: min over all decoders of sum_j beta_j = 10 = v  =>  x_K = 1')

if __name__ == '__main__':
    main()
