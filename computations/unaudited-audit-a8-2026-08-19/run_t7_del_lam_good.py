#!/usr/bin/env python3
"""A8 T7 -- adversarial tests of W28-DEL, W28-LAM and W28-GOOD.

(a) W28-DEL.  The lemma is scoped to the NO-CANCELLATION stratum; the
    justification printed in W28 ("(B),(C),(D) are monotone decreasing under
    deleting edges ... deleting edges only kills terms") is a statement about
    SUB-SUMS of a vanishing sum and is FALSE without the no-cancellation
    hypothesis.  We construct an explicit counterexample to the unqualified
    monotonicity claim, and verify monotonicity inside the stratum.

(b) W28-LAM.  We confirm  X_4 (diagonal, N=8)  =>  Haf(sum lam_c t^c) =
    sum lam_c^4, and test the REPORT's converse ("the diagonal X_4 problem =
    the Waring identity") by hunting a diagonal source satisfying the identity
    that is NOT in X_4.

(c) W28-GOOD.  The vertex expansion of the hafnian, and the lemma's conclusion
    tested on (A)+(B) configurations whose supports STRICTLY CONTAIN a perfect
    matching (W28 only tested it on disjoint-PM triples, where it is trivial).
"""
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, permutations, product

BASE = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a8-2026-08-19"
sys.path.insert(0, BASE)
from a8_core import (checkpoint, diag_blocks, haf, H_raw, is_constant, offcount,
                     perfect_matchings, profile, require, words)

R, RAN = {}, []
rng = random.Random(707)
V = tuple(range(8))
E8 = [tuple(sorted(e)) for e in combinations(V, 2)]
PMS8 = perfect_matchings(V)
FOUR = [tuple(S) for S in combinations(V, 4)]


def sect(s):
    print("=" * 74)
    print(s)
    print("=" * 74)


def hafw(t, S):
    return haf(t, S)


def conditions_violated(t3, kmax=4):
    """(A)-(D) violations of a diagonal source given as three weight dicts."""
    bad = []
    for c in range(3):
        if hafw(t3[c], V) != 1:
            bad.append(("A", c))
    for c in range(3):
        for d in range(3):
            if d == c:
                continue
            for e in E8:
                if t3[d].get(e, 0) == 0:
                    continue
                if hafw(t3[c], [x for x in V if x not in e]) != 0:
                    bad.append(("B", c, d, e))
    if kmax >= 4:
        for c in range(3):
            for d in range(3):
                if d == c:
                    continue
                for S in FOUR:
                    if hafw(t3[c], S) == 0:
                        continue
                    if hafw(t3[d], tuple(x for x in V if x not in S)) != 0:
                        bad.append(("C", c, d, S))
        for c in range(3):
            d, e2 = [x for x in range(3) if x != c]
            for S in FOUR:
                if hafw(t3[c], S) == 0:
                    continue
                T = [x for x in V if x not in S]
                for f in ((T[0], T[1]), (T[0], T[2]), (T[0], T[3])):
                    g = tuple(x for x in T if x not in f)
                    for (p, q) in ((d, e2), (e2, d)):
                        if t3[p].get(f, 0) and t3[q].get(g, 0):
                            bad.append(("D", c, p, q, S, f, g))
    return bad


# ------------------------------------------------------------------- (a)
sect("(a) W28-DEL: is the monotonicity claim true WITHOUT no-cancellation?")
# Build t^0 with a support on which haf(t^0 | V - e) = 0 BY CANCELLATION, and
# t^1 carrying the edge e.  Then (B) holds; delete one edge of L_0 and (B) is
# violated -- a NEW violation created by a deletion.
# Take V - e = {2,...,7}: give t^0 two perfect matchings of it with weights
# +1 and -1 and nothing else.
e = (0, 1)
W6 = (2, 3, 4, 5, 6, 7)
m1 = ((2, 3), (4, 5), (6, 7))
m2 = ((2, 4), (3, 5), (6, 7))
t0 = {}
for x in m1:
    t0[x] = Fraction(1)
for x in m2:
    t0[x] = t0.get(x, Fraction(0)) + Fraction(0)      # keep support
