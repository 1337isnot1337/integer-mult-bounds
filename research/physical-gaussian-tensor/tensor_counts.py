"""Exact finite-byte schoolbook multiplication for encoded setup counters."""
from contextlib import contextmanager
from unittest.mock import patch
from tensor_sources import active
active()
from cardinal_counts import Count
from compact_counts import Counter
from router_metadata import owned
from session import borrowed_tape
from tensor_word import accumulator_byte, byte_product, read_byte, write_byte
from words import RIGHT, need


def byte_count_product(cls, left, right):
    """Keep both arbitrary-width operands and the result on their own tapes."""
    first = second = count = backward = result = None
    try:
        first, second = cls(left), cls(right)
        if first.zero() or second.zero():
            return cls.literal(0)
        count = cls.literal(0)
        while second.read() != RIGHT:
            read_byte(second)
            count.increment()
        second.rewind()
        backward = cls(count)
        backward.multiply_small(8)
        result = cls.literal(0)
        borrowed_tape(result.tape).clear()
        result.tape.append(RIGHT)
        result.rewind()
        while first.read() != RIGHT:
            a, carry = read_byte(first), 0
            second.rewind()
            while second.read() != RIGHT:
                b = read_byte(second)
                previous, extend = accumulator_byte(result.tape)
                total = previous+byte_product(a, b)+carry
                need(0 <= total <= 65535, "sixteen-bit setup multiply-add control")
                write_byte(result.tape, total & 255, extend)
                carry = total >> 8
            need(result.read() == RIGHT, "setup product next high byte")
            write_byte(result.tape, carry, True)
            with owned(Counter(backward)) as (steps,):
                while not steps.finished:
                    result.step(-1)
                    steps.decrement()
        result.rewind()
        result.normalize()
        returned, result = result, None
        return returned
    finally:
        for value in (result, backward, count, second, first):
            if value is not None:
                value.close()


@contextmanager
def exact_byte_counts():
    """Specialize the retained setup class within one outer invocation only."""
    original = Count.__dict__["product"]
    need(original.__func__ is not byte_count_product, "one setup arithmetic adaptation")
    with patch.object(Count, "product", classmethod(byte_count_product)):
        yield
    need(Count.__dict__["product"] is original, "restore the retained setup arithmetic class")
