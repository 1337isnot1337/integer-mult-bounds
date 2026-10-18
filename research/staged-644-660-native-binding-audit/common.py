# SPDX-License-Identifier: Apache-2.0
"""Bounded source loading for the staged 644/660 native-binding audit.

Adapted from research/rank7-group-d-native-widths-audit/common.py (Wentao Li).
"""

import gzip
import hashlib
import io
import json
import sys
import types
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]
LOCAL = "research/staged-644-660-native-binding-audit/inputs/"
SNAPSHOT = "research/staged-644-660-width-reduction/"
PR3605 = "3efbb5de06a49ffeea6684482f2d3fe48cdca3fb"
PARENT = "research/rank7-coupled-586-588-carrier-fold/edits/"
ENGINE = "research/t74-native-fast/vendor/native/new/code/borrow/"
COMPILER = ENGINE + "vendor/clifford/clifford_exact.py"
KERNEL = "research/frontier1094-recipes-exact-seed76/clifford.py"
PROVIDERS = ("base", "extra")
HELPERS = (644, 660)
FULL = [256, 128, 64, 32, 16, 8, 4, 2, 1]
ENTRANCE = [429, 30]
PARENT_ENTRANCE = [30]
# Same dimension as ENTRANCE and in reduced echelon form; it contains 429 but not 30.
WRONG_ENTRANCE = [429, 18]
# The contained line 429 (dimension one, so a different native width).
CONTAINED_LINE = [429]
LIMIT = 64 * 1024 * 1024


def require(ok, message):
    if not ok:
        raise ValueError(message)


def unique(pairs):
    result = dict(pairs)
    require(len(result) == len(pairs), "duplicate JSON key")
    return result


def decode(raw, compressed=False):
    if compressed:
        with gzip.GzipFile(fileobj=io.BytesIO(raw)) as stream:
            raw = stream.read(LIMIT + 1)
    require(len(raw) <= LIMIT, "decoded input capacity")
    return json.loads(raw, object_pairs_hook=unique)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def authenticate(root=ROOT):
    rows = decode((PACKAGE / "SOURCES.json").read_bytes())["files"]
    pins = {r["path"]: r["sha256"] for r in rows if r["usage"] == "input"}
    declared = set(decode((PACKAGE / "VERIFY.json").read_bytes())["inputs"])
    require(set(pins) == declared and len(pins) <= 16, "exact live input inventory")
    # Package-local copies of PR3605's words: their bytes must equal the
    # provenance rows pinned at PR3605's head under the original path.
    for tag in PROVIDERS:
        origin = SNAPSHOT + f"STAGED644-660-{tag}.json.gz"
        row = [r for r in rows if r["path"] == origin]
        require(len(row) == 1 and row[0]["usage"] == "provenance" and
                row[0].get("pin") == f"head:{PR3605}:{origin}", "snapshot provenance pin")
        pins[staged_name(tag)] = row[0]["sha256"]
    blobs = {}
    for name, sha in pins.items():
        path = root / name
        require(path.stat().st_size <= LIMIT, "raw input capacity")
        raw = path.read_bytes()
        require(digest(raw) == sha, "source SHA256: " + name)
        blobs[name] = raw
    return blobs


def staged_name(tag):
    return LOCAL + f"STAGED644-660-{tag}.json.gz"


def parent_name(tag):
    return PARENT + f"FINAL-WORD-{tag}.json.gz"


def module(raw, name):
    """Compile authenticated bytes directly, without consulting a .pyc file."""
    result = types.ModuleType(name)
    sys.modules[name] = result
    exec(compile(raw, name, "exec"), result.__dict__)
    return result


def reject(action, reason):
    try:
        action()
    except (ValueError, AssertionError) as error:
        return str(error)
    raise ValueError("control accepted: " + reason)
