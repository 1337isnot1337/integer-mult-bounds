"""Encoded word banks, two padded roots, reuse and the elementary fallback."""
from pathlib import Path
import json
import sys
from time import monotonic
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import source
source.activate()
from cardinal_counts import Count
from check_support import no_decode
import check_nested_model as model
from check_join import Binding, body
from directory import Context
from macro_code import compile_node
from ordinary import Ordinary
from physical_words import PhysicalWord
from provenance import Provenance
from records import Tape
import scheduler
from words import Arena, BLANK, Ring, Word, need


def fixture_engine():
    catalogue = model.Catalogue()
    topology = model.Topology(catalogue)
    arena, indices = Arena(3), Arena(8)
    modulus = arena.input(2)
    ring = Ring(modulus)
    context = Context(ring, catalogue.codes)
    plans = model.compile_coefficients(catalogue, context, indices, model.UnitIncoming(context))
    binding = Binding(catalogue, plans)
    program = compile_node(topology, binding, 0)
    context.close()
    ring.close()
    arena.free(modulus)
    return Ordinary(2, binding, topology, (program,), capacity=128, fixture_index_floor=64)


def toy_plan():
    values = dict(width=1, depth=1, stock=6, rows=8, borrowed=3, body=2, remainder=0)
    return dict(fits=True, **{name: Count.literal(value) for name, value in values.items()})


def check_case(engine, width, prefix, gap, suffix, fitted):
    extent = 2**width
    volume = prefix*extent*gap*extent*suffix
    payload = Tape()
    for address in range(volume):
        payload.append(((address * 13) ^ (address >> 3) ^ (address >> 7) ^ 0x53) & 1)
    payload.rewind()
    initial = body(payload)
    original, prefixes, middle, tail = (Count.literal(value) for value in (width, prefix, gap, suffix))
    provenance = Provenance(volume)
    provenance.mark(payload)
    def forbidden(*_args, **_kwargs):
        raise ValueError("fixture-only construction or decoding during execution")
    with no_decode(), provenance.installed(), patch.object(Word, "__init__", forbidden), \
            patch.object(PhysicalWord, "inspect", forbidden), \
            patch.object(scheduler.Invocation, "__init__", forbidden):
        output = (engine.execute_plan(payload, original, prefixes, middle, tail, toy_plan)
                  if fitted else engine.run(payload, original, prefixes, middle, tail))
        expected, masks = bytearray(volume), [0]*volume
        for address, bit in enumerate(initial):
            quotient, last = divmod(address, suffix)
            quotient, second = divmod(quotient, extent)
            quotient, between = divmod(quotient, gap)
            first_prefix, first = divmod(quotient, extent)
            target = ((((first_prefix*extent+second)*gap+between)*extent+first)*suffix+last)
            expected[target], masks[target] = bit, 1 << address
        need(body(output) == expected and provenance.masks(output, volume) == tuple(masks),
             "complete independent-column ordinary endpoint")
        need(body(payload) == initial and payload.head == output.head == 1,
             "borrowed source and output boundary")
        need(engine.closed and engine.runtime.closed and engine.last_fitted == fitted,
             "closed ordinary invocation with the expected branch")
        work = [*engine.pool.tapes, *engine.runtime.pool.tapes, *engine.runtime.roles.values(),
                *engine.runtime.handoff.values(), engine.runtime.output]
        for bank in (*engine.banks, engine.runtime.arena, engine.runtime.indices):
            need(not bank.live and not bank.initialized, "closed encoded word banks")
            work.extend(word.tape for word in (*bank.words, bank.template))
        need(all(all(bit == BLANK for bit in tape.cells) for tape in work),
             "erase owned bodies, markers and templates after ordinary return")
        need(engine.runtime.numerical.machine.tapes == [{}, {}], "erase owned parking workspace")
        output.clear()
    result = dict(width=width, shape=[prefix, gap, suffix], independent_columns=volume,
                  fitted=fitted, roots=engine.runtime.completed_roots,
                  outer_peak=engine.pool.peak, inner_peak=engine.runtime.pool.peak)
    payload.clear()
    for value in (original, prefixes, middle, tail):
        value.close()
    return result


def run():
    started = monotonic()
    engine = fixture_engine()
    result = [check_case(engine, 5, 1, 1, 1, True),
              check_case(engine, 2, 2, 3, 2, False),
              check_case(engine, 5, 1, 1, 1, True)]
    print("completed encoded physical ordinary engine in", round(monotonic()-started, 2), "seconds", flush=True)
    return result


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
    print("PASS_PHYSICAL_ORDINARY_ENGINE")
