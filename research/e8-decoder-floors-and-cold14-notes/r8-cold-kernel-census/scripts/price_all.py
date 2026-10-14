"""Price every census candidate exactly with the #1186 exact frame toolkit (scalar exactness mod p, cone caps, exact frames).
usage: price_all.py WORD CANDS.json OUT.json [workers]"""
import sys,json,time
sys.path.insert(0,'/Users/joelpulikkan/imb-harness/r7/tk')
from multiprocessing import Pool
P=None
def init(w):
    global P
    import harness as H; P=H.Pricer(w)
def job(a):
    k,c=a
    r=P.price(c['ed'],timeout=int(__import__('os').environ.get('TMO','120'))); r.pop('word',None)
    return k,r
if __name__=='__main__':
    w,cp,op=sys.argv[1:4]; nw=int(sys.argv[4]) if len(sys.argv)>4 else 10
    C=json.load(open(cp)); t=time.time(); import os; out=json.load(open(op)) if os.path.exists(op) else {}; out={int(k):v for k,v in out.items()}
    with Pool(nw,initializer=init,initargs=(w,),maxtasksperchild=200) as pool:
        for n,(k,r) in enumerate(pool.imap_unordered(job,[(k,c) for k,c in enumerate(C) if k not in out],chunksize=1)):
            out[k]=r
            if r.get('status')=='ok' and r['delta']<0: print('GAIN',k,C[k]['pivot'],C[k]['kind'],r['delta'],r['profile'],flush=True)
            if n%200==0: print('progress',n,len(C),round(time.time()-t),flush=True); json.dump(out,open(op,'w'))
    json.dump(out,open(op,'w'))
    import collections
    print('status',collections.Counter(r['status'] for r in out.values()))
    print('ok deltas',collections.Counter(r['delta'] for r in out.values() if r['status']=='ok').most_common(20))
