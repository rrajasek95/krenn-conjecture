#!/usr/bin/env python3
"""Exact full-color fifth-order onset in a resonant first-jet branch."""
from pathlib import Path
from itertools import combinations, product
import sys
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'computations/higher-order-2026-09-26'))
from shared import E, ZERO, ONE, OMEGA, require, critical_core
from critical import coefficient


def build_source(row,parameters):
    cells=tuple((i,j,a,b) for i,j in combinations(range(6),2) for a,b in product(range(3),repeat=2))
    source={c:{} for c in cells}
    for (i,j),z in critical_core().items():source[i,j,0,0][0,()]=z
    variable=parameters
    first={}
    for c in cells:
        i,j,a,b=c
        if j==5 and b==1 and a in (0,1):
            if a==0:
                for v,z in row.get(i,{}).items():source[c][1,(v,)]=z
        else:
            first[c]=variable;source[c][1,(variable,)]=ONE;variable+=1
    second={}
    for degree in (2,3,4):
        for c in cells:
            if degree==2:second[c]=variable
            source[c][degree,(variable,)]=ONE;variable+=1
    return source,first,second,variable


def resonant_branch(pair,k):
    q=critical_core();i,j=pair
    ratio=-q[tuple(sorted((j,k)))]/q[tuple(sorted((i,k)))]
    row={i:{0:ONE},j:{0:ratio}}
    source,first,second,variable=build_source(row,1)
    require(variable==531,'126 independent first-jet parameters and 405 higher-jet variables')
    values=[row.get(v,{}).get(0,ZERO) for v in range(5)]
    q=critical_core();allowed=[];forced=[]
    for u,v in combinations(range(5),2):
        rest=[s for s in range(5) if s not in (u,v)]
        g=sum((values[s]*q[tuple(t for t in rest if t!=s)] for s in rest),ZERO)
        word=[0]*6;word[u]=word[v]=word[5]=1
        expected={} if not g else {tuple(sorted((0,first[u,v,1,1]))):g}
        require(coefficient(source,tuple(word),2)==expected,'Quadratic gate isolates gamma times one core bb cell')
        (forced if g else allowed).append((u,v))
    other=tuple(s for s in range(5) if s not in (i,j,k));l,m=other
    require(set(allowed)=={pair,other} and len(forced)==8,'Only two disjoint core bb edges survive in each resonant branch')
    for u,v in forced:source[u,v,1,1].pop((1,(first[u,v,1,1],)))
    protected=tuple(0 if s in other else 1 for s in range(6))
    third=coefficient(source,protected,3)
    expected3={tuple(sorted((first[i,j,1,1],second[k,5,1,1]))):q[other]}
    require(third==expected3,'Protected cubic coefficient in every labeled resonant branch')
    fourth=coefficient(source,(1,)*6,4)
    expected4={tuple(sorted((first[i,j,1,1],first[l,m,1,1],second[k,5,1,1]))):ONE}
    require(fourth==expected4,'The pure fourth-order b amplitude has exactly one surviving monomial')
    multiplied={tuple(sorted((first[l,m,1,1],)+monomial)):z/q[other] for monomial,z in third.items()}
    require(fourth==multiplied,'Fourth pure coefficient is a first-jet multiple of a cubic error')
    # Restore the forbidden bb entries; the scope restriction matters.
    relaxed={c:dict(p) for c,p in source.items()}
    for u,v in forced:relaxed[u,v,1,1][1,(first[u,v,1,1],)]=ONE
    wrong3=coefficient(relaxed,protected,3)
    wrong4=coefficient(relaxed,(1,)*6,4)
    require(wrong4!={tuple(sorted((first[l,m,1,1],)+mon)):z/q[other] for mon,z in wrong3.items()},
            'Dropping the quadratic gate invalidates the claimed identity')
    return dict(pair=list(pair),third_vertex=k)


def check():
    resonant=[resonant_branch(pair,k) for pair in combinations(range(5),2) for k in range(5) if k not in pair]
    simple=0
    for support in [(i,) for i in range(5)]+list(combinations(range(5),2)):
        row={i:{v:ONE} for v,i in enumerate(support)}
        source,first,second,variables=build_source(row,len(support))
        allowed={e for e in combinations(range(5),2) if support[0] in e} if len(support)==1 else {tuple(support)}
        # The written quadratic gate forces this support in the single-entry
        # and nonresonant two-entry cases. No two surviving bb edges are disjoint.
        for i,j in combinations(range(5),2):
            if (i,j) not in allowed:source[i,j,1,1].pop((1,(first[i,j,1,1],)))
        require(not coefficient(source,(1,)*6,4),'Single-entry and generic two-entry branches have zero fourth pure coefficient')
        simple+=1
    return dict(resonant_branches=len(resonant),single_or_nonresonant_branches=simple,
                resonant_variables_before_gate=531,resonant_active_variables_after_gate=523,
                arbitrary_higher_jet_cells=405,resonant_quadratic_word_gates=300,
                canonical_identity='H4(b^6) = B34(bb) * H3(bbbaab)',
                conclusion='A nonzero first row supported in ground color on at most two core sites forces GHZ onset to order five or later',
                negative_control='Dropping the quadratic gate REJECTED',
                limitation='Sparse ground-only first-row branches; not all critical-core directions or a universal rate bound')


def main():
    dependencies=json.loads((HERE/'dependencies.json').read_text())
    for name,expected in dependencies.items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,'Pinned dependency: '+name)
    result=dict(status='PASS',evidence_status='Exact polynomial certificate for a written branch theorem; independent audit pending',
                certificate=check(),dependencies=dependencies)
    files=sorted(p for p in HERE.iterdir() if p.suffix in ('.py','.json','.md') and p.name not in ('results.json','exploration.json'))
    files.append(ROOT/'notes/critical-core-fifth-order-branch-2026-09-26.md')
    result['sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
