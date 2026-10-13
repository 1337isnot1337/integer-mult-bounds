"""First cheap non-centre functional: puncture the pair {0,1} and the 9 triples {0,1,x}.  Exact star evaluation."""
import sys, itertools
sys.dont_write_bytecode = True
import punct
punct._REPO = sys.argv[1]
LN = list(itertools.combinations(range(11), 3)) + list(itertools.combinations(range(11), 2))
dead = {LN.index((0, 1))} | {LN.index(tuple(sorted((0, 1, x)))) for x in range(2, 11)}
live = [i for i in range(220) if i not in dead]
r = punct.evaluate(11, live)
xs = punct.Xstar(r['h'], r['x'])
print('punctured %d: v=%d h=%d star=%d per total %s thmC=%d x=%s=%.4f X*=%.5e@s%d' % (
    len(dead), r['v'], r['h'], r['star'], sorted(c for c, _ in r['star_totals']), r['thmC'], r['x'], float(r['x']),
    float(xs[1]), xs[0]))
