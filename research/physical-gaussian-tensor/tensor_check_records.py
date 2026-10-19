"""Exact fixed records, signed limits, cursors, fallback and ownership failures."""
from hashlib import sha256
from unittest.mock import patch
from tensor_sources import require


def run():
    from cardinal_counts import Count
    from check_support import no_decode
    from expansion_check_block import packet_bytes
    from records import Tape
    import ring_words
    from ring_check_words import decode, tape, word_bits
    from ring_words import Signed, read_signed, write_signed
    from router_metadata import owned
    from scratch_pool import ScratchPool
    from session import OuterScope, borrowed_count, borrowed_tape, erase_marker, initialize_marker, sealed_constructors
    import tensor_records as codecs
    from words import BLANK, RIGHT
    pool, digest = ScratchPool(64), sha256()
    scope = OuterScope(pool)
    for item in pool.tapes:
        erase_marker(item)
    widths = (0, 1, 31, 32, 33, 50, 86, 256, 546, 1096, 4095, 4096, 4097)
    original_read, original_write = codecs.original_read_fixed, codecs.original_write_fixed
    fallbacks = dict(read=0, write=0)
    def read_fallback(*args):
        fallbacks["read"] += 1
        return original_read(*args)
    def write_fallback(*args):
        fallbacks["write"] += 1
        return original_write(*args)
    def installed(call):
        for item in pool.tapes:
            initialize_marker(item)
        try:
            with sealed_constructors(), scope.installed():
                call()
                require(not pool.live, "record operation releases its owned scratch")
                pool.empty()
        finally:
            for item in pool.tapes:
                erase_marker(item)
    cases = binary_cases = 0
    with codecs.bounded_record_io():
        require(all(getattr(module, name) is replacement for module, name, _, replacement in codecs.CODEC_BINDINGS),
                "all seven actual numerical-record bindings")
        require(read_signed.__globals__["read_fixed"] is codecs.read_fixed
                and write_signed.__globals__["write_fixed"] is codecs.write_fixed,
                "actual retained signed wrappers reach the scoped codecs")
        with patch.object(codecs, "original_read_fixed", read_fallback), patch.object(codecs, "original_write_fixed", write_fallback):
            for bits in widths:
                for value in dict.fromkeys((0, (1 << bits)-1, ((1 << bits)-1)//3)):
                    with owned(Count.literal(bits), Count.literal(value)) as (width, number):
                        raw = word_bits(value, bits)
                        source, target = tape(bytes((0,))+raw+bytes((1,))), tape(b"")
                        source.step(1)
                        source_before = bytes(source.cells)
                        def check():
                            with no_decode():
                                result = ring_words.read_fixed(source, width)
                            with owned(result):
                                require(decode(result) == value and source.head == bits+2 and source.read() == 1,
                                        "complete record from a non-origin cursor leaves its sentinel")
                            with no_decode():
                                ring_words.write_fixed(borrowed_count(number), target, width)
                            require(target.head == bits+1 and packet_bytes(target) == raw,
                                    "fixed record preserves complete padding and target cursor")
                        installed(check)
                        require(bytes(source.cells) == source_before and width.tape.head == number.tape.head == 1,
                                "fixed records preserve borrowed bytes and parameter origins")
                        digest.update(bits.to_bytes(4, "little")+raw)
                        for item in (source, target):
                            item.clear()
                            erase_marker(item)
                        cases += 1
            require(fallbacks == dict(read=3, write=3), "4097-bit records use both retained fallbacks")
        for bits, raw in ((33, bytes(32)), (33, bytes(32)+bytes((RIGHT,)))):
            source = tape(raw)
            saved = bytes(source.cells)
            with owned(Count.literal(bits)) as (width,):
                def reject_read():
                    try:
                        with no_decode():
                            result = ring_words.read_fixed(source, width)
                    except ValueError as error:
                        require("complete fixed-width binary key" in str(error), "specific partial-record rejection")
                    else:
                        result.close()
                        raise ValueError("missing partial-record rejection")
                installed(reject_read)
                require(bytes(source.cells) == saved and width.tape.head == 1, "failed read preserves borrowed data")
            source.clear()
            erase_marker(source)
        for bits in (0, 50):
            target = tape(b"")
            with owned(Count.literal(1 << bits), Count.literal(bits)) as (number, width):
                def reject_write():
                    try:
                        with no_decode():
                            ring_words.write_fixed(number, target, width)
                    except ValueError as error:
                        require("key fits declared width" in str(error), "specific oversized-record rejection")
                    else:
                        raise ValueError("missing oversized-record rejection")
                installed(reject_write)
                require(number.tape.head == width.tape.head == 1, "failed write restores borrowed origins")
            target.clear()
            erase_marker(target)
        for bits in (1, 50, 546, 1096):
            limit = 1 << (bits-1)
            for value in (-limit, 0, limit-1, -limit-1, limit):
                target = tape(b"")
                with owned(Signed(Count.literal(abs(value)), value < 0), Count.literal(bits)) as (number, width):
                    def signed_case():
                        try:
                            with no_decode():
                                write_signed(number, target, width)
                        except ValueError as error:
                            require(value in (-limit-1, limit) and "signed data-word headroom" in str(error),
                                    "retained signed headroom rejection")
                            require(target.read() == BLANK, "signed rejection precedes output")
                        else:
                            require(-limit <= value < limit, "signed boundary admission")
                            target.rewind()
                            with no_decode():
                                result = read_signed(target, width)
                            with owned(result):
                                require((-1 if result.negative else 1)*decode(result.magnitude) == value,
                                        "complete signed boundary round trip")
                    installed(signed_case)
                    require(width.tape.head == number.magnitude.tape.head == 1, "signed wrappers restore origins")
                target.clear()
                erase_marker(target)
        with owned(Count.literal(1)) as (width,):
            def alias_case():
                with no_decode():
                    result = ring_words.read_fixed(borrowed_tape(width.tape), borrowed_count(width))
                with owned(result):
                    require(decode(result) == 1 and width.tape.head == 2,
                            "aliased width/source keeps the consumed source cursor")
            installed(alias_case)
            width.rewind()
        with owned(Count.literal(1 << 129)) as (width,):
            with no_decode():
                require(codecs.bounded_width(width) is None and width.tape.head == 1,
                        "large encoded widths never enter finite control")
        for position in (0, 1, 31, 32, 33, 50, 546, 1096, 4096, 4097):
            with owned(Count.literal(position)) as (index,):
                def check_power():
                    with no_decode():
                        result = ring_words.power_two(index)
                    with owned(result):
                        require(decode(result) == 1 << position and result.tape.head == 1,
                                "exact physical power of two including zero exponent and fallback")
                installed(check_power)
                for value in (0, 1, (1 << position)-1, 1 << position, (1 << (position+1))-1):
                    with owned(Count.literal(value)) as (number,):
                        saved = bytes(number.tape.cells)
                        def check_bit():
                            with no_decode():
                                bit = ring_words.bit_at(borrowed_count(number), index)
                            require(bit == (value >> position) & 1, "exact selected bit including early right marker")
                        installed(check_bit)
                        require(bytes(number.tape.cells) == saved and number.tape.head == index.tape.head == 1,
                                "bit selection preserves borrowed data and origins")
                        binary_cases += 1
        with owned(Count.literal(3)) as (number,):
            def shared_index():
                with no_decode():
                    bit = ring_words.bit_at(number, borrowed_count(number))
                require(bit == 0 and number.tape.head == 1, "physical value/index alias returns its origin")
            installed(shared_index)
        with owned(Count.literal(4097)) as (index,):
            def binary_fallbacks():
                with patch.object(codecs, "original_power_two", wraps=codecs.original_power_two) as power_call:
                    with patch.object(codecs, "original_bit_at", wraps=codecs.original_bit_at) as bit_call:
                        with no_decode():
                            result = ring_words.power_two(index)
                        with owned(result):
                            with no_decode():
                                bit = ring_words.bit_at(result, index)
                            require(bit == 1 and decode(result) == 1 << 4097,
                                    "complete larger-parameter power and bit results")
                        require(power_call.call_count == bit_call.call_count == 1,
                                "both4097-parameter binary helpers reach their retained fallbacks")
            installed(binary_fallbacks)
        for position, fragment in ((0, "bit-window digit"), (1, "bit-window source digit")):
            with owned(Count.literal(3), Count.literal(position)) as (number, index):
                number.tape.write(BLANK)
                saved = bytes(number.tape.cells)
                def malformed_bit():
                    try:
                        with no_decode():
                            ring_words.bit_at(number, index)
                    except ValueError as error:
                        require(str(error) == fragment, "specific selected/skipped bit rejection")
                    else:
                        raise ValueError("missing malformed-bit rejection")
                installed(malformed_bit)
                require(bytes(number.tape.cells) == saved and number.tape.head == index.tape.head == 1,
                        "malformed bit selection restores borrowed origins")
        with owned(Count.literal(32)) as (index,):
            original_append, appends = Tape.append, 0
            def interrupted_append(target, value):
                nonlocal appends
                appends += 1
                if appends == 5:
                    raise ValueError("planned power construction interruption")
                return original_append(target, value)
            def interrupted_power():
                try:
                    with no_decode(), patch.object(Tape, "append", interrupted_append):
                        result = ring_words.power_two(index)
                except ValueError as error:
                    require(str(error) == "planned power construction interruption", "specific partial-power rejection")
                else:
                    result.close()
                    raise ValueError("missing partial-power rejection")
                require(appends == 5 and not pool.live and index.tape.head == 1,
                        "interrupted power construction releases its partial result")
            installed(interrupted_power)
    require(all(getattr(module, name) is original for module, name, original, _ in codecs.CODEC_BINDINGS),
            "restore all seven actual record bindings after successful scope")
    try:
        with codecs.bounded_record_io():
            raise RuntimeError("planned record scope interruption")
    except RuntimeError:
        pass
    require(all(getattr(module, name) is original for module, name, original, _ in codecs.CODEC_BINDINGS),
            "restore all seven actual record bindings after scope interruption")
    require(not pool.live and all(item.head == 1 and all(v == BLANK for v in item.cells) for item in pool.tapes),
            "fixed record inventory and head restoration")
    return {"unsigned_cases": cases, "signed_cases": 20, "binary_cases": binary_cases,
            "powers": 10, "widths": list(widths), "fallbacks": fallbacks,
            "sha256": digest.hexdigest(), "pool_peak": pool.peak,
            "controls": ["truncated_record", "late_nonbinary", "oversized_record", "signed_headroom",
                         "aliased_width_source", "large_encoded_width", "interrupted_scope",
                         "aliased_value_index", "malformed_bits", "interrupted_power"],
            "scope": "exact numerical records and binary support through4096 with original larger-parameter fallbacks"}
