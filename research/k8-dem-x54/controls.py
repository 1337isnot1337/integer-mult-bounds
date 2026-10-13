"""NewBArch's unchanged run_controls.py on the X54 recipe: C0, recipe, and four mutants globally and for X=54 (10 outcomes)."""
import argparse,json,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
BARCH=ROOT/'research/gauge44-slots/construction/barch'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();assert not a.out.exists()
 subprocess.run([sys.executable,'-B',str(BARCH/'run_controls.py'),str(P.parent/'k8-three-demotions/FULL-WORD.json.gz'),str(P/'RECIPE-X54-dem.json'),str(ROOT/'research/gauge44-slots/independent/audit_local.py'),str(a.out)],check=True)
 res=json.loads((a.out/'controls.json').read_text());assert len(res)==10 and all(x['ok'] for x in res.values());print('PASS_X54_CONTROLS',len(res))
if __name__=='__main__':main()
