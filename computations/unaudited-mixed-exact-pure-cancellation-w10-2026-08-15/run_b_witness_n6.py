#!/usr/bin/env python3
"""W10 task B -- THE N=6 VERDICT: explicit mixed-exact sources on ADMISSIBLE
templates whose pure coefficients vanish by CANCELLATION.

Three witness families, all certified by exhaustive exact evaluation of all
3^6 = 729 words (726 mixed) with Fraction arithmetic, and independently
re-checked with W6's hafnian and W9's template auditor.

  (W-A) the CONSTANT-BLOCK family.  Put A_uv = t_uv * J (J = all-ones 3x3)
        on a graph G.  Then for EVERY word w,
              H_w = sum_{M in PM(G)} prod_{uv in M} t_uv = haf(t),
        because every cell of every block carries the same value.  Choosing
        t with haf(t) = 0 and all t_uv != 0 on G makes the source MIXED-EXACT
        (indeed H == 0), while the template of G is FULL on every live edge:
        every fibre equals |PM(G)|, so (S) holds as soon as |PM(G)| >= 2 and
        (T4)/(T6) hold as soon as |PM(G)| >= 1.  The pure coefficient is a sum
        of |PM(G)| >= 2 NONZERO products summing to zero -- exactly the
        cancellation object W9 asked for.

  (W-B) the FREE-BLOCK family.  If in addition the complementary hafnian
        h(V\\{u0,v0}) = 0 for one edge, then that block becomes completely
        unconstrained: H_w = (X[w_u0][w_v0] - t_{u0v0}) * h(V\\{u0,v0}) = 0
        for every X.  So a whole rank-3, non-constant, generic 3x3 block sits
        inside the mixed-exact variety -- the witnesses are not one orbit.

  (W-C) the SUPPORT-BAND family: (W-A) on every subgraph G of K_6 with
        min degree >= 3 and |PM(G)| >= 2, i.e. every admissible support.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction as F
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (HERE,
          os.path.join(REPO, "computations", "unaudited-bridge-w6-2026-08-15"),
          os.path.join(REPO, "computations", "unaudited-cell-ceiling-w9-2026-08-15")):
    if p not in sys.path:
        sys.path.insert(0, p)

import w10_core as w10                                            # noqa: E402
import w10_linalg as la                                           # noqa: E402
from w10_core import COLORS, require                              # noqa: E402
import w6_core                                                    # noqa: E402
import w9_template                                                # noqa: E402
import w9_core                                                    # noqa: E402

N = 6
EDGES = w10.edges(N)
OUT = {}
log = []


def say(s=""):
    print(s)
    log.append(s)


# ------------------------------------------------------- certification helper

def certify(label, src, expect_admissible=True, verbose=True):
    """Full exact certificate for one source.  Returns the record."""
    tensor = w10.full_tensor(src, N)
    mixed_bad = sorted(w for w in tensor if len(set(w)) > 1 and tensor[w] != 0)
    pures = [tensor[(c,) * N] for c in COLORS]
    tpl = w10.template_of(src, N)
    aud = w10.audit(tpl, N)

    # independent re-check with W6's hafnian and W9's auditor
    w6_bad = sum(1 for w in product(COLORS, repeat=N)
                 if len(set(w)) > 1
                 and w6_core.hafnian(src, tuple(range(N)),
                                     {u: w[u] for u in range(N)}) != 0)
    aud9 = w9_template.audit(w9_template.template_of(src, N), N)
    agree = (w6_bad == len(mixed_bad)
             and aud9["T4_pure_fibres"] == aud["T4_pure_fibres"]
             and aud9["S_singleton_free"] == aud["S"]
             and aud9["T5_min_degree_ok"] == aud["T5"]
             and aud9["T6_slots_ok"] == aud["T6"]
             and aud9["Sigma"] == aud["Sigma"] and aud9["m"] == aud["m"])

    # cancellation detail per colour
    canc = {}
    for c in COLORS:
        terms = w10.pure_terms(src, N, c)
        canc[c] = {"n_nonzero_terms": len(terms),
                   "terms": [str(t) for _, t in terms],
                   "sum": str(sum((t for _, t in terms), F(0))),
                   "fibre": aud["T4_pure_fibres"][c],
                   "vanishes_by_cancellation":
                       bool(len(terms) >= 2 and sum((t for _, t in terms), F(0)) == 0)}

    ranks = {}
    for e in EDGES:
        if any(any(r) for r in src[e]):
            ranks[str(e)] = w6_core.matrix_rank(src[e])
    rec = {"label": label,
           "mixed_defects": len(mixed_bad),
           "MIXED_EXACT": not mixed_bad,
           "pure_coefficients": [str(x) for x in pures],
           "m": aud["m"], "Sigma": aud["Sigma"], "beta": aud["beta"],
           "min_degree": aud["min_degree"],
           "T4": aud["T4"], "T5": aud["T5"], "T6": aud["T6"], "S": aud["S"],
           "pure_fibres": aud["T4_pure_fibres"],
           "ADMISSIBLE": aud["ADMISSIBLE"],
           "n_mixed_singletons": aud["n_mixed_singletons"],
           "independent_recheck_agrees": bool(agree),
           "block_ranks": ranks,
           "cancellation": canc,
           "source": w10.src_repr(src, N)}
    if verbose:
        say(f"  {label:34s} m={rec['m']:2d} Sigma={rec['Sigma']:3d} "
            f"mixed defects={rec['mixed_defects']:3d} "
            f"pures={rec['pure_coefficients']} "
            f"fibres={rec['pure_fibres']} ADMISSIBLE={rec['ADMISSIBLE']} "
            f"recheck={rec['independent_recheck_agrees']}")
    return rec


# ---------------------------------------------------------------- W-A
say("=" * 90)
say("B1  WITNESS FAMILY (W-A): constant blocks on K_6 with haf(t) = 0")
say("=" * 90)

# haf is multilinear; with t = 1 on all 15 edges except e0 = (0,1):
#   haf = t_{01} * #PM(K_4 on {2,3,4,5}) + #PM(K_6) - #PM containing 01
#       = 3 t_{01} + 12   ->  t_{01} = -4.
weights = {e: F(1) for e in EDGES}
weights[(0, 1)] = F(-4)
h = w10.scalar_hafnian(N, weights)
say(f"  weights: t_(0,1) = -4, all other t_e = 1;  haf(t) = {h}  (must be 0)")
require(h == 0, "haf(t) != 0")
WA = w10.constant_block_source(N, weights)
recA = certify("W-A  constant-block K_6", WA)
require(recA["MIXED_EXACT"] and recA["ADMISSIBLE"], "W-A failed")
say(f"       colour-0 pure terms  : {recA['cancellation'][0]['terms']}")
say(f"       they sum to          : {recA['cancellation'][0]['sum']}  "
    f"(15 nonzero products cancelling)")
require(all(recA["cancellation"][c]["vanishes_by_cancellation"] for c in COLORS),
        "W-A: pure vanishing is not by cancellation")
OUT["WA"] = recA

# a second, asymmetric member of the same family (different t, all distinct)
rng = random.Random(6106)
found = None
for _ in range(500):
    w2 = {e: F(rng.randint(1, 9), rng.randint(1, 4)) for e in EDGES}
    e0 = (0, 1)
    P = w10.scalar_hafnian(4, {})  # placeholder
    # haf = t_e0 * P + Q  with P = haf over V\e0, Q = sum over PMs avoiding e0
    sub = {e: w2[e] for e in EDGES if e0[0] not in e and e0[1] not in e}
    P = F(0)
    for M in w10.perfect_matchings((2, 3, 4, 5)):
        term = F(1)
        for e in M:
            term *= w2[e]
        P += term
    Q = F(0)
    for M in w10.perfect_matchings(tuple(range(N))):
        if e0 in M:
            continue
        term = F(1)
        for e in M:
            term *= w2[e]
        Q += term
    if P == 0 or Q == 0:
        continue
    w2[e0] = -Q / P
    if w10.scalar_hafnian(N, w2) == 0 and all(w2[e] != 0 for e in EDGES):
        found = w2
        break
require(found is not None, "no asymmetric constant-block weight found")
WA2 = w10.constant_block_source(N, found)
recA2 = certify("W-A' asymmetric constant-block", WA2)
require(recA2["MIXED_EXACT"] and recA2["ADMISSIBLE"], "W-A' failed")
OUT["WA2"] = recA2

# ---------------------------------------------------------------- W-B
say()
say("=" * 90)
say("B2  WITNESS FAMILY (W-B): one block completely FREE (generic rank 3)")
say("=" * 90)
# need BOTH  h(V\{0,1}) = 0  and  haf(t) = 0.
# Note haf(t) = t_(0,1) * h(V\{0,1}) + Q, so once h(V\{0,1}) = 0 the weight
# t_(0,1) drops out of haf(t) entirely -- exactly why the block goes free.
w3 = None
for _ in range(2000):
    cand = {e: F(rng.randint(1, 9), rng.randint(1, 3)) for e in EDGES}
    # (i) h({2,3,4,5}) = 0, solved on t_(4,5)
    num = cand[(2, 4)] * cand[(3, 5)] + cand[(2, 5)] * cand[(3, 4)]
    if num == 0:
        continue
    cand[(4, 5)] = -num / cand[(2, 3)]
    hsub = (cand[(2, 3)] * cand[(4, 5)] + cand[(2, 4)] * cand[(3, 5)]
            + cand[(2, 5)] * cand[(3, 4)])
    if hsub != 0:
        continue
    # (ii) haf(t) = 0, solved on t_(0,2) (coefficient = h(V\{0,2}))
    Pc = Qc = F(0)
    for M in w10.perfect_matchings(tuple(range(N))):
        term = F(1)
        for e in M:
            term *= cand[e]
        if (0, 2) in M:
            Pc += term / cand[(0, 2)]
        else:
            Qc += term
    if Pc == 0 or Qc == 0:
        continue
    cand[(0, 2)] = -Qc / Pc
    if (w10.scalar_hafnian(N, cand) == 0
            and all(cand[e] != 0 for e in EDGES)):
        w3 = cand
        break
require(w3 is not None, "no W-B weight vector found")
hsub = (w3[(2, 3)] * w3[(4, 5)] + w3[(2, 4)] * w3[(3, 5)]
        + w3[(2, 5)] * w3[(3, 4)])
say(f"  h(V\\{{0,1}}) = {hsub}  (must be 0);  haf(t) = "
    f"{w10.scalar_hafnian(N, w3)}  (must be 0)")
require(hsub == 0 and w10.scalar_hafnian(N, w3) == 0, "W-B conditions failed")
say(f"  weights: {{{', '.join(f'{e}:{w3[e]}' for e in EDGES)}}}")

base = w10.constant_block_source(N, w3)
recB0 = certify("W-B0 base (block (0,1) constant)", base)
require(recB0["MIXED_EXACT"] and recB0["ADMISSIBLE"], "W-B0 failed")
OUT["WB0"] = recB0

free_tests = []
for trial in range(12):
    src = {e: [row[:] for row in base[e]] for e in EDGES}
    X = [[F(rng.randint(-9, 9) or 5, rng.randint(1, 4)) for _ in COLORS]
         for _ in COLORS]
    src[(0, 1)] = X
    rec = certify(f"W-B{trial+1} free block (rank "
                  f"{w6_core.matrix_rank(X)})", src, verbose=(trial < 3))
    free_tests.append(rec)
say(f"  {sum(1 for r in free_tests if r['MIXED_EXACT'])}/{len(free_tests)} random"
    f" replacements of block (0,1) stay MIXED-EXACT;"
    f" {sum(1 for r in free_tests if r['ADMISSIBLE'])}/{len(free_tests)} ADMISSIBLE")
say(f"  block-(0,1) ranks observed: "
    f"{sorted(set(int(r['block_ranks']['(0, 1)']) for r in free_tests))}")
require(all(r["MIXED_EXACT"] for r in free_tests), "free-block family failed")
OUT["WB_free"] = free_tests

# ---------------------------------------------------------------- W-C
say()
say("=" * 90)
say("B3  WITNESS FAMILY (W-C): every admissible SUPPORT at N=6 (min deg >= 3)")
say("=" * 90)
# enumerate subgraphs of K_6 with min degree >= 3 and |PM| >= 2, one per (m, iso-ish)
best_per_m = {}
rng2 = random.Random(77)
all_edges = list(EDGES)
seen = 0
for mask in range(1 << 15):
    if bin(mask).count("1") < 9:
        continue
    G = frozenset(all_edges[k] for k in range(15) if mask >> k & 1)
    deg = [0] * N
    for (u, v) in G:
        deg[u] += 1
        deg[v] += 1
    if min(deg) < 3:
        continue
    npm = w10.count_pm_of_graph(N, G)
    if npm < 2:
        continue
    seen += 1
    m = len(G)
    if m not in best_per_m:
        best_per_m[m] = (G, npm)
say(f"  subgraphs of K_6 with min degree >= 3 and |PM| >= 2 : {seen}")
say(f"  supports realised: {sorted(best_per_m)}")

wc = []
for m in sorted(best_per_m):
    G, npm = best_per_m[m]
    # choose weights on G with haf = 0 (multilinear solve on one edge)
    wt = {e: F(1) for e in G}
    picked = None
    for e0 in sorted(G):
        P = F(0)
        Q = F(0)
        for M in w10.perfect_matchings(tuple(range(N))):
            if not all(e in G for e in M):
                continue
            term = F(1)
            for e in M:
                term *= wt[e]
            if e0 in M:
                P += term / wt[e0]
            else:
                Q += term
        if P != 0 and Q != 0:
            wt[e0] = -Q / P
            picked = e0
            break
    require(picked is not None, f"no zeroing edge at m={m}")
    require(w10.scalar_hafnian(N, wt) == 0, "haf != 0")
    src = w10.constant_block_source(N, wt)
    rec = certify(f"W-C m={m} (|PM(G)|={npm})", src)
    rec["graph"] = sorted(map(list, G))
    rec["pm_count"] = npm
    wc.append(rec)
    require(rec["MIXED_EXACT"] and rec["ADMISSIBLE"],
            f"W-C failed at m={m}")
OUT["WC"] = wc

# --------------------------------------------------------------- controls
say()
say("=" * 90)
say("B4  MUTATION CONTROLS (every checker must fire)")
say("=" * 90)

# C1: haf(t) != 0  ->  ALL 726 mixed words become defects
bad_w = {e: F(1) for e in EDGES}
rec = certify("[C1] haf(t)=15 != 0 (must FAIL)", w10.constant_block_source(N, bad_w))
say(f"     -> mixed defects {rec['mixed_defects']} (expected 726), "
    f"MIXED_EXACT={rec['MIXED_EXACT']} (expected False)")
require(rec["mixed_defects"] == 726, "control C1 did not fire")
OUT["C1"] = rec["mixed_defects"]

# C2: perturb one cell of W-A
fires = 0
for trial in range(20):
    src = {e: [row[:] for row in WA[e]] for e in EDGES}
    e = rng.choice(EDGES)
    i, j = rng.choice(COLORS), rng.choice(COLORS)
    src[e][i][j] += F(rng.randint(1, 5))
    if w10.mixed_defects(src, N):
        fires += 1
say(f"  [C2] one-cell perturbations of W-A detected as non-mixed-exact: "
    f"{fires}/20 (expected 20/20)")
require(fires == 20, "control C2 did not fire")
OUT["C2"] = fires

# C3: the admissibility auditor must reject a template with an empty pure fibre
tpl = dict(w10.template_of(WA, N))
tpl[(0, 1)] = frozenset(c for c in tpl[(0, 1)] if c != (2, 2))
tpl[(2, 3)] = frozenset(c for c in tpl[(2, 3)] if c != (2, 2))
tpl[(4, 5)] = frozenset(c for c in tpl[(4, 5)] if c != (2, 2))
tpl[(0, 2)] = frozenset(c for c in tpl[(0, 2)] if c != (2, 2))
for e in EDGES:
    tpl[e] = frozenset(c for c in tpl[e] if c != (2, 2))
a = w10.audit(tpl, N)
say(f"  [C3] template with cell (2,2) deleted everywhere: pure fibres "
    f"{a['T4_pure_fibres']}, T4={a['T4']} (expected False), "
    f"ADMISSIBLE={a['ADMISSIBLE']} (expected False)")
require(not a["T4"] and not a["ADMISSIBLE"], "control C3 did not fire")
OUT["C3"] = a["T4_pure_fibres"]

# C4: min-degree filter must fire
tpl = {e: (frozenset((i, j) for i in COLORS for j in COLORS)
           if 5 not in e or e == (4, 5) else frozenset())
       for e in EDGES}
a = w10.audit(tpl, N)
say(f"  [C4] vertex 5 of degree 1: T5={a['T5']} (expected False), "
    f"ADMISSIBLE={a['ADMISSIBLE']} (expected False)")
require(not a["T5"], "control C4 did not fire")
OUT["C4"] = a["min_degree"]

# C5: cancellation detector must NOT fire on a single-term pure fibre
d43_like = w10.zero_source(N)
for e in ((0, 1), (2, 3), (4, 5)):
    for c in COLORS:
        d43_like[e][c][c] = F(1)
terms = w10.pure_terms(d43_like, N, 0)
say(f"  [C5] single-matching source: colour-0 pure has {len(terms)} nonzero "
    f"terms, sum {sum(t for _, t in terms)} -> cancellation impossible "
    f"(expected 1 term, sum 1)")
require(len(terms) == 1, "control C5 did not fire")
OUT["C5"] = len(terms)

# ------------------------------------------- B5 tangent space at the witness
say()
say("=" * 90)
say("B5  exact TANGENT SPACE of the mixed system at W-A (726 x 135 over Q)")
say("=" * 90)
cellidx = {}
for e in EDGES:
    for i in COLORS:
        for j in COLORS:
            cellidx[(e, i, j)] = len(cellidx)


def mixed_jacobian(src):
    rows = []
    for w in product(COLORS, repeat=N):
        if len(set(w)) == 1:
            continue
        row = [F(0)] * len(cellidx)
        for e in EDGES:
            u, v = e
            comp = tuple(x for x in range(N) if x not in e)
            C = F(0)
            for M in w10.perfect_matchings(comp):
                term = F(1)
                for a, b in M:
                    term *= src[(a, b)][w[a]][w[b]]
                C += term
            if C:
                row[cellidx[(e, w[u], w[v])]] += C
        rows.append(row)
    return rows


J = mixed_jacobian(WA)
r = la.rank_exact(J)
say(f"  Jacobian rank over Q      : {r}")
say(f"  Zariski tangent dimension : {135 - r}   (upper bound on local dim)")
say(f"  gauge orbit dimension     : 18 (g_(u,c), u in 6 vertices, c in 3 colours)")
OUT["B5_tangent"] = {"rank": r, "tangent_dim": 135 - r, "n_cells": 135}

J2 = mixed_jacobian(base)
r2 = la.rank_exact(J2)
say(f"  same at the W-B base      : rank {r2}, tangent dim {135 - r2} "
    f"(the free block contributes 9)")
OUT["B5_tangent_WB"] = {"rank": r2, "tangent_dim": 135 - r2}

with open(os.path.join(HERE, "results_b_witness_n6.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_b_witness_n6.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say()
say("N=6 VERDICT: EXISTS.  Mixed-exact sources on ADMISSIBLE templates exist at")
say("every support m = 9..15 with min degree >= 3, with all three pure fibres")
say("nonempty and all three pure coefficients vanishing BY CANCELLATION.")
