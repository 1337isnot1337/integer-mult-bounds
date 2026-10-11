"""Audit the separate basis stage on the pinned PR438 reset/kernel word."""
from fractions import Fraction
import copy
import hashlib
import json
from postprocess import reorder_basis
from verify import ROOT, raw, read, digest, forms, restores, gates, prefix, coefficient

P = 'port438/'

def verify_port():
    binding = read(P+'SOURCE-BINDING.json')
    assert binding['commit'] == 'e3b56de7869f6af88d48ac0ab1d7959c4c9e6176'
    supplier = read(P+'supplier/MANIFEST.json')['files']
    assert digest(P+'supplier/MANIFEST.json') == binding['manifest_sha256']
    for name, pin in supplier.items():
        assert binding['files'][name]['sha256'] == pin
    for path in (ROOT/P/'supplier').rglob('*'):
        if path.is_file():
            name = path.relative_to(ROOT/P/'supplier').as_posix()
            data = path.read_bytes()
            assert hashlib.sha256(data).hexdigest() == binding['files'][name]['sha256']
            assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == binding['files'][name]['git_blob']
    completed = read(P+'COMPLETION.json')
    assert completed['status'] == 'PASS_CHANGED_PR438_BIT_FINITE_CHECK'
    assert completed['source_before'] == completed['source_after'] == {k:v['sha256'] for k,v in binding['files'].items()}
    assert completed['inputs_before'] == completed['inputs_after']
    assert digest(P+'adapter/MANIFEST.json') == completed['adapter_manifest_sha256']
    for name, pin in read(P+'adapter/MANIFEST.json')['files'].items():
        assert digest(P+'adapter/'+name) == pin
    assert digest('postprocess.py') == digest(P+'adapter/basis_postprocess.py')
    for name, path in read(P+'RECEIPT-MAP.json').items():
        assert digest(P+'inputs/'+name) == completed['output_hashes'][path]
    assert [s['name'] for s in completed['steps']] == ['bit_construct','bit_reset','bit_kernel','post_basis','export','global','audit','price','combined']
    for step in completed['steps']:
        assert step['returncode'] == 0
        assert digest(P+'logs/'+step['name']+'.log') == step['log_sha256'] == completed['output_hashes'][step['name']+'.log']
    reset = json.loads(raw(P+'logs/bit_reset.log'))
    kernel = read(P+'inputs/KERNEL.json')
    selection = read(P+'supplier/stages/kernel-selection.json')
    stage = read(P+'inputs/BASIS-STAGE.json')
    assert reset['R'] == 747 and reset['helpers_removed'] == 11 and len(reset['controls']) == 3
    assert reset['sha256'] == kernel['input_sha256'] == selection['input_sha256']
    assert kernel['output_sha256'] == selection['output_sha256'] == stage['input_sha256'] == digest(P+'inputs/original-word.json.gz')
    assert stage['output_sha256'] == digest(P+'inputs/word.json.gz')
    assert kernel['entries'] == len(selection['entries']) == 118
    assert kernel['total_entrance_rank'] == 160 and kernel['donor_slots'] == 119
    assert kernel['new_frames'] == 0 and kernel['columns'] == stage['columns'] == 987
    assert kernel['local_histogram'] == stage['profile']
    old, word = read(P+'inputs/original-word.json.gz'), read(P+'inputs/word.json.gz')
    assert reorder_basis(old) == word and reorder_basis(word) == word
    a, b = old['source_basis_gates'], word['source_basis_gates']
    assert (a, b) == (559,575)
    assert set(old) == set(word)
    for key in set(word)-{'A','B','ret','source_basis_gates'}:
        assert old[key] == word[key], key
    assert old['A'][:-a] == word['A'][:-b] and old['B'][a:] == word['B'][b:]
    assert word['A'][-b:] == list(reversed(word['B'][:b])) and forms(old) == forms(word)
    for item in [old, word]:
        assert restores(item) and restores(item, reverse=True)
    assert not restores(word, omit_inverse=True) and not restores(word, omit_dirt=True)
    g, audit = read(P+'inputs/GLOBAL.json'), read(P+'inputs/AUDIT.json')
    result = read(P+'inputs/RESULT.json')
    assert g['status'] == 'PASS_SOURCE_BOUND_NINE_STAGE_BIT_TEMPLATE'
    assert audit['status'] == 'PASS_INDEPENDENT_COMPRESSED_BIT_TEMPLATE_AUDIT'
    assert g['word_sha256'] == stage['output_sha256']
    assert g['template_sha256'] == audit['template_sha256'] == result['bit_template_sha256']
    assert g['geometry_sha256'] == digest(P+'inputs/GEOMETRY.json.gz')
    assert (g['m'],g['R'],g['live'],g['physical'],g['banks_per_stage']) == (64,747,14223,14232,727)
    assert g['all_scalar_columns_restored'] and g['independent_unbanked_scalar_columns'] == 7683
    assert len(g['omitted_bridge_shears_rejected']) == 18 and len(audit['mutations_rejected']) == 8
    assert g['profile'] == audit['profile']
    assert g['paid_calls'] == sum(g['profile'].values()) == 328536
    assert sum(int(r)*n for r,n in g['profile'].items()) == 64*g['live']-2496
    before = [prefix(old, r) for r in [False,True]]
    after = [prefix(word, r) for r in [False,True]]
    assert before == [4749873,18976454] and after == [352915,1686810]
    for reverse, factor in zip(['forward','reverse'],after):
        local=g['local_checks'][reverse]
        assert local['cancellation_free_row_l1'] == factor and local['all_columns'] == 987
        assert local['profile'] == stage['profile'] and local['adds'] == g['local_additions']
    assert int(g['global_prefix_bound']) == 2**18*after[0]**5*after[1]**4
    assert len(gates(word)) == g['local_additions'] == 14757
    assert len(gates(old)) == 14725
    geo = read(P+'inputs/GEOMETRY.json.gz')
    value,two = coefficient(g,geo)
    # Same geometry and schedule; recompute the baseline's two changed terms.
    # This algebraic counterfactual is not a second baseline global replay.
    baseline = copy.deepcopy(g)
    baseline['local_additions'] = len(gates(old))
    baseline['global_prefix_bound'] = str(2**18*before[0]**5*before[1]**4)
    old_value,old_two = coefficient(baseline,geo)
    nomination=read(P+'inputs/FINITE-COMPARISON.json')
    assert value == int(nomination['candidate_coefficient']) < old_value == int(nomination['source_projected_coefficient'])
    assert (old_value.bit_length(),value.bit_length(),old_two.bit_length(),two.bit_length()) == (226,193,488,423)
    assert two < 2**512 and value < 2**256
    expected = read(P+'supplier/EXPECTED.json')
    for key in set(expected)-{'bit_invoice','bit_template_sha256'}:
        assert result[key] == expected[key],key
    assert result['kappa'] == '45340333148791/40000000000000000'
    assert len(result['strict_outer_constraints']) == 47 and all(Fraction(x)>0 for x in result['strict_outer_constraints'].values())
    assert len(result['outer_controls']) == 4
    assert result['bit_invoice']['coefficient_bits'] == value.bit_length()
    assert result['bit_invoice']['two_level_coefficient_bits'] == two.bit_length()
    reuse = read(P+'COMPLEX-REUSE-BINDING.json')
    old_completed = read('inputs/baseline/COMPLETION.json')
    old_supplier = read('inputs/SUPPLIER-MANIFEST.json')['files']
    assert reuse['completion_sha256'] == digest('inputs/baseline/COMPLETION.json') == completed['inputs_before']['completion']
    assert digest(P+'COMPLEX-REUSE-BINDING.json') == completed['inputs_before']['reuse_binding']
    for name,pin in reuse['verified_outputs'].items():
        assert pin == old_completed['output_hashes'][name] == completed['inputs_before'][name]
        assert pin == completed['output_hashes'][name.removeprefix('run/')]
    assert set(reuse['changed_files']) == {'code/complex_phases.py','inputs/complex-phase-receipt.json'}
    for name, entry in reuse['scientific_source_comparison'].items():
        assert supplier[name] == entry['sha256']
        assert entry['identical_433'] == (old_supplier[name] == supplier[name])
    phase=read(P+'supplier/inputs/complex-phase-receipt.json')
    assert phase['canonical_word_sha256'] == reuse['verified_outputs']['run/split-centres/CANONICAL-WORD.json.gz']
    assert phase['recipe_sha256'] == reuse['verified_outputs']['run/split-centres/CLIFFORD-RECIPES.json']
    for name in ['INTEGRATION.json','INDEPENDENT-REPLAY.json']:
        assert digest('inputs/complex/'+name) == reuse['verified_outputs']['run/split-centres/'+name]
    assert read('inputs/complex/INTEGRATION.json')['global_template_sha256'] == result['complex_template_sha256']
    return dict(status='PASS_POST_KERNEL_BASIS_TRANSFER',candidate_sha256=stage['output_sha256'],
                coefficient=str(value),two_level_coefficient=str(two),coefficient_bits=[226,193],
                two_level_bits=[488,423],local_add_delta=32,kappa=result['kappa'],
                scope='Pinned PR438 finite accounting; baseline reconstructed algebraically; completed PR433 complex evidence reused.')
