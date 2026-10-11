"""Independent literal-word and retained-evidence audit of basis reordering."""
from pathlib import Path
import gzip
import hashlib
import json
import difflib

if not __debug__:
    raise RuntimeError('Assertions must remain enabled')
ROOT = Path(__file__).resolve().parent


def raw(name):
    data = (ROOT/name).read_bytes()
    return gzip.decompress(data) if str(name).endswith('.gz') else data


def read(name):
    return json.loads(raw(name))


def digest(name):
    return hashlib.sha256(raw(name)).hexdigest()


def snapshot():
    assert not any(p.is_symlink() for p in ROOT.rglob('*'))
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in ROOT.rglob('*') if p.is_file() and p != ROOT/'MANIFEST.json'}


def gates(word, omit_inverse=False, omit_dirt=False):
    result = []
    def append(group):
        for _, destination, sources in group:
            for source in sources:
                assert destination != source
                result.append((destination, source))
    if not omit_dirt:
        append(word['D'])
    append(word['A'])
    for index, source in enumerate(word['ret']):
        assert source < word['v']
        for target, selected in enumerate(word['scatter']):
            if index in selected:
                result.append((word['v']+target, source))
    append(word['B'][word['source_basis_gates']:] if omit_inverse else word['B'])
    append(word['C'])
    return result


def restores(word, reverse=False, **options):
    size = 2*word['v']+word['R']
    values = [1 << i for i in range(size)]
    stream = gates(word, **options)
    for destination, source in reversed(stream) if reverse else stream:
        values[destination] ^= values[source]
    expected = [1 << i for i in range(size)]
    for target in range(word['v']):
        expected[word['v']+target] ^= 1 << target
    return values == expected


def prefix(word, reverse):
    norms = [1]*(2*word['v']+word['R'])
    peak = 1
    stream = gates(word)
    for destination, source in reversed(stream) if reverse else stream:
        norms[destination] += norms[source]
        peak = max(peak, norms[destination])
    return peak


def forms(word):
    values = [1 << i for i in range(word['v'])]
    for frame, destination, sources in word['A'][-word['source_basis_gates']:]:
        assert frame == word['final'][0]
        assert destination < word['v'] and len(sources) == 1 and sources[0] < word['v']
        values[destination] ^= values[sources[0]]
    return [values[index] for index in word['ret']]


def coefficient(g, geo):
    paid = sum(g['profile'].values())
    routes = 576*(240+758)+61440+2*g['bank_assignments']+2*g['copy_erase_episodes']
    selectors = 144*((14502-1)+758*64*(geo['max_route_factors']+63+64))
    value = (72*g['local_additions']+g['bridge_additions']
             + routes*(16*4097**2+14511)+paid*(8*64**2+8+128*128**3)
             + 16*64**3+g['copy_erase_episodes']+selectors+int(g['global_prefix_bound'])+1)
    return value, (value+1)**2*(paid+1)**2


