"""Bind the joint native receipt to the retained complete finite compiler."""
from pathlib import Path
from fractions import Fraction as Q
from hashlib import sha256
import json,gzip,importlib.util,sys,argparse
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
if sys.flags.optimize:raise RuntimeError('Run without -O')
P={'1':2201,'2':412,'3':510,'4':127,'5':40,'8':8};H={'4':28,'7':7,'8':47,'9':326}
def run():
 native=json.loads(gzip.decompress((HERE/'NATIVE-RESULT.json.gz').read_bytes()));assert native['status']=='PASS_JOINT_HELPER_WARP_NATIVE_AND_ABSOLUTE_PHASE'
 assert native['paid']==P and native['helpers']==H
 assert native['candidate_payload_sha256']==json.load(open(HERE/'FROZEN.json'))['payload_sha256']
 for direction,allowance,prefix,den in [('forward',158120,'457',32),('backward',158168,'169',64)]:
  r=native['native'][direction];assert r['paid_profile']==P and r['independent_persistent_columns']==632
  assert r['scalar_frames_checked'] and r['arbitrary_owned_C0_cleared'] and r['real_scalar_allowance']==allowance
  assert str(r['max_formal_prefix_l1'])==prefix and r['max_denominator']==den
  assert r['second_literal']['independent_borrowed_input_fields']==632
 for f,h in json.load(open(HERE/'INPUTS.json')).items():assert sha256((ROOT/f).read_bytes()).hexdigest()==h
 vendor=HERE/'vendor/price_profile_4610.py';pin=json.load(open(HERE/'VENDOR.json'));assert sha256(vendor.read_bytes()).hexdigest()==pin['sha256']
 spec=importlib.util.spec_from_file_location('joint_full_price',vendor);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
 result=m.run(native,Q('.003021769'))
 assert result['local_paid']==P and result['local_helpers']==H and result['rank_mass_surplus']==752
 assert result['paid_calls']==64404 and result['productive_fields']==10928
 result['gain_over_PR4626']=str(Q('.003021769')-Q('.003021569'))
 result['native_receipt_sha256']=sha256((HERE/'NATIVE-RESULT.json.gz').read_bytes()).hexdigest()
 result['candidate_payload_sha256']=native['candidate_payload_sha256']
 result['arithmetic_engine_sha256']=pin['sha256']
 return result
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();out=run();p=HERE/'ARITHMETIC.json'
 if args.write:p.write_text(json.dumps(out,indent=2)+'\n')
 else:assert json.loads(p.read_text())==out
 print(json.dumps({k:out[k] for k in ['status','kappa','gain_over_PR4626','raw_root_interval','paid_calls']},indent=2))
