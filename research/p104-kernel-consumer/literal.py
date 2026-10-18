"""Two exact P104 kernel-witness executions, with independent native arithmetic.

Clear1nsight, with substantial OpenAI assistance. Apache-2.0.
Gaussian and signed-floor formulas are adapted with credit from the separately
written PR3554 independent.py (SHA256 e7e06d875ffcf1b34946f844141b3c9fcf2f7395e35aba4e18277e6fea279428).
No predecessor executable is imported. The orchestrator authenticates the raw
WORD/NATIVE bytes; this module binds their complete occurrence/frame structure.
Only the specified p and 4p fixtures are executed; all other initial banks are zero.
"""

from collections import Counter
from fractions import Fraction
import hashlib
import json


RANK = 9
SIZE = 512
ZERO = (0, 0)
WATCH_CUTS = (1099, 2121, 3278, 4241, 5086, 5397)
WATCH_BANKS = ('Q0', 'G0', 'X0')


class LiteralFailure(ValueError):
    def __init__(self, record):
        super().__init__(record['kind'])
        self.record = record


def need(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def field(values):
    need(type(values) in (list, tuple) and len(values) == SIZE, 'rank-nine field')
    need(all(type(z) in (list, tuple) and len(z) == 2
             and all(type(x) is int for x in z) for z in values), 'Gaussian integer field')
    return [tuple(z) for z in values]


def plus(a, b):
    return a[0] + b[0], a[1] + b[1]


def minus(a, b):
    return a[0] - b[0], a[1] - b[1]


def rotate(z, phase):
    a, b = z
    return ((a, b), (-b, a), (-a, -b), (b, -a))[phase % 4]


def newton_failure(values):
    """Return a first exact Mobius-coefficient divisibility witness, if any."""
    if not any(z != ZERO for z in values):
        return None
    coefficients = list(values)
    for bit in range(RANK):
        step = 1 << bit
        for mask in range(SIZE):
            if mask & step:
                coefficients[mask] = minus(coefficients[mask], coefficients[mask ^ step])
    for mask, original in enumerate(coefficients):
        a, b = original
        for divided in range(mask.bit_count()):
            if (a + b) % 2 or (b - a) % 2:
                return {'mask': mask, 'degree': mask.bit_count(), 'mobius_coefficient': original,
                        'pi_divisions_completed': divided, 'remaining_gaussian': (a, b)}
            a, b = (a + b) // 2, (b - a) // 2
    return None


def bind(word, native):
    need(len(word['program']) == 5398 and len(word['initial_frames']) == 358,
         'frozen full-word dimensions')
    need(word['chart'] == native['chart'], 'word/native chart convention')
    need(len(native['transports']) == 1245, 'frozen native class count')
    result = {}
    for record in native['transports']:
        rank = record['recipe']['rank']
        need(type(rank) is int and 1 <= rank <= RANK, 'native rank')
        for event in record['events']:
            need(type(event) is int and 0 <= event < 5398 and event not in result,
                 'unique bounded native occurrence')
            row = word['program'][event]
            need(row[0] == 'transport' and row[2:] == [record['old'], record['new'], rank],
                 'exact native occurrence and frame binding')
            result[event] = record['recipe']
    expected = {i for i, row in enumerate(word['program']) if row[0] == 'transport'}
    need(set(result) == expected and len(result) == 2070, 'all actual native occurrences')
    return result


def wrapper_plan(raw):
    rows, linear, quadratic = (raw[k] for k in ('matrix_rows', 'linear_Z4', 'quadratic_rows'))
    need(len(rows) == len(linear) == len(quadratic) == RANK, 'wrapper dimensions')
    need(all(type(x) is int and 0 <= x < SIZE for x in rows + quadratic), 'binary wrapper rows')
    need(all(type(x) is int and 0 <= x < 4 for x in linear), 'linear Z4 phase')
    need(type(raw['offset']) is int and 0 <= raw['offset'] < SIZE, 'affine offset')
    need(type(raw['phase']) is int and 0 <= raw['phase'] < 4, 'global phase')
    result = []
    for address in range(SIZE):
        target = raw['offset'] ^ sum(((address & row).bit_count() % 2) << j
                                     for j, row in enumerate(rows))
        phase = raw['phase']
        for j in range(RANK):
            if address & (1 << j):
                upper = quadratic[j] & ~((1 << (j + 1)) - 1)
                phase += linear[j] + 2 * (upper & address).bit_count()
        result.append((target, phase % 4))
    need({target for target, _ in result} == set(range(SIZE)), 'wrapper permutation')
    return result


def wrapper(values, mapping, inverse):
    result = [ZERO] * SIZE
    for source, (target, phase) in enumerate(mapping):
        if inverse:
            result[source] = rotate(values[target], -phase)
        else:
            result[target] = rotate(values[source], phase)
    return result


def pair(a, b, inverse, event, bit, address):
    dr, di = minus(a, b)
    ar, ai = plus(a, b)
    sign = -1 if inverse else 1
    numerators = ((ar - sign * di, ai + sign * dr),
                  (ar + sign * di, ai - sign * dr))
    if any(x % 2 for z in numerators for x in z):
        raise LiteralFailure({'kind': 'nonintegral_ideal_native_pair', 'event': event,
                              'bit': bit, 'address': address, 'inverse': inverse,
                              'input_pair': (a, b), 'twice_ideal_outputs': numerators})
    ideal = tuple((r // 2, i // 2) for r, i in numerators)
    midpoint = plus(b, (dr // 2, di // 2))
    turned = (di, -dr) if inverse else (-di, dr)
    second = minus(midpoint, (turned[0] // 2, turned[1] // 2))
    literal = (plus(second, turned), second)
    need(literal == ideal, 'literal signed-floor pair differs from integral ideal pair')
    return literal


class Arithmetic:
    def __init__(self, bound):
        self.bound = bound
        self.cache = {}

    def plan(self, raw):
        key = canonical(raw)
        if key not in self.cache:
            need(len(self.cache) < 2490, 'bounded native wrapper cache')
            self.cache[key] = wrapper_plan(raw)
        return self.cache[key]

    def native(self, values, event, inverse, counts):
        recipe = self.bound[event]
        counts['native_events_entered'] += 1
        if not any(z != ZERO for z in values):
            counts['zero_native_events'] += 1
            counts['zero_native_pairs_proved_zero'] += recipe['rank'] * (SIZE // 2)
            return list(values)
        first, last = ('left', 'right') if inverse else ('right', 'left')
        result = wrapper(values, self.plan(recipe[first]), inverse)
        bits = reversed(range(recipe['rank'])) if inverse else range(recipe['rank'])
        for bit in bits:
            step = 1 << bit
            for address in range(SIZE):
                if not address & step:
                    result[address], result[address | step] = pair(
                        result[address], result[address | step], inverse, event, bit, address)
                    counts['completed_literal_ideal_pairs'] += 1
        result = wrapper(result, self.plan(recipe[last]), inverse)
        counts['active_native_events_completed'] += 1
        counts['active_native_rank_mass'] += recipe['rank']
        return result


def derive_p(word, arithmetic):
    """Derive a44's zero-gap field from the actual Y91 path, without K imports."""
    row = word['program'][1817]
    need(row[:4] == ['add', 'D27', 'Y91', '1/4'], 'a44 actual read event')
    need(word['program'][1819][:4] == ['add', 'D27', 'Y90', '1/4'], 'a44 cancellation read')
    path = [i for i, event in enumerate(word['program'][:1817])
            if event[:2] == ['transport', 'Y91']]
    need(word['initial_frames']['Y91'] == [], 'empty Y91 source frame')
    need(not any(event[1] == 'D27' for event in word['program'][1818:1819]),
         'zero-native D27 interval')
    values = [(-4, 0) if address & 15 == 15 else ZERO for address in range(SIZE)]
    counts = Counter()
    current = tuple(row[4])
    for event in reversed(path):
        literal = word['program'][event]
        need(tuple(literal[3]) == current, 'inverse Y91 path composability')
        values = arithmetic.native(values, event, True, counts)
        current = tuple(literal[2])
    need(current == (), 'inverse Y91 path reaches original source frame')
    need(newton_failure(values) is None, 'derived p belongs to B9')
    return values, {'coefficient_slot': 44, 'coefficient_mask': 15,
                    'read_event': 1817, 'cancellation_event': 1819, 'source_path': path,
                    'profile': 'E9 delta15 = -4 on the 32 supersets of mask15',
                    'inverse_path_arithmetic': dict(counts), 'p_sha256': digest(values)}


def increment(values, coefficient, event, source, target):
    numerator, denominator = coefficient.as_integer_ratio()
    result = []
    for address, z in enumerate(values):
        for component, value in enumerate(z):
            product = numerator * value
            if product % denominator:
                raise LiteralFailure({'kind': 'nonintegral_fractional_addend', 'event': event,
                                      'source': source, 'target': target, 'address': address,
                                      'component': ('real', 'imaginary')[component],
                                      'source_value': z, 'coefficient': str(coefficient),
                                      'exact_increment': str(Fraction(product, denominator))})
        result.append((numerator * z[0] // denominator, numerator * z[1] // denominator))
    return result


def advance(state, frames, row, event, arithmetic, counts):
    op, target = row[:2]
    if op == 'transport':
        need(frames[target] == tuple(row[2]), 'actual native input frame')
        state[target] = arithmetic.native(state[target], event, False, counts)
        frames[target] = tuple(row[3])
    elif op == 'add':
        source = row[2]
        need(frames[target] == frames[source] == tuple(row[4]), 'equal-frame ADD')
        coefficient = Fraction(str(row[3]))
        addend = increment(state[source], coefficient, event, source, target)
        state[target] = [plus(a, b) for a, b in zip(state[target], addend, strict=True)]
        counts['weighted_adds'] += 1
        if coefficient.denominator > 1:
            counts['fractional_adds'] += 1
            counts['nonzero_fractional_adds'] += int(any(z != ZERO for z in addend))
    elif op == 'sign':
        need(str(row[2]) == '-1' and frames[target] == tuple(row[3]), 'actual signed frame')
        state[target] = [(-a, -b) for a, b in state[target]]
        counts['signs'] += 1
    elif op == 'zero':
        need(target not in state, 'private bank absent before initialization')
        state[target], frames[target] = [ZERO] * SIZE, tuple(row[2])
        counts['private_zero'] += 1
    else:
        need(op == 'erase' and frames[target] == tuple(row[2]), 'actual private erase frame')
        bad = next((i for i, z in enumerate(state[target]) if z != ZERO), None)
        if bad is not None:
            raise LiteralFailure({'kind': 'nonzero_private_erase', 'event': event,
                                  'target': target, 'address': bad, 'value': state[target][bad]})
        del state[target], frames[target]
        counts['private_zero_erase'] += 1


def snapshot(state, frames):
    return {bank: {'frame': list(frames[bank]), 'values': list(state[bank])} for bank in WATCH_BANKS}


def trace(word, arithmetic, p, multiplier):
    frames = {bank: tuple(value) for bank, value in word['initial_frames'].items()}
    state = {bank: [ZERO] * SIZE for bank in frames}
    need(frames['Y91'] == frames['Y90'] == (), 'paired initial source frame')
    state['Y91'] = [(multiplier * a, multiplier * b) for a, b in p]
    state['Y90'] = [(-a, -b) for a, b in state['Y91']]
    counts, checkpoints = Counter(), {}
    first_non_B, failure = None, None
    for event, row in enumerate(word['program']):
        try:
            advance(state, frames, row, event, arithmetic, counts)
        except LiteralFailure as error:
            failure = {**error.record, 'actual_word_event': row}
            break
        counts['events_completed'] += 1
        target = row[1]
        if first_non_B is None and target in state:
            witness = newton_failure(state[target])
            if witness is not None:
                first_non_B = {'event': event, 'bank': target,
                               'frame': list(frames[target]), 'witness': witness}
        if event in WATCH_CUTS:
            checkpoints[str(event)] = snapshot(state, frames)
    complete = failure is None
    if complete:
        need(frames == {b: tuple(f) for b, f in word['final_frames'].items()},
             'all final physical frames exactly match original word')
        need(counts['events_completed'] == 5398 and counts['native_events_entered'] == 2070,
             'complete actual full-word inventory')
        need(counts['private_zero'] == counts['private_zero_erase'] == 8, 'all eight private erasures')
    receipt = {'multiplier': multiplier, 'status': 'PASS_EXACT_LITERAL_WORD' if complete else 'EXACT_LITERAL_FAILURE',
               'counts': dict(counts), 'first_literal_failure': failure,
               'first_completed_event_outside_B9': first_non_B,
               'checkpoint_sha256': {cut: {bank: digest(item['values']) for bank, item in values.items()}
                                     for cut, values in checkpoints.items()},
               'final_frames_checked': complete,
               'nonzero_final_banks': sorted(b for b, v in state.items() if any(z != ZERO for z in v)) if complete else None,
               'final_Q0_sha256': digest(state['Q0']) if complete else None,
               'final_X0_sha256': digest(state['X0']) if complete else None}
    return {'receipt': receipt, 'checkpoints': checkpoints,
            'final_Q0': list(state['Q0']) if complete else None,
            'final_X0': list(state['X0']) if complete else None,
            'final_Y90': list(state['Y90']) if complete else None,
            'final_Y91': list(state['Y91']) if complete else None}


def run_literal(word, native, p):
    """Probe only the supplied K a44 witness and its strong-domain multiple four.

    The caller authenticates raw sources. All other 356 initial public banks,
    including dirty D/Q roles, are zero in these two witnesses. The returned
    complete Q0/G0/X0 checkpoint arrays are for exact comparison by the caller.
    Zero native branches are evaluated by their proved zero action, not counted
    as executed nonzero pair comparisons. No predecessor suite is invoked.
    """
    p = field(p)
    arithmetic = Arithmetic(bind(word, native))
    derived, derivation = derive_p(word, arithmetic)
    need(p == derived and any(z != ZERO for z in p), 'exact independently derived nonzero K witness')
    unscaled = trace(word, arithmetic, p, 1)
    strong = trace(word, arithmetic, p, 4)
    need(strong['receipt']['status'] == 'PASS_EXACT_LITERAL_WORD'
         and strong['receipt']['first_completed_event_outside_B9'] is None,
         '4p strong-domain word must execute exactly in B9')
    y_writes = [(i, row) for i, row in enumerate(word['program']) if row[1].startswith('Y')]
    need(len(y_writes) == 728 and all(row[0] == 'transport' for _, row in y_writes),
         'actual word has only bank-local Y writes')
    return {'receipt': {'status': 'PASS_TWO_LITERAL_KERNEL_PROBES', 'derivation': derivation,
                        'fixture_scope': 'Y91=p,Y90=-p or Y91=4p,Y90=-4p; all other initial banks zero.',
                        'all_native_occurrences_bound': 2070, 'all_Y_target_events': 728,
                        'cross_bank_Y_writes': 0,
                        'actual_final_Y_frame_dimensions': dict(Counter(len(word['final_frames']['Y' + str(i)])
                                                                      for i in range(104))),
                        'unscaled': unscaled['receipt'], 'strong': strong['receipt'],
                        'zero_branch_rule': 'Every affine monomial and each exact signed-floor pair sends an all-zero field to zero.'},
            'arrays': {'derived_p': derived, 'unscaled': unscaled, 'strong': strong}}