t0[(2, 4)] = Fraction(1)
t0[(3, 5)] = Fraction(-1)
t0[(6, 7)] = Fraction(1)
t0[(2, 3)] = Fraction(1)
t0[(4, 5)] = Fraction(1)
h_before = hafw(t0, W6)
print(f"   L_0 = {sorted(t0)}   haf(t^0 | V - (0,1)) = {h_before} "
      f"(0 by CANCELLATION, not by absence of matchings)")
npm_before = sum(1 for m in perfect_matchings(W6) if all(x in t0 for x in m))
print(f"   number of perfect matchings of L_0 on V - (0,1): {npm_before} (> 1 => cancellation)")
require(h_before == 0 and npm_before > 1, "cancellation setup failed")
t1 = {e: Fraction(1)}
t2 = {}
# (B) for the pair (c=0, d=1, edge e): haf(t^0|V-e) * t^1_e = 0  -- holds.
print(f"   (B) at (c=0,d=1,e={e}) before deletion: "
      f"{h_before} * {t1[e]} = {h_before * t1[e]}  -> HOLDS")
t0b = dict(t0)
del t0b[(3, 5)]                       # delete one edge of L_0
h_after = hafw(t0b, W6)
print(f"   after deleting (3,5) from L_0: haf(t^0|V-e) = {h_after}  -> "
      f"(B) now VIOLATED ({h_after} * {t1[e]} != 0)")
require(h_after != 0, "counterexample failed")
R["t7a_del_counterexample"] = dict(
    L0=[list(x) for x in sorted(t0)], deleted=[3, 5],
    haf_before=str(h_before), haf_after=str(h_after),
    verdict="the UNQUALIFIED monotonicity claim is FALSE; the lemma needs the "
            "no-cancellation hypothesis, under which haf = 0 <=> no matching "
            "and deletion is monotone")
RAN.append("T7a_del_counterexample")
# and the positive half: inside the stratum, monotonicity is immediate
print("   inside the no-cancellation stratum haf(t^c|S) = 0 <=> npm(L_c|S) = 0,")
print("   and npm is monotone under deletion, so (B)/(C)/(D) are.  [verified below]")
tested = viol = 0
for trial in range(300):
    t3 = [{}, {}, {}]
    pool = list(E8)
    rng.shuffle(pool)
    i = 0
    for c in range(3):
        k = rng.randint(4, 8)
        for x in pool[i:i + k]:
            t3[c][x] = Fraction(rng.randint(1, 3))     # POSITIVE -> no cancellation
        i += 9
    b0 = set(map(str, conditions_violated(t3)))
    b0 = {x for x in b0 if not x.startswith("('A'")}
    c = rng.randrange(3)
    if not t3[c]:
        continue
    ee = rng.choice(list(t3[c]))
    t4 = [dict(x) for x in t3]
    del t4[c][ee]
    b1 = {x for x in map(str, conditions_violated(t4)) if not x.startswith("('A'")}
    tested += 1
    viol += (not b1 <= b0)
print(f"   positive-weight (no-cancellation) deletions: {tested} tested, {viol} new "
      f"violations (must be 0)")
require(viol == 0, "monotonicity inside the stratum")
R["t7a_del_instratum"] = dict(tested=tested, new_violations=viol)
RAN.append("T7a_del_instratum")

# ------------------------------------------------------------------- (b)
sect("(b) W28-LAM: implication vs the REPORT's claimed equivalence")


def Haf_lambda(t3, lam):
    tt = {}
    for x in E8:
        tt[x] = sum(lam[c] * t3[c].get(x, 0) for c in range(3))
    return hafw(tt, V)


# generating identity control
bad = 0
for _ in range(5):
    Aw = {x: Fraction(rng.randint(-3, 3)) for x in E8}
    Bw = {x: Fraction(rng.randint(-3, 3)) for x in E8}
    lhs = hafw({x: Aw[x] + Bw[x] for x in E8}, V)
    rhs = Fraction(0)
    for m in range(0, 9, 2):
        for S in combinations(V, m):
            rhs += hafw(Aw, S) * hafw(Bw, tuple(x for x in V if x not in S))
    bad += (lhs != rhs)
