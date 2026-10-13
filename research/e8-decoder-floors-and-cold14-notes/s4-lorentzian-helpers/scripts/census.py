"""Reader-set census of the label functionals of I_{n,1} (S_n orbit = Hamming weight of the functional).
For each weight k: |R(p)|, its type split (triples / pairs), span rank over Q, Gram (pairing) rank of G[R,R]."""
import sys, json
import numpy as np
sys.dont_write_bytecode = True
import units as U

def census(n):
    L, G, lab = U.lorentz_family(n)
    out = []
    for k in range(1, n + 1):
        p = np.array([1] * k + [0] * (n - k))
        R = np.nonzero((lab @ p) % 2)[0]
        ntri = int((R < len(L) - n * (n - 1) // 2).sum())
        sp = U.rank_q(L[R].tolist()) if len(R) else 0
        gr = U.gram_rank(G, R)
        out.append(dict(k=k, readers=len(R), triples=ntri, pairs=len(R) - ntri, span=sp, gram=gr))
    return out

if __name__ == '__main__':
    res = {}
    for n in map(int, sys.argv[1:] or ['9', '11', '13']):
        res[n] = census(n)
        for r in res[n]:
            print(n, r, flush=True)
