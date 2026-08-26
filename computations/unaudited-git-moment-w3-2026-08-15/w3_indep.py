"""UNAUDITED PROBE (W3, Route A, 2026-08-15). HEAD 26ba69f7.

Identification of the gauge mechanism with the independent-half-set move.

PROPOSITION.  Let H <= K_8 with minimum degree >= 3 (which the pure rows
force, via the committed forced-incidence theorem).  Then some edge of H
lies in no fractional perfect matching of H  <=>  H has an independent set
I with |I| = 4 and at least one edge inside V\I; and the edges lying in no
fpm are exactly the union of E(H[V\I]) over such I.

PROOF SKETCH (see REPORT.md).  A barrier for "e in no fpm" is a set S* with
i(H-S*) = |S*|, whose isolated set I satisfies N(I) <= S* and |I| = |S*|.
If R = V\(S* u I) is nonempty then I u {r} is independent for r in R, and
|I| <= 3 forces deg(v) <= |S*| = |I| <= 2 for v in I, contradicting minimum
degree 3.  Hence R = empty and |I| = |S*| = 4.

CONSEQUENCE (all orders, arbitrary cell supports).  If the aggregate
support graph of an exact source has an independent set I with |I| = n/2,
then w = 1_{V\I} - 1_I (colour-independent) is admissible with
<pi_c, w> = 0, so the source degenerates onto the bipartite part.
"""
from __future__ import annotations
import itertools, random
from w3_band import ALL_EDGES, VERTS, failing_edges

def indep4_dead(H):
    out=set()
    for I in itertools.combinations(VERTS,4):
        if any(a in I and b in I for (a,b) in H): continue
        out.update(e for e in H if e[0] not in I and e[1] not in I)
    return out

def mindeg(H):
    d={v:0 for v in VERTS}
    for (u,v) in H: d[u]+=1; d[v]+=1
    return min(d.values())

if __name__=="__main__":
    print("UNAUDITED PROBE  W3 / Route A  HEAD 26ba69f7")
    print("PROPOSITION CHECK: min-degree-3 => (no-fpm edges) == (independent-4-set edges)")
    print("="*78)
    rng=random.Random(4)
    for tag,gen in (("random p=0.35",lambda: [e for e in ALL_EDGES if rng.random()<0.35]),
                    ("random p=0.5", lambda: [e for e in ALL_EDGES if rng.random()<0.50]),
                    ("random p=0.7", lambda: [e for e in ALL_EDGES if rng.random()<0.70])):
        n=agree=viol=nodeg=0
        for _ in range(20000):
            H=tuple(gen())
            if len(H)<4: continue
            if mindeg(H)<3: nodeg+=1; continue
            n+=1
            a=set(failing_edges(H)); b=indep4_dead(H)
            if a==b: agree+=1
            else: viol+=1
        print(f"  {tag:14s}: min-deg-3 graphs tested={n:6d}  agree={agree:6d}  VIOLATIONS={viol}")
    # exhaustive over all graphs with <=12 edges and min degree 3
    n=agree=viol=0
    for k in (12,13):
        for H in itertools.combinations(ALL_EDGES,k):
            if mindeg(H)<3: continue
            n+=1
            if set(failing_edges(H))==indep4_dead(H): agree+=1
            else: viol+=1
    print(f"  EXHAUSTIVE |E| in 12,13, min deg 3: tested={n}  agree={agree}  VIOLATIONS={viol}")
    # and a check that min-degree-2 breaks it (sharpness of the hypothesis)
    bad=0; tested=0
    for _ in range(30000):
        H=tuple(e for e in ALL_EDGES if rng.random()<0.4)
        if len(H)<4 or mindeg(H)!=2: continue
        tested+=1
        if set(failing_edges(H))!=indep4_dead(H): bad+=1
    print(f"  sharpness: min-degree-2 graphs tested={tested}  DISAGREEMENTS={bad} "
          f"(the hypothesis min-deg>=3 is needed)")
