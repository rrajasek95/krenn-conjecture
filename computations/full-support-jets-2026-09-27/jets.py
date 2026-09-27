"""Exact cubic and quartic jet identities with every complex jet cell free."""
from pathlib import Path
from itertools import combinations, product
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'computations/boundary-structure-2026-09-26'))
from exact import E, ZERO, ONE, OMEGA, Q, require, matchings, cell, outputs

CELLS=tuple((i,j,a,b) for i,j in combinations(range(6),2) for a,b in product(range(3),repeat=2))
INDEX={c:i for i,c in enumerate(CELLS)}
MATCHINGS=tuple(matchings(tuple(range(6))))


def add(p,q):
    out=p.copy()
    for monomial,z in q.items():
        out[monomial]=out.get(monomial,ZERO)+z
        if not out[monomial]:del out[monomial]
    return out


def times_variable(p,variable,scalar=ONE):
    return {tuple(sorted(m+(variable,))):z*scalar for m,z in p.items() if z*scalar}


def coefficient(ground,word,degree):
    out={}
    for matching in MATCHINGS:
        for orders in product(range(degree+1),repeat=3):
            if sum(orders)!=degree:continue
            scalar=ONE;monomial=[]
            for (i,j),order in zip(matching,orders):
                c=(i,j,word[i],word[j])
                if order==0:
                    scalar*=ground.get((i,j),ZERO) if word[i]==word[j]==0 else ZERO
                else:monomial.append((order-1)*len(CELLS)+INDEX[c])
            if scalar:
                key=tuple(sorted(monomial));out[key]=out.get(key,ZERO)+scalar
    return {m:z for m,z in out.items() if z}


def base():
    D={(0,1):ONE,(2,3):ONE,(0,2):OMEGA,(1,3):OMEGA,
       (0,3):OMEGA*OMEGA,(1,2):OMEGA*OMEGA,(4,5):E(-2)}
    D.update({(i,j):ONE for i in range(4) for j in (4,5)})
    return D


def verify_identities(ground):
    require(all(ground.get(e,ZERO) for e in combinations(range(6),2)),
            'Every ground-color edge must be nonzero')
    cache={};counts={3:0,4:0};monomials={3:0,4:0}
    for word in product((1,2),repeat=6):
        for degree,jet in ((3,1),(4,2)):
            left=coefficient(ground,word,degree)
            if degree==3:left={m:3*z for m,z in left.items()}
            right={}
            for i,j in combinations(range(6),2):
                mixed=list(word);mixed[i]=mixed[j]=0;mixed=tuple(mixed)
                if mixed not in cache:cache[mixed]=coefficient(ground,mixed,2)
                variable=(jet-1)*len(CELLS)+INDEX[i,j,word[i],word[j]]
                right=add(right,times_variable(cache[mixed],variable,ONE/ground[i,j]))
            require(left==right,'Exact full-palette jet reconstruction identity')
            counts[degree]+=1;monomials[degree]+=len(left)
    return dict(identities=counts,left_monomials=monomials,second_order_mixed_words=len(cache),
                formally_available_jet_variables=4*len(CELLS))


def check():
    D=base()
    require(not outputs({(i,j,0,0):z for (i,j),z in D.items()}),'Rank-25 reference has zero base output')
    result=verify_identities(D)
    dense={e:E(1+(i+2*j)%3,(i+j)%3) for e in combinations(range(6),2) for i,j in (e,)}
    # The identities require full ground support, not zero base output.
    second=verify_identities(dense)
    require(second['identities']==result['identities'],'Independent complex full-support base')
    missing=dict(D);del missing[0,1]
    try:verify_identities(missing)
    except ValueError:negative='REJECTED'
    else:raise ValueError('Missing base denominator was accepted')
    word=(1,)*6;wrong=coefficient(D,word,3)
    require(wrong!={m:3*z for m,z in wrong.items()},'The Euler factor three is necessary')
    return dict(reference=result,second_complex_base=second,missing_edge_negative_control=negative,
                scope='Written all-even theorem; exact full-jet replay at six sites',
                unresolved='Error versus signal cubed; fifth parameter order is not a uniform fifth distance power')
