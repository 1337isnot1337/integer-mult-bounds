#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Standard-library replay of the #1297/#1305 helper-donor kernel census (no new kappa).

Checks:
  1. inputs: SHA256 and Git blob ids of the three vendored words equal inputs/PINS.json (the #1297/#1305 blobs);
  2. census replay: census.py (exact rational two-shock relations, both restoration rules) is rerun on both final words
     and on the control word; every result equals evidence/CENSUS-*.json exactly;
  3. binding: every record of evidence/PRICES-*.json is exactly one census match, and every match is priced once;
  4. tallies: PRICES, RETIME, DELETION and IDLE-OPTIMUM evidence recount to RESULT.json; no priced or re-timed
     candidate has a negative delta (no gain);
  5. positive control: on #1297's input word the census reproduces #1297's five hooks for each of pivots 555 and 567
     (including its committed donors 620 and 628), each priced at the realized kernel gain -11707 (H1 -3, H3 +1);
  6. failure controls: a one-byte input change, a changed early-read coefficient, a forged negative price and a priced
     edit absent from the census are each rejected at the intended check.
The exact frame prices themselves need PR #1186's toolkit; regenerate.py reruns them and compares byte-for-byte.
"""
import collections, copy, gzip, hashlib, json, sys
from pathlib import Path
assert __debug__, 'assertions are the checks; do not run with -O'
PKG = Path(__file__).resolve().parent
sys.path.insert(0, str(PKG))
import census  # noqa: E402
EV = PKG / 'evidence'
rd = lambda p: json.loads(Path(p).read_text())
canon = lambda x: json.dumps(x, sort_keys=True, separators=(',', ':'))
def blob(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()

def check_pins(raw):
    pins = rd(PKG / 'inputs/PINS.json')['files']
    for name, pin in pins.items():
        b = raw[name]
        assert hashlib.sha256(b).hexdigest() == pin['sha256'], 'input pin: ' + name
        assert blob(b) == pin['git_blob'], 'input git blob: ' + name
    return pins

def pivots(w):
    B = w['B']; first = {}
    for i, g in enumerate(B): first.setdefault(g[1], i)
    return sorted({g[2] for i, g in enumerate(B) if g[0] == 'add' and g[2] >= 224 and i < first.get(g[2], len(B))})

def run_census(word_json, restore, only=None):
    census.W = word_json; census.RESTORE = restore
    return json.loads(canon(sorted((census.relations(q) for q in (only or pivots(word_json))), key=lambda r: r['pivot'])))

def match_key(m): return canon({k: v for k, v in m.items() if k != 'price'})

def check_binding(cen, priced):
    a = collections.Counter(match_key(m) for r in cen for m in r['matches'])
    b = collections.Counter(match_key(m) for m in priced)
    assert a == b, 'priced records must be exactly the census matches'

def tally(records, key):
    return dict(sorted(collections.Counter(key(r) for r in records).items()))

def price_key(r): return '%s:%s' % (r['price']['status'], r['price'].get('delta'))

def check_no_gain(priced, label):
    assert all(r['price'].get('delta') is None or r['price']['delta'] >= 0 for r in priced), 'negative price in ' + label

def main():
    res = rd(PKG / 'RESULT.json'); raw = {n: (PKG / 'inputs' / n).read_bytes() for n in ('BASE-WORD.json.gz', 'EXTRA-WORD.json.gz', 'CONTROL-WORD.json.gz')}
    check_pins(raw)
    words = {k: json.loads(gzip.decompress(raw[f])) for k, f in (('base', 'BASE-WORD.json.gz'), ('extra', 'EXTRA-WORD.json.gz'), ('control', 'CONTROL-WORD.json.gz'))}
    out = dict(census={}, prices={}, retime={}, deletion={})
    for w in ('base', 'extra'):
        for rule in ('tail', 'first'):
            name = f'{w}-{rule}'; cen = run_census(words[w], rule)
            assert cen == rd(EV / f'CENSUS-{name}.json'), 'census replay differs: ' + name
            priced = rd(EV / f'PRICES-{name}.json'); check_binding(cen, priced); check_no_gain(priced, name)
            out['census'][name] = dict(pivots=len(cen), with_matches=sum(1 for r in cen if r['matches']), matches=sum(len(r['matches']) for r in cen))
            out['prices'][name] = tally(priced, price_key)
        rt = rd(EV / f'RETIME-{w}.json'); assert all(r['delta'] is None or r['delta'] >= 0 for r in rt), 'negative re-timing price'
        out['retime'][w] = tally(rt, lambda r: '%s:%s' % (r['status'], r['delta']))
        dl = rd(EV / f'DELETION-{w}.json')
        out['deletion'][w] = dict(statuses=tally(dl, lambda r: r['status']), negative=sum(1 for r in dl if r.get('delta') is not None and r['delta'] < 0))
    cen = run_census(words['control'], 'tail', [555, 567]); assert cen == rd(EV / 'CENSUS-control-tail.json'), 'control census replay differs'
    priced = rd(EV / 'PRICES-control-tail.json'); check_binding(cen, priced)
    by = {r['pivot']: r['matches'] for r in cen}
    assert [len(by[555]), len(by[567])] == [5, 5] and 620 in {m['donor'] for m in by[555]} and 628 in {m['donor'] for m in by[567]}, 'control hooks'
    assert {m['helper'] for m in by[555]} == {383} and {m['helper'] for m in by[567]} == {399}, 'control partners'
    assert all(r['price'] == dict(status='ok', delta=-11707, profile={'1': 2349, '2': 504, '3': 413, '4': 130, '5': 82}) for r in priced), 'control prices'
    out['control'] = dict(matches=len(priced), delta=-11707, deletion=[r['status'] for r in rd(EV / 'DELETION-control.json')])
    idle = rd(EV / 'IDLE-OPTIMUM-1305.json')
    assert idle['status'] == 'PASS_1305_IDLE_SELECTION_EQUALS_EXACT_GROUP_OPTIMUM' and idle['improvable_groups'] == 0
    assert all(s['current'] == s['optimum'] for s in idle['shapes']) and sum(s['groups'] for s in idle['shapes']) == idle['groups']
    out['idle'] = {k: idle[k] for k in ('eligible', 'groups', 'group_sizes', 'improvable_groups', 'donors', 'receivers')}
    assert out == res['tallies'], 'evidence tallies differ from RESULT.json'
    # failure controls
    rejected = {}
    def expect(fn, needle, label):
        try: fn()
        except AssertionError as e:
            assert needle in str(e), (label, str(e)); rejected[label] = str(e); return
        raise AssertionError('control accepted: ' + label)
    bad = dict(raw); b = bytearray(bad['BASE-WORD.json.gz']); b[-5] ^= 1; bad['BASE-WORD.json.gz'] = bytes(b)
    expect(lambda: check_pins(bad), 'input pin', 'one-byte input change')
    w2 = copy.deepcopy(words['control']); first = next(i for i, g in enumerate(w2['B']) if g[1] == 555)
    j = next(i for i in range(first) if w2['B'][i][0] == 'add' and w2['B'][i][2] == 555); w2['B'][j][3] *= 3
    def mutated():
        assert run_census(w2, 'tail', [555]) == [r for r in rd(EV / 'CENSUS-control-tail.json') if r['pivot'] == 555], 'census replay differs: mutated coefficient'
    expect(mutated, 'census replay differs', 'changed early-read coefficient')
    forged = copy.deepcopy(rd(EV / 'PRICES-base-tail.json')); next(r for r in forged if r['price']['status'] == 'ok')['price']['delta'] = -1
    expect(lambda: check_no_gain(forged, 'forged'), 'negative price', 'forged negative price')
    moved = copy.deepcopy(rd(EV / 'PRICES-base-tail.json')); moved[0]['ed']['insert'][2][0] += 1
    expect(lambda: check_binding(rd(EV / 'CENSUS-base-tail.json'), moved), 'exactly the census matches', 'priced edit absent from census')
    print(json.dumps(dict(status='PASS_FRONTIER1305_KERNEL_CENSUS_NO_GAIN', tallies=out, controls_rejected=sorted(rejected)), indent=2))

if __name__ == '__main__':
    main()
