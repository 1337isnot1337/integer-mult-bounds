"""Minimal line set O on which the candidate's confined decoder is infeasible (UNSAT core over per-line assumptions + deletion)."""
from pysat.formula import IDPool
from pysat.solvers import Solver
from f2check import NO
def build(opts):
    pool=IDPool(); cl=[]; W={}; U={}
    act=[pool.id(('a',T)) for T in range(60)]
    for j,alts in enumerate(opts):
        sels=[pool.id(('s',j,k)) for k in range(len(alts))]; cl.append(sels)
        for a in range(len(sels)):
            for b in range(a+1,len(sels)): cl.append([-sels[a],-sels[b]])
        for T in set().union(*[set(X) for X,Y in alts]):
            W[T,j]=pool.id(('w',T,j)); cl.append([-W[T,j]]+[sels[k] for k,(X,Y) in enumerate(alts) if T in X])
        for T in set().union(*[set(Y) for X,Y in alts]):
            U[T,j]=pool.id(('u',T,j)); cl.append([-U[T,j]]+[sels[k] for k,(X,Y) in enumerate(alts) if T in Y])
    def AND(a,b):
        z=pool.id(('and',a,b)); cl.extend([[-z,a],[-z,b],[z,-a,-b]]); return z
    def XOR(a,b):
        z=pool.id(('xor',a,b)); cl.extend([[-z,a,b],[-z,-a,-b],[z,-a,b],[z,a,-b]]); return z
    for T in range(60):
        for S_ in range(60):
            if not (T==S_ or NO[T,S_]): continue
            terms=[AND(W[T,j],U[S_,j]) for j in range(len(opts)) if (T,j) in W and (S_,j) in U]
            g=[-act[T]]+([-act[S_]] if S_!=T else [])
            if not terms:
                if T==S_: cl.append(g)
                continue
            acc=terms[0]
            for t in terms[1:]: acc=XOR(acc,t)
            cl.append(g+([acc] if T==S_ else [-acc]))
    return cl,act
def min_core(opts,solver='cadical153'):
    cl,act=build(opts)
    with Solver(name=solver,bootstrap_with=cl) as s:
        if s.solve(assumptions=act): return None
        core=sorted(act.index(x) for x in s.get_core())
        cur=list(core)
        for T in list(core):
            trial=[x for x in cur if x!=T]
            if not s.solve(assumptions=[act[x] for x in trial]): cur=trial
        return cur
if __name__=='__main__':
    import sys
    perp=lambda l:[T for T in range(60) if T!=l and not NO[l,T]]
    D=eval(sys.argv[1])
    O=min_core([[(perp(a),perp(b)),(perp(b),perp(a))] for a,b in D])
    print('minimal infeasible O:',len(O),O)
