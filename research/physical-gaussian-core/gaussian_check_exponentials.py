"""Directed coefficients against a separate exact-rational interval oracle."""
from fractions import Fraction as Q
from gaussian_sources import require


def pi_oracle():
    def atan(d):
        value = sum((Q((-1)**j, (2*j+1)*d**(2*j+1)) for j in range(40)), Q(0))
        other = value + Q(1, 81*d**81)
        return value, other
    al, ah = atan(5)
    bl, bh = atan(239)
    return 16*al-4*bh, 16*ah-4*bl


def positive_exp_oracle(x):
    if not x:
        return Q(1), Q(1)
    k = 0
    while x > Q(1, 8):
        x /= 2
        k += 1
    term = total = Q(1)
    for j in range(1, 41):
        term *= x/j
        total += term
    following = term*x/41
    tail = following/(1-x/42)
    scale = 1 << 80
    def floor(value):
        return Q((value*scale).__floor__(), scale)
    def ceil(value):
        return Q((value*scale).__ceil__(), scale)
    lower, upper = floor(total), ceil(total+tail)
    for _ in range(k):
        lower, upper = floor(lower*lower), ceil(upper*upper)
    return lower, upper


def oracle(argument, positive=False, binary_scale=0):
    pl, ph = pi_oracle()
    lower, _ = positive_exp_oracle(argument*pl)
    _, upper = positive_exp_oracle(argument*ph)
    if not positive:
        lower, upper = 1/upper, 1/lower
    return lower/(1 << binary_scale), upper/(1 << binary_scale)


def run():
    from cardinal_counts import Count
    from check_support import no_decode
    from gaussian_exponentials import Exponentials
    from gaussian_rationals import Rational
    from ring_check_words import decode
    from ring_words import Signed
    from router_metadata import owned
    from scratch_pool import ScratchPool
    from session import OuterScope, erase_marker, sealed_constructors
    from words import BLANK
    pool = ScratchPool(256)
    scope = OuterScope(pool)
    results = []
    with owned(Count.literal(12), Count.literal(2)) as (precision, bound):
        with sealed_constructors(), scope.installed():
            setup = None
            try:
                with no_decode():
                    setup = Exponentials(precision, bound)
                for argument, positive, binary_scale in (
                    (Q(0), False, 0), (Q(1, 16), False, 0), (Q(1, 3), False, 0),
                    (Q(1), False, 0), (Q(2), False, 0), (Q(1), True, 6)):
                    with owned(Rational(Signed(Count.literal(argument.numerator)),
                                        Count.literal(argument.denominator))) as (value,):
                        with owned(Count.literal(binary_scale)) as (scale,):
                            with no_decode():
                                lower, upper = setup.grid_interval(value, positive, scale)
                            with owned(lower, upper):
                                lo, hi = decode(lower), decode(upper)
                    reference_lower, reference_upper = oracle(argument, positive, binary_scale)
                    require(Q(lo, 1 << 12) <= reference_lower <= reference_upper <= Q(hi, 1 << 12),
                            "physical Gaussian enclosure contains independent exact oracle")
                    require(hi-lo < 4, "strict four-ulp Gaussian coefficient allowance")
                    results.append({"argument": str(argument), "positive": positive,
                                    "binary_scale": binary_scale, "lower": lo, "upper": hi})
                parameters = {name: decode(getattr(setup, name)) for name in ("R", "J", "terms", "k")}
            finally:
                if setup is not None:
                    setup.close()
                pool.empty()
    for tape in pool.tapes:
        erase_marker(tape)
        require(tape.head == 1 and all(v == BLANK for v in tape.cells), "Gaussian setup restoration")
    return {"precision": 12, "argument_bound": 2, "parameters": parameters,
            "coefficients": results, "pool_peak": pool.peak,
            "scope": "complete encoded coefficient producer at finite precision; production P=32768p remains separate"}
