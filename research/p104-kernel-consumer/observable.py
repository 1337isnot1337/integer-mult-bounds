"""A source-bound adjoint audit of one P104 kernel observable.

This module does not execute rounded native arithmetic. It checks one named
normalized endpoint, assuming the credited native covariance, and returns the
frames that any physical interpretation must respect. Literal admission and
the caller bill are separate obligations.

Clear1nsight, with OpenAI assistance. Apache-2.0.
"""

from collections import Counter
from fractions import Fraction
import hashlib
import json


WORD_SHA = "cec1fb3fbd0067b500ad5119a62ba60685be718e769374d7ec8abdd2beaa7e50"
COMPLETION_SHA = "f68a2e6f3bd771b9692772909df200102350a80deda35532f3cc348b75d0c044"
ADAPTERS_SHA = "db424edfb316f06f4913946b2b0cafa2f200b75392cacb35244b8705db02387c"
NATIVE_SHA = "ab91c78835c3e10cf3b2cb8a5d4e0b7cfc3df1ae5a811298d27842f2193e1e3d"
FULL = [256, 128, 64, 32, 16, 8, 4, 2, 1]
O = [256, 136, 64, 40, 16, 4, 2, 1]
O0 = [257, 129, 65, 33, 16, 9, 5, 2]
D_BANKS = ["D31", "D30", "D29", "D28", "D27"]


class AuditError(ValueError):
    """The exact finite contract was not met."""


def require(condition, message):
    if not condition:
        raise AuditError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def authenticated(raw, expected, name):
    require(type(raw) is bytes, name + " must be bytes")
    require(hashlib.sha256(raw).hexdigest() == expected, name + " hash")
    value = json.loads(raw)
    require(type(value) is dict, name + " object")
    return value


def rational(value):
    require(type(value) in (int, str), "coefficient type")
    result = Fraction(value)
    require(result in (Fraction(1, 4), Fraction(-1, 4), Fraction(1, 2),
                       Fraction(-1, 2), -2, -1, 1, 2), "coefficient alphabet")
    return result


def fraction_record(value):
    return [value.numerator, value.denominator]


def row_record(row):
    return {bank: fraction_record(value) for bank, value in sorted(row.items())}


def frame(value):
    require(type(value) is list and len(value) <= 9, "frame list")
    require(all(type(x) is int and 0 < x < 512 for x in value), "frame entry")
    require(len(value) == len(set(value)), "frame duplicate")
    return value


def frame_audit(word):
    """Check every syntactic frame transition, not its native semantics."""
    program = word["program"]
    initial, final = word["initial_frames"], word["final_frames"]
    require(type(program) is list and len(program) == 5398, "word length")
    require(type(initial) is dict and type(final) is dict, "frame dictionaries")
    require(set(initial) == set(final) and len(initial) == 358, "public banks")
    state = {bank: frame(value)[:] for bank, value in initial.items()}
    after = []
    counts = Counter()
    for event, instruction in enumerate(program):
        require(type(instruction) is list and instruction, "instruction list")
        op, bank = instruction[:2]
        require(type(bank) is str, "bank name")
        counts[op] += 1
        if op == "zero":
            require(len(instruction) == 3 and bank not in state, "zero lifetime")
            state[bank] = frame(instruction[2])[:]
        else:
            require(bank in state, "live target")
            if op == "transport":
                require(len(instruction) == 5, "transport arity")
                require(state[bank] == frame(instruction[2]), "transport entrance")
                require(type(instruction[4]) is int, "native rank type")
                require(1 <= instruction[4] <= 9, "native rank")
                state[bank] = frame(instruction[3])[:]
            elif op == "add":
                require(len(instruction) == 5, "ADD arity")
                source = instruction[2]
                require(type(source) is str and source in state, "live source")
                require(source != bank, "distinct ADD banks")
                require(state[bank] == state[source] == frame(instruction[4]),
                        "same-frame ADD")
                rational(instruction[3])
                require(not bank.startswith("Y"), "Y is transport-only")
            elif op == "sign":
                require(len(instruction) == 4, "sign arity")
                require(rational(instruction[2]) == -1, "sign coefficient")
                require(state[bank] == frame(instruction[3]), "sign frame")
            elif op == "erase":
                require(len(instruction) == 3 and bank not in initial,
                        "private erasure")
                require(state[bank] == frame(instruction[2]), "erase frame")
                del state[bank]
            else:
                raise AuditError("unknown opcode " + str(op))
        after.append({b: state[b][:] for b in ("D1", "Q0", "G0", "X0", "C")
                      if b in state})
    require(state == final, "all declared endpoint frames")
    require(dict(counts) == {"transport": 2070, "sign": 208, "add": 3104,
                             "zero": 8, "erase": 8}, "operation inventory")
    ys = sorted(bank for bank in initial if bank.startswith("Y"))
    require(set(ys) == {"Y" + str(i) for i in range(104)}, "104 Y banks")
    require(all(initial[b] == [] and len(final[b]) == 8 for b in ys),
            "actual Y endpoint dimensions")
    bindings = {b: [initial[b], final[b]] for b in ys}
    return after, dict(counts), bindings


