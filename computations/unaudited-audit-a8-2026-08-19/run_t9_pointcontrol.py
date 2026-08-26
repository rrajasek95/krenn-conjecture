#!/usr/bin/env python3
"""A8 T9 -- the ledger-18 explicit-point control for the W28-T1 verdicts.

For every "I_Y = <1>" verdict at k = 4 we must produce a point of a KNOWN
FEASIBLE relaxation and check the pipeline against it.  The relaxation is the
same construction at k = 3, where the sigma slice IS feasible.  We take the
exact sigma-symmetric X_3 point built in T5, read off its colour-0 star, and
show that it is an exact rational point of MY OWN k=3 ideal I_Y -- so the
encoding cannot be manufacturing unit ideals -- while the same point makes the
k=4 generators nonzero (it lies outside the k=4 locus, as ledger 18 demands).
"""
import json
import sys
from fractions import Fraction
from itertools import combinations, product

BASE = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a8-2026-08-19"
sys.path.insert(0, BASE)
from a8_core import H_raw, checkpoint, is_constant, offcount, perfect_matchings, require, words
import a8_sym as S

R, RAN = {}, []
VP, Z, EP = S.VP, S.Z, S.EP
d = json.load(open(BASE + "/results_t5_sweep.json"))
pat = tuple(d["explicit_point"]["pattern"])
vals = [Fraction(x) for x in d["explicit_point"]["orbit_values"]]
star = {int(y): [[Fraction(x) for x in row] for row in M]
        for y, M in d["explicit_point"]["star"].items()}
print(f"pattern {pat}")
t = [{e: vals[S.ORBIDX[(c, e)]] for e in EP} for c in range(3)]


def hafn(tc, Sset):
    out = Fraction(0)
    for m in S.pms(tuple(sorted(Sset))):
        p = Fraction(1)
        for e in m:
            p *= tc[tuple(sorted(e))]
        out += p
    return out


# the colour-0, d=0 unknowns
x = {y: star[y][0][0] for y in VP}
print(f"x_y = A_(y,z)[0][0]: {[str(x[y]) for y in VP]}")
print(f"support of x: {[y for y in VP if x[y] != 0]}")


def free_set(kmax):
    F = []
    for y in VP:
        W = tuple(v for v in VP if v != y)
        ok = True
        for (S1, S2) in S.even_splits(W):
            if S.offcount8(S.word8(S1, S2)) > kmax:
                continue
            if hafn(t[1], S1) * hafn(t[2], S2) != 0:
                ok = False
                break
        if ok:
            F.append(y)
    return F


F3, F4 = free_set(3), free_set(4)
print(f"free set at k=3: {F3}    at k=4: {F4}")
supp = [y for y in VP if x[y] != 0]
print(f"supp(x) subset F3? {set(supp) <= set(F3)}   (W28-FREE at the rung of the point)")
require(set(supp) <= set(F3), "W28-FREE violated by the explicit point")
require(supp, "q(V') = 1 needs a nonzero x_y")
print(f"q(V') = sum_y haf(t^0|V'-y) x_y = "
      f"{sum(hafn(t[0], tuple(v for v in VP if v != y)) * x[y] for y in VP)} (must be 1)")
require(sum(hafn(t[0], tuple(v for v in VP if v != y)) * x[y] for y in VP) == 1, "q(V')")
RAN.append("T9_free_lemma_at_point")

# evaluate MY ideal generators at this point
for kmax, tag in ((3, "k3"), (4, "k4")):
    Y = tuple(sorted(supp))
    gens, tags, ce, nv = S.build_ideal(S.sym_t(), S.NPAR, Y, kmax)
    pt = list(vals) + [x[y] for y in Y]
    nz = [(tg, str(g.evaluate(pt))) for g, tg in zip(gens, tags) if g.evaluate(pt) != 0]
    cev = ce.evaluate(pt)
    print(f"   k={kmax}, Y={Y}: {len(gens)} generators, {len(nz)} nonzero at the point; "
          f"constant generator = {cev} (must be 0)")
    if nz[:3]:
        print(f"      first nonzero: {nz[:3]}")
    R[f"point_{tag}"] = dict(Y=list(Y), ngens=len(gens), nonzero=len(nz),
                             const_gen=str(cev), first=[str(z) for z in nz[:3]])
    if kmax == 3:
        require(not nz and cev == 0,
                "the k=3 ideal does NOT vanish at a genuine k=3 solution -- encoding bug")
        print("      => I_Y at k=3 has an EXACT RATIONAL POINT: it is NOT the unit "
              "ideal.  The pipeline is not manufacturing kills.")
    else:
        require(nz, "the k=4 generators all vanish at a k=3 point -- control is vacuous")
        print("      => the same point is OUTSIDE the k=4 locus (ledger 18 control "
              "is non-vacuous).")
RAN.append("T9_point_in_k3_ideal")
RAN.append("T9_point_outside_k4_locus")

MAN = dict(declared=["T9_free_lemma_at_point", "T9_point_in_k3_ideal",
                     "T9_point_outside_k4_locus"], ran=RAN)
MAN["missing"] = [z for z in MAN["declared"] if z not in RAN]
print("CONTROL MANIFEST:", MAN)
require(not MAN["missing"], "manifest")
R["manifest"] = MAN
R["pattern"] = list(pat)
checkpoint(BASE + "/results_t9_pointcontrol.json", R)
