#!/usr/bin/env python3
"""W10 task Q -- the SHARP form of the W10 object at N=6:
a MIXED-EXACT source with a NONZERO pure coefficient (H_{0^6} = 1) whose other
two pure FIBRES are NONEMPTY, so that H_{1^6} and H_{2^6} vanish BY
CANCELLATION while the source is genuinely close to exact.

Task D found this system solvable (181/1500 float starts hit machine
precision).  Here the hits are extracted, audited, and pushed to an EXACT
witness over Q: the mixed system is LINEAR in each 3x3 block separately, so
after rationalising all but one block the remaining block is solved EXACTLY.
"""
from __future__ import annotations
import json, os, sys
from fractions import Fraction as F
from itertools import product
import numpy as np
from scipy.optimize import least_squares
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w10_core as w10                                            # noqa: E402
import w10_numeric as wn                                          # noqa: E402
import w10_linalg as la                                           # noqa: E402
from w10_core import COLORS, require                              # noqa: E402

N = 6
EDGES = w10.edges(N)
log = []; OUT = {}
def say(s="", flush=True):
    print(s, flush=flush); log.append(s)

s = wn.System(N, d=3)
M = ((0, 1), (2, 3), (4, 5))
PT = {0: 1.0}
ANC = [(1, M), (2, M)]
rs = np.random.default_rng(777)
hits = []
say("=" * 96)
say("Q  MIXED-EXACT at N=6 with H_{0^6}=1 and both other pure fibres nonempty")
say("=" * 96)
for t in range(600):
    x0 = rs.normal(size=s.nv) * (0.3 + 1.5 * rs.random())
    sol = least_squares(lambda x: s.residual(x, pure_targets=PT, anchors=ANC),
                        x0, jac=lambda x: s.jacobian(x, pure_targets=PT,
                                                     anchors=ANC),
                        method="lm", xtol=1e-15, ftol=1e-15, gtol=1e-15,
                        max_nfev=2000)
    c = float(np.max(np.abs(sol.fun)))
    if c < 1e-12:
        hits.append(sol.x.copy())
        if len(hits) >= 25:
            break
say(f"  [SEARCH] float hits collected: {len(hits)} (residual < 1e-12)")
require(hits, "no hit")

# ---- audit the achieved templates -------------------------------------
say()
say("  achieved templates (cells |x| > 1e-7):")
best = None
for k, x in enumerate(hits[:25]):
    src = w10.zero_source(N)
    for (e, i, j), idx in s.vidx.items():
        if abs(x[idx]) > 1e-7:
            src[e][i][j] = F(x[idx]).limit_denominator(10 ** 9)
    a = w10.audit(w10.template_of(src, N), N)
    score = (a["T4"], a["T5"], a["T6"], a["S"])
    if k < 6:
        say(f"    hit {k}: m={a['m']:2d} Sigma={a['Sigma']:3d} beta={a['beta']:2d} "
            f"fibres {a['T4_pure_fibres']} T4 {a['T4']} T5 {a['T5']} T6 {a['T6']} "
            f"S {a['S']} ADMISSIBLE {a['ADMISSIBLE']}")
    if best is None or sum(score) > best[0]:
        best = (sum(score), k, x, a)
say(f"  best admissibility score among {len(hits)} hits: {best[0]}/4 "
    f"(hit {best[1]}, ADMISSIBLE {best[3]['ADMISSIBLE']})")
OUT["Q_hits"] = {"n_hits": len(hits),
                 "best_audit": {kk: vv for kk, vv in best[3].items()
                                if kk != "mixed_fibre_histogram"}}

# ---- EXACT witness: rationalise all blocks but one, solve that one over Q ---
say()
say("  EXACTIFICATION.  H_w is LINEAR in each block, so fix 14 blocks at exact")
say("  rationals near the float hit and solve the 15th block's 9 cells over Q.")
x = best[2]
found_exact = None
for denom in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6):
    for e0 in EDGES:
        src = w10.zero_source(N)
        for (e, i, j), idx in s.vidx.items():
            if e == e0:
                continue
            src[e][i][j] = F(x[idx]).limit_denominator(denom)
        # equations: for each mixed word w, A_e0[w_u][w_v]*C(w) + D(w) = 0
        u0, v0 = e0
        comp = tuple(z for z in range(N) if z not in e0)
        rows = []
        rhs = []
        for w in product(COLORS, repeat=N):
            if len(set(w)) == 1:
                continue
            C = F(0)
            for Mm in w10.perfect_matchings(comp):
                term = F(1)
                for a1, b1 in Mm:
                    term *= src[(a1, b1)][w[a1]][w[b1]]
                C += term
            D = F(0)
            for Mm in w10.perfect_matchings(tuple(range(N))):
                if e0 in Mm:
                    continue
                term = F(1)
                for a1, b1 in Mm:
                    term *= src[(a1, b1)][w[a1]][w[b1]]
                D += term
            row = [F(0)] * 9
            row[3 * w[u0] + w[v0]] = C
            rows.append(row)
            rhs.append(-D)
        solu = la.solve_exact(rows, rhs, 9)
        if solu is None:
            continue
        cand = {e: [r[:] for r in src[e]] for e in EDGES}
        cand[e0] = [[solu[3 * i + j] for j in COLORS] for i in COLORS]
        if w10.mixed_defects(cand, N):
            continue
        pc = w10.pure_coefficients(cand, N)
        a = w10.audit(w10.template_of(cand, N), N)
        found_exact = (e0, denom, cand, pc, a)
        break
    if found_exact:
        break

if found_exact:
    e0, denom, cand, pc, a = found_exact
    say(f"  EXACT witness found: solved block {e0} over Q (others rationalised "
        f"at denominator <= {denom})")
    say(f"    mixed defects 0/726 | pures {[str(v) for v in pc]}")
    say(f"    m={a['m']} Sigma={a['Sigma']} beta={a['beta']} "
        f"fibres {a['T4_pure_fibres']} | T4 {a['T4']} T5 {a['T5']} T6 {a['T6']} "
        f"S {a['S']} | ADMISSIBLE {a['ADMISSIBLE']}")
    canc = {}
    for c in COLORS:
        terms = w10.pure_terms(cand, N, c)
        tot = sum((t for _, t in terms), F(0))
        canc[c] = {"n_terms": len(terms), "sum": str(tot)}
        say(f"    colour {c}: {len(terms)} nonzero matching products, sum {tot}")
    OUT["Q_exact"] = {"block_solved": str(e0), "denominator": denom,
                      "pures": [str(v) for v in pc],
                      "audit": {k: v for k, v in a.items()
                                if k != "mixed_fibre_histogram"},
                      "cancellation": canc,
                      "source": w10.src_repr(cand, N)}
else:
    say("  EXACTIFICATION: no consistent one-block solve found at these "
        "denominators (the float hit is on a positive-dimensional stratum; "
        "reported as NOT exactified).")
    OUT["Q_exact"] = None

with open(os.path.join(HERE, "results_q_onepure.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_q_onepure.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say("Q DONE")
