#!/usr/bin/env python3
import json, subprocess, sys, tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as d:
    out=Path(d)/"RESULT.json"
    p=subprocess.run([sys.executable,"-I","-B",str(HERE/"verify.py"),"--write-result",str(out)],capture_output=True,text=True,check=True)
    assert p.stdout.strip().startswith("PASS_U8_B_SHEAR_REWRITE_SEED32")
    assert json.loads(out.read_text())==json.loads((HERE/"RESULT.json").read_text())
print("PASS_U8_B_SHEAR_PACKAGE deterministic_result=1")