def adjoint(program, stop, bank, omitted=()):
    """Pull one output covector backward; no forward scalar state is used."""
    require(type(stop) is int and 0 <= stop <= len(program), "adjoint cut")
    row = {bank: Fraction(1)}
    for event in range(stop - 1, -1, -1):
        if event in omitted:
            continue
        instruction = program[event]
        op, target = instruction[:2]
        coefficient = row.get(target, Fraction(0))
        if op == "add" and coefficient:
            source = instruction[2]
            value = row.get(source, Fraction(0)) + coefficient * rational(instruction[3])
            if value:
                row[source] = value
            else:
                row.pop(source, None)
        elif op == "sign" and coefficient:
            row[target] = -coefficient
        elif op == "zero":
            row.pop(target, None)
        elif op == "erase":
            require(not coefficient, "backward erased lifetime")
    return row


def pair_value(row):
    return row.get("Y91", Fraction(0)) - row.get("Y90", Fraction(0))


def source_groups(program):
    groups = []
    flat = []
    for bank in D_BANKS:
        reads = []
        for event, instruction in enumerate(program[:2025]):
            if instruction[:2] != ["add", bank]:
                continue
            require(instruction[2].startswith("Y"), "D producer source")
            require(rational(instruction[3]) == Fraction(1, 4), "D producer quarter")
            reads.append({"source": instruction[2], "event": event,
                          "frame": instruction[4], "slot": len(flat)})
            flat.append(instruction[2])
        expected = {bank: Fraction(1)}
        for read in reads:
            expected[read["source"]] = Fraction(1, 4)
        require(adjoint(program, 2025, bank) == expected, "actual D cut row")
        groups.append({"bank": bank, "reads": reads, "rho_coefficient": [1, 4]})
    require([len(g["reads"]) for g in groups] == [3, 7, 7, 11, 24], "five groups")
    require(len(flat) == len(set(flat)) == 52, "distinct 52 Y sources")
    require(flat[44:46] == ["Y91", "Y90"], "actual a44 source slots")
    require([g["reads"][-1]["source"] for g in groups] ==
            ["Y99", "Y100", "Y66", "Y72", "Y80"], "terminal sources")
    rho = [sum((Fraction(int(r["source"] == "Y91") -
                        int(r["source"] == "Y90"), 4) for r in g["reads"]),
               Fraction(0)) for g in groups]
    require(rho == [0] * 5, "rho5 kernel direction")
    return groups, rho


def named_reads(program):
    wanted = {
        1099: ["add", "D1", "Y90", "1/4", [381, 241, 2]],
        1817: ["add", "D27", "Y91", "1/4", O],
        1819: ["add", "D27", "Y90", "1/4", O],
        2118: ["add", "C", "D1", 1, O0],
        2121: ["add", "Q0", "C", "1", [400]],
        2166: ["add", "D1", "Y90", "-1/4", FULL],
        3025: ["add", "G0", "Q0", 1, [400]],
        3278: ["add", "X0", "G0", -2, [400, 85]],
        4104: ["add", "G0", "Q0", -1, FULL],
        4241: ["add", "Q0", "Y90", "-1/4", FULL],
        5086: ["sign", "X0", "-1", [258, 130, 64, 32, 16, 8, 4, 1]],
        5190: ["transport", "X0", [258, 130, 64, 32, 16, 8, 4, 1], FULL, 1],
    }
    for event, expected in wanted.items():
        require(canonical(program[event]) == canonical(expected), "named event " + str(event))
    d27_reads = [i for i, e in enumerate(program) if e[0] == "add" and e[2] == "D27"]
    require(d27_reads == [916, 2030, 2034], "all D27 source reads")
    require(not any(1817 < i < 1819 for i in d27_reads), "unobserved D27 interval")
    pair_reads = [{"event": i, "instruction": e} for i, e in enumerate(program)
                  if e[0] == "add" and e[2] in ("Y90", "Y91")]
    d1_pair = [r for r in pair_reads if r["instruction"][1] == "D1"]
    require([r["event"] for r in d1_pair] == [1099, 2166], "D1 pair asymmetry")
    return {"events": [{"event": i, "instruction": e} for i, e in sorted(wanted.items())],
            "all_pair_reads": pair_reads, "all_D27_source_reads": d27_reads,
            "intervening_event": {"event": 1818, "instruction": program[1818]}}


