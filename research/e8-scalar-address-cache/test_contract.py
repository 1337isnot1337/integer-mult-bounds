"""Address boundaries, stage-local cache lifetime and contract failure controls."""
import ast
import copy
from pathlib import Path
import tempfile
import unittest
import contract


class AddressContractTest(unittest.TestCase):
    def test_stage_reflection_helper_and_private_boundaries(self):
        tree=ast.parse((contract.SOURCE/'candidate_emit.py').read_text())
        mapper=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='mapper']
        setup=[n for n in ast.walk(tree) if isinstance(n,ast.Assign) and
               any(isinstance(t,ast.Name) and t.id=='global_indices' for t in n.targets)]
        self.assertEqual((len(mapper),len(setup)),(1,1))
        code=compile(ast.fix_missing_locations(ast.Module(body=copy.deepcopy(mapper+setup),type_ignores=[])),'<exact-cache-boundaries>','exec')
        V,R=3,2;LOCAL=2*V+R;temp=10*V+11*R;helper_sets=[]
        for stage in range(11):
            for pair in range(5):
                for reverse in [False,True]:
                    ns=dict(V=V,R=R,K=5,LOCAL=LOCAL,temp=temp,s=stage,p=pair,rev=reverse)
                    exec(code,ns);table=ns['global_indices']
                    left=list(range(2*pair*V,(2*pair+1)*V))
                    right=list(range((2*pair+1)*V,(2*pair+2)*V))
                    self.assertEqual(table[:2*V],right+left if reverse else left+right)
                    helpers=list(range(10*V+stage*R,10*V+(stage+1)*R))
                    self.assertEqual(table[2*V:LOCAL],helpers)
                    self.assertEqual(table[LOCAL:], [temp])
                    self.assertEqual(len(set(table)),LOCAL+1)
            helper_sets.append(set(helpers))
        self.assertEqual(len(set.union(*helper_sets)),11*R)

    def test_invalid_operands_and_missing_private_endpoint_are_rejected(self):
        extract,validate,_=contract.load_functions()
        _,recipe,section=extract(contract.SOURCE/'original_emit.py')
        LOCAL=8
        valid=[[2,0,LOCAL,0,0,8,0],[3,0,LOCAL,0,0,0,0]]
        for bad in [-1,LOCAL+1]:
            events=valid+[[1,0,bad,1,0,0]]
            with self.subTest(index=bad),self.assertRaises(AssertionError):
                validate(section,{'forward':events,'reverse':events},3,2,recipe())
        source=(contract.SOURCE/'candidate_emit.py').read_text()
        self.assertEqual(source.count('range(LOCAL + 1)'),1)
        scratch=Path(tempfile.mkdtemp(prefix='e8-address-cache-endpoint-control-'))
        mutant=scratch/'missing-private.py'
        mutant.write_text(source.replace('range(LOCAL + 1)','range(LOCAL)',1))
        run,_,_=extract(mutant)
        fixture=contract.load_fixtures()[0]
        with self.assertRaises(IndexError):
            run(fixture['local_programs'],120,747)


if __name__=='__main__':unittest.main()