print(f"   haf(A+B) = sum_S haf(A|S)haf(B|V-S): {bad} mismatches (must be 0)")
require(bad == 0, "generating identity")
RAN.append("T7b_generating_identity")

# a (C)-passing, (D)-failing disjoint triple; tune weights to KILL the (2,1,1)
# coefficients while keeping (A).  If it works, the Waring identity holds but
# the source is NOT in X_4 -- refuting the "=" in the REPORT.
PMSET = [frozenset(m) for m in PMS8]


def union_ham(M1, M2):
    adj = {v: [] for v in V}
    for (u, w) in list(M1) + list(M2):
        adj[u].append(w)
        adj[w].append(u)
    seen, prev, cur = {0}, None, 0
    for _ in range(7):
        nxt = adj[cur][0] if adj[cur][0] != prev else adj[cur][1]
        prev, cur = cur, nxt
        if cur in seen:
            return False
        seen.add(cur)
    return len(seen) == 8


trip = None
for a in range(105):
    for b in range(a + 1, 105):
        if PMSET[a] & PMSET[b] or not union_ham(PMSET[a], PMSET[b]):
            continue
        for c in range(b + 1, 105):
            if (PMSET[a] & PMSET[c]) or (PMSET[b] & PMSET[c]):
                continue
            if union_ham(PMSET[a], PMSET[c]) and union_ham(PMSET[b], PMSET[c]):
                trip = (PMSET[a], PMSET[b], PMSET[c])
                break
        if trip:
            break
    if trip:
        break
require(trip is not None, "no (C)-passing triple")
sup = [sorted(m) for m in trip]
print(f"   (C)-passing triple: {sup}")
# enumerate the (2,1,1) configurations
cfgs = {0: [], 1: [], 2: []}
for M in PMS8:
    sig = [0, 0, 0]
    ok = True
    for x in M:
        w = [c for c in range(3) if x in trip[c]]
        if not w:
            ok = False
            break
        sig[w[0]] += 1
    if not ok:
        continue
    if sorted(sig) == [1, 1, 2]:
        a = sig.index(2)
        cfgs[a].append(M)
print(f"   (2,1,1) configurations per leading colour: "
      f"{{0: {len(cfgs[0])}, 1: {len(cfgs[1])}, 2: {len(cfgs[2])}}}")
found = None
for attempt in range(200000):
    wts = [{x: Fraction(rng.choice([1, -1, 2, -2, 3, -3])) for x in sorted(m)}
           for m in trip]
    prods = [1, 1, 1]
    for c in range(3):
        p = Fraction(1)
        for x in wts[c]:
            p *= wts[c][x]
        prods[c] = p
    if any(p == 0 for p in prods):
        continue
    sums = []
    for a in range(3):
        s = Fraction(0)
        for M in cfgs[a]:
            pr = Fraction(1)
            for x in M:
                cc = [c for c in range(3) if x in trip[c]][0]
                pr *= wts[cc][x]
            s += pr
        sums.append(s)
    if all(s == 0 for s in sums):
        found = (wts, prods, sums)
        break
print(f"   weight search for vanishing (2,1,1) sums: "
      f"{'FOUND after ' + str(attempt) + ' tries' if found else 'not found'}")
R["t7b"] = dict(cfg_counts={str(a): len(cfgs[a]) for a in range(3)},
                found=bool(found))
if found:
    wts, prods, sums = found
    # rescale each class so haf(t^c|V) = 1 -- over Q only if prods are 4th powers;
    # the identity test is homogeneous, so verify it in the scaled-to-1 form
    # symbolically instead: Haf(sum lam t) with the UNSCALED weights equals
    # sum prods_c lam_c^4 exactly iff the mixed coefficients vanish.
    t3 = [dict(wts[c]) for c in range(3)]
    ok = True
    for lam in [(1, 1, 1), (1, -1, 0), (2, 1, 1), (1, 2, 3), (1, 1, -2), (3, -1, 2)]:
        lhs = Haf_lambda(t3, lam)
        rhs = sum(prods[c] * lam[c] ** 4 for c in range(3))
        if lhs != rhs:
            ok = False
            print(f"      lam={lam}: {lhs} vs {rhs}  MISMATCH")
    print(f"   Waring identity Haf(sum lam t) = sum prod_c lam_c^4 holds: {ok}")
    # and this source is NOT in X_4 (it fails (D)) -- check by the RAW word def
    A = diag_blocks({c: t3[c] for c in range(3)}, 8)
    bad4 = [w for w in words(8) if offcount(w) <= 4 and not is_constant(w)
            and H_raw(A, w, PMS8) != 0]
    print(f"   raw X_4 mixed-word failures of this source: {len(bad4)} "
          f"(> 0 => the Waring identity does NOT imply X_4)")
    R["t7b"].update(waring_holds=ok, x4_failures=len(bad4),
                    weights=[{str(k): str(v) for k, v in w.items()} for w in wts],
                    prods=[str(p) for p in prods],
                    verdict="REPORT's 'the diagonal X_4 problem = the Waring "
                            "identity' is an OVERSTATEMENT: the identity is "
                            "implied by, but does not imply, X_4")
