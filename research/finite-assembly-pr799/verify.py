"""Offline supplied-cap sibling verifier; no supplier reconstruction.
George Lydakis, with OpenAI Codex assistance. Apache-2.0.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import sys
import tarfile
from fractions import Fraction

HERE = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_bytes())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def write(path, value):
    temporary = path.with_name(path.name + '.partial')
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    os.replace(temporary, path)


def load(name, path):
    require(name not in sys.modules, 'Already imported: ' + name)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def bound_files(root, entries):
    for name, entry in entries.items():
        parts = PurePosixPath(name)
        require(not parts.is_absolute() and '..' not in parts.parts, 'Unsafe source name')
        path = root.joinpath(*parts.parts)
        require(path.resolve().is_relative_to(root.resolve()), 'Source outside snapshot')
        require(path.is_file() and not path.is_symlink(), 'Missing ordinary file: ' + name)
        require(path.stat().st_size == entry['bytes'] and digest(path) == entry['sha256'],
                'Source binding: ' + name)
        if 'git_blob' in entry:
            data = path.read_bytes()
            blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            require(blob == entry['git_blob'], 'Git binding: ' + name)


def unpack(path, entries, destination):
    destination.mkdir()
    seen = set()
    total = 0
    maximum = sum(entry['bytes'] for entry in entries.values())
    with tarfile.open(path, 'r:gz') as archive:
        for member in archive:
            parts = PurePosixPath(member.name)
            require(not parts.is_absolute() and '..' not in parts.parts, 'Unsafe archive name')
            if member.isdir():
                continue
            require(member.isfile() and member.name in entries and member.name not in seen,
                    'Unexpected, duplicate or special member')
            seen.add(member.name)
            entry = entries[member.name]
            require(member.size == entry['bytes'], 'Archive size')
            total += member.size
            require(total <= maximum, 'Archive total')
            output = destination.joinpath(*parts.parts)
            output.parent.mkdir(parents=True, exist_ok=True)
            with archive.extractfile(member) as source, output.open('xb') as target:
                remaining = member.size
                while remaining:
                    chunk = source.read(min(1048576, remaining))
                    require(bool(chunk), 'Short archive member')
                    target.write(chunk)
                    remaining -= len(chunk)
                require(not source.read(1), 'Long archive member')
            require(digest(output) == entry['sha256'], 'Archive member hash')
    require(seen == set(entries) and total == maximum, 'Incomplete archive')


def check_sibling():
    for name, expected in read(HERE / 'MANIFEST.json')['files'].items():
        require(Path(name).name == name and digest(HERE / name) == expected,
                'Sibling source manifest')


def verify(upstream, core, output, journal):
    check_sibling()
    spec = read(HERE / 'UPSTREAM.json')
    bound_files(upstream, spec['files'])
    bound_files(core, spec['core_files'])
    journal['active_stage'] = 'extract'; write(output / 'JOURNAL.json', journal)
    unpack(upstream / spec['ancestor_archive'], spec['ancestor_members'], output / 'ancestor')
    unpack(upstream / spec['current_archive'], spec['current_members'], output / 'current')
    package = upstream / 'research/gauge44-frames-x'
    sys.path[:0] = [str(upstream / 'scripts'), str(package / 'code')]
    ancestry = load('verify_frontier741_bindings', upstream / 'scripts/verify_frontier741_bindings.py')
    ancestry.ROOT = upstream
    ancestry.PACKAGE = upstream / 'research/complex-sw4-frame8'
    checker = load('verify_frontier799_bindings', upstream / 'scripts/verify_frontier799_bindings.py')
    checker.ROOT = upstream
    checker.PACKAGE = package
    current = output / 'current'
    journal['active_stage'] = 'reuse-admission'; write(output / 'JOURNAL.json', journal)
    binding = checker.check(output / 'ancestor', current / 'native', current / 'global',
                            current / 'INDEPENDENT-LOCAL.json', current / 'INDEPENDENT-PRICE.json')
    expected_binding = read(upstream / 'research/community-frontier799-audit/RESULT.json')
    require(binding == {k: v for k, v in expected_binding.items() if k != 'reused_ancestry'},
            'Current composition binding')
    write(output / 'BINDING.json', binding)
    engine_source = output / 'engine-source'
    (engine_source / 'engines').mkdir(parents=True)
    for name in ('moment.py', 'base_two_moment.py', 'outer.py'):
        (engine_source / 'engines' / name).write_bytes((core / 'vendor' / name).read_bytes())
    for key in ('WITNESS_DISCOVER', 'WITNESS_RECORD', 'PYTHONOPTIMIZE'):
        os.environ.pop(key, None)
    os.environ['WITNESS_SPEC'] = str(package / 'data/SPEC.json')
    os.environ['GAIN_PR564_SOURCE'] = str(engine_source)
    witness = load('witness', package / 'code/witness.py')
    require(not witness.DISCOVER, 'Strict witness required')
    admission = load('pinned_pr799_admission', package / 'code/assemble.py')
    require(admission.P == engine_source.resolve() and
            admission.BIT_PATH.resolve() == (package / 'inputs/PR589-EXPECTED.json').resolve(),
            'Constrained admission sources')
    owner_path = current / 'global/global/audit/OWNERS-AND-PROFILE.json'
    invoice_path = current / 'global/global/audit/PREFIX-AND-INVOICE.json'
    owner, invoice = read(owner_path), read(invoice_path)
    require(owner['template_sha256'] == read(current / 'global/global/hosted/HOSTED.json')['template_sha256'],
            'Hosted template')
    journal['active_stage'] = 'baseline'; write(output / 'JOURNAL.json', journal)
    baseline = json.loads(json.dumps(admission.assemble(owner, invoice, digest(owner_path), digest(invoice_path))))
    require(baseline == read(current / 'global/ASSEMBLY.json') ==
            read(upstream / 'research/community-frontier799-audit/ASSEMBLY.json'), 'Full current baseline')
    write(output / 'BASELINE.json', baseline)
    assembly = load('finite_assembly_application', core / 'assembly.py')
    bit = read(package / 'inputs/PR589-EXPECTED.json')
    b, c = Fraction(baseline['complex_lower']), Fraction(baseline['bit_lower'])
    grid = Fraction(1, 10**27)
    target = assembly.greatest_grid_target(c, b, grid)
    result = assembly.construct(c, b, target, coefficient_bits=512)
    require(target > Fraction(baseline['kappa']) and target < result['supremum'] <= target + grid,
            'Strict target comparison')
    write(output / 'ASSEMBLY.json', assembly.jsonable(result))
    journal['active_stage'] = 'seed-checks'; write(output / 'JOURNAL.json', journal)
    intervals = []
    for side, profile, dimension, live, bad in [
        ('complex', {int(k): v for k, v in owner['paid_profile'].items()}, 73, owner['live'], False),
        ('bit', {int(k): v for k, v in bit['nine']['profile'].items()}, 64, bit['nine']['bit']['live'], True),
    ]:
        seed = result['seed']
        lower, upper = admission.M.moment(profile, dimension, live, seed, bad)
        lo, hi = admission.B.moment(dimension, live, list(profile.items()), seed)
        if bad:
            fallback = 32 * dimension**2 * sum(profile.values())
            fl, fu = admission.B.moment(dimension, live, [(1, fallback)], seed)
            lo += fl / 10**16
            hi += fu / 10**16
        require(upper < 1 and hi < 1, 'Seed moment admission')
        intervals.append({'side': side, 'surcharge': bad, 'seed': str(seed), 'mercator': [str(lower), str(upper)],
                          'base_two': [str(lo), str(hi)]})
        write(output / 'SEED-MOMENTS.json', intervals)
    for cutoff in result['cutoffs']:
        require(cutoff['cutoff_log2'] * cutoff['gap']**2 >= 36 and
                cutoff['cutoff_log2'] * cutoff['gap'] >= 2 * (4 + 512), 'Finite cutoff')
    require(len(result['strict_constraints']) == 47 and
            all(margin > 0 for margin in result['strict_constraints'].values()), 'Outer margins')
    controls = []
    def reject(name, operation):
        try:
            operation()
        except (AssertionError, ValueError):
            controls.append(name)
            write(output / 'CONTROLS.json', controls)
        else:
            raise ValueError('Accepted control: ' + name)
    reject('ceiling_endpoint', lambda: assembly.construct(c, b, assembly.ceiling(c, b)))
    reject('next_grid', lambda: assembly.construct(c, b, target + grid))
    outer = assembly.load_outer()
    value = result['bootstrap_chain'][-1]
    reject('zero_eta', lambda: outer.assembly(value, b, assembly.BRIDGE, target,
                                             eta=Fraction(0), beta=result['beta']))
    reject('zero_beta', lambda: outer.assembly(value, b, assembly.BRIDGE, target,
                                              eta=result['eta'], beta=Fraction(0)))
    reject('unit_beta', lambda: outer.assembly(value, b, assembly.BRIDGE, target,
                                              eta=result['eta'], beta=Fraction(1)))
    expected = read(HERE / 'EXPECTED.json')
    require(assembly.jsonable(result) == expected['assembly'] and
            intervals == expected['seed_moments'] and controls == expected['controls'],
            'Whole admitted target payload')
    require(str(target) == expected['target'] and baseline['kappa'] == expected['baseline'] and
            str(target - Fraction(baseline['kappa'])) == expected['difference'] and
            len(result['bootstrap_chain']) - 1 == expected['levels'], 'Admitted target comparison')
    bound_files(upstream, spec['files'])
    bound_files(core, spec['core_files'])
    check_sibling()
    write(output / 'RESULT.json', {'status': 'PASS_CONDITIONAL_PR799_FINITE_APPLICATION',
          'target': str(target), 'baseline': baseline['kappa'],
          'difference': str(target - Fraction(baseline['kappa'])),
          'levels': len(result['bootstrap_chain']) - 1, 'controls': controls,
          'scope': 'Physical evidence and bit coefficient bound reused; all-size assumptions retained. '
                   'Reusable theorem application, not substantive frontier gain.'})


def main():
    require(__debug__, 'Assertions required')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upstream', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--core', type=Path, default=HERE.parent / 'finite-assembly-frontier')
    args = parser.parse_args()
    upstream, core, output = args.upstream.resolve(), args.core.resolve(), args.output.resolve()
    require(not output.exists() and not output.is_relative_to(upstream) and
            not output.is_relative_to(core) and not output.is_relative_to(HERE), 'Fresh external output')
    output.mkdir()
    journal = {'status': 'ACTIVE', 'active_stage': 'preflight'}
    write(output / 'JOURNAL.json', journal)
    try:
        verify(upstream, core, output, journal)
        journal['status'] = 'PASS'; write(output / 'JOURNAL.json', journal)
        artifacts = {p.name: digest(p) for p in output.iterdir() if p.is_file()}
        write(output / 'COMPLETION.json', {'status': 'PASS_CONDITIONAL_PR799_FINITE_APPLICATION',
                                          'artifacts': artifacts})
    except BaseException as error:
        journal.update(status='FAIL_RETAINED',first_failure=repr(error))
        try:
            write(output / 'JOURNAL.json', journal)
        except BaseException as retention:
            try:
                print('PRIMARY_FAILURE', repr(error), 'RETENTION_FAILURE', repr(retention), flush=True)
            except BaseException:
                pass
        raise


if __name__ == '__main__':
    main()
