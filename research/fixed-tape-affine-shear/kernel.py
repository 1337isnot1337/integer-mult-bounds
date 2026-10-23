# SPDX-License-Identifier: Apache-2.0
"""Literal runtime-coefficient affine shear, using PR2776's paid macros."""

C_INPUT, C_COUNT, OFFSET_INPUT, OFFSET_COUNT, X_COUNT = range(14, 19)
TAPES = 19
EXTRA_WORK = (C_COUNT, OFFSET_COUNT, X_COUNT)


def build_program(modules, inverse=False):
    if type(inverse) is not bool:
        raise ValueError('fixed Boolean direction')
    b, m, c = (modules[k] for k in ('shear', 'machine', 'counters'))
    a = m.Assembler(TAPES)
    fail = a.fresh('invalid_affine_interface')
    work = b.SCRATCH_TAPES + EXTRA_WORK

    def trim_one(tape, prefix):
        b._seek_right(a, tape, fail, prefix + '_end')
        a.write(tape, m.BLANK)
        a.move(tape, -1)
        good = a.fresh(prefix + '_positive')
        a.branch(tape, {m.UNIT: good}, fail)
        a.label(good)
        a.write(tape, m.RIGHT)
        c.emit_rewind(a, tape, prefix + '_return')

    def strict_below_q(tape, prefix):
        c.emit_rewind(a, X_COUNT, prefix + '_Q')
        loop, unit, advance, end, good = (a.fresh(prefix + s) for s in
                                        ('_loop', '_unit', '_advance', '_end', '_good'))
        a.label(loop)
        a.branch(tape, {m.UNIT: unit, m.RIGHT: end}, fail)
        a.label(unit)
        a.branch(X_COUNT, {m.UNIT: advance}, fail)
        a.label(advance)
        a.move(tape, 1)
        a.move(X_COUNT, 1)
        a.goto(loop)
        a.label(end)
        a.branch(X_COUNT, {m.UNIT: good}, fail)
        a.label(good)
        c.emit_rewind(a, tape, prefix + '_coefficient')
        c.emit_rewind(a, X_COUNT, prefix + '_Q_return')

    def transfer_one(prefix):
        b._decrease_left_increase_right(a, fail, prefix + '_transfer')
        a.move(b.LEFT_LENGTH, -1)
        nonzero, zero, done = (a.fresh(prefix + s) for s in ('_positive', '_zero', '_done'))
        a.branch(b.LEFT_LENGTH, {m.UNIT: nonzero, m.LEFT: zero}, fail)
        a.label(nonzero)
        a.move(b.LEFT_LENGTH, 1)
        a.goto(done)
        a.label(zero)
        a.move(b.LEFT_LENGTH, 1)
        b._reset_lengths(a, fail, prefix + '_wrap')
        a.label(done)

    def advance_by(tape, prefix):
        c.emit_rewind(a, tape, prefix + '_counter')
        loop, unit, done = (a.fresh(prefix + s) for s in ('_loop', '_unit', '_done'))
        a.label(loop)
        a.branch(tape, {m.UNIT: unit, m.RIGHT: done}, fail)
        a.label(unit)
        transfer_one(prefix + '_one')
        a.move(tape, 1)
        a.goto(loop)
        a.label(done)

    def phase(operations, prefix):
        c.emit_rewind(a, b.P_COUNT, prefix + '_P_return')
        p_loop, p_body, x_loop, x_body, g_loop, body, next_x, next_p, done = (
            a.fresh(prefix + s) for s in
            ('_P', '_P_body', '_x', '_x_body', '_G', '_body', '_next_x', '_next_P', '_done'))
        a.label(p_loop)
        a.branch(b.P_COUNT, {m.UNIT: p_body, m.RIGHT: done}, fail)
        a.label(p_body)
        c.emit_rewind(a, X_COUNT, prefix + '_x_return')
        a.label(x_loop)
        a.branch(X_COUNT, {m.UNIT: x_body, m.RIGHT: next_p}, fail)
        a.label(x_body)
        c.emit_rewind(a, b.G_COUNT, prefix + '_G_return')
        a.label(g_loop)
        a.branch(b.G_COUNT, {m.UNIT: body, m.RIGHT: next_x}, fail)
        a.label(body)
        for i, (length, source, destination, consume) in enumerate(operations):
            b._segment(a, length, source, destination, consume, fail, prefix + '_segment_' + str(i))
        a.move(b.G_COUNT, 1)
        a.goto(g_loop)
        a.label(next_x)
        advance_by(C_COUNT, prefix + '_coefficient')
        a.move(X_COUNT, 1)
        a.goto(x_loop)
        a.label(next_p)
        a.move(b.P_COUNT, 1)
        a.goto(p_loop)
        a.label(done)

    for tape in (b.OUTPUT,) + work:
        empty = a.fresh('initialize')
        a.branch(tape, {m.BLANK: empty}, fail)
        a.label(empty)
        a.write(tape, m.LEFT)
        a.move(tape, 1)
    for src, dst, name in ((b.P_INPUT, b.P_COUNT, 'P'), (b.Q_INPUT, b.LEFT_LENGTH, 'Q'),
                           (b.G_INPUT, b.G_COUNT, 'G'), (b.S_INPUT, b.S_COUNT, 'S'),
                           (b.Q_INPUT, X_COUNT, 'x_extent'),
                           (C_INPUT, C_COUNT, 'coefficient_plus_one'),
                           (OFFSET_INPUT, OFFSET_COUNT, 'offset_plus_one')):
        c.emit_binary_to_unary(a, src, b.BINARY_WORK, dst, 'prepare_' + name)
    trim_one(C_COUNT, 'decode_coefficient')
    trim_one(OFFSET_COUNT, 'decode_offset')
    strict_below_q(C_COUNT, 'bound_coefficient')
    strict_below_q(OFFSET_COUNT, 'bound_offset')
    a.write(b.RIGHT_LENGTH, m.RIGHT)
    b._seek_right(a, b.LEFT_LENGTH, fail, 'initial_left_end')
    advance_by(OFFSET_COUNT, 'initial_offset')
    gather = ((b.LEFT_LENGTH, b.SOURCE, b.SPLIT_A, False),
              (b.RIGHT_LENGTH, b.SOURCE, b.SPLIT_B, False))
    emit = ((b.RIGHT_LENGTH, b.SPLIT_B, b.OUTPUT, True),
            (b.LEFT_LENGTH, b.SPLIT_A, b.OUTPUT, True))
    if inverse:
        gather, emit = tuple(reversed(gather)), tuple(reversed(emit))
    phase(gather, 'gather')
    complete = a.fresh('source_complete')
    a.branch(b.SOURCE, {m.RIGHT: complete}, fail)
    a.label(complete)
    for tape in (b.SPLIT_A, b.SPLIT_B):
        a.write(tape, m.RIGHT)
        c.emit_rewind(a, tape, 'bucket_return_' + str(tape))
    phase(emit, 'emit')
    for tape in (b.SPLIT_A, b.SPLIT_B):
        complete = a.fresh('bucket_complete')
        a.branch(tape, {m.RIGHT: complete}, fail)
        a.label(complete)
    a.write(b.OUTPUT, m.RIGHT)
    c.emit_rewind(a, b.SOURCE, 'source_return')
    c.emit_rewind(a, b.OUTPUT, 'output_return')
    for tape in work:
        b._erase_back_to_origin(a, tape, 'clear_' + str(tape))
    a.halt()
    a.label(fail)
    a.reject('canonical affine extents, bounded coefficients and blank owned workspace')
    return a.finish()
