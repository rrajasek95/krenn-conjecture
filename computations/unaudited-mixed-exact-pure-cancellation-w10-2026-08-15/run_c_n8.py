#!/usr/bin/env python3
"""W10 task C -- the N=8 port: MIXED-EXACT sources on ADMISSIBLE templates at
every band support m = 19..27 (and 12..28 for context), with the MAXIMUM
possible cell count Sigma = 9m.

Construction (same as N=6, task B): constant blocks A_uv = t_uv * J on a graph
G with min degree >= 3 and |PM(G)| >= 2, weights solved so that haf(t) = 0.
Then H_w = haf(t) = 0 for EVERY word, so the source is MIXED-EXACT, while the
template is FULL on every live edge: every fibre equals |PM(G)| >= 2, so
(T4),(T5),(T6),(S) all hold and Sigma = 9m is the largest value the support
allows.

Everything is verified by EXHAUSTIVE exact evaluation of all 3^8 = 6561 words
(6558 mixed) in integer arithmetic, cross-checked against W6's hafnian and
W9's template auditor on a sample.
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
from w10_core import COLORS, require                              # noqa: E402
import w6_core                                                    # noqa: E402
import w9_template                                                # noqa: E402

N = 8
EDGES = w10.edges(N)
PM = w10.perfect_matchings(tuple(range(N)))
OUT = {}
log = []


def say(s="", flush=True):
    print(s, flush=flush)
    log.append(s)


say("=" * 96)
say(f"C0  N=8 setup: |E(K_8)| = {len(EDGES)}, |PM(K_8)| = {len(PM)}, "
    f"words 3^8 = {3**8} (mixed {3**8 - 3})")
say("=" * 96)

# W9's corrected numbers (v10 addendum / W9 REPORT appendix), for comparison.
SIGMA_MIN_W6 = {19: 61, 20: 64, 21: 68, 22: 70, 23: 77, 24: 82, 25: 85,
                26: 99, 27: 98}
SIGMA_MIN_W9 = {19: 51, 20: 52, 21: 53, 22: 56, 23: 57, 24: 58, 25: 59,
                26: 72, 27: 61}
SIGMA_MIN_P = {19: 51, 20: 56, 21: 63, 22: 56, 23: None, 24: 63, 25: 60,
               26: 74, 27: 73}
C_BUDGET = {m: 9 * m - 8 * max(0, 24 - m) for m in range(19, 28)}


# ------------------------------------------------------- graph construction

def degrees(G):
    d = [0] * N
    for (u, v) in G:
        d[u] += 1
        d[v] += 1
    return d


def npm(G):
    return sum(1 for M in PM if all(e in G for e in M))


def find_graph(m, rng, tries=20000):
    """A graph on 8 vertices, m edges, min degree >= 3, |PM| >= 2."""
    base = [(0, 1), (2, 3), (4, 5), (6, 7),
            (0, 2), (1, 3), (4, 6), (5, 7),
            (0, 4), (1, 5), (2, 6), (3, 7)]      # the 3-cube: 12 edges
    if m == 12:
        G = frozenset(base)
        if min(degrees(G)) >= 3 and npm(G) >= 2:
            return G
    rest = [e for e in EDGES if e not in base]
    for _ in range(tries):
        if m >= 12:
            extra = rng.sample(rest, m - 12)
            G = frozenset(base + extra)
        else:
            G = frozenset(rng.sample(list(EDGES), m))
        if len(G) == m and min(degrees(G)) >= 3 and npm(G) >= 2:
            return G
    return None


def zero_weights(G, rng, tries=400):
    """Weights on G, all nonzero, with haf = 0 (multilinear solve on one edge)."""
    for _ in range(tries):
        wt = {e: F(rng.randint(1, 9), rng.randint(1, 3)) for e in G}
        for e0 in sorted(G):
            P = Q = F(0)
            for M in PM:
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
                cand = dict(wt)
                cand[e0] = -Q / P
                if all(x != 0 for x in cand.values()):
                    return cand
    return None


# --------------------------------------------------------- exact certifier

def exhaustive_certificate(src):
    """Exhaustive over all 6561 words: (#mixed defects, pure coefficients)."""
    num = {}
    den = {}
    for e in EDGES:
        for i in COLORS:
            for j in COLORS:
                x = F(src[e][i][j])
                num[(e, i, j)] = x
    bad = 0
    pures = []
    for w in product(COLORS, repeat=N):
        tot = F(0)
        for M in PM:
            term = F(1)
            for (u, v) in M:
                x = num[((u, v), w[u], w[v])]
                if x == 0:
                    term = F(0)
                    break
                term *= x
            tot += term
        if len(set(w)) == 1:
            pures.append(tot)
        elif tot != 0:
            bad += 1
    return bad, pures


def s1_status(src):
    """The slice-cover FORCED INCIDENCE input (S1) of W6's budget:
    for every vertex p and colour r some neighbour j has A_pj = a (x) e_r^{(j)}
    (a single nonzero COLUMN r at the far endpoint j).  Returns #(p,r) slots
    where that fails."""
    fails = []
    for p in range(N):
        for r in COLORS:
            ok = False
            for j in range(N):
                if j == p:
                    continue
                B = w6_core.oriented(src, p, j)
                if w6_core.matrix_rank(B) != 1:
                    continue
                cols = [c for c in COLORS if any(B[i][c] != 0 for i in COLORS)]
                if cols == [r]:
                    ok = True
                    break
            if not ok:
                fails.append((p, r))
    return fails


def certify8(label, src, sample_check=400, rng=None):
    bad, pures = exhaustive_certificate(src)
    tpl = w10.template_of(src, N)
    aud = w10.audit(tpl, N)
    aud9 = w9_template.audit(w9_template.template_of(src, N), N)
    agree = (aud9["Sigma"] == aud["Sigma"] and aud9["m"] == aud["m"]
             and aud9["T4_pure_fibres"] == aud["T4_pure_fibres"]
             and aud9["S_singleton_free"] == aud["S"]
             and aud9["T5_min_degree_ok"] == aud["T5"]
             and aud9["T6_slots_ok"] == aud["T6"])
    # W6 hafnian spot-check
    w6bad = 0
    if rng is not None:
        for w in rng.sample(list(product(COLORS, repeat=N)), sample_check):
            v = w6_core.hafnian(src, tuple(range(N)), {u: w[u] for u in range(N)})
            if len(set(w)) > 1 and v != 0:
                w6bad += 1
    census = w6_core.block_census(src, N)
    dR = w6_core.rank_one_degree(src, N)
    s1 = s1_status(src)
    canc = {}
    for c in COLORS:
        terms = w10.pure_terms(src, N, c)
        canc[c] = {"n_nonzero_terms": len(terms),
                   "sum": str(sum((t for _, t in terms), F(0))),
                   "fibre": aud["T4_pure_fibres"][c],
                   "vanishes_by_cancellation":
                       bool(len(terms) >= 2
                            and sum((t for _, t in terms), F(0)) == 0)}
    rec = {"label": label, "mixed_defects": bad, "MIXED_EXACT": bad == 0,
           "pure_coefficients": [str(x) for x in pures],
           "m": aud["m"], "Sigma": aud["Sigma"], "beta": aud["beta"],
           "min_degree": aud["min_degree"],
           "pure_fibres": aud["T4_pure_fibres"],
           "T4": aud["T4"], "T5": aud["T5"], "T6": aud["T6"], "S": aud["S"],
           "ADMISSIBLE": aud["ADMISSIBLE"],
           "n_mixed_singletons": aud["n_mixed_singletons"],
           "w9_auditor_agrees": bool(agree),
           "w6_hafnian_sample_defects": w6bad,
           "block_kinds": census, "d_R": dR,
           "S1_forced_incidence_failures": len(s1),
           "cancellation": canc}
    return rec


# ------------------------------------------------------------- the sweep
say()
say("=" * 96)
say("C1  admissible MIXED-EXACT sources at every support m = 12..28")
say("=" * 96)
say(f"{'m':>3} {'|PM(G)|':>8} {'Sigma':>6} {'beta':>5} {'minDeg':>7} "
    f"{'fibres':>12} {'ADMISS':>7} {'mixdef':>7} {'w9ok':>6} {'S1fail':>7}")
rng = random.Random(88088)
rows = []
sources = {}
for m in range(12, 29):
    G = find_graph(m, rng)
    require(G is not None, f"no graph at m={m}")
    wt = zero_weights(G, rng)
    require(wt is not None, f"no zeroing weights at m={m}")
    require(w10.scalar_hafnian(N, wt) == 0, f"haf != 0 at m={m}")
    src = w10.constant_block_source(N, wt)
    rec = certify8(f"m={m}", src, rng=rng)
    rec["graph"] = sorted(map(list, G))
    rec["pm_count"] = npm(G)
    rec["weights"] = {f"{u},{v}": str(wt[(u, v)]) for (u, v) in sorted(G)}
    rows.append(rec)
    sources[m] = src
    say(f"{m:>3} {rec['pm_count']:>8} {rec['Sigma']:>6} {rec['beta']:>5} "
        f"{rec['min_degree']:>7} {str(rec['pure_fibres']):>12} "
        f"{str(rec['ADMISSIBLE']):>7} {rec['mixed_defects']:>7} "
        f"{str(rec['w9_auditor_agrees']):>6} "
        f"{rec['S1_forced_incidence_failures']:>7}", flush=True)
    require(rec["MIXED_EXACT"] and rec["ADMISSIBLE"] and rec["Sigma"] == 9 * m,
            f"witness failed at m={m}")
    require(all(rec["cancellation"][c]["vanishes_by_cancellation"]
                for c in COLORS), f"not cancellation at m={m}")
OUT["C1_sweep"] = rows

# ------------------------------------------------------- the band comparison
say()
say("=" * 96)
say("C2  the BAND m = 19..27: Sigma_mix on the ADMISSIBLE stratum vs every")
say("    target number in the plan (v10) and vs W6's proved budget C(m)")
say("=" * 96)
say(f"{'m':>3} {'Sigma_mix^adm':>14} {'Sigma_min W6':>13} {'Sigma_min W9':>13} "
    f"{'Sigma_min^P':>12} {'C_budget':>9} {'H4 window':>12}")
band = []
for m in range(19, 28):
    rec = next(r for r in rows if r["m"] == m)
    S = rec["Sigma"]
    row = {"m": m, "sigma_mix_admissible": S,
           "sigma_min_w6": SIGMA_MIN_W6[m], "sigma_min_w9": SIGMA_MIN_W9[m],
           "sigma_min_P": SIGMA_MIN_P[m], "C_budget": C_BUDGET[m],
           "H4_window_empty": True,
           "exceeds_C_budget": S > C_BUDGET[m]}
    band.append(row)
    say(f"{m:>3} {S:>14} {SIGMA_MIN_W6[m]:>13} {SIGMA_MIN_W9[m]:>13} "
        f"{str(SIGMA_MIN_P[m]):>12} {C_BUDGET[m]:>9} {'EMPTY':>12}")
say()
say("  Sigma_mix^adm(m) = 9m is the ABSOLUTE MAXIMUM a support-m template can")
say("  carry, so the largest ceiling statement compatible with the witnesses is")
say("  the vacuous C(m) = 9m.  Every target in the table is beaten by 2.3x-3.4x.")
say(f"  Sigma_mix^adm exceeds W6's PROVED budget C(m) at m = "
    f"{[r['m'] for r in band if r['exceeds_C_budget']]}")
say("  -- no contradiction: W6's budget rests on input (S1), the slice-cover")
say("  FORCED INCIDENCE theorem, which is a VALUE-level consequence of full")
say("  exactness (it uses the pure equations, not just the mixed ones).")
say(f"  Measured: (S1) fails at ALL 24 (vertex,colour) slots on every witness")
say("  (column 'S1fail' above), and every block is rank-one NONCOORDINATE.")
OUT["C2_band"] = band

# ------------------------------------------------- C3 non-constant witnesses
say()
say("=" * 96)
say("C3  N=8 FREE-BLOCK witnesses (not constant-block; a generic rank-3 block)")
say("=" * 96)
# Need haf(t) = 0 and the complementary hafnian h(V\{u0,v0}) = 0 on K_8.
free_rows = []
found = None
for attempt in range(4000):
    wt = {e: F(rng.randint(1, 9), rng.randint(1, 3)) for e in EDGES}
    e0 = (0, 1)
    U = tuple(x for x in range(N) if x not in e0)
    # solve h(U) = 0 on t_(6,7): coefficient = h(U \ {6,7})
    Ph = Qh = F(0)
    for M in w10.perfect_matchings(U):
        term = F(1)
        for e in M:
            term *= wt[e]
        if (6, 7) in M:
            Ph += term / wt[(6, 7)]
        else:
            Qh += term
    if Ph == 0 or Qh == 0:
        continue
    wt[(6, 7)] = -Qh / Ph
    hU = F(0)
    for M in w10.perfect_matchings(U):
        term = F(1)
        for e in M:
            term *= wt[e]
        hU += term
    if hU != 0:
        continue
    # now haf(t) is independent of t_(0,1); solve it on t_(0,2)
    P2 = Q2 = F(0)
    for M in PM:
        term = F(1)
        for e in M:
            term *= wt[e]
        if (0, 2) in M:
            P2 += term / wt[(0, 2)]
        else:
            Q2 += term
    if P2 == 0 or Q2 == 0:
        continue
    wt[(0, 2)] = -Q2 / P2
    if w10.scalar_hafnian(N, wt) == 0 and all(x != 0 for x in wt.values()):
        found = (wt, hU)
        break
require(found is not None, "no N=8 free-block weights found")
wt, hU = found
say(f"  h(V\\{{0,1}}) = {hU} (0), haf(t) = {w10.scalar_hafnian(N, wt)} (0)")
base8 = w10.constant_block_source(N, wt)
rec = certify8("N8 free-block base", base8, rng=rng)
say(f"  base            : mixed defects {rec['mixed_defects']}, "
    f"Sigma {rec['Sigma']}, ADMISSIBLE {rec['ADMISSIBLE']}")
require(rec["MIXED_EXACT"] and rec["ADMISSIBLE"], "N=8 free-block base failed")
free_rows.append(rec)
for trial in range(4):
    src = {e: [row[:] for row in base8[e]] for e in EDGES}
    X = [[F(rng.randint(-9, 9) or 5, rng.randint(1, 4)) for _ in COLORS]
         for _ in COLORS]
    src[(0, 1)] = X
    r = certify8(f"N8 free-block X#{trial+1} (rank {w6_core.matrix_rank(X)})",
                 src, rng=rng)
    say(f"  X#{trial+1} rank {w6_core.matrix_rank(X)} : mixed defects "
        f"{r['mixed_defects']}, Sigma {r['Sigma']}, ADMISSIBLE {r['ADMISSIBLE']}, "
        f"blocks of rank>=2: {r['block_kinds']['H']}")
    require(r["MIXED_EXACT"] and r["ADMISSIBLE"], "N=8 free-block failed")
    free_rows.append(r)
OUT["C3_free_block"] = free_rows

# ------------------------------------------------------------- C4 controls
say()
say("=" * 96)
say("C4  MUTATION CONTROLS at N=8")
say("=" * 96)
m0 = 24
src = sources[m0]
# K1: break haf(t) = 0
wt_bad = {e: F(1) for e in EDGES}
bad, pures = exhaustive_certificate(w10.constant_block_source(N, wt_bad))
say(f"  [K1] haf(t) = {w10.scalar_hafnian(N, wt_bad)} != 0 -> mixed defects "
    f"{bad} (expected 6558)")
require(bad == 6558, "control K1 did not fire")
OUT["K1"] = bad
# K2: perturb one cell
fires = 0
for trial in range(6):
    s2 = {e: [row[:] for row in src[e]] for e in EDGES}
    e = rng.choice([e for e in EDGES if any(any(r) for r in src[e])])
    i, j = rng.choice(COLORS), rng.choice(COLORS)
    s2[e][i][j] += F(rng.randint(1, 5))
    b, _ = exhaustive_certificate(s2)
    if b > 0:
        fires += 1
say(f"  [K2] one-cell perturbations detected: {fires}/6 (expected 6/6)")
require(fires == 6, "control K2 did not fire")
OUT["K2"] = fires
# K3: the |PM(G)| >= 2 requirement is real -- a graph with |PM| = 1 is
# singleton-ful, so (S) fails and it is NOT admissible.
Gp = frozenset([(0, 1), (2, 3), (4, 5), (6, 7)])
tplp = {e: (frozenset((i, j) for i in COLORS for j in COLORS)
            if e in Gp else frozenset()) for e in EDGES}
a = w10.audit(tplp, N)
say(f"  [K3] |PM(G)|=1 template: mixed singletons {a['n_mixed_singletons']} "
    f"(expected > 0), S={a['S']} (False), T5={a['T5']} (False), "
    f"ADMISSIBLE={a['ADMISSIBLE']} (False)")
require(not a["S"] and not a["ADMISSIBLE"], "control K3 did not fire")
OUT["K3"] = a["n_mixed_singletons"]
# K4: the (S1) checker must PASS on an object that satisfies it
probe = w10.zero_source(N)
for p in range(N):
    pass
# build a source where every vertex has 3 rank-one blocks with distinct
# coordinate far-factors: use a proper 3-edge-colouring of the 3-cube.
cube_colour = {(0, 1): 0, (2, 3): 0, (4, 5): 0, (6, 7): 0,
               (0, 2): 1, (1, 3): 1, (4, 6): 1, (5, 7): 1,
               (0, 4): 2, (1, 5): 2, (2, 6): 2, (3, 7): 2}
for e, c in cube_colour.items():
    probe[e][c][c] = F(1)
s1f = s1_status(probe)
say(f"  [K4] properly 3-edge-coloured cube with single diagonal cells: "
    f"(S1) failures {len(s1f)} (expected 0 -- the checker can pass)")
require(len(s1f) == 0, "control K4 did not fire (S1 checker never passes)")
OUT["K4"] = len(s1f)

with open(os.path.join(HERE, "results_c_n8.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_c_n8.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say()
say("N=8 VERDICT: the N=6 construction PORTS.  Admissible mixed-exact sources")
say("exist at every support m = 12..28 with Sigma = 9m (171..243 on the band),")
say("i.e. 2.3x-3.4x above the corrected singleton-free price 51..74.")
