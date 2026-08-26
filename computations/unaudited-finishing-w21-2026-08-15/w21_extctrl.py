#!/usr/bin/env python3
"""W21 -- CONTROL for the extension machinery of w21_extend.py.
UNAUDITED.  Exact only.  (a) the single-cell polynomials must reproduce H_w
exactly at random exact values of the twelve singles (checked against a
from-the-definition H engine); (b) a MUTATION control: corrupting one
polynomial coefficient must make the check fail; (c) an EXPLICIT-POINT
control for the 'inconsistent' verdict: a linear system built the same way
from a DELIBERATELY CONSISTENT variant must be reported consistent."""
import json, os, random, sys
sys.dont_write_bytecode = True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from fractions import Fraction
import w21_core as K
exec(open(os.path.join(HERE,"w21_extend.py")).read().split("res={\"_header\"")[0].split("import w21_core as K")[1])

def H_full(bl, sv, w):
    """H_w from the definition with the singles set to sv (dict edge->value)."""
    tot=Fraction(0)
    for M in K.PMS:
        p=Fraction(1); ok=True
        for (u,v) in M:
            if (u,v) in gam: p*=bl[(u,v)][w[u]][w[v]]
            elif (u,v) in SCELL:
                if SCELL[(u,v)]!=(w[u],w[v]): ok=False;break
                p*=sv[(u,v)]
            else: ok=False;break
        if ok: tot+=p
    return tot

bl=load(os.path.join(HERE,"tensor","results_zero.json"))
rng=random.Random(1234)
sv={e:Fraction(rng.randint(1,9),rng.randint(1,4)) for e in SING}
val=[sv[e] for e in SING]
bad=0; tested=0
for w in list(K.MIXED)[::7]:
    p=poly_of(bl,w)
    tot=Fraction(0)
    for k,c in p.items():
        t=c
        for i in k: t*=val[i]
        tot+=t
    tested+=1
    if tot!=H_full(bl,sv,w): bad+=1
print("(a) polynomial reconstruction: %d mismatches / %d words" % (bad,tested))
# (b) mutation
w0=list(K.MIXED)[3]
p=poly_of(bl,w0); k0=sorted(p)[0]; p2=dict(p); p2[k0]=p2[k0]+1
tot=Fraction(0)
for k,c in p2.items():
    t=c
    for i in k: t*=val[i]
    tot+=t
print("(b) MUTATION control: corrupted polynomial differs from H_w: %s" % (tot!=H_full(bl,sv,w0)))
# (c) explicit-point control for the linear-inconsistency verdict:
#     build a linear system with a KNOWN solution and check it is reported consistent.
rows=[]
target=[Fraction(rng.randint(1,7)) for _ in range(12)]
for _ in range(400):
    r=[Fraction(rng.randint(-5,5)) for _ in range(12)]
    c=sum(r[i]*target[i] for i in range(12))
    rows.append(r+[c])
R,piv=K.rref(rows,13)
print("(c) EXPLICIT-POINT control: consistent system reported inconsistent? %s "
      "(want False)" % (12 in piv))
json.dump(dict(reconstruction_mismatches=bad,tested=tested,
               mutation_fires=bool(tot!=H_full(bl,sv,w0)),
               explicit_point_false_kill=bool(12 in piv)),
          open(os.path.join(HERE,"results_extctrl.json"),"w"),indent=1)
