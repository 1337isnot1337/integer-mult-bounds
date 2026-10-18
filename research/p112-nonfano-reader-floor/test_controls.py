"""Optimized CLI corruption and restoration checks. Nick Petalas. Apache-2.0."""

import json
import os
import runpy
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
INPUT = "research/adaptive-kernel-demotion/inputs/DATA-PHASES.json"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def invoke(root, program, expected=None):
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-O",
            "-Werror",
            "-B",
            str(root / "research" / HERE.name / program),
        ],
        capture_output=True,
        text=True,
        timeout=90,
        cwd=root,
    )
    if expected is None:
        need(result.returncode == 0, "positive CLI: " + result.stdout + result.stderr)
    else:
        need(
            result.returncode != 0 and expected in result.stderr,
            "specific CLI rejection: " + result.stdout + result.stderr,
        )
    return result.returncode


def edit_json(path, change):
    original = path.read_bytes()
    try:
        data = json.loads(original)
        change(data)
        path.write_text(json.dumps(data) + "\n")
        return original
    except BaseException:
        path.write_bytes(original)
        raise


def faults(root):
    package = root / "research" / HERE.name
    specifications = [
        (
            "FIXTURES.json",
            lambda d: d[0]["q"][0].__setitem__("111", "1e1000000000"),
            "independent.py",
            "bounded rational literal",
        ),
        (
            "TEMPLATES.json",
            lambda d: d["points"][0].__setitem__(3, [1, 1, 0]),
            "verify.py",
            "reader-span request",
        ),
        (
            "TEMPLATES.json",
            lambda d: d.__setitem__("polynomial", 19),
            "verify.py",
            "GF4 polynomial",
        ),
        (
            "FIXTURES.json",
            lambda d: d[0]["q"][0].__setitem__("111", "2"),
            "independent.py",
            "independent rational operator",
        ),
        (
            "FIXTURES.json",
            lambda d: d[0]["new_q"][0].__setitem__("109", "1"),
            "independent.py",
            "independent query support",
        ),
        (
            "RESULT.json",
            lambda d: d["fixture_bills"][0][2].__setitem__(0, -1),
            "independent.py",
            "independent actual tariffs",
        ),
    ]
    exits = []
    for name, change, program, diagnostic in specifications:
        path = package / name
        original = edit_json(path, change)
        try:
            exits.append(invoke(root, program, diagnostic))
        finally:
            path.write_bytes(original)
    path = root / INPUT
    original = path.read_bytes()
    try:
        path.write_bytes(original + b" ")
        exits.append(invoke(root, "verify.py", "source SHA256"))
    finally:
        path.write_bytes(original)
    return exits


def local_controls():
    # run_path is confined to this authenticated package's single local module.
    module = runpy.run_path(str(HERE / "verify.py"))
    solve, rank, mul = module["solve"], module["rank"], module["mul"]
    need(solve([[2]], [1], 1) == [module["F"](1, 2)], "rational halves")
    need(solve([[0]], [1], 1) is None, "inconsistent rational request")
    need(solve([], [], 3, True) == [0, 0, 0], "empty GF4 request")
    need(all(mul(x, mul(x, x)) == 1 for x in range(1, 4)), "GF4 inverses")
    for rows, width, binary, expected in [
        ([[4]], 1, True, "GF4 value"),
        ([[1, 2]], 1, False, "linear shape"),
        ([], 7, False, "linear capacity"),
    ]:
        try:
            rank(rows, width, binary)
        except ValueError as error:
            need(expected in str(error), "specific boundary error")
        else:
            raise ValueError("invalid boundary accepted")
    return 7


def main():
    controls = local_controls()
    files = list(HERE.iterdir())
    need(
        len(files) <= 32
        and all(
            p.is_file() and not p.is_symlink() and p.stat().st_size <= 1_048_576
            for p in files
        ),
        "regular bounded package files",
    )
    # All disposable copies and subprocess caches live under the caller's TMPDIR.
    with tempfile.TemporaryDirectory(
        prefix="nonfano-controls-", dir=os.environ.get("TMPDIR")
    ) as tmp:
        root = Path(tmp)
        destination = root / "research" / HERE.name
        destination.parent.mkdir()
        shutil.copytree(HERE, destination, symlinks=True)
        source = root / INPUT
        source.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / INPUT, source)
        invoke(root, "verify.py")
        invoke(root, "independent.py")
        exits = faults(root)
        invoke(root, "verify.py")
        invoke(root, "independent.py")
    print(
        "PASS_NONFANO_CONTROLS",
        json.dumps(
            {"local_controls": controls, "CLI_rejections": exits, "restored": True}
        ),
    )


if __name__ == "__main__":
    main()
