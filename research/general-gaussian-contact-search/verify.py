#!/usr/bin/env python3
"""Exact geometry, invoice and positive calibration; Apache-2.0, Codex assistance."""
from collections import Counter
from fractions import Fraction as Q
import hashlib,importlib.util,itertools,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
import model as M

def power(r,C):
    if r==1:return Q(1),Q(1)
    z=Q(r-1,r+1);term=z;lower=Q(0)
    for k in range(64):lower+=2*term/(2*k+1);term*=z*z
    upper=lower+2*term/(129*(1-z*z))
    def exp_negative(x,n):
        value=term=Q(1)
        for k in range(1,n+1):term*=-x/k;value+=term
        return value
    return r*exp_negative(C*upper,11),r*exp_negative(C*lower,10)

def moment(profile,C):
    out=[Q(0),Q(0)]
    for r,n in profile.items():
        lo,hi=power(r,C);out[0]+=n*lo;out[1]+=n*hi
    return out

def geometry():
    path=ROOT/'research/t74-native-fast/vendor/native/new/code/borrow/vendor/clifford/clifford_exact.py'
    spec=importlib.util.spec_from_file_location('contact_clifford',path);ce=importlib.util.module_from_spec(spec);sys.modules[spec.name]=ce;spec.loader.exec_module(ce)
    checked=0
    for n in (1,2,3):
        spaces={frozenset({0}):[]}
        for v in range(1,1<<n):
            for s,b in list(spaces.items()):
                if v not in s:spaces.setdefault(frozenset(s|{x^v for x in s}),b+[v])
        for a,ba in spaces.items():
            for b,bb in spaces.items():
                op=ce.canonical_frame(n,ba).adjoint().then(ce.canonical_frame(n,bb))
                actual=ce.rank([x for x,z,p in op.tab[n:]])
                M.need(actual==M.fourier_rank(M.mask(a),M.mask(b)),'exact Clifford B-block rank')
                checked+=1
    # Previously zero edges and non-nested moves cannot be priced by dim difference.
    line=M.mask({0,1});other=M.mask({0,2});zero=1;full=M.mask({0,1,2,3})
    M.need(M.fourier_rank(line,line)==0 and M.fourier_rank(line,zero)==1,'old zero edge becomes a paid child')
    M.need(M.fourier_rank(line,other)==2 and M.fourier_rank(line,full)==1,'nonnested physical rank')
    return checked

def phase_geometry():
    path=ROOT/'research/t74-native-fast/vendor/native/new/code/borrow/vendor/clifford/clifford_exact.py'
    spec=importlib.util.spec_from_file_location('phase_clifford',path)
    ce=importlib.util.module_from_spec(spec);sys.modules[spec.name]=ce;spec.loader.exec_module(ce)
    paid_checks=warp_checks=0
    for n in (1,2,3):
        spaces={frozenset({0}):[]}
        for v in range(1,1<<n):
            for a,b in list(spaces.items()):
                if v not in a:spaces.setdefault(frozenset(a|{x^v for x in a}),b+[v])
        maps=[]
        for cols in itertools.product(range(1,1<<n),repeat=n):
            if ce.rank(cols)==n:maps.append(cols)
            if len(maps)==12:break
        coordinates=[(i,j) for i in range(n) for j in range(i,n)]
        for bits in range(1<<len(coordinates)):
            q=[0]*n
            for k,(i,j) in enumerate(coordinates):
                if bits>>k&1:q[i]|=1<<j;q[j]|=1<<i
            q9=q+[0]*(9-n);diagonal=ce.diag(n,q)
            charts={a:[ce.canonical_frame(n,b),diagonal.then(ce.canonical_frame(n,b))]
                    for a,b in spaces.items()}
            for a,ba in spaces.items():
                for b,bb in spaces.items():
                    intersection=spaces[frozenset(a&b)]
                    base=len(ba)+len(bb)-2*len(intersection)
                    extra=M.binary_rank(M.restrict_form(q9,intersection))
                    for i,j in itertools.product(range(2),repeat=2):
                        op=charts[a][i].adjoint().then(charts[b][j])
                        actual=ce.rank([x for x,z,p in op.tab[n:]])
                        M.need(actual==base+(extra if i!=j else 0),'physical symmetric-form transition rank')
                        paid_checks+=1
            for cols in maps:
                G=ce.transpose(cols,n);gi=ce.inv(G,n);git=ce.transpose(gi,n)
                correction=tuple((1<<i)^sum(ce.parity(x&y)<<j for j,y in enumerate(git))
                                 for i,x in enumerate(git))
                native=ce.perm(n,G).then(ce.diag(n,correction))
                for a,ba in spaces.items():
                    image=[ce.mv(G,x) for x in ba]
                    target=[ce.canonical_frame(n,image),diagonal.then(ce.canonical_frame(n,image))]
                    source_form=M.restrict_form(q9,ba);target_form=M.restrict_form(q9,image)
                    expected=[0,ce.rank(source_form),ce.rank(target_form),
                              ce.rank([x^y for x,y in zip(source_form,target_form)])]
                    for i,j in itertools.product(range(2),repeat=2):
                        op=charts[a][i].adjoint().then(native).then(target[j])
                        actual=ce.rank([x for x,z,p in op.tab[n:]])
                        M.need(actual==expected[i+2*j],'physical paid-phase native warp rank')
                        warp_checks+=1
    return dict(paid_pairs=paid_checks,native_warps=warp_checks,
                scope='All symmetric forms and all subspaces in dimensions 1..3; first 12 invertible maps in product order per dimension.')

