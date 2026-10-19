"""Executable q2 physical cohort, distinct from the enormous production prime."""
from types import SimpleNamespace


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
