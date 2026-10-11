"""Parent preservation and scalar regressions for idle-axis hosting."""
import copy
import gzip
import importlib.util
import json
from pathlib import Path
import unittest
from schedule_guard import require_hosted_bit_contract, validate_nine_stage_bit_schedule

ROOT = Path(__file__).resolve().parent

def read(name):
    data=(ROOT/name).read_bytes()
    return json.loads(gzip.decompress(data) if name.endswith('.gz') else data)


def mutate(template, name):
    result=copy.deepcopy(template)
    if name == 'exchange':
        result['schedule'].pop()
    elif name in ['bridge_zero','bridge_sign']:
        event=next(e for e in result['schedule'] if e['kind']=='bridge')
        event['coefficient']=0 if name=='bridge_zero' else -event['coefficient']
    elif name == 'level':
        next(e for e in result['schedule'] if e['kind']=='idle')['source_level'] -= 1
    elif name == 'orientation':
        result['calls'][0]['orientation']='reverse'
    elif name == 'duplicate_invocation':
        result['calls'][1]=copy.deepcopy(result['calls'][0])
    elif name == 'idle_index':
        next(e for e in result['schedule'] if e['kind']=='idle')['idx']=True
    elif name == 'nonidle_metadata':
        result['schedule'][0]['idx']=0
    elif name == 'inherited_field':
        result['replicas'] += 1
    elif name == 'numeric_type':
        result['calls'][0]['stage']=0.0
    return result


def scalar_columns(schedule):
    # Unrestricted F2 evaluation, separate from the guard's validity checks.
    rows = [1 << i for i in range(8)]
    for event in schedule:
        if event['kind'] == 'local_cover_sweep':
            pair = event['pair']
            source, destination = (2*pair+1,2*pair) if event['reverse'] else (2*pair,2*pair+1)
            rows[destination] ^= rows[source]
        elif event['kind'] == 'bridge' and event['coefficient'] % 2:
            destination, source = event['dst'],event['src']
            rows[2*destination] ^= rows[2*source]
            rows[2*source+1] ^= rows[2*destination+1]
        elif event['kind'] == 'exchange':
            rows = [rows[i^1] for i in range(8)]
    return rows


class HostedBitContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parent=read('inputs/parent.json.gz')
        cls.hosted=read('inputs/hosted.json.gz')
        cls.widths=read('inputs/widths.json')
        spec=importlib.util.spec_from_file_location('original_hosting_audit', ROOT/'vendor/audit.py')
        cls.original=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.original)

    def test_authentic_hosted_template_preserves_parent(self):
        before=copy.deepcopy(self.hosted)
        report=require_hosted_bit_contract(self.hosted,self.parent)
        self.assertEqual(report['scalar_columns'],8)
        self.assertEqual(self.hosted,before)
        profile,hosted=self.original.audit_bit(self.hosted,self.parent,self.widths)
        expected=read('EXPECTED.json')
        self.assertEqual({str(r):n for r,n in profile.items()},expected['profile'])
        self.assertEqual(hosted,expected['hosted_residuals'])

    def test_original_audit_accepts_scalar_regressions_guard_rejects(self):
        original_profile,original_count=self.original.audit_bit(self.hosted,self.parent,self.widths)
        for name,wrong in [('exchange',8),('bridge_zero',3)]:
            with self.subTest(mutation=name):
                bad=mutate(self.hosted,name)
                profile,count=self.original.audit_bit(bad,self.parent,self.widths)
                self.assertEqual((profile,count),(original_profile,original_count))
                self.assertEqual(sum(a != 1<<i for i,a in enumerate(scalar_columns(bad['schedule']))),wrong)
                with self.assertRaises(ValueError):
                    validate_nine_stage_bit_schedule(bad['schedule'])
                with self.assertRaises(ValueError):
                    require_hosted_bit_contract(bad,self.parent)

    def test_binds_sign_levels_headers_indices_and_inherited_fields(self):
        for name in ['bridge_sign','level','orientation','duplicate_invocation',
                     'idle_index','nonidle_metadata','inherited_field','numeric_type']:
            with self.subTest(mutation=name):
                with self.assertRaises(ValueError):
                    require_hosted_bit_contract(mutate(self.hosted,name),self.parent)

    def test_bad_parent_is_not_admitted_by_matching_child(self):
        parent=mutate(self.parent,'bridge_zero')
        child=mutate(self.hosted,'bridge_zero')
        with self.assertRaises(ValueError):
            require_hosted_bit_contract(child,parent)


if __name__ == '__main__':
    unittest.main()
