"""Apply the X54 triangle-hybrid slot (unchanged NewBArch builder) to the frozen three-demotion word."""
import argparse,gzip,hashlib,json,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
BARCH=ROOT/'research/gauge44-slots/construction/barch'
def main():
 assert __debug__
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();assert not a.out.exists()
 base=P.parent/'k8-three-demotions/FULL-WORD.json.gz';r=json.loads((P/'RECIPE-X54-dem.json').read_text())
 assert hashlib.sha256(gzip.decompress(base.read_bytes())).hexdigest()==r['base_sha256']
 subprocess.run([sys.executable,'-B',str(BARCH/'build_tri.py'),str(base),str(P/'RECIPE-X54-dem.json'),str(a.out)],check=True)
 assert hashlib.sha256(gzip.decompress(a.out.read_bytes())).hexdigest()==r['expect_sha256'];print('PASS_X54_ON_THREE_DEMOTIONS')
if __name__=='__main__':main()
