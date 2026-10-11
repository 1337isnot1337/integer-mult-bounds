"""Behavioral contracts for the guarded source-basis postprocessor."""
import copy
import gzip
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('postprocess', ROOT/'postprocess.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def read(path):
    data = path.read_bytes()
    return json.loads(gzip.decompress(data) if path.suffix == '.gz' else data)


class PostprocessTests(unittest.TestCase):
    def test_reconstructs_both_selected_words_without_mutation(self):
        for before, after in [
            ('inputs/baseline/word.json.gz', 'inputs/candidate/word.json.gz'),
            ('port438/inputs/original-word.json.gz', 'port438/inputs/word.json.gz'),
        ]:
            with self.subTest(source=before):
                source = read(ROOT/before)
                snapshot = copy.deepcopy(source)
                candidate = module.reorder_basis(source)
                self.assertEqual(candidate, read(ROOT/after))
                self.assertEqual(source, snapshot)
                self.assertEqual(module.reorder_basis(candidate), candidate)

    def test_rejects_unsafe_basis_interfaces(self):
        word = read(ROOT/'inputs/baseline/word.json.gz')
        count = word['source_basis_gates']
        for name in ['undelimited', 'inverse', 'helper', 'frame', 'dependent', 'touch_set']:
            with self.subTest(case=name):
                bad = copy.deepcopy(word)
                if name == 'undelimited':
                    bad['source_basis_gates'] = 0
                elif name == 'inverse':
                    bad['B'][0][2][0] = bad['B'][0][1]
                elif name in ['helper', 'frame']:
                    gate = bad['A'][-count]
                    if name == 'helper':
                        gate[1] = word['v']*2
                    else:
                        gate[0] = -1
                    bad['B'][:count] = copy.deepcopy(list(reversed(bad['A'][-count:])))
                elif name == 'dependent':
                    bad['ret'][1] = bad['ret'][0]
                else:
                    # This invertible two-row basis copies an untouched third row.
                    # Replacing it with the identity would drop full-frame visits.
                    bad = dict(v=3, R=0, final=[1]*6, start=[0]*6,
                               A=[[1, 0, [1]]], B=[[1, 0, [1]]], D=[], C=[],
                               source_basis_gates=1, ret=[2], scatter=[[], [], [0]])
                with self.assertRaises((ValueError, AssertionError)):
                    module.reorder_basis(bad)

    def test_cli_preserves_input_and_refuses_overwrite(self):
        source = ROOT/'inputs/baseline/word.json.gz'
        directory = tempfile.mkdtemp(prefix='basis-postprocess-test-')
        print('Retained CLI test outputs:', directory)
        source_path = Path(directory)/'input.json'
        output = Path(directory)/'output.json'
        raw = gzip.decompress(source.read_bytes())
        source_path.write_bytes(raw)
        cmd = [sys.executable, '-B', str(ROOT/'postprocess.py'), str(source_path), str(output)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(read(output), read(ROOT/'inputs/candidate/word.json.gz'))
        saved = output.read_bytes()
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output.read_bytes(), saved)
        self.assertEqual(source_path.read_bytes(), raw)


if __name__ == '__main__':
    unittest.main()
