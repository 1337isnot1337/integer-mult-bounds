"""Executable q2 physical cohort, distinct from the enormous production prime."""
from types import SimpleNamespace
from contextlib import contextmanager
from unittest.mock import patch
from tensor_sources import require


def literal_native():
    from macro_code import Code
    from retuned_native import active, retune
    state = active()
    # Retain the fresh-native recipe from check_composed.fixture. Literal
    # routing does not execute the selected production macro program.
    return retune(state.ordinary.Ordinary(
        2, SimpleNamespace(codes=SimpleNamespace(q=2)), SimpleNamespace(families=0),
        (Code((("unreachable",),), 0),), capacity=64))


def finite_chirp():
    from check_composed import fixture
    from chirp_engine import Chirp
    from convolution_engine import Convolution
    from cyclic_engine import Cyclic
    from fourier_engine import Fourier
    return Chirp(Cyclic(Convolution(Fourier(fixture()[0]))))


@contextmanager
def p48_setup():
    """Exact constant metadata for the declared two-axis p48 witness only."""
    from cardinal_counts import Count
    from encoded import compare
    from router_metadata import owned
    require(50**1000 <= 51**997 < 51**1000 and 51**1000 <= 52**997 < 52**1000
            and 1**500 == 1, "exact p48 fractional-power metadata certificates")
    calls = {"51^(.997)": 0, "52^(.997)": 0, "1^(.002)": 0}
    def floor_power(value, numerator, denominator):
        if (numerator, denominator) == (997, 1000):
            for incoming, output in ((51, 50), (52, 51)):
                with owned(Count.literal(incoming)) as (constant,):
                    if compare(value, constant) == 0:
                        calls[str(incoming)+"^(.997)"] += 1
                        return Count.literal(output)
        elif (numerator, denominator) == (1, 500):
            with owned(Count.literal(1)) as (one,):
                if compare(value, one) == 0:
                    calls["1^(.002)"] += 1
                    return Count.literal(1)
        raise ValueError("outside the certified two-axis p48 setup fixture")
    with patch("composed_plan.floor_power", floor_power), patch("active_plan.floor_power", floor_power):
        yield calls
