import json,gzip
from collections import Counter,defaultdict
D='/Users/joelpulikkan/imb-r2/research/pr638-improvement-20261013/witness638/data'
P=json.load(open(D+'/PLAN.json'))
rows=json.loads(gzip.decompress(open(D+'/OWNERS.json.gz','rb').read()))
reg=P['provider_registry']
def fam(owner,child,port): return owner*896+(2*P['pairs'][str(child)]+P['sides'][str(child)])*112+port
