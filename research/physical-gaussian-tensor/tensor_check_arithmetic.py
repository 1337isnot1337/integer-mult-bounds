"""Effective-width exact products preserve nominal guards and ownership."""
from hashlib import sha256
from tensor_sources import require


def run():
    from cardinal_counts import Count
    from check_support import no_decode
    from fft_word_engine import FftWord
    from ring_check_words import decode
    from ring_words import Signed
    from router_metadata import owned
    from scratch_pool import ScratchPool
    from session import OuterScope, borrowed_tape, erase_marker, initialize_marker, sealed_constructors
    from tensor_arithmetic import NarrowArithmetic
    from tensor_word import adapt_fft_word
    from words import BLANK
    word = adapt_fft_word(FftWord(base_bits=4096))
    pool, digest = ScratchPool(64), sha256()
    scope = OuterScope(pool)
    arithmetic = NarrowArithmetic(word, scope)
    for tape in pool.tapes:
        erase_marker(tape)
    cases = [(a, b, width) for a, b in ((0, 0), (0, -3), (-3, 0), (-7, 9), (19, -21), (-31, -63), (255, 255))
             for width in (8, 50, 546)]
    cases.extend(((1 << 79, -(1 << 80)+1, 546), ((1 << 160)-1, (1 << 79)+3, 1092),
                  ((1 << 512)-1, -(1 << 511)+3, 600)))
    def evaluate(a, b, width, reject=False):
        with owned(Signed(Count.literal(abs(a)), a < 0), Signed(Count.literal(abs(b)), b < 0),
                   Count.literal(width)) as (left, right, nominal):
            saved = [bytes(value.tape.cells) for value in (left.magnitude, right.magnitude, nominal)]
            for tape in pool.tapes:
                initialize_marker(tape)
            try:
                with sealed_constructors(), scope.installed():
                    try:
                        if reject:
                            try:
                                with no_decode():
                                    result = arithmetic.multiply(left, right, nominal)
                            except ValueError:
                                pass
                            else:
                                result.close()
                                raise ValueError("missing nominal-width guard")
                        else:
                            with no_decode():
                                result = arithmetic.multiply(left, right, nominal)
                            with owned(result):
                                actual = decode(result.magnitude)*(-1 if result.negative else 1)
                                require(actual == a*b, "effective-width physical word matches the complete signed product")
                                digest.update(bytes(borrowed_tape(result.magnitude.tape).cells))
                    finally:
                        pool.empty()
            finally:
                for tape in pool.tapes:
                    erase_marker(tape)
            require(saved == [bytes(value.tape.cells) for value in (left.magnitude, right.magnitude, nominal)]
                    and all(value.tape.head == 1 for value in (left.magnitude, right.magnitude, nominal)),
                    "effective-width scalar preserves its borrowed ports")
            require(not pool.live and all(t.head == 1 and all(v == BLANK for v in t.cells) for t in pool.tapes),
                    "effective-width arithmetic restores fixed parent scratch")
            word.idle()
            require(word.closed and word.output.read() == BLANK, "effective-width arithmetic consumes its actual word return")
    for case in cases:
        evaluate(*case)
    for case in ((0, 0, 0), (1 << 16, 0, 16), (0, 1 << 16, 16), (1 << 16, 1, 16)):
        evaluate(*case, reject=True)
    evaluate(-31, 17, 546)
    return {"products": len(cases)+1, "rejections": 4, "pool_peak": pool.peak,
            "sha256": digest.hexdigest(), "scope": "actual shorter word calls after both nominal-width guards"}
