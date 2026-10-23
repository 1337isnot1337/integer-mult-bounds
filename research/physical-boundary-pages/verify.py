"""Source-bound literal boundary page protocol and independent rounded oracle."""
import argparse
from fractions import Fraction as Q
import hashlib
import importlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PHYSICAL = ROOT / 'research/physical-gaussian-core'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def multiply(a, b):
    return [[sum((x * y for x, y in zip(row, column)), Q()) for column in zip(*b)] for row in a]


def invert(a):
    n = len(a)
    rows = [list(row) + [Q(i == j) for j in range(n)] for i, row in enumerate(a)]
    for k in range(n):
        pivot = rows[k][k]
        need(bool(pivot), 'oracle invertible block')
        rows[k] = [x / pivot for x in rows[k]]
        for i in range(n):
            if i != k:
                factor = rows[i][k]
                rows[i] = [x - factor * y for x, y in zip(rows[i], rows[k])]
    return [row[n:] for row in rows]


def rnd(x, p):
    return Q(int(x * (1 << p)), 1 << p)


def pages(matrix, block, precision, reverse=False):
    n = len(matrix)
    extent = ((n + block - 1) // block) * block
    a = [[matrix[i][j] if i < n and j < n else Q(i == j)
          for j in range(extent)] for i in range(extent)]
    if reverse:
        a = [list(reversed(row)) for row in reversed(a)]
    result = []
    for start in range(0, extent, block):
        d = [[rnd(x, precision) for x in row]
             for row in invert([r[start:start + block] for r in a[start:start + block]])]
        b = None if start == 0 else [[rnd(x, precision) for x in r[start - block:start]]
                                    for r in a[start:start + block]]
        result.append((d, b))
    return result


def oracle(lower, upper, rhs, block, precision):
    lo, hi = pages(lower, block, precision), pages(upper, block, precision, True)
    n, columns = len(rhs), len(rhs[0])
    rows = len(lo) * block
    out = []
    for start in range(0, columns, block):
        data = [[rhs[i][j] if i < n and j < columns else Q()
                 for j in range(start, start + block)] for i in range(rows)]
        for index, factors in enumerate((lo, hi)):
            result, previous = [], None
            for offset, (d, b) in enumerate(factors):
                current = data[offset * block:(offset + 1) * block]
                if b is not None:
                    product = multiply(b, previous)
                    current = [[rnd(x - y, precision) for x, y in zip(r, s)]
                               for r, s in zip(current, product)]
                previous = [[rnd(x, precision) for x in r] for r in multiply(d, current)]
                result.extend(previous)
            data = list(reversed(result))
        out.extend(x for row in data for x in row)
    return out


def run_fixture(module, data, lower_data, upper_data, block_size=2, precision_bits=6):
    from cardinal_counts import Count
    from check_support import no_decode
    from gaussian_matrix import Matrix
    from gaussian_rationals import Rational
    from ring_check_words import body, decode
    from ring_words import Signed, read_signed, write_signed
    from router_metadata import owned
    from scratch_pool import ScratchPool
    from session import OuterScope, borrowed_tape, erase_marker, sealed_constructors
    from words import BLANK
    n, columns = len(data), len(data[0])
    expected = oracle(lower_data, upper_data, data, block_size, precision_bits)
    owner = module.BoundaryPages()
    pool, scope = ScratchPool(256), None
    scope = OuterScope(pool)
    matrices, source_pages, rhs = [], (), None
    actual = []
    def make(value):
        return Rational(Signed(Count.literal(abs(value.numerator)), value < 0),
                        Count.literal(value.denominator))
    with owned(Count.literal(n), Count.literal(columns), Count.literal(block_size),
               Count.literal(24), Count.literal(precision_bits)) as (length, column_count, block, width, precision):
        try:
            with sealed_constructors(), scope.installed():
                matrices = [Matrix(length, length, pool,
                                   lambda i, j, values=values: make(values[decode(i)][decode(j)]))
                            for values in (lower_data, upper_data)]
                with no_decode():
                    source_pages = module.prepare_pages(*matrices, block, width, precision, pool)
                rhs = pool.acquire()
                extent = ((n + block_size - 1) // block_size) * block_size
                for start in range(0, columns, block_size):
                    for i in range(extent):
                        for j in range(start, start + block_size):
                            value = data[i][j] if i < n and j < columns else Q()
                            integer = int(value * (1 << precision_bits))
                            with owned(Signed(Count.literal(abs(integer)), integer < 0)) as (encoded,):
                                write_signed(encoded, rhs, width)
                rhs.rewind()
                snapshot = [body(borrowed_tape(p)) for p in (*source_pages, rhs)]
                dirty = pool.acquire()
                with owned(Signed(Count.literal(13), True)) as (value,):
                    write_signed(value, dirty, width)
                dirty.rewind()
                saved_dirty = body(borrowed_tape(dirty))
                with scope.suspended(), no_decode():
                    result = owner.run(*source_pages, rhs, length, column_count, block, width, precision)
                for _ in expected:
                    with owned(read_signed(result, width)) as (value,):
                        actual.append(Q((-1 if value.negative else 1) * decode(value.magnitude),
                                        1 << precision_bits))
                need(result.read() == BLANK and actual == expected, 'literal two-pass blocked oracle')
                need(snapshot == [body(borrowed_tape(p)) for p in (*source_pages, rhs)],
                     'borrowed factor and RHS bytes restored')
                need(saved_dirty == body(borrowed_tape(dirty)), 'arbitrary parked dirty owner restored')
                need(owner.closed and not owner.pool.live, 'closed boundary owner')
                need(all(t.head == 1 and all(v == BLANK for v in t.cells) for t in owner.pool.tapes),
                     'owned physical role erasure')
                blocks, batches = (n + block_size - 1) // block_size, (columns + block_size - 1) // block_size
                matrix_products = 2 * (2 * blocks - 1) * batches
                need(owner.products == matrix_products
                     and owner.arithmetic.products == matrix_products * block_size ** 3,
                     'complete charged classical product census')
                result.clear()
                erase_marker(result)
                owner.idle()
                dirty.clear()
                receipt = {'rows': n, 'RHS_columns': columns, 'block_width': block_size,
                           'precision': precision_bits, 'matrix_products': owner.products,
                           'physical_scalar_products': owner.arithmetic.products,
                           'pool_peak': owner.pool.peak, 'values': list(map(str, actual))}
        finally:
            for matrix in matrices:
                matrix.close()
            for page in (*source_pages, rhs):
                if page is not None:
                    page.clear()
            pool.empty()
    for value in pool.tapes:
        erase_marker(value)
    return receipt


def verify():
    pins = json.loads((HERE / 'SOURCES.json').read_text())
    for row in pins['files']:
        if row['usage'] == 'input':
            need(hashlib.sha256((ROOT / row['path']).read_bytes()).hexdigest() == row['sha256'], 'source bytes: ' + row['path'])
    need('gaussian_sources' not in sys.modules and 'boundary_pages' not in sys.modules, 'cold physical namespace')
    sys.path.insert(0, str(PHYSICAL))
    import gaussian_sources
    with gaussian_sources.opened():
        sys.path.insert(0, str(HERE))
        module = importlib.import_module('boundary_pages')
        lower = [[Q(i == j) + (Q((-1) ** (i + j), 32) if i > j else 0)
                  for j in range(4)] for i in range(4)]
        upper = [[Q(3, 2) if i == j else (Q((-1) ** j, 32) if i < j else Q())
                  for j in range(4)] for i in range(4)]
        data = [[Q((3 * i + 2 * j) % 9 - 4, 16) for j in range(3)] for i in range(4)]
        return {'status': 'PASS_PHYSICAL_BOUNDARY_PAGES',
                'fixtures': [run_fixture(module, data, lower, upper)],
                'kernel': 'charged classical sequential products; no seven-product speed claim'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = verify()
    target = HERE / 'RESULT.json'
    if args.write:
        target.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    else:
        need(json.dumps(json.loads(target.read_text()), sort_keys=True) == json.dumps(result, sort_keys=True),
             'typed physical boundary receipt')
    print(result['status'])


if __name__ == '__main__':
    main()
