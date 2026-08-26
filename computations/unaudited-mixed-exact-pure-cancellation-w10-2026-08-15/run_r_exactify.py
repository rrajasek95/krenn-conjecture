#!/usr/bin/env python3
"""W10 task R -- EXACTIFY the sharp N=6 object of task Q by STAR LINEARISATION.

Every H_w is LINEAR in the star at a fixed vertex p (the five blocks A_pq,
45 cells), because every perfect matching uses exactly one edge at p:
    H_w = sum_{q != p} A_pq[w_p][w_q] * C_q(w),   C_q(w) = H_{V\{p,q}}(w).
So: rationalise the OFF-STAR sub-source (the 10 blocks on V\{p}) at the float
hit, then solve the 726 mixed equations + H_{0^6} = 1 for the 45 star
coordinates EXACTLY over Q.  If the linear system is consistent and the
resulting template is admissible, the object is certified exactly.
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
rs = np.random.default_rng(2024)
say("=" * 96)
say("R  exactify: mixed-exact at N=6, H_{0^6}=1, all three pure fibres nonempty")
say("=" * 96)
hits = []
for t in range(900):
    x0 = rs.normal(size=s.nv) * (0.3 + 1.5 * rs.random())
    sol = least_squares(lambda x: s.residual(x, pure_targets=PT, anchors=ANC),
                        x0, jac=lambda x: s.jacobian(x, pure_targets=PT,
                                                     anchors=ANC),
                        method="lm", xtol=1e-15, ftol=1e-15, gtol=1e-15,
                        max_nfev=2000)
    if float(np.max(np.abs(sol.fun))) < 1e-12:
        src = w10.zero_source(N)
        for (e, i, j), idx in s.vidx.items():
            if abs(sol.x[idx]) > 1e-7:
                src[e][i][j] = F(sol.x[idx]).limit_denominator(10 ** 9)
        a = w10.audit(w10.template_of(src, N), N)
        if a["ADMISSIBLE"]:
            hits.append((sol.x.copy(), a))
            if len(hits) >= 40:
                break
say(f"  [SEARCH] admissible float hits: {len(hits)} "
    f"(Sigma range {min(a['Sigma'] for _, a in hits)}..{max(a['Sigma'] for _, a in hits)})")
require(hits, "no admissible hit")

STAR_IDX = {}
def star_system(x, p, denom, tol=1e-7):
    """Rationalise the off-star; return (rows, rhs, off) for the 45 star cells."""
    off = w10.zero_source(N)
    for (e, i, j), idx in s.vidx.items():
        if p in e:
            continue
        if abs(x[idx]) > tol:
            off[e][i][j] = F(x[idx]).limit_denominator(denom)
    cols = {}
    for q in range(N):
        if q == p:
            continue
        for i in COLORS:
            for j in COLORS:
                cols[(q, i, j)] = len(cols)
    rows, rhs = [], []
    for w in product(COLORS, repeat=N):
        mixed = len(set(w)) > 1
        if not mixed and w[0] != 0:
            continue
        row = [F(0)] * 45
        for q in range(N):
            if q == p:
                continue
            comp = tuple(z for z in range(N) if z not in (p, q))
            C = F(0)
            for Mm in w10.perfect_matchings(comp):
                term = F(1)
                for a1, b1 in Mm:
                    term *= off[(a1, b1)][w[a1]][w[b1]]
                C += term
            row[cols[(q, w[p], w[q])]] += C
        rows.append(row)
        rhs.append(F(0) if mixed else F(1))
    return rows, rhs, off, cols

found = None
for denom in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7):
    for hidx, (x, aud) in enumerate(hits):
        for p in range(N):
            rows, rhs, off, cols = star_system(x, p, denom)
            sol = la.solve_exact(rows, rhs, 45)
            if sol is None:
                continue
            cand = {e: [r[:] for r in off[e]] for e in EDGES}
            for (q, i, j), k in cols.items():
                u, v = (p, q) if p < q else (q, p)
                if p < q:
                    cand[(u, v)][i][j] = sol[k]
                else:
                    cand[(u, v)][j][i] = sol[k]
            if w10.mixed_defects(cand, N):
                continue
            pc = w10.pure_coefficients(cand, N)
            a = w10.audit(w10.template_of(cand, N), N)
            if a["ADMISSIBLE"] and pc[0] != 0:
                found = (denom, hidx, p, cand, pc, a)
                break
        if found:
            break
    if found:
        break

if found:
    denom, hidx, p, cand, pc, a = found
    say(f"  EXACT WITNESS: star at vertex {p} solved over Q "
        f"(off-star rationalised at denominator <= {denom}, hit #{hidx})")
    say(f"    mixed defects 0/726 | pures {[str(v) for v in pc]}")
    say(f"    m={a['m']} Sigma={a['Sigma']} beta={a['beta']} "
        f"fibres {a['T4_pure_fibres']} | T4 {a['T4']} T5 {a['T5']} T6 {a['T6']} "
        f"S {a['S']} | ADMISSIBLE {a['ADMISSIBLE']}")
    canc = {}
    for c in COLORS:
        terms = w10.pure_terms(cand, N, c)
        tot = sum((t for _, t in terms), F(0))
        canc[c] = {"n_nonzero_terms": len(terms), "sum": str(tot),
                   "terms": [str(t) for _, t in terms],
                   "by_cancellation": bool(len(terms) >= 2 and tot == 0)}
        say(f"    colour {c}: {len(terms)} nonzero matching products, "
            f"sum {tot}{'  <-- CANCELLATION' if len(terms)>=2 and tot==0 else ''}")
    OUT["R_exact"] = {"vertex": p, "denominator": denom,
                      "pures": [str(v) for v in pc],
                      "audit": {k: v for k, v in a.items()
                                if k != "mixed_fibre_histogram"},
                      "cancellation": canc,
                      "source": w10.src_repr(cand, N)}
else:
    say("  no consistent star solve found -- reported as NOT exactified")
    OUT["R_exact"] = None
OUT["R_float_hits"] = [{k: v for k, v in a.items()
                        if k != "mixed_fibre_histogram"} for _, a in hits[:10]]
with open(os.path.join(HERE, "results_r_exactify.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_r_exactify.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say("R DONE")
