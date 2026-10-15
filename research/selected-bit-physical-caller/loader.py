"""Load the immutable logical caller and bank codec into one module namespace."""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[1]
CALLER = HERE / "inputs/pr2753"
PARKING = HERE / "inputs/pr2769"
_active = False


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


def authenticate():
    entries = json.loads((HERE / "SNAPSHOTS.json").read_text())["files"]
    expected = set()
    for entry in entries:
        path = entry["path"]
        if path in expected or not path.startswith("inputs/"):
            raise ValueError("unique frozen input inventory")
        expected.add(path)
        if sha256((HERE / path).read_bytes()).hexdigest() != entry["sha256"]:
            raise ValueError("frozen source changed: " + path)
    observed = {path.relative_to(HERE).as_posix() for path in (HERE / "inputs").rglob("*")
                if path.is_file() and "__pycache__" not in path.parts}
    if expected != observed:
        raise ValueError("complete frozen input inventory")
    source_verifier = module("frozen_caller_verifier", CALLER / "verify.py")
    source_verifier.authenticate(here=CALLER, root=REPOSITORY)


def activate():
    global _active
    if _active:
        return sys.modules["bank_codec"]
    authenticate()
    module("bootstrap", CALLER / "bootstrap.py")
    import sources
    sources.ROOT = REPOSITORY
    sys.path.insert(0, str(HERE))
    sys.path.append(str(PARKING / "vendor"))
    import words
    if sha256(Path(words.__file__).read_bytes()).digest() != sha256((PARKING / "vendor/words.py").read_bytes()).digest():
        raise ValueError("logical caller and codec use one unchanged Word interface")
    codec = module("bank_codec", PARKING / "codec.py")
    _active = True
    return codec
