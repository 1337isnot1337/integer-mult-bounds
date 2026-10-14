"""Eisenstein E8 (Witting, 40 lines, w = 4): every decoder on the pattern costs >= 40 (Theorem C pairing rank).

Checks (exact):
 1. hE(x,y) = (<x,y> - w<x,rho y>)/4 is Z[w]-valued, sesquilinear (hE(x,rho y) = w hE, hE(rho x,y) = w^2 hE),
    diag = 2+w on all 40 representatives (norm 3: a 2-adic unit), |hE|^2 = 1 on the 27 non-orthogonal pairs per line.
 2. For random line sets R, A: K-rank of hE[R,A] (realified, exact) == Theorem-C pairing rank (real rank / 2).
 3. Line lattices: Gram of {r, rho r} is [[2,-1],[-1,2]] (det 3, odd) for every line.
 4. Reduction: for random integer N with N_TT odd and N_TS even on non-orthogonal pairs (arbitrary on orthogonal
    pairs), (hE o N) mod 2 over F4 = Z[w]/2 has rank 40, hence rank_K(hE o N) = 40.
 5. Sum-rank: on random term families, sum_j rank hE[R_j,A_j] >= rank (hE o N).
"""
import sys, random; sys.path.insert(0, sys.path[0])
from lines import *

def f4_rank(Ma, Mb):
    """rank over F4 = F2[w]/(w^2+w+1) of the matrix (Ma + Mb w) mod 2.  Elements as 2-bit ints a + 2b."""
    mul = [[0]*4 for _ in range(4)]
    def m(x, y):  # (a+bw)(c+dw) = ac + (ad+bc)w + bd w^2, w^2 = w+1
        a, b = x & 1, x >> 1; c, d = y & 1, y >> 1
        r0 = (a*c + b*d) & 1; r1 = (a*d + b*c + b*d) & 1
        return r0 | (r1 << 1)
    for x in range(4):
        for y in range(4): mul[x][y] = m(x, y)
    inv = {1: 1, 2: 3, 3: 2}
    M = [[int(a % 2) | (int(b % 2) << 1) for a, b in zip(ra, rb)] for ra, rb in zip(Ma, Mb)]
    n, mm = len(M), len(M[0]); r = 0
    for c in range(mm):
        p = next((i for i in range(r, n) if M[i][c]), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        iv = inv[M[r][c]]; M[r] = [mul[iv][x] for x in M[r]]
        for i in range(n):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [x ^ mul[f][y] for x, y in zip(M[i], M[r])]
        r += 1
    return r

def realify(Ma, Mb):
    """a + b w acting on Q^2 = Q(w) (basis 1, w): mult by w maps 1->w, w->w^2=-1-w."""
    n, m = Ma.shape
    R = np.zeros((2*n, 2*m), dtype=object)
    for i in range(n):
        for j in range(m):
            a, b = int(Ma[i, j]), int(Mb[i, j])
            R[2*i:2*i+2, 2*j:2*j+2] = [[a, -b], [b, a - b]]
    return R

def main(seed=1, trials=200):
    W = views(); S = W['Eisen']; V = S.reps; rho4 = W['_rho']; v = S.v
    assert v == 40 and S.w == 4
    a, b = eisen_gram(V, rho4)
    # 1. sesquilinearity on all representative pairs and their rho-images
    rV = (V @ rho4.T) // 4
    a2, b2 = eisen_gram_pair(V, rV, rho4)
    # hE(x, rho y) = w hE(x,y):  w(a + b w) = a w + b(-1 - w) = -b + (a - b) w
    assert (a2 == -b).all() and (b2 == a - b).all()
    a3, b3 = eisen_gram_pair(rV, V, rho4)
    # hE(rho x, y) = w^2 hE = (-1-w)(a+bw) = -a - (a) w - b w - b w^2 = -a + b + (-a) w ... compute: w^2(a+bw)=a w^2 + b w^3 = a(-1-w) + b
    assert (a3 == -a + b).all() and (b3 == -a).all()
    assert set(zip(np.diag(a).tolist(), np.diag(b).tolist())) == {(2, 1)}
    nrm = a*a - a*b + b*b
    off = ~np.eye(v, dtype=bool)
    assert ((nrm > 0) & off == S.NO).all() and set(nrm[S.NO].tolist()) == {1} and (S.NO.sum(1) == 27).all()
    print('PASS eisen.gram: hE sesquilinear, diag 2+w (norm 3), 27 non-orthogonal pairs per line all of norm 1')
    # 3. line lattices
    for T in range(v):
        r = V[T]; rr = rho4 @ r // 4
        Gm = [[r @ r // 4, r @ rr // 4], [rr @ r // 4, rr @ rr // 4]]
        assert Gm == [[2, -1], [-1, 2]]
    print('PASS eisen.linelattice: every line lattice <r, rho r> has Gram [[2,-1],[-1,2]] (det 3, odd)')
    rnd = random.Random(seed)
    # 2. K-rank of hE block == Theorem C pairing rank
    for _ in range(trials):
        R = rnd.sample(range(v), rnd.randint(1, 8)); A = rnd.sample(range(v), rnd.randint(1, 8))
        Rk = rank_q(realify(a[np.ix_(R, A)], b[np.ix_(R, A)]).tolist())
        assert Rk % 2 == 0 and Rk // 2 == S.pair_rank(R, A)
    print(f'PASS eisen.krank: rank_K hE[R,A] == pairing rank on {trials} random (R,A)')
    # 4. reduction
    for _ in range(trials // 4):
        N = np.zeros((v, v), dtype=np.int64)
        for T in range(v):
            for U_ in range(v):
                if T == U_: N[T, U_] = 2 * rnd.randint(0, 3) + 1
                elif S.NO[T, U_]: N[T, U_] = 2 * rnd.randint(0, 3)
                else: N[T, U_] = rnd.randint(0, 7)
        assert f4_rank(a * N, b * N) == 40
    print(f'PASS eisen.reduction: (hE o N) mod 2 has F4-rank 40 for {trials//4} random admissible N')
    # 5. sum-rank on random term families (not necessarily decoders)
    for _ in range(trials // 10):
        terms = [(rnd.sample(range(v), rnd.randint(1, 10)), rnd.sample(range(v), rnd.randint(1, 10))) for _ in range(rnd.randint(1, 6))]
        N = np.zeros((v, v), dtype=np.int64)
        for R, A in terms:
            for T in R:
                for U_ in A: N[T, U_] += 1
        lhs = sum(S.pair_rank(R, A) for R, A in terms)
        rhs = rank_q(realify(a * N, b * N).tolist()) // 2
        assert lhs >= rhs
    print(f'PASS eisen.sumrank: sum_j rank >= rank(hE o N) on {trials//10} random term families')
    print('RESULT eisen: every decoder (any number of totals, asymmetric) has sum_j beta_j >= 40 = v  =>  x_K >= 1')

def eisen_gram_pair(X, Y, rho4):
    A = X @ Y.T; Bm = X @ rho4 @ Y.T
    assert (A % 4 == 0).all() and (Bm % 16 == 0).all()
    return A // 4, -(Bm // 16)

if __name__ == '__main__':
    main()
