"""Compare every recomputed log with the frozen expected log, ignoring run times ('sec ...') and float noise in the
model lines (relative 1e-9).  Usage: python check.py EXPECTED_DIR OUT_DIR"""
import os, re, sys
exp, out = sys.argv[1], sys.argv[2]
num = re.compile(r'-?\d+\.\d+(?:e[-+]?\d+)?')
norm = lambda s: re.sub(r'sec [\d.]+', 'sec *', re.sub(r'\d+\.\d+s user.*', '', s)).strip()
bad = 0
for f in sorted(os.listdir(exp)):
    if not f.endswith('.log'):
        continue
    a = [norm(l) for l in open(os.path.join(exp, f)) if l.strip()]
    try:
        b = [norm(l) for l in open(os.path.join(out, f)) if l.strip()]
    except FileNotFoundError:
        print('FAIL', f, 'missing'); bad += 1; continue
    ok = len(a) == len(b)
    if ok:
        for x, y in zip(a, b):
            if num.sub('#', x) != num.sub('#', y):
                ok = False; break
            for u, w in zip(num.findall(x), num.findall(y)):
                if abs(float(u) - float(w)) > 1e-9 * max(1.0, abs(float(u))):
                    ok = False
    print('PASS' if ok else 'FAIL', f)
    bad += not ok
print('%d FAIL' % bad)
sys.exit(1 if bad else 0)
