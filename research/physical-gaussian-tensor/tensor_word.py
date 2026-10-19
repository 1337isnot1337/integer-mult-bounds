"""Exact byte-control leaves inside the retained physical Karatsuba owner."""
from tensor_sources import active
active()
from cardinal_counts import Count, positive
from compact_counts import Counter
from encoded import compare
from ring_words import fits
from router_metadata import owned
from word_product import WordProduct
from words import BLANK, RIGHT, need

LEAF_BITS = 1024


def byte_product(first, second):
    """Eight fixed shift/add phases; no data register exceeds sixteen bits."""
    need(type(first) is int and type(second) is int and 0 <= first <= 255 and 0 <= second <= 255,
         "eight-bit finite-control operands")
    result, shifted, remaining = 0, first, second
    for _ in range(8):
        if remaining & 1:
            result += shifted
        remaining >>= 1
        shifted <<= 1
    need(0 <= result <= 65025 and remaining == 0 and shifted <= 65280,
         "sixteen-bit finite-control product")
    return result


def read_byte(source):
    value = 0
    for position in range(8):
        symbol = source.read()
        if symbol == RIGHT:
            break
        need(symbol in (0, 1), "complete canonical magnitude byte")
        value |= symbol << position
        source.step(1)
    return value


def accumulator_byte(source):
    if source.read() == RIGHT:
        return 0, True
    value = 0
    for position in range(8):
        bit = source.read()
        need(bit in (0, 1), "complete accumulated byte")
        value |= bit << position
        source.step(1)
    for _ in range(8):
        source.step(-1)
    return value, False


def write_byte(target, value, extend):
    need(type(value) is int and 0 <= value <= 255, "eight-bit output control")
    for position in range(8):
        target.write((value >> position) & 1)
        target.step(1)
    if extend:
        need(target.read() == BLANK, "vacant accumulated-byte extension")
        target.write(RIGHT)


class ByteWordProduct(WordProduct):
    """Preserve the original recursive continuation and exact word boundary."""
    def __init__(self):
        super().__init__(leaf_bits=LEAF_BITS)
        self.byte_counts = dict(products=0, rows=0, updates=0, max_control=0)

    def leaf(self, first, second):
        self.byte_counts["products"] += 1
        if first.zero() or second.zero():
            return Count.literal(0)
        count = backward = result = None
        first.rewind()
        second.rewind()
        try:
            count = Count.literal(0)
            while second.read() != RIGHT:
                read_byte(second)
                count.increment()
            positive(count)
            second.rewind()
            backward = Count(count)
            backward.multiply_small(8)
            tape = self.pool.acquire()
            result = object.__new__(Count)
            result.tape = tape
            result.tape.append(RIGHT)
            result.rewind()
            while first.read() != RIGHT:
                a, carry = read_byte(first), 0
                second.rewind()
                while second.read() != RIGHT:
                    b = read_byte(second)
                    old, extend = accumulator_byte(result.tape)
                    total = old+byte_product(a, b)+carry
                    need(0 <= total <= 65535, "bounded byte multiply-add control")
                    write_byte(result.tape, total & 255, extend)
                    carry = total >> 8
                    self.byte_counts["updates"] += 1
                    self.byte_counts["max_control"] = max(self.byte_counts["max_control"], total)
                need(result.read() == RIGHT, "new high byte after each product row")
                write_byte(result.tape, carry, True)
                with owned(Counter(backward)) as (steps,):
                    while not steps.finished:
                        result.step(-1)
                        steps.decrement()
                self.byte_counts["rows"] += 1
            result.rewind()
            result.normalize()
            output, result = result, None
            return output
        finally:
            first.rewind()
            second.rewind()
            for value in (result, backward, count):
                if value is not None:
                    value.close()

    def enter(self):
        need(self.leaf_bits == LEAF_BITS, "fixed byte-leaf compile parameter")
        n, a, b = self.c("n"), self.c("a"), self.c("b")
        with owned(Count.literal(LEAF_BITS)) as (cutoff,):
            small = compare(n, cutoff) <= 0
        if not small:
            return super().enter()
        self.calls["nodes"] += 1
        positive(n)
        fits(a, n)
        fits(b, n)
        self.finish(self.leaf(a, b))
        self.clear_active()
        self.calls["leaves"] += 1
        return False


def pristine(word):
    need(type(word) is WordProduct and word.closed and not word.pool.live
         and all(value == 0 for value in word.calls.values())
         and word.output.read() == BLANK
         and all(tape.read() == BLANK for tape in word.canonical),
         "pristine retained word owner before source adaptation")


def adapt_scalar(owner):
    pristine(owner.word)
    need(owner.arithmetic.word is owner.word, "retained scalar arithmetic owner link")
    word = ByteWordProduct()
    owner.word = word
    owner.arithmetic.word = word
    return word


def adapt_fft_word(owner):
    from tensor_twiddles import adapt_twiddles
    need(owner.closed and not owner.pool.live and owner.output.read() == BLANK
         and all(value == 0 for value in owner.calls.values()), "fresh FFT-word source adaptation")
    pristine(owner.base)
    owner.base = ByteWordProduct()
    adapt_scalar(owner.product)
    adapt_twiddles(owner.product)
    owner.canonical = (*owner.base.canonical, owner.base.output, owner.product.output,
                       *owner.product.word.canonical, owner.product.word.output,
                       owner.product.twiddles.output)
    return owner


def adapt_chirp(owner):
    need(owner.closed and owner.current is owner.retained is None
         and all(value == 0 for value in owner.calls.values()), "fresh complete chirp source adaptation")
    for scalar in (owner, owner.kernel, owner.cyclic, owner.cyclic.convolution.product):
        adapt_scalar(scalar)
    return owner