def run():
    fixture=M.load(HERE/'CALIBRATION.json');old=M.load(HERE/'inputs/round2-word.json.gz')
    m=M.build(old,fixture['functionals']);p0,h0=M.invoice(m,[]);p1,h1=M.invoice(m,fixture['selected_nodes'])
    M.need(p1=={1:2183,2:416,3:507,4:135,5:40,8:8},'known complete paid calibration')
    M.need(h1=={4:28,7:5,8:38,9:337},'known actual helper calibration')
    C=Q('0.00302177585');P0=moment(p0,C);P1=moment(p1,C);H0=moment(h0,C);H1=moment(h1,C)
    gain=(P0[0]-P1[1]+H1[0]-H0[1],P0[1]-P1[0]+H1[1]-H0[0])
    M.need(gain[0]>0,'strict positive calibration with rational power intervals')
    rejected=False
    try:M.invoice(m,[m['fixed'][0]])
    except ValueError:rejected=True
    M.need(rejected,'frozen boundary mutation rejected')
    current=M.load(HERE/'inputs/round3-word.json.gz');mc=M.build(current,[1,2]);pc,hc=M.invoice(mc,[])
    M.need(pc=={1:2201,2:412,3:510,4:127,5:40,8:8},'current complete baseline')
    M.need(hc=={4:28,7:7,8:47,9:326},'current arbitrary-helper census')
    phase=M.build_phase(current,[1]);pp,hp=M.invoice(phase,[])
    M.need(pp==pc and hp==hc,'paid-phase baseline invoice')
    # Rank-two Q is represented by the sum of its rank-one constituents.
    M.need(M.phase_matrix([1,2])==[1,2,0,0,0,0,0,0,0],'phase matrix XOR construction')
    M.need(M.phase_matrix([1,2,3])==[2,1,0,0,0,0,0,0,0],'off-diagonal phase construction')
    # Synthetic moment sign control only, not a supplier: paid 2->3, helper 1->2.
    two=power(2,C);three=power(3,C)
    M.need(2*two[0]-three[1]-1>0,'paid-phase synthetic concavity gain control')
    phase_checks=phase_geometry()
    mass=lambda p:sum(r*n for r,n in p.items())
    return dict(status='PASS_GENERAL_GAUSSIAN_CONTACT_MODEL_NO_NEW_KAPPA',
                exact_clifford_pair_checks=geometry(),paid_phase_physical_checks=phase_checks,calibration_selected_nodes=len(fixture['selected_nodes']),
                calibration_paid=dict(p1),calibration_helpers=dict(h1),
                calibration_positive_local_gain_interval=[str(x) for x in gain],
                calibration_local_gain_decimal=[float(x) for x in gain],
                old_rank_mass_deficit=mass(p0)-mass(h0),new_rank_mass_deficit=mass(p1)-mass(h1),
                current_nodes=len(mc['nodes']),current_edge_count=len(mc['edges']),
                current_paid=dict(pc),current_helpers=dict(hc),
                controls=['newly_paid_old_zero_edge','nonnested_rank_not_dimension_difference','frozen_boundary_rejected'])

def main():
    pins=M.load(HERE/'SOURCES.json')
    for row in pins['files']:
        if row['usage']=='input':M.need(hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256'],'input source bytes')
    result=json.loads(json.dumps(run()));path=HERE/'RESULT.json'
    if '--write' in sys.argv:path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:M.need(result==M.load(path),'stored exact receipt')
    print('PASS_GENERAL_GAUSSIAN_CONTACT_MODEL: physical transition/phase/warp ranks, known positive calibration; no new kappa')
if __name__=='__main__':main()
