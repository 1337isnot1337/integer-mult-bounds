"""Guard the declared width, then multiply at the actual encoded width."""
from tensor_sources import active
active()
from cardinal_counts import Count, positive
from compact_counts import read_fixed
from encoded import compare
from fft_arithmetic import Arithmetic
from ring_words import Signed, fits
from router_metadata import owned
from session import borrowed_count, erase_marker
from words import BLANK, RIGHT, need


def magnitude_width(value):
    result = Count.literal(0)
    value.rewind()
    try:
        while value.read() != RIGHT:
            need(value.read() in (0, 1), "complete scalar magnitude width")
            result.increment()
            value.step(1)
        positive(result)
        return result
    except BaseException:
        result.close()
        raise
    finally:
        value.rewind()


class NarrowArithmetic(Arithmetic):
    def multiply(self, left, right, width):
        positive(width)
        fits(left.magnitude, width)
        fits(right.magnitude, width)
        with owned(magnitude_width(left.magnitude), magnitude_width(right.magnitude)) as (a, b):
            size = a if compare(a, b) >= 0 else b
            with self.scope.suspended():
                returned = self.word.run(borrowed_count(left.magnitude),
                                         borrowed_count(right.magnitude), borrowed_count(size))
            magnitude = None
            try:
                with owned(Count(size)) as (output_width,):
                    output_width.multiply_small(2)
                    magnitude = read_fixed(returned, output_width)
                need(returned.read() == BLANK, "complete effective-width scalar product return")
                result = Signed(magnitude, left.negative != right.negative)
                magnitude = None
                self.products += 1
                return result
            finally:
                if magnitude is not None:
                    magnitude.close()
                returned.clear()
                erase_marker(returned)


def adapt_arithmetic(owner):
    need(type(owner.arithmetic) is Arithmetic and owner.arithmetic.products == 0
         and owner.arithmetic.word is owner.word and owner.arithmetic.scope is owner.scope,
         "fresh exact scalar interface before width adaptation")
    owner.arithmetic = NarrowArithmetic(owner.word, owner.scope)
