"""Read-only exact certificates for the declared family limit in FAMILY-LIMIT.md.

Apache-2.0. Mathematical extension by Cinna Davis / 1337isnot1337
with OpenAI assistance, building on zxv and Jacob Alan Sussman.
No native admission is inferred from these arithmetic checks.
"""
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
import json

INVOICES = {
    "original": {
        "helpers": {5: 28, 6: 18, 7: 56, 8: 93, 9: 213},
        "paid": {1: 2487, 2: 713, 3: 224, 4: 102, 5: 20, 8: 8},
        "positive_test": Q("0.00268648"),
        "negative_test": Q("0.00268649"),
    },
    "trimmed": {
        "helpers": {4: 22, 5: 6, 6: 18, 7: 56, 8: 93, 9: 213},
        "paid": {1: 2465, 2: 713, 3: 224, 4: 102, 5: 20, 8: 8},
        "positive_test": Q("0.00269635"),
        "negative_test": Q("0.002696357"),
    },
}


def require(test, message):
    if not test:
        raise ValueError(message)


@lru_cache(None)
def log_bounds(n):
    require(n >= 1, "positive integer logarithm input")
    power = n.bit_length() - 1

    def atanh(x):
        z = (x - 1) / (x + 1)
        terms = 60
        lower = 2 * sum((z ** (2*j+1) / (2*j+1) for j in range(terms)), Q(0))
        tail = 2*z ** (2*terms+1) / ((2*terms+1)*(1-z*z))
        return lower, lower + tail

    a, b = atanh(Q(2))
    c, d = atanh(Q(n, 2**power))
    return power*a+c, power*b+d


def exp_bounds(x):
    require(0 <= x <= Q(1, 2), "small nonnegative exponential argument")
    term = total = Q(1)
    terms = 40
    for j in range(1, terms+1):
        term *= x/j
        total += term
    next_term = term*x/(terms+1)
    return total, total + next_term/(1-x/(terms+2))


@lru_cache(None)
def power_bounds(n, saving):
    if n == 1:
        return Q(1), Q(1)
    lower_log, upper_log = log_bounds(n)
    lower_exp, _ = exp_bounds(saving*lower_log)
    _, upper_exp = exp_bounds(saving*upper_log)
    return Q(n)/upper_exp, Q(n)/lower_exp


def moments(histogram, saving):
    lower = upper = Q(0)
    for rank, count in histogram.items():
        a, b = power_bounds(rank, saving)
        lower += count*(a if count >= 0 else b)
        upper += count*(b if count >= 0 else a)
    return lower, upper


def declared_profile(p, a, helpers, local_paid):
    b = p-1-a
    require(p >= 1 and a >= 0 and b >= 0, "legal split")
    targets = Counter({r: (2*p+1)*n for r, n in helpers.items()})
    paid = Counter({r: (2*p+1)*n for r, n in local_paid.items()})
    targets[16*p+9] += 224
    for length in (a, b):
        for j in range(length):
            targets[16*j+25] += 224
            paid[16*j+16] += 224
    paid[8] += 224*(p-1)
    targets.subtract(paid)
    return targets


def formula_profile(p, helpers, local_paid):
    result = Counter()
    for rank, count in helpers.items():
        result[rank] += (2*p+1)*count
    for rank, count in local_paid.items():
        result[rank] -= (2*p+1)*count
    result[16*p+9] += 224
    result[8] -= 224*(p-1)
    for length in ((p-1)//2, p-1-(p-1)//2):
        for j in range(length):
            result[16*j+25] += 224
            result[16*j+16] -= 224
    return result


def decimal_bounds(interval):
    scale = 10**30
    lo, hi = interval
    low = lo.numerator*scale//lo.denominator
    high = -((-hi.numerator*scale)//hi.denominator)

    def show(n):
        sign = "-" if n < 0 else ""
        s = str(abs(n)).rjust(31, "0")
        return sign+s[:-30]+"."+s[-30:]

    return {"lower": show(low), "upper": show(high)}


def run():
    original, trimmed = INVOICES["original"], INVOICES["trimmed"]
    helper_delta = Counter(trimmed["helpers"])
    helper_delta.subtract(original["helpers"])
    paid_delta = Counter(trimmed["paid"])
    paid_delta.subtract(original["paid"])
    require({k: v for k, v in helper_delta.items() if v} == {4: 22, 5: -22},
            "exact terminal helper width change")
    require({k: v for k, v in paid_delta.items() if v} == {1: -22},
            "exact paid-child deletion")
    result = {}
    for name, invoice in INVOICES.items():
        tests = {}
        for side in ("positive_test", "negative_test"):
            saving = invoice[side]
            rows = {}
            for p in (6, 7, 8):
                literal = declared_profile(p, (p-1)//2,
                                           invoice["helpers"], invoice["paid"])
                formula = formula_profile(p, invoice["helpers"], invoice["paid"])
                require(literal == formula, "literal invoice agrees with chain formula")
                require(sum(r*n for r, n in literal.items()) == 96*p-64,
                        "complete rank-one surplus")
                rows[p] = moments(literal, saving)
            require(rows[7][0] > rows[6][1], "strict increase from p6 to p7")
            require(rows[7][0] > rows[8][1], "strict decrease from p7 to p8")
            require(rows[7][0] > 0 if side == "positive_test" else rows[7][1] < 0,
                    "p7 lies strictly on the declared side of the test value")
            tests[side] = {"saving": str(saving),
                           "moments": {str(p): decimal_bounds(v) for p, v in rows.items()},
                           "unique_maximizing_pair_count": 7}
        result[name] = tests
    return {"status": "PASS_EXACT_DECLARED_FAMILY_LIMIT",
            "invoices": result,
            "infinite_step": "Strict discrete concavity proved in FAMILY-LIMIT.md",
            "scope": "Declared prefix/suffix family and stated moment-preserving transfers; no universal lower bound"}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