RAN.append("T7b_waring")

# ------------------------------------------------------------------- (c)
sect("(c) W28-GOOD: vertex expansion + supports strictly containing a PM")
bad = 0
for _ in range(5):
    tw = {x: Fraction(rng.randint(-4, 4)) for x in E8}
    for u in V:
        lhs = hafw(tw, V)
        rhs = sum(tw[tuple(sorted((u, y)))] *
                  hafw(tw, tuple(x for x in V if x not in (u, y)))
                  for y in V if y != u)
        bad += (lhs != rhs)
print(f"   haf(t|V) = sum_y t_uy haf(t|V-u-y) at every vertex: {bad} mismatches "
      f"(must be 0)")
require(bad == 0, "vertex expansion")
RAN.append("T7c_vertex_expansion")

# build (A)+(B) configurations with |L_c| = 5
made = 0
okgood = 0
details = []
for _ in range(4000):
    idx = rng.sample(range(105), 3)
    Ms = [PMSET[i] for i in idx]
    if Ms[0] & Ms[1] or Ms[0] & Ms[2] or Ms[1] & Ms[2]:
        continue
    t3 = [{x: Fraction(1) for x in m} for m in Ms]
    c0 = rng.randrange(3)
    f = rng.choice([x for x in E8 if not any(x in m for m in Ms)])
    t3[c0][f] = Fraction(rng.choice([1, -1, 2]))
    if hafw(t3[c0], V) != 1:
        continue
    if any(("B",) == tuple(x[:1]) for x in conditions_violated(t3, kmax=0)):
        continue
    viol = [x for x in conditions_violated(t3, kmax=0) if x[0] in ("A", "B")]
    if viol:
        continue
    made += 1
    good = []
    for c in range(3):
        good.append({x for x in t3[c]
                     if hafw(t3[c], tuple(v for v in V if v not in x)) != 0})
    cover = all(set(v for x in good[c] for v in x) == set(V) for c in range(3))
    disj = all(not (good[a] & good[b]) for a, b in combinations(range(3), 2))
    cross = all(not (good[a] & set(t3[b])) for a in range(3) for b in range(3) if a != b)
    okgood += (cover and disj and cross)
    if made <= 3:
        details.append(dict(supports=[sorted(map(list, t3[c])) for c in range(3)],
                            good=[sorted(map(list, g)) for g in good],
                            cover=cover, disj=disj, cross=cross))
    if made >= 60:
        break
print(f"   (A)+(B) configurations with a support of size 5: {made} built; "
      f"{okgood} have the three good classes spanning, pairwise disjoint, and "
      f"each disjoint from the other FULL classes (must be all)")
require(made > 0 and okgood == made, "W28-GOOD failed on an enlarged support")
R["t7c"] = dict(built=made, good_ok=okgood, examples=details)
RAN.append("T7c_good_enlarged")

MAN = dict(declared=["T7a_del_counterexample", "T7a_del_instratum",
                     "T7b_generating_identity", "T7b_waring",
                     "T7c_vertex_expansion", "T7c_good_enlarged"], ran=RAN)
MAN["missing"] = [x for x in MAN["declared"] if x not in RAN]
print("CONTROL MANIFEST:", MAN)
require(not MAN["missing"], "manifest")
R["manifest"] = MAN
checkpoint(BASE + "/results_t7_del_lam_good.json", R)