def verify():
    manifest = read('MANIFEST.json')['files']
    assert snapshot() == manifest
    source = read('SOURCES.json')
    for entry in source['files']:
        assert digest(entry['path']) == entry['original_sha256'], entry['path']
    assert digest('inputs/SUPPLIER-MANIFEST.json') == source['supplier_manifest_sha256']
    binding = read('inputs/SUPPLIER-SOURCE-BINDING.json')
    assert binding['head'] == source['commit'] and binding['repository'] == source['repository']
    for local, upstream in [('vendor/bit_construct.py', 'code/bit_construct.py'),
                            ('inputs/SUPPLIER-MANIFEST.json', 'MANIFEST.json')]:
        entry = next(e for e in binding['files'] if e['path'] == upstream)
        data = raw(local)
        assert hashlib.sha256(data).hexdigest() == entry['sha256']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == entry['git_blob']
    original = raw('vendor/bit_construct.py').decode()
    derived = original
    for before, after in [
        ('sorted(echelon.items())', 'sorted(echelon.items(), reverse=True)'),
        ('p = (row & -row).bit_length() - 1', 'p = row.bit_length() - 1'),
        ('pivots = sorted(echelon)', 'pivots = sorted(echelon, reverse=True)'),
    ]:
        assert derived.count(before) == 1
        derived = derived.replace(before, after)
    assert hashlib.sha256(derived.encode()).hexdigest() == '61578d8959893e7fec667d5e7697cc6faef773d1e7c50a45e929e69a0038f279'
    patch = ''.join(difflib.unified_diff(original.splitlines(True), derived.splitlines(True),
        fromfile='a/research/split-centres-global/code/bit_construct.py',
        tofile='b/research/split-centres-global/code/bit_construct.py'))
    assert raw('basis-order.patch').decode() == patch
    completed = read('inputs/candidate/COMPLETION.json')
    baseline_completed = read('inputs/baseline/COMPLETION.json')
    assert completed['status'] == 'PASS_CHANGED_BIT_FINITE_CHECK'
    assert completed['input_before'] == completed['input_after']
    assert completed['source_manifest_sha256'] == source['supplier_manifest_sha256']
    assert baseline_completed['status'] == 'PASS_RETAINED_DEFAULT_PR433_REPLAY'
    assert baseline_completed['source_manifest_before'] == baseline_completed['source_manifest_after'] == source['supplier_manifest_sha256']
    for name, original in [('word.json.gz', 'bit426-source-centres/bit-source-centres.json'),
                            ('GLOBAL.json', 'bit426-source-centres/global/GLOBAL.json'), ('RESULT.json', 'RESULT.json')]:
        assert digest('inputs/baseline/'+name) == baseline_completed['output_hashes']['run/'+original]
    paths = {'word.json.gz': 'bit426-source-centres/bit-source-centres.json',
             'GLOBAL.json': 'bit426-source-centres/global/GLOBAL.json',
             'GEOMETRY.json.gz': 'bit426-source-centres/global/GEOMETRY.json',
             'AUDIT.json': 'bit426-source-centres/global/AUDIT.json',
             'BIT-PRICE.json': 'BIT-PRICE.json', 'RESULT.json': 'RESULT.json'}
    for name, original in paths.items():
        assert digest('inputs/candidate/'+name) == completed['output_hashes'][original]
    assert len(completed['steps']) == 5
    for step in completed['steps']:
        assert step['returncode'] == 0
        assert digest('inputs/candidate/'+step['name']+'.log') == step['log_sha256']
    for name in ['INTEGRATION.json', 'INDEPENDENT-REPLAY.json']:
        assert digest('inputs/complex/'+name) == completed['reused']['split-centres/'+name]
        assert digest('inputs/complex/'+name) == baseline_completed['output_hashes']['run/split-centres/'+name]
    old, word = read('inputs/baseline/word.json.gz'), read('inputs/candidate/word.json.gz')
    assert set(word) == set(old)
    assert {k: v for k, v in word.items() if k not in ['A', 'B', 'ret', 'source_basis_gates']} == {
        k: v for k, v in old.items() if k not in ['A', 'B', 'ret', 'source_basis_gates']}
    a, b = old['source_basis_gates'], word['source_basis_gates']
    assert (a, b) == (559, 575)
    assert old['A'][:-a] == word['A'][:-b] and old['B'][a:] == word['B'][b:]
    assert word['A'][-b:] == list(reversed(word['B'][:b]))
    assert forms(word) == forms(old)
    for item in [old, word]:
        assert restores(item) and restores(item, reverse=True)
    assert not restores(word, omit_inverse=True) and not restores(word, omit_dirt=True)
    bg, g = read('inputs/baseline/GLOBAL.json'), read('inputs/candidate/GLOBAL.json')
    audit = read('inputs/candidate/AUDIT.json')
    assert g['status'] == 'PASS_SOURCE_BOUND_NINE_STAGE_BIT_TEMPLATE'
    assert audit['status'] == 'PASS_INDEPENDENT_COMPRESSED_BIT_TEMPLATE_AUDIT'
    assert (g['m'], g['R'], g['live'], g['physical']) == (64, 758, 14502, 14511)
    assert g['all_scalar_columns_restored'] and g['independent_unbanked_scalar_columns'] == 7782
    result, previous = read('inputs/candidate/RESULT.json'), read('inputs/baseline/RESULT.json')
    for key in ['profile', 'live', 'physical', 'rank_mass', 'paid_calls', 'bank_assignments',
                'maxchild', 'local_invocations', 'deficit', 'copy_erase_episodes', 'bridge_additions']:
        assert g[key] == bg[key], key
    assert g['profile'] == audit['profile'] and len(audit['mutations_rejected']) == 8
    assert g['template_sha256'] == audit['template_sha256'] == result['bit_template_sha256']
    assert g['geometry_sha256'] == digest('inputs/candidate/GEOMETRY.json.gz')
    for key in ['bit_lower', 'complex_lower', 'kappa', 'strict_outer_constraints',
                'bootstrap', 'outer_controls', 'complex_template_sha256']:
        assert result[key] == previous[key], key
    for w, receipt in [(old, bg), (word, g)]:
        assert len(gates(w)) == receipt['local_additions']
        factors = [prefix(w, reverse) for reverse in [False, True]]
        assert factors == [receipt['local_checks'][key]['cancellation_free_row_l1'] for key in ['forward', 'reverse']]
        assert int(receipt['global_prefix_bound']) == 2**18*factors[0]**5*factors[1]**4
    geo = read('inputs/candidate/GEOMETRY.json.gz')
    value, two = coefficient(g, geo)
    old_value, old_two = coefficient(bg, geo)
    assert old_value == int(read('inputs/baseline/ASSEMBLY-LOCALS.json')['coefficient'])
    assert value < old_value and two < old_two
    assert (old_value.bit_length(), value.bit_length(), old_two.bit_length(), two.bit_length()) == (223, 192, 483, 420)
    assert g['local_additions']-bg['local_additions'] == 32
    assert g['word_sha256'] == digest('inputs/candidate/word.json.gz')
    report = dict(status='PASS_BASIS_ORDER_FINITE_OVERCHARGE',
                  candidate_sha256=g['word_sha256'], coefficient=str(value), two_level_coefficient=str(two),
                  kappa=result['kappa'], local_add_delta=32, coefficient_bits=[223, 192],
                  two_level_bits=[483, 420], scope='Pinned PR433 finite-cost comparison; coarse caps and exponent unchanged.')
    for key, value in read('EXPECTED.json').items():
        assert report[key] == value
    assert snapshot() == manifest
    return report


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
