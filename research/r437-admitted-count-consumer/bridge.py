"""Original entry to the literal binary NODE prefix, opt-in quotient only.

JoyboyBrian; substantial OpenAI Codex assistance; Apache-2.0.
Source functions belong to the retained selected physical caller authors.
"""
import ast, copy, hashlib
from pathlib import Path
from types import SimpleNamespace


def compile_node_prefix(module, quotient):
    """Keep every NODE statement before its first payload call, byte-source bound."""
    tree=ast.parse(Path(module.__file__).read_text())
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Machine')
    node=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='node')
    stop=next(i for i,n in enumerate(node.body) if isinstance(n,ast.Assign) and
              isinstance(n.targets[0],ast.Name) and n.targets[0].id=='peeled')
    kept=copy.deepcopy(node);kept.name='bound_node_prefix';kept.body=kept.body[:stop]
    namespace=dict(vars(module));namespace['fresh_rows']=SimpleNamespace(quotient=quotient)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[kept],type_ignores=[])),
                 '<literal original NODE before peel>','exec'),namespace)
    return namespace['bound_node_prefix'],dict(statements=stop,
        ast_sha256=hashlib.sha256(ast.dump(ast.Module(body=kept.body,type_ignores=[])).encode()).hexdigest(),
        boundary='all original NODE statements before peeled=peel.run; no payload call')
