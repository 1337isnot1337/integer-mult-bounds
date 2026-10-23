"""Authenticate the compact source and reuse its identical physical interfaces.

JoyboyBrian, substantial OpenAI Codex assistance. Apache-2.0.
Predecessors: ai-nanachi/Ross Richardson compact provider; Jose Manuel physical
caller/codec; David Arias logical caller. No predecessor bytes are changed.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMPACT = ROOT / 'research/bit-compact-carrier-retirement/provider'
PHYSICAL = ROOT / 'research/selected-bit-physical-caller'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    exec(compile(path.read_bytes(), str(path), 'exec', dont_inherit=True, optimize=0), result.__dict__)
    return result


def authenticate():
    rows = json.loads((HERE / 'SOURCES.json').read_text())['files']
    inputs = [row for row in rows if row['usage'] == 'input']
    for row in inputs:
        path = ROOT / row['path']
        need(path.is_file() and not path.is_symlink(), 'regular source ' + row['path'])
        need(digest(path.read_bytes()) == row['sha256'], 'source hash ' + row['path'])
    return len(inputs)


def build():
    """Fresh-process binding; preserve both source authenticators and guards.

    CALLER is also ScratchPool's module-location selector, not only an input
    archive path. Rebind it only after the complete 84-file byte equality and
    the retained physical authenticator succeed. The source bytecode, globals,
    defaults, and allocation sites then receive the SAME existing pool lowering.
    """
    inputs = authenticate()
    caller = module('compact_target114', COMPACT / 'caller.py')
    catalogue, frozen, provenance = caller.build_provider(3)
    equality = []
    for local, (_path, raw, pin) in sorted(frozen.sources.items()):
        target = PHYSICAL / 'inputs/pr2753' / local
        need(target.read_bytes() == raw and digest(raw) == pin, 'identical logical interface ' + local)
        equality.append([local, pin])
    need(len(equality) == 84, 'complete unchanged logical interface')
    sys.path.insert(0, str(PHYSICAL))
    legacy = module('loader', PHYSICAL / 'loader.py')
    with TemporaryDirectory(prefix='target114-source-projection-') as temporary:
        projection = Path(temporary)
        for row in json.loads((legacy.CALLER / 'SOURCES.json').read_text())['files']:
            if row['usage'] != 'input':
                continue
            target = projection / row['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            source = (ROOT / 'research/r437-prefix-consumer-fusion/retained/selected-result.json'
                      if row['path'] == 'certificates/selected-result.json' else ROOT / row['path'])
            shutil.copyfile(source, target)
        legacy.REPOSITORY = projection
        legacy.compatibility_controls()
        legacy.activate()
    historical_caller = legacy.CALLER
    legacy.CALLER = COMPACT / 'inputs/caller'
    # No imported logical module may escape the exact source-to-pool binding.
    for name, pin in frozen.loaded.items():
        need(digest(Path(sys.modules[name].__file__).read_bytes()) == pin,
             'loaded logical module binding ' + name)
    return caller, catalogue, legacy, historical_caller, dict(
        input_files=inputs, identical_logical_files=len(equality),
        interface_sha256=digest(json.dumps(equality, separators=(',', ':')).encode()),
        source_provenance=provenance)
