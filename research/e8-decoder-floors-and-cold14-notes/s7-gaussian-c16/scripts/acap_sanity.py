"""Sanity: how many level-k reps have a member that is 'a-capable' (some 2-flat Z inside it with every 3-flat through Z a valid substitute)."""
import sys; sys.path.insert(0, sys.path[0])
from refine import good, inside, through, ok
for k in range(1, 16):
    n = 0; mem = 0
    for T in good[k]:
        T = list(T); c = 0
        for i in range(k):
            subst = lambda h: sorted(T[:i] + [h] + T[i + 1:])
            if any(all(h == T[i] or (h not in T and ok(subst(h))) for h in through[z]) for z in inside[T[i]]): c += 1
        n += c > 0; mem += c
    print('k=%2d reps %4d with a-capable member %4d (total a-capable members %d)' % (k, len(good[k]), n, mem), flush=True)
