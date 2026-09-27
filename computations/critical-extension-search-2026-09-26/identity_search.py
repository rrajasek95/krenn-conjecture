"""Search a polynomial certificate for fourth-order vanishing.

Exploratory modular linear algebra; an answer requires exact replay over
Q(omega) before it can support a characteristic-zero claim.
"""
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import sys
import json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'critical-cone-2026-09-26'))
import probe

EDGES=probe.EDGES
BCELLS=probe.CELLS
BI={c:i+10 for i,c in enumerate(BCELLS)}
LI={key:i for i,key in enumerate(probe.ROWS)}


def matching4(vertices):
    for j in range(1,4):
        e=(vertices[0],vertices[j]);f=tuple(v for v in vertices if v not in e)
        yield e,f


def polynomials(omega,prime):
    q={(0,1):1,(2,3):1,(0,2):omega,(1,3):omega,(0,3):omega*omega%prime,(1,2):omega*omega%prime,
       **{(i,4):1 for i in range(4)}}
    second={};third={}
    for word in probe.WORDS:
        s={};t={}
        for k in range(5):
            rest=tuple(v for v in range(5) if v!=k)
            for e,f in matching4(rest):
                mon=tuple(sorted((LI[k,word[k]],BI[e[0],e[1],word[e[0]],word[e[1]]],BI[f[0],f[1],word[f[0]],word[f[1]]])))
                t[mon]=(t.get(mon,0)+1)%prime
                for base,edge in ((e,f),(f,e)):
                    if all(word[v]==0 for v in base):
                        mon=tuple(sorted((LI[k,word[k]],BI[edge[0],edge[1],word[edge[0]],word[edge[1]]])))
                        s[mon]=(s.get(mon,0)+q[base])%prime
        second[word]={m:z for m,z in s.items() if z};third[word]={m:z for m,z in t.items() if z}
    target={}
    for e,weight in q.items():
        word=tuple(0 if i in e else 1 for i in range(5))
        factor=pow(2*weight,-1,prime);v=BI[e[0],e[1],1,1]
        for m,z in third[word].items():
            key=tuple(sorted(m+(v,)));target[key]=(target.get(key,0)+factor*z)%prime
    return second,third,{m:z for m,z in target.items() if z}


def columns(second,third,full=False):
    # Target color degree is a^2 b^5 on core-variable occurrences.
    out=[]
    for word,poly in third.items():
        zeros=word.count(0)
        if zeros>1:continue
        for cell,var in BI.items():
            if cell[2:].count(0)==2-zeros:
                out.append((('H3',word,(var,)),{tuple(sorted(m+(var,))):z for m,z in poly.items()}))
    for word,poly in second.items():
        zeros=word.count(0)
        if not 2<=zeros<=4:continue
        for c,d in combinations_with_replacement(BCELLS,2):
            if not full and len(set(c[:2]+d[:2]))<4:continue
            if c[2:].count(0)+d[2:].count(0)!=4-zeros:continue
            mon=(BI[c],BI[d])
            out.append((('H2',word,mon),{tuple(sorted(m+mon)):z for m,z in poly.items()}))
    return out


def solve(omega,prime,full=False):
    second,third,target=polynomials(omega,prime)
    cols=columns(second,third,full)
    basis={};target=dict(target);combination={}
    def subtract(v,w,factor):
        for key,value in w.items():
            new=(v.get(key,0)-factor*value)%prime
            if new:v[key]=new
            else:v.pop(key,None)
    for j,(label,original) in enumerate(cols):
        vector=dict(original);combo={j:1}
        while vector:
            pivot=min(vector)
            if pivot not in basis:break
            other,weights=basis[pivot];factor=vector[pivot]
            subtract(vector,other,factor);subtract(combo,weights,factor)
        if vector:
            pivot=min(vector);inverse=pow(vector[pivot],-1,prime)
            vector={k:v*inverse%prime for k,v in vector.items()}
            combo={k:v*inverse%prime for k,v in combo.items()}
            basis[pivot]=(vector,combo)
        while target:
            pivot=min(target)
            if pivot not in basis:break
            other,weights=basis[pivot];factor=target[pivot]
            subtract(target,other,factor)
            # Original target = remaining target + combination of columns.
            subtract(combination,weights,-factor)
        if not target:
            return dict(status='MODULAR_IDENTITY_FOUND',prime=prime,omega=omega,columns_considered=j+1,
                        columns_total=len(cols),rank=len(basis),terms=len(combination),
                        coefficients={str(i):v for i,v in combination.items()},
                        labels={str(i):cols[i][0] for i in combination})
    return dict(status='NO_IDENTITY_IN_THIS_MULTIPLIER_SPACE',prime=prime,omega=omega,columns=len(cols),rank=len(basis),residual_terms=len(target))


if __name__=='__main__':
    print(json.dumps(solve(probe.W,probe.P,'--full' in sys.argv),indent=2,sort_keys=True))
