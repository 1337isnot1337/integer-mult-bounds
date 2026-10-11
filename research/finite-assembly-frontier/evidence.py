"""Validate retained supplier receipts and recompute their assembly inputs.

This is evidence reuse after one pinned supplier replay, not a new word replay.
"""
import gzip
import hashlib
import importlib.util
import json
from fractions import Fraction as Q
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def raw(relative):
    data = (ROOT/relative).read_bytes()
    return gzip.decompress(data) if str(relative).endswith('.gz') else data


def read(relative):
    return json.loads(raw(relative))


def sha(relative):
    return hashlib.sha256(raw(relative)).hexdigest()


def engine(name):
    spec = importlib.util.spec_from_file_location('evidence_'+name, ROOT/'vendor'/(name+'.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def moment_pair(profile, dimension, live, value):
    first = engine('moment').moment(profile, dimension, live, value, True)
    other = engine('base_two_moment')
    lo, hi = other.moment(dimension, live, list(profile.items()), value)
    fallback = 32*dimension*dimension*sum(profile.values())
    bad_lo, bad_hi = other.moment(dimension, live, [(1, fallback)], value)
    second = lo+bad_lo/10**16, hi+bad_hi/10**16
    assert first[1] < 1 and second[1] < 1
    return [list(map(str, first)), list(map(str, second))]


def supplier_inputs():
    for entry in read('SOURCES.json')['files']:
        data = raw(entry['local_path'])
        assert hashlib.sha256(data).hexdigest() == entry['sha256']
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert blob == entry['git_blob']
    completion = read('inputs/COMPLETION.json')
    assert completion['status'] == 'PASS_RETAINED_DEFAULT_PR433_REPLAY'
    assert completion['returncode'] == 0 and completion['error'] is None
    manifest_hash = sha('inputs/supplier-MANIFEST.json')
    assert completion['source_manifest_before'] == completion['source_manifest_after'] == manifest_hash
    assert read('inputs/LAUNCH.json')['assertions_enabled']
    replay_map = read('inputs/REPLAY-MAP.json')
    assert replay_map['source_manifest_sha256'] == manifest_hash
    for entry in replay_map['files']:
        assert sha(entry['local_path']) == entry['output_sha256']
        assert entry['output_sha256'] == completion['output_hashes'][entry['output_path']]
    prefix = 'inputs/replay/'
    result = read(prefix+'RESULT.json')
    published = read('inputs/pr433-published-certificate.json')
    assert {k: v for k, v in result.items() if k != 'manifest_sha256'} == published
    assert result['manifest_sha256'] == manifest_hash
    assert len(result['verification_steps']) == 13
    for step in result['verification_steps']:
        assert any(e['output_path'] == 'run/'+step+'.log' for e in replay_map['files'])
    g = read(prefix+'bit426-source-centres/global/GLOBAL.json')
    geo_path = prefix+'bit426-source-centres/global/GEOMETRY.json.gz'
    geo = read(geo_path)
    audit = read(prefix+'bit426-source-centres/global/AUDIT.json')
    cx = read(prefix+'split-centres/INTEGRATION.json')
    ca = read(prefix+'split-centres/INDEPENDENT-REPLAY.json')
    scalar_path = prefix+'split-centres/SCALAR-FRAME-AUDIT.json'
    phase_path = prefix+'split-centres/CLIFFORD-REVIEW.json'
    scalar, phase = read(scalar_path), read(phase_path)
    assert cx['scalar_audit_sha256'] == sha(scalar_path)
    assert cx['exact_phase_receipt_sha256'] == sha(phase_path)
    assert cx['canonical_word_sha256'] == scalar['canonical_word_sha256'] == phase['canonical_word_sha256']
    assert phase['all_child_equalities_include_global_phase']
    assert g['geometry_sha256'] == sha(geo_path)
    assert g['template_sha256'] == audit['template_sha256'] == result['bit_template_sha256']
    assert cx['global_template_sha256'] == ca['template_sha256'] == result['complex_template_sha256']
    assert g['status'] == 'PASS_SOURCE_BOUND_NINE_STAGE_BIT_TEMPLATE'
    assert audit['status'] == 'PASS_INDEPENDENT_COMPRESSED_BIT_TEMPLATE_AUDIT'
    assert ca['status'] == 'PASS_INDEPENDENT_NEW_STRUCTURAL_IR_REPLAY'
    assert len(audit['mutations_rejected']) == 8 and len(ca['mutation_controls_rejected']) == 7
    bit, complex_ = Q(result['bit_lower']), Q(result['complex_lower'])
    assert complex_ == Q(cx['complex_b']) == Q(ca['complex_b']) == Q(scalar['prospective_complex_b'])
    price = read(prefix+'BIT-PRICE.json')
    assert bit == Q(price['lower']) and price['source_template_sha256'] == g['template_sha256']
    profile = {int(r): n for r, n in audit['profile'].items()}
    cp = {int(r): n for r, n in ca['paid_profile'].items()}
    assert profile == {int(r): n for r, n in g['profile'].items()}
    assert cp == {int(r): n for r, n in cx['global_profile'].items()}
    assert (g['m'], g['R'], g['live'], g['physical']) == (64, 758, 14502, 14511)
    assert 64*g['live']-sum(r*n for r, n in profile.items()) == 2496
    assert 73*cx['live']-sum(r*n for r, n in cp.items()) == 2496
    assert 2*max(profile)**2 < 64**2 and 2*max(cp)**2 < 73**2
    assert geo['bad_prime_factors'] == [2] and geo['route_denominators'] == [1, 2, 4]
    # Independently express every term of the immutable combined.py invoice.
    paid = sum(profile.values())
    local = 72*g['local_additions']+g['bridge_additions']
    routes = 576*(240+758)+61440+2*g['bank_assignments']+2*g['copy_erase_episodes']
    selectors = 144*((14502-1)+758*64*(geo['max_route_factors']+63+64))
    prefix_bound = int(g['global_prefix_bound'])
    coefficient = (local + routes*(16*4097**2+14511)
                   + paid*(8*64**2+8+128*128**3)+16*64**3
                   + g['copy_erase_episodes']+selectors+prefix_bound+1)
    two = (coefficient+1)**2*(paid+1)**2
    captured = read('inputs/BASELINE-ASSEMBLY-LOCALS.json')
    assert captured['combined_source_sha256'] == sha('vendor/combined433.py')
    assert captured['source_result_sha256'] == sha(prefix+'RESULT.json')
    assert (coefficient, two, routes, selectors, local) == (
        int(captured['coefficient']), int(captured['two_level_coefficient']),
        captured['route_items'], captured['selectors'], captured['unit_additions'])
    assert prefix_bound < 2**256 and two < 2**512
    invoice = dict(prefix_bits=prefix_bound.bit_length(), charged_prefix_bits=256,
                   coefficient_bits=coefficient.bit_length(), two_level_coefficient_bits=two.bit_length(),
                   charged_two_level_coefficient_bits=512, row_coefficient=2*(64**2+1)+9909+252,
                   live=g['live'], physical=g['physical'])
    assert invoice == result['bit_invoice'] and invoice['row_coefficient'] < 20161
    finite = cx['finite_invoice']
    assert finite['router_bits'] < finite['G_exponent'] == 30000
    assert finite['literal_bits'] < finite['E_exponent'] == 100000
    assert finite['required_C0_bits'] < finite['C0_exponent'] == 210000
    assert finite['physical_row_coefficient'] < finite['retained_row_coefficient'] == 20161
    moments = {'bit': moment_pair(profile, 64, g['live'], bit),
               'complex': moment_pair(cp, 73, cx['live'], complex_)}
    return dict(bit=bit, complex=complex_, baseline=Q(result['kappa']),
                profile=profile, live=g['live'], moments=moments,
                coefficient=coefficient, two_level_coefficient=two, invoice=invoice,
                source_manifest_sha256=manifest_hash, published=result)
