"""Behavior and source-boundary controls, including optimized Python. Apache-2.0."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from common import HERE, INPUTS, ROOT, authenticate, same
from verify import arithmetic


class Controls(unittest.TestCase):
    def test_strict_boundary(self):
        self.assertEqual(arithmetic(35)["D6_82"], {"required": 47, "upper": 46})
        with self.assertRaisesRegex(ValueError, "strict E6 gap"):
            arithmetic(36)

    def test_types(self):
        for cut in (True, 35.0, "35", -1, 37):
            with self.subTest(cut=cut), self.assertRaises(ValueError):
                arithmetic(cut)
        with self.assertRaises(ValueError):
            same({"cut": True}, {"cut": 1})

    def test_source_usage(self):
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary)
            manifest = json.loads((HERE / "SOURCES.json").read_bytes())
            next(row for row in manifest["files"] if row["usage"] == "input")[
                "usage"
            ] = "context"
            (package / "SOURCES.json").write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, "complete input inventory"):
                authenticate(package=package)

    def test_actual_corrupted_cli(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / "research" / HERE.name
            shutil.copytree(HERE, package, ignore=shutil.ignore_patterns("__pycache__"))
            for relative in INPUTS:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / relative).read_bytes())
            for relative in INPUTS:
                target = root / relative
                original = target.read_bytes()
                target.write_bytes(original + b"\n# corrupted source control\n")
                completed = subprocess.run(
                    [
                        sys.executable,
                        "-O",
                        "-W",
                        "error",
                        "-B",
                        str(package / "verify.py"),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                )
                self.assertNotEqual(completed.returncode, 0)
                self.assertIn("source SHA256", completed.stderr)
                self.assertNotIn("PASS_CONDITIONAL", completed.stdout)
                target.write_bytes(original)

    def test_actual_incomplete_or_false_receipt(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / "research" / HERE.name
            shutil.copytree(HERE, package, ignore=shutil.ignore_patterns("__pycache__"))
            for relative in INPUTS:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / relative).read_bytes())
            original = json.loads((HERE / "RESULT.json").read_bytes())
            for mutant in ("omit84", "false44", "wrongtype"):
                receipt = json.loads(json.dumps(original))
                if mutant == "omit84":
                    del receipt["arithmetic"]["D6_84"]
                elif mutant == "false44":
                    receipt["near_axis"]["maximum_coverage"] = 44
                else:
                    receipt["ordered_axis_orbit"] = "7560"
                (package / "RESULT.json").write_text(json.dumps(receipt))
                completed = subprocess.run(
                    [
                        sys.executable,
                        "-O",
                        "-W",
                        "error",
                        "-B",
                        str(package / "verify.py"),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                )
                self.assertNotEqual(completed.returncode, 0)
                self.assertIn("exact result receipt", completed.stderr)
                self.assertNotIn("PASS_CONDITIONAL", completed.stdout)


if __name__ == "__main__":
    unittest.main()
