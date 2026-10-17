"""Replay three source-closed checks on the identical freshly admitted map."""

import json
import subprocess
import sys

import replay
from swap import need

MANIFEST_HASHES = {
    "exact-score": "d1a87fc9b86ad57196a7eaed64f2aa7a7c35990b346349f7324328445c5b65a2",
    "construction": "1dc7534d29d8ac484cf6762dd36f8d35e7d21b9f3f5cb1d8bea9a74bb76dcacb",
    "invoice": "6b14700be4e593338649f51894c7e734ce4a7318fd4013137b45f5b255f60d75",
}


def authenticate(bundle, expected):
    need(replay.sha(bundle / "MANIFEST.json") == expected, "support manifest changed")
    document = json.loads((bundle / "MANIFEST.json").read_text())
    files = document.get("files", document)
    need(len(files) <= 64, "support inventory budget")
    for name, digest in files.items():
        path = bundle / name
        need(
            path.resolve().is_relative_to(bundle.resolve()) and not path.is_symlink(),
            "support path",
        )
        need(replay.sha(path) == digest, "support source changed: " + name)
    actual = {
        path.relative_to(bundle).as_posix()
        for path in bundle.rglob("*")
        if path.is_file()
    }
    need(actual == set(files) | {"MANIFEST.json"}, "support inventory mismatch")


def command(arguments, work, name):
    argv = [
        sys.executable,
        "-B",
        "-X",
        "pycache_prefix=" + str(work / "bytecode"),
        *map(str, arguments),
    ]
    with (work / (name + ".log")).open("w") as log:
        subprocess.run(
            argv,
            stdout=log,
            stderr=subprocess.STDOUT,
            env=replay.environment(work),
            check=True,
            timeout=60,
        )
    output = (work / (name + ".log")).read_bytes()
    need(len(output) <= 65536, "support stdout budget")
    print(output.decode("utf-8"), end="", flush=True)


def score(package, work):
    bundle = package / "support/exact-score"
    strict = work / "strict"
    output = work / "INDEPENDENT-SCORE.json"
    command(
        [
            bundle / "score.py",
            "--assembly",
            strict / "ASSEMBLY.json",
            "--data",
            work / "source/data",
            "--invoice",
            strict / "global/audit/PREFIX-AND-INVOICE.json",
            "--owners-audit",
            strict / "global/audit/OWNERS-AND-PROFILE.json",
            "--bit-source",
            work / "source/inputs/PR589-EXPECTED.json",
            "--output",
            output,
        ],
        work,
        "score",
    )
    need(
        output.read_bytes() == (bundle / "RESULT.json").read_bytes(),
        "independent score differs",
    )
    command(["-Werror", bundle / "test_score.py"], work, "score-tests")
    command(["-O", "-Werror", bundle / "test_score.py"], work, "score-tests-optimized")
    return output, bundle / "score.py"


def construction(main, package, work):
    bundle = package / "support/construction"
    pins = bundle / "SOURCES-PR3308.json"
    output = work / "INDEPENDENT-ADMISSION.json"
    common = [
        "--repo",
        main,
        "--pins",
        pins,
        "--source",
        work / "source",
        "--data",
        package / "data",
        "--strict",
        work / "strict",
    ]
    command(
        [
            bundle / "check_strict_bundle.py",
            *common,
            "--local",
            work / "local",
            "--output",
            output,
        ],
        work,
        "admission",
    )
    command(
        [
            bundle / "test_strict_bundle.py",
            *common,
            "--scratch",
            work,
            "--output",
            work / "ADMISSION-CONTROLS.json",
        ],
        work,
        "admission-tests",
    )
    actual = json.loads(output.read_text())
    frozen = json.loads((bundle / "ADMISSION.json").read_text())
    for key in (
        "candidate_data",
        "profile",
        "idle",
        "controls",
        "roles",
        "calls",
        "charts",
    ):
        need(actual[key] == frozen[key], "independent construction mismatch: " + key)
    for key in ("assembly", "invoice", "owner", "controller"):
        need(
            actual["artifacts"][key] == frozen["artifacts"][key],
            "construction hash mismatch: " + key,
        )


def invoice(main, package, work, report, scorer):
    bundle = package / "support/invoice"
    output = work / "INDEPENDENT-INVOICE.json"
    command(
        [
            bundle / "review_complete_invoice.py",
            "--main",
            main,
            "--strict",
            work / "strict",
            "--score",
            report,
            "--scorer",
            scorer,
            "--out",
            output,
        ],
        work,
        "invoice-review",
    )
    need(
        output.read_bytes() == (bundle / "RESULT.json").read_bytes(),
        "independent invoice differs",
    )


def run(main, package, work):
    for name, expected in MANIFEST_HASHES.items():
        authenticate(package / "support" / name, expected)
    report, scorer = score(package, work)
    construction(main, package, work)
    invoice(main, package, work, report, scorer)
    print("PASS_THREE_SOURCE_BOUND_INDEPENDENT_GATES", flush=True)