def cut_audit(program, after):
    cuts = [(1099, "D1", "-1/4"), (2118, "C", "-1/4"),
            (2121, "Q0", "-1/4"), (2166, "D1", "0"),
            (3025, "G0", "-1/4"), (3278, "X0", "1/2"),
            (4104, "G0", "0"), (4241, "Q0", "0"),
            (5085, "X0", "1/2"), (5086, "X0", "-1/2"),
            (5190, "X0", "-1/2")]
    out = []
    for event, bank, expected in cuts:
        row = adjoint(program, event + 1, bank)
        require(pair_value(row) == Fraction(expected), "named adjoint cut")
        require(all(b != "C" for b in row), "private zero eliminated")
        record = row_record(row)
        out.append({"event_after": event, "bank": bank, "frame": after[event][bank],
                    "pair_value": fraction_record(pair_value(row)),
                    "row_sha256": digest(record), "row_nonzeros": len(record),
                    "Y91_coefficient": fraction_record(row.get("Y91", Fraction(0))),
                    "Y90_coefficient": fraction_record(row.get("Y90", Fraction(0)))})
    require(adjoint(program, 2128, "C") == {}, "actual collector C erasure")
    for bank in ("D1", "Q0", "G0"):
        require(adjoint(program, len(program), bank) == {bank: Fraction(1)},
                "normalized arbitrary-dirty restoration " + bank)
    gather = adjoint(program, 2122, "Q0")
    require(gather.get("Q0") == 1 and all(b == "Q0" or b.startswith("Y")
                                         for b in gather), "Q0 dirty D cancellation")
    return out, row_record(gather)


def completion_audit(program, completion, adapters, word):
    require(completion["source_sha256"] == {
        "research/p104-rounded-collector/inputs/WORD.json": WORD_SHA,
        "research/p104-rounded-collector/inputs/NATIVE.json.gz": NATIVE_SHA},
        "completion original sources")
    a, c = completion["factor"]["A"], completion["factor"]["C"]
    require(type(a) is list and len(a) == 8, "eight credited query rows")
    require(all(type(r) is dict and all(type(x) is int for x in r.values())
                for r in a), "integer A rows")
    c0 = c["X0"]
    require(type(c0) is list and all(type(x) is int for x in c0), "integer C X0")
    require(c0 == [1, 0, 0, 0, 0, 0, 0, 0], "X0 basis row")
    delta = [r.get("Y91", 0) - r.get("Y90", 0) for r in a]
    require(delta == [-1, 1, 0, 0, 1, -1, 1, 1], "credited pair query vector")
    final_row = adjoint(program, len(program), "X0")
    require(final_row.pop("X0", None) == 1, "X0 original dirty coefficient")
    expected = {"Y" + str(i): sum((Fraction(c0[j] * a[j].get("Y" + str(i), 0), 2)
                                  for j in range(8)), Fraction(0)) for i in range(104)}
    expected = {b: x for b, x in expected.items() if x}
    require(final_row == expected, "full X0 adjoint row versus published CA/2")
    require(pair_value(final_row) == Fraction(-1, 2), "observable coefficient")
    gap = completion["unfilled_physical_frame_gaps"]["X0"]
    require(gap == [word["initial_frames"]["X0"], word["final_frames"]["X0"]],
            "X0 projection omission and endpoint gap")
    x_entries = [x for x in adapters["omitted_banks"] if x["bank"] == "X0"]
    require(x_entries == [{"bank": "X0", "recipe_key": [386], "rank": 8}],
            "credited X0 native-only adapter")
    recipes = [r for r in adapters["recipes"] if r["old"] == [386] and r["new"] == FULL]
    require(len(recipes) == 1 and recipes[0]["recipe"]["rank"] == 8, "unique adapter")
    require(adapters["projection_event_sha256"] == completion["closure"]["events_sha256"],
            "same credited projection")
    return {"A_pair_difference": delta, "C_X0": c0,
            "X0_Y_row": row_record(final_row), "X0_Y_nonzeros": len(final_row),
            "X0_pair_coefficient": [-1, 2], "X0_frame_gap": gap,
            "X0_omitted_from_4027_event_projection": True,
            "adapter_rank": 8, "adapter_recipe_sha256": digest(recipes[0]["recipe"]),
            "credited_adapter_certificate": recipes[0]["certificate"]}


