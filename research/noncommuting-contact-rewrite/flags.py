"""Exact common-map extension with a prescribed line image. Apache-2.0."""
from warp_merge import F
from intervals import basis

def matching_flag(A,B,line_a,line_b):
    inside=line_a in F.span(A)
    F.need(inside==(line_b in F.span(B)),'Same fixed-line incidence')
    def grow(v,more):
        v=list(v)
        for x in more:
            if len(basis(v+[x]))>len(v):v.append(x)
        return v
    if inside:
        S=grow([line_a],A);T=grow([line_b],B)
    else:S=A+[line_a];T=B+[line_b]
    S=grow(S,[1<<i for i in range(9)]);T=grow(T,[1<<i for i in range(9)])
    F.need(len(S)==len(T)==9,'Complete paired bases')
    images={0:0}
    for a,b in zip(S,T):images.update({x^a:y^b for x,y in list(images.items())})
    F.need(len(images)==len(set(images.values()))==512,'Invertible flag map')
    return [images[1<<i] for i in range(9)]



# Ordinary basis completion retained from Cao Yifan PR4610.
def matching_map(A,B):
    assert len(A)==len(B)
    def extend(a):
        a=a[:]
        for i in range(9):
            if len(basis(a+[1<<i]))>len(a):a.append(1<<i)
        assert len(a)==9;return a
    A,B=extend(A),extend(B);images={0:0}
    for a,b in zip(A,B):images.update({x^a:y^b for x,y in list(images.items())})
    assert len(images)==512 and len(set(images.values()))==512
    return [images[1<<i] for i in range(9)]

