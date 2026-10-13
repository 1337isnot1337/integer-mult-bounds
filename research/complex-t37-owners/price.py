# SPDX-License-Identifier: Apache-2.0
"""Two unchanged exact moment engines and all 47 outer inequalities for T37.

The retained outer helper checks its bootstrap cutoffs against the old 512-bit
charge; they are rechecked here against the charged 1024-bit payload.
"""
import argparse
import hashlib
from fractions import Fraction
from pathlib import Path
from common import HERE, ROOT, read, require, sha, dump, load


def bootstrap(c, b, payload=1024):
    """The seven retained bootstrap levels with cutoffs charged at 2*(4+payload)."""
    eta = beta = Fraction(1, 10**24)
    s = min(c, (1-beta)*b)-Fraction(1, 10**27)
    a, rows = Fraction(384599, 10**10), []
    for _ in range(7):
        old, a = a, (1-s)*s+s*a
        gap = min(s-a, 1-a-s, 1-a-s*(1-old), 1-s)
        require(old < a < s < 1-a and gap > 0, 'bootstrap gap')
        cut = max(-(-36//gap**2), -(-(2*(4+payload))//gap))
        require(cut*gap**2 >= 36 and cut*gap >= 2*(4+payload), 'payload-charged bootstrap cutoff')
        rows.append(dict(gap=str(gap), cutoff_log2=str(cut)))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    old = load(ROOT/'research/complex-t21-owners/vendor/pr870/independent/price_profile_t16.py', 'unchanged_price_helpers')
    pins = read(ROOT/'research/complex-t21-owners/vendor/pr870/data/UPSTREAM-PINS.json')
    for name in ('moment', 'base_two_moment', 'outer'):
        relative = old.SOURCE/'engines'/(name+'.py')
        require(sha(ROOT/relative) == pins[relative.as_posix()], 'Exact arithmetic source pin')
    M, B, A = [old.load(ROOT/old.SOURCE/'engines', name) for name in ('moment', 'base_two_moment', 'outer')]
    supplied, claim = read(args.profile), read(HERE/'data/CLAIM.json')
    require((supplied['live'], supplied['deficit']) == (33152, 11840), 'T37 profile stock and deficit')
    profile = {int(rank): count for rank, count in supplied['profile'].items()}
    bit_bytes = old.BIT_PATH.read_bytes()
    require(hashlib.sha1(b'blob '+str(len(bit_bytes)).encode()+b'\0'+bit_bytes).hexdigest() == old.BIT_BLOB, 'PR589 bit supplier blob')
    bit = read(old.BIT_PATH)
    deficit = old.pr589_deficit(bit['word'], bit['nine']['bit']['live'])
    c = Fraction(bit['nine']['bit_lower'])
    bit_checks = old.moment_checks(M, B, {int(r): n for r, n in bit['nine']['profile'].items()},
                                  64, bit['nine']['bit']['live'], c, deficit, True)
    prices = {}
    for mode, surcharge in (('native', False), ('conservative', True)):
        root = M.certify(profile, 73, 33152, surcharge)
        b = Fraction(root['lower'])
        prices[mode] = dict(root=root, moments=old.moment_checks(M, B, profile, 73, 33152, b, 11840, surcharge),
                            outer=old.outer47(c, b, A), bootstrap_payload1024=bootstrap(c, b))
    require(prices['native']['outer']['kappa'] == str(Fraction(claim['kappa'])), 'Claimed T21 exponent')
    require(Fraction(prices['native']['root']['lower']) == Fraction(claim['complex_lower']), 'Claimed complex endpoint')
    result = dict(status='PASS_T37_TWO_EXACT_ENGINES_AND_OUTER47', prices=prices, bit_checks=bit_checks,
                  profile_sha256=sha(args.profile), gain_over_pr890=str(Fraction(claim['kappa'])-Fraction(claim['baseline890_kappa'])),
                  scope='Exact arithmetic for the independently recounted T37 profile; full controller and invoice admission are separate mandatory stages.')
    dump(args.out, result)
    print(result['status'], prices['native']['outer']['kappa_decimal'])


if __name__ == '__main__':
    main()