def controls(program, raws):
    faulty = adjoint(program, len(program), "X0", omitted=(5086,))
    require(pair_value(faulty) == Fraction(1, 2), "omitted sign separating control")
    dirty = adjoint(program, len(program), "Q0", omitted=(4241,))
    require(pair_value(dirty) == Fraction(-1, 4), "omitted Q0 cleanup control")
    corruption = []
    for raw, sha, name in raws:
        try:
            authenticated(raw + b" ", sha, name)
        except AuditError:
            corruption.append(name)
        else:
            raise AuditError("source corruption was accepted")
    return {"omitted_sign_5086_X0_pair": [1, 2],
            "omitted_Q0_cleanup_4241_pair": [-1, 4],
            "source_corruption_rejected": corruption}


def analyze(word_bytes, completion_certificate_bytes, adapters_bytes):
    """Return exact named scalar/caller evidence; execute no native suite."""
    raws = [(word_bytes, WORD_SHA, "WORD"),
            (completion_certificate_bytes, COMPLETION_SHA, "PR3462 certificate"),
            (adapters_bytes, ADAPTERS_SHA, "PR3469 adapters")]
    word, completion, adapters = [authenticated(*r) for r in raws]
    program = word["program"]
    after, counts, y_bindings = frame_audit(word)
    groups, rho = source_groups(program)
    reads = named_reads(program)
    cuts, gather = cut_audit(program, after)
    result = completion_audit(program, completion, adapters, word)
    paths = {b: [{"event": i, "instruction": e} for i, e in enumerate(program)
                 if e[:2] == ["transport", b]]
             for b in ("Y90", "Y91", "D1", "Q0", "G0", "X0")}
    return {
        "schema_version": 1, "status": "PASS",
        "method": "One-output reverse adjoints and exact source/certificate binding",
        "source_sha256": {name: sha for _, sha, name in raws},
        "event_numbering": "zero-based source WORD program indices",
        "word_operation_counts": counts,
        "five_source_groups": groups, "rho5_pair_response": [fraction_record(x) for x in rho],
        "source_read_audit": reads, "named_cuts": cuts,
        "Q0_after_2121_initial_row": gather, "completion": result,
        "named_native_paths": paths,
        "Y_endpoint_audit": {"count": 104, "all_initial_frames_empty": True,
                             "all_final_dimensions": 8, "all_transport_only": True,
                             "bindings_sha256": digest(y_bindings),
                             "Y90": y_bindings["Y90"], "Y91": y_bindings["Y91"]},
        "restoration": {"D1_Q0_G0": "initial normalized rows; physical final frame F",
                        "C": "actual 2114..2128 collector has zero adjoint at erasure",
                        "Y": "normalized source payloads retained at their actual final frames"},
        "separation": {
            "formal_pair": "Y91=p, Y90=-p, all other initial increments zero",
            "rho5": "zero on all five group readouts",
            "Q0_after_2121": "-p/4", "X0_after_3278": "+p/2",
            "X0_final": "-p/2", "strong_4p_X0_final": "-2p",
            "claim": "The required X0 residual cannot factor through rho5 alone",
            "physical_meaning": "X0 increment is J_F(-p/2), conditional on native covariance and admission",
            "limitation": "This does not erase retained Y/coefficient outputs or prove a benefit from L/S",
        },
        "controls": controls(program, raws),
        "scope_limits": [
            "No literal full-word admission is proved by this scalar audit",
            "No fresh full-map rank, recipient closure, or adapter optimality is claimed",
            "Paid acquisition, physical layouts/routes, widths, and supplier advantage are not inferred",
        ],
    }
