"""Exact signed-record codecs with bounded width control and a retained fallback."""
from contextlib import ExitStack, contextmanager
from unittest.mock import patch
from tensor_sources import active
active()
from cardinal_counts import Count
from compact_counts import read_fixed as original_read_fixed, write_fixed as original_write_fixed
import ring_words
import gaussian_convolution
import word_product
from session import borrowed_tape
from words import RIGHT, need

WIDTH_LIMIT = 4096
WIDTH_BITS = 13


def bounded_width(width):
    width.rewind()
    value = 0
    try:
        for position in range(WIDTH_BITS):
            bit = width.read()
            if bit == RIGHT:
                return value if value <= WIDTH_LIMIT else None
            if bit not in (0, 1):
                return None
            value |= bit << position
            width.step(1)
        return value if width.read() == RIGHT and value <= WIDTH_LIMIT else None
    finally:
        width.rewind()


def read_fixed(source, width):
    size = bounded_width(width)
    if size is None:
        return original_read_fixed(source, width)
    result = Count.literal(0)
    borrowed_tape(result.tape).clear()
    try:
        for _ in range(size):
            bit = source.read()
            need(bit in (0, 1), "complete fixed-width binary key")
            result.tape.append(bit)
            source.step(1)
        result.tape.append(RIGHT)
        result.normalize()
        return result
    except BaseException:
        result.close()
        raise


def write_fixed(value, target, width):
    size = bounded_width(width)
    if size is None:
        return original_write_fixed(value, target, width)
    value.rewind()
    try:
        for _ in range(size):
            ended = value.read() == RIGHT
            bit = 0 if ended else value.read()
            need(bit in (0, 1), "fixed-width key digit")
            target.append(bit)
            if not ended:
                value.step(1)
        need(value.read() == RIGHT or value.zero(), "key fits declared width")
    finally:
        value.rewind()


CODEC_BINDINGS = ((ring_words, "read_fixed", original_read_fixed, read_fixed),
                  (ring_words, "write_fixed", original_write_fixed, write_fixed),
                  (gaussian_convolution, "read_fixed", original_read_fixed, read_fixed),
                  (gaussian_convolution, "write_fixed", original_write_fixed, write_fixed),
                  (word_product, "write_fixed", original_write_fixed, write_fixed))


@contextmanager
def bounded_record_io():
    """Adapt signed records, Gaussian packed slots and complete word returns."""
    need(all(getattr(module, name) is original for module, name, original, _ in CODEC_BINDINGS),
         "one retained numerical-record codec cohort")
    with ExitStack() as stack:
        for module, name, _, replacement in CODEC_BINDINGS:
            stack.enter_context(patch.object(module, name, replacement))
        yield
    need(all(getattr(module, name) is original for module, name, original, _ in CODEC_BINDINGS),
         "restore retained numerical-record codecs")
