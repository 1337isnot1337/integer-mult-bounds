"""Independent finite oracle, source witnesses, boundaries, and large counts."""
from collections import deque
from itertools import product
from pathlib import Path
import copy
import hashlib
import json
import unittest

from bank_optimizer import RANKS, NoSaturatingPacking, check, construct, minimum_replicas

ROOT=Path(__file__).resolve().parent


class OptimizerTests(unittest.TestCase):
    def test_exhaustive_independent_pattern_oracle(self):
        # Enumerate all width-73 equality patterns directly from rank and item
        # equations, without the algorithm's grouping or feasibility predicates.
        patterns=[]
        for a,b,c,d in product(range(2),range(3),range(5),range(9)):
            e=9-a-b-c-d
            if e>=0 and 4*a+5*b+7*c+8*d+9*e==73:
                patterns.append((a,b,c,d,e))
        patterns.append((0,0,0,0,8))
        self.assertEqual(len(patterns),12)
        limits=(2,4,4,8,24)
        zero=(0,)*5
        reachable={zero}
        pending=deque([zero])
        while pending:
            state=pending.popleft()
            for p in patterns:
                nxt=tuple(a+b for a,b in zip(state,p))
                if all(v<=m for v,m in zip(nxt,limits)) and nxt not in reachable:
                    reachable.add(nxt);pending.append(nxt)
        count=0
        for state in product(*(range(m+1) for m in limits)):
            inventory=dict(zip(RANKS,state))
            try:
                patterns_out,certificate=construct(inventory,replicas=1)
            except (NoSaturatingPacking,ValueError):
                success=False
            else:
                success=True
                self.assertEqual(check(patterns_out,inventory)['items'],sum(state))
            self.assertEqual(success,state in reachable,state)
            count+=1
        self.assertEqual(count,16875)

    def test_published_and_composed_inventories(self):
        for case in json.loads((ROOT/'inputs/cases.json').read_text()):
            n={int(r):v for r,v in case['inventory_per_replica'].items()}
            source=ROOT/case['source_patterns_file']
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),case['source_patterns_sha256'])
            check(json.loads(source.read_text()),{r:v*case['source_replicas'] for r,v in n.items()})
            patterns,cert=construct(n)
            self.assertEqual(cert['minimum_replicas'],case['minimum_replicas'],case['name'])
            self.assertEqual(cert['banks'],case['banks'],case['name'])
            self.assertEqual(cert['padding'],case['padding'],case['name'])
            self.assertLessEqual(len(patterns),12)

    def test_compressed_large_counts_and_replication(self):
        n={4:15,5:28,7:9,8:152,9:577}
        patterns,cert=construct(n)
        self.assertEqual((cert['replicas'],cert['banks'],cert['padding']),(64,5891,3035))
        for multiplier in (3,10**40+1):
            scaled={r:v*multiplier for r,v in n.items()}
            p,c=construct(scaled,replicas=64)
            self.assertEqual(c['banks'],5891*multiplier)
            self.assertEqual(c['padding'],3035*multiplier)
            self.assertLessEqual(len(p),12)
        for invalid in (0,-1,32,65,True):
            with self.assertRaises(ValueError):construct(n,replicas=invalid)
        original={4:15,5:27,7:9,8:143,9:587}
        _,c=construct(original,replica_multiple=8)
        self.assertEqual((c['minimum_replicas'],c['minimum_admissible_replicas'],c['banks']),(4,8,738))
        with self.assertRaises(ValueError):construct(original,replicas=4,replica_multiple=8)

    def test_certificate_controls_and_domain(self):
        n={4:15,5:28,7:9,8:152,9:577}
        p,c=construct(n)
        target={r:v*64 for r,v in n.items()}
        changed=copy.deepcopy(p);changed[0]['count']+=1
        with self.assertRaises(ValueError):check(changed,target)
        changed=copy.deepcopy(p);changed[0]['padding']=7
        with self.assertRaises(ValueError):check(changed,target)
        for invalid in ({6:1},{8:-1},{8:0.5},{8:True}):
            with self.assertRaises(ValueError):construct(invalid)
        # Each of the three independent impossibility conditions.
        for n in ({4:1,7:2,9:100},{4:1,8:1,9:100},{8:1}):
            with self.assertRaises(NoSaturatingPacking):minimum_replicas(n)


if __name__=='__main__':unittest.main()
