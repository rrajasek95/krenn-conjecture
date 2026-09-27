#!/usr/bin/env python3
"""Replay exact support for the site-balancing reduction and sharp response bound."""
from itertools import combinations,product
from collections import Counter
from math import factorial
from pathlib import Path
import hashlib
import json
from core import *
from examples import critical_core

HERE=Path(__file__).resolve().parent


def graph_census():
    edges=tuple(combinations(range(6),2));index={e:i for i,e in enumerate(edges)}
    mask=lambda es:sum(1<<index[e] for e in es)
    perfect=[mask(M) for M in matchings(tuple(range(6)))]
    triangles=[]
    for other in combinations(range(1,6),2):
        left=(0,)+other;right=tuple(i for i in range(6) if i not in left)
        triangles.append(mask(tuple(combinations(left,2))+tuple(combinations(right,2))))
    pm_count=0;fractional_without_pm=[]
    for G in range(1<<15):
        has_pm=any((G&M)==M for M in perfect)
        if has_pm:pm_count+=1
        elif any((G&T)==T for T in triangles):
            require(G in triangles,'A six-site fractional matching without a perfect matching is exactly two triangles')
            fractional_without_pm.append(G)
    require(len(fractional_without_pm)==10,'Ten labeled triangle-pair supports')
    return dict(supports=1<<15,perfect_matching_supports=pm_count,fractional_without_perfect=10,
                fractional_extreme_cover_types={'perfect_matchings':15,'triangle_pairs':10})


def polynomial_identity(source,n=6,colors=3):
    """Expand the commuting polynomial independently, including collisions."""
    terms=[((i*colors+a,j*colors+b),z) for (i,j,a,b),z in source.items() if z]
    squared={}
    for p,(left,x) in enumerate(terms):
        for q in range(p,len(terms)):
            right,y=terms[q]
            monomial=tuple(sorted(left+right))
            coefficient=x*y/(2 if p==q else 1)
            squared[monomial]=squared.get(monomial,ZERO)+coefficient
    categories={2:Q(0),3:Q(0),4:Q(0)}
    for monomial,z in squared.items():
        weight=1
        for multiplicity in Counter(monomial).values():weight*=factorial(multiplicity)
        categories[len({v//colors for v in monomial})]+=weight*z.abs2()
    M=[[source.get(cell(i//colors,j//colors,i%colors,j%colors),ZERO)
        if i//colors!=j//colors else ZERO for j in range(n*colors)] for i in range(n*colors)]
    S,degrees,weights=energy_degrees(source,n)
    require(sum(categories.values())==S*S/2+norm2(gram(M,M))/4,'Independent polynomial contraction identity')
    rho={(i,j):gram(block(source,i,j,colors),block(source,i,j,colors))
         for i in range(n) for j in range(n) if i!=j}
    two=sum((w*w+norm2(rho[i,j]))/2 for (i,j),w in weights.items())
    three=Q(0)
    for i in range(n):
        for j,k in combinations([v for v in range(n) if v!=i],2):
            three+=weights.get(tuple(sorted((i,j))),Q(0))*weights.get(tuple(sorted((i,k))),Q(0))+trace_product(rho[i,j],rho[i,k])
    require(categories[2]==two and categories[3]==three,'Both collision multiplicity formulas')
    require(str(categories[4])==response_identity(source,n,colors)['four_site_norm_squared'],'Four distinct sites reproduce matching tensors')
    return dict(monomials=len(squared),norm_by_distinct_sites={str(k):str(v) for k,v in categories.items()})


def examples():
    prism={(0,1,0,0):ONE,(0,2,2,2):ONE,(1,2,1,1):ONE,
           (3,4,0,0):ONE,(3,5,2,2):ONE,(4,5,1,1):ONE,
           (0,3,1,1):E(Q(1,10)),(1,4,2,2):E(Q(1,10)),(2,5,0,0):E(Q(1,10))}
    factors=[Q(2),Q(1,2),Q(3),Q(1,3),Q(5),Q(1,5)]
    distorted=scale(prism,factors)
    balanced,receipt=certify_scaling(distorted,[1/x for x in factors])
    require(balanced==prism and outputs(distorted)==outputs(prism),'Balancing preserves every complex output coefficient')
    require(receipt['balanced_energy']=='603/100','Exact balanced prism energy')
    dangling={(0,1,0,0):ONE,(2,3,0,0):ONE,(4,5,0,0):ONE,(1,2,1,2):OMEGA}
    cleaned,removed=certify_scaling(dangling,[Q(1)]*6)
    require(outputs(cleaned)==outputs(dangling) and removed['removed_cells']==1,'An edge in no perfect matching contributes no output')
    require(removed['rate_gain']=='64/27','Exact rate gain from pruning')
    dense={(i,j,a,b):E(1+(i+2*j+a)%3,(a+b+j)%3-1) for i,j in combinations(range(6),2) for a,b in product(range(3),repeat=2)}
    colored={(i,j,(i+j)%3,(2*i+j)%3):OMEGA if (i+j)%2 else ONE for i,j in combinations(range(6),2)}
    paley={(i,j,0,0):E(1 if j==5 or (i-j)%5 in (1,4) else -1) for i,j in combinations(range(6),2)}
    critical={(i,j,0,0):z for (i,j),z in critical_core().items()}
    identities={name:response_identity(A) for name,A in [('dense_complex',dense),('unbalanced_dense',scale(dense,factors)),('balanced_colored',colored),
                  ('balanced_prism',prism),('sharp_conference',paley),('unbalanced_critical',critical)]}
    require(identities['sharp_conference']['energy']=='15' and identities['sharp_conference']['four_site_norm_squared']=='15',
            'Sharp constant attained by a six-site real symmetric conference matrix')
    require(identities['sharp_conference']['local_gram_slack']=='0' and identities['sharp_conference']['off_diagonal_gram_norm_squared']=='0',
            'Conference example saturates every nonnegative remainder')
    require(identities['unbalanced_critical']['four_site_norm_squared']=='0' and not identities['unbalanced_critical']['balanced'],
            'Dropping balance would make the lower-bound claim false')
    try:scale(prism,[Q(2)]*6)
    except ValueError:negative='REJECTED'
    else:raise ValueError('A non-unit product of factors was accepted')
    return dict(scaling=receipt,pruning=removed,norm_identities=identities,
                independent_polynomial_expansion=polynomial_identity(dense),
                negative_controls={'non_unit_product':negative,'dropping_balance':'REJECTED'},output_words_compared=729)


def main():
    dependencies=json.loads((HERE/'dependencies.json').read_text())
    for name,expected in dependencies.items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,'Pinned dependency: '+name)
    result=dict(status='PASS',evidence_status='Written normalization and sharp norm proofs with exact support; independent audit pending',
                support_census=graph_census(),examples=examples(),dependencies=dependencies,
                consequences=['Universal normalized-rate bounds may be proved on balanced sources',
                              'At six sites every balanced source has a derivative column of norm at least S/15',
                              'Complete four-site cancellation forces support matching number at most two',
                              'The completely flat isolated-core limit cannot be a balanced counterexample limit'],
                unresolved='Partial rank loss, target-specific cancellation, the unrestricted square-root law, and the global unrestricted W optimum')
    files=sorted(p for p in HERE.iterdir() if p.suffix in ('.py','.json','.md') and p.name!='results.json')
    files += [ROOT/'notes'/name for name in ('site-balancing-rate-reduction-2026-09-26.md','balanced-four-site-response-bound-2026-09-26.md')]
    result['sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
