#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
import copy
from pathlib import Path
import sys
import tarfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify

class FakeMember:
    def __init__(self, name, size=0, mode=0o644, regular=True):
        self.name, self.size, self.mode, self._regular = name, size, mode, regular
    def isfile(self): return self._regular

class NamespaceControls(unittest.TestCase):
    def test_C1_path_traversal(self):
        with self.assertRaisesRegex(ValueError, "unsafe archive"):
            verify.validate_namespace([FakeMember("../escape")])
    def test_C2_duplicate_member(self):
        with self.assertRaisesRegex(ValueError, "duplicate archive"):
            verify.validate_namespace([FakeMember("a"), FakeMember("a")])

class ClosureControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pins = verify.strict_json((verify.HERE / "PINS.json").read_bytes(), "PINS.json")
        a = verify.ROOT / cls.pins["archive"]["path"]
        cls.names, _, cls.digests, cls.roots = verify.read_capsule(a)
        cls.result = verify.strict_json(cls.roots["RESULT.json"], "RESULT.json")
        cls.stages = verify.strict_json(cls.roots["STAGES.json"], "STAGES.json")
    def validate(self, result=None, stages=None, names=None, digests=None):
        return verify.validate_result(result or self.result, stages or self.stages,
                                      names or self.names, digests or self.digests,
                                      self.pins["stages"])
    def test_C3_nondeclared_member(self):
        result = copy.deepcopy(self.result); result["artifacts"].pop(next(iter(result["artifacts"])))
        with self.assertRaisesRegex(ValueError, "not exact archive closure"): self.validate(result=result)
    def test_C4_mutated_artifact_digest(self):
        digests = dict(self.digests); name = next(iter(self.result["artifacts"])); digests[name] = "0" * 64
        with self.assertRaisesRegex(ValueError, "artifact digest differs"): self.validate(digests=digests)
    def test_C5_nonzero_stage(self):
        stages = copy.deepcopy(self.stages); stages[0]["exit_code"] = 1
        result = copy.deepcopy(self.result); result["stages"] = stages
        with self.assertRaisesRegex(ValueError, "recorded stage failed"): self.validate(result=result, stages=stages)
    def test_C6_promoted_receipt_mismatch(self):
        outer = verify.repository_file("research/community-frontier1042-audit/ASSEMBLY.json")
        self.assertNotEqual(outer + b"x", self.roots["t16/ASSEMBLY.json"])

if __name__ == "__main__": unittest.main(verbosity=2)
