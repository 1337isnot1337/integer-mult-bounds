"""Byte-identical encoding for the emit.py renamed-instruction SHA stream.
No semantic/invoice transformation. Caller retains original ownership/paid-rank checks.
Precondition: streams and owners remain unchanged while compiled records are encoded.
Only the actual emit.py schema is accepted: op0/1 length6, op2/3 length7.
"""
import json

def compile_stream(events):
 out=[]
 for z in events:
  op=z[0]
  assert type(op) is int and op in (0,1,2,3)
  assert len(z)==(6 if op in (0,1) else 7)
  assert all(type(x) is int for x in z)
  x=z[1]
  if op==0:
   out.append((b'['+str(op).encode()+b',',x,None,b','+json.dumps(z[2:],separators=(',',':')).encode()[1:]+b'\n'))
  else:
   out.append((b'['+str(op).encode()+b',',x,z[2],b','+json.dumps(z[3:],separators=(',',':')).encode()[1:]+b'\n'))
 return tuple(out)

def encoded_records(compiled,owners,private_owner):
 enc=[json.dumps(o,separators=(',',':')).encode() for o in owners]
 private=json.dumps(private_owner,separators=(',',':')).encode();n=len(enc)
 for prefix,x,y,suffix in compiled:
  assert 0<=x<n
  if y is None:yield prefix+enc[x]+suffix
  else:
   assert y>=0
   yield prefix+enc[x]+b','+(enc[y] if y<n else private)+suffix
