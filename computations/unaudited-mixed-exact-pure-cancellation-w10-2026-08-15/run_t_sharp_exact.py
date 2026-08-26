#!/usr/bin/env python3
"""W10 task T -- EXACT sharp N=6 witness, obtained by first FIXING the template.

Task S found a float point that is mixed-exact to 1e-15 but whose support is
not robust (cells at 1e-3..1e-7 that "want" to vanish).  Truncating to the
robust cells (|x| > 1e-2) gives a clean ADMISSIBLE template with Sigma = 54,
m = 13, pure fibres [1,2,2].  Here the mixed system is RE-SOLVED with that
template FIXED, and the solution is pushed to an exact witness over Q by the
one-block exact solve (H_w is linear in each block).
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

full = wn.System(N, d=3)
M = ((0, 1), (2, 3), (4, 5))
PT = {0: 1.0}
ANC = [(1, M), (2, M)]
say("=" * 96)
say("T  EXACT sharp N=6 witness on a fixed admissible template")
say("=" * 96)
rs = np.random.default_rng(99)
tpls = []
for t in range(600):
    x0 = rs.normal(size=full.nv) * (0.3 + 1.5 * rs.random())
    sol = least_squares(lambda x: full.residual(x, pure_targets=PT, anchors=ANC),
                        x0, jac=lambda x: full.jacobian(x, pure_targets=PT,
                                                        anchors=ANC),
                        method="lm", xtol=1e-15, ftol=1e-15, gtol=1e-15,
                        max_nfev=2000)
    if float(np.max(np.abs(sol.fun))) > 1e-13:
        continue
    for thr in (1e-2, 3e-2, 1e-1):
        src = w10.zero_source(N)
        for (e, i, j), idx in full.vidx.items():
            if abs(sol.x[idx]) > thr:
                src[e][i][j] = F(sol.x[idx]).limit_denominator(10 ** 9)
        a = w10.audit(w10.template_of(src, N), N)
        if a["ADMISSIBLE"] and a["T4_pure_fibres"][0] >= 1:
            tpls.append((w10.template_of(src, N), a, thr))
    if len(tpls) >= 12:
        break
say(f"  robust admissible templates harvested: {len(tpls)} "
    f"(Sigma {sorted(set(a['Sigma'] for _, a, _ in tpls))})")
require(tpls, "no robust admissible template")

found = None
for tpl, aud, thr in tpls:
    sysT = wn.System(N, d=3, template=tpl)
    rs2 = np.random.default_rng(7)
    hit = None
    for t in range(600):
        x0 = rs2.normal(size=sysT.nv) * (0.3 + 1.5 * rs2.random())
        sol = least_squares(lambda x: sysT.residual(x, pure_targets=PT), x0,
                            jac=lambda x: sysT.jacobian(x, pure_targets=PT),
                            method="lm", xtol=1e-15, ftol=1e-15, gtol=1e-15,
                            max_nfev=2000)
        c = float(np.max(np.abs(sol.fun)))
        mn = float(np.min(np.abs(sol.x)))
        if c < 1e-13 and mn > 1e-3:
            hit = sol.x.copy()
            break
    if hit is None:
        continue
    say(f"  template Sigma={aud['Sigma']} m={aud['m']} fibres "
        f"{aud['T4_pure_fibres']}: float solution found (min |cell| "
        f"{float(np.min(np.abs(hit))):.2e}); exactifying...")
    for denom in (10, 50, 200, 10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6):
        for e0 in EDGES:
            if not tpl[e0]:
                continue
            src = w10.zero_source(N)
            for (e, i, j), idx in sysT.vidx.items():
                if e != e0:
                    src[e][i][j] = F(hit[idx]).limit_denominator(denom)
            u0, v0 = e0
            comp = tuple(z for z in range(N) if z not in e0)
            rows, rhs = [], []
            for w in product(COLORS, repeat=N):
                mixed = len(set(w)) > 1
                if not mixed and w[0] != 0:
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
                rhs.append((F(1) if not mixed else F(0)) - D)
            solu = la.solve_exact(rows, rhs, 9)
            if solu is None:
                continue
            cand = {e: [r[:] for r in src[e]] for e in EDGES}
            cand[e0] = [[solu[3 * i + j] for j in COLORS] for i in COLORS]
            if w10.mixed_defects(cand, N):
                continue
            pc = w10.pure_coefficients(cand, N)
            a2 = w10.audit(w10.template_of(cand, N), N)
            if a2["ADMISSIBLE"] and pc[0] != 0:
                found = (e0, denom, cand, pc, a2)
                break
        if found:
            break
    if found:
        break

if found:
    e0, denom, cand, pc, a2 = found
    say()
    say(f"  *** EXACT SHARP WITNESS *** (block {e0} solved over Q, rest at "
        f"denominator <= {denom})")
    say(f"    mixed defects 0/726 | pure coefficients {[str(v) for v in pc]}")
    say(f"    m={a2['m']} Sigma={a2['Sigma']} beta={a2['beta']} min degree "
        f"{a2['min_degree']} | fibres {a2['T4_pure_fibres']}")
    say(f"    T4 {a2['T4']} T5 {a2['T5']} T6 {a2['T6']} S {a2['S']} | "
        f"ADMISSIBLE {a2['ADMISSIBLE']}")
    canc = {}
    for c in COLORS:
        terms = w10.pure_terms(cand, N, c)
        tot = sum((t for _, t in terms), F(0))
        canc[str(c)] = {"n_nonzero_terms": len(terms), "sum": str(tot),
                        "terms": [str(t) for _, t in terms],
                        "by_cancellation": bool(len(terms) >= 2 and tot == 0)}
        say(f"    colour {c}: {len(terms)} nonzero products "
            f"{[str(t) for _, t in terms]} -> {tot}"
            f"{'   <-- CANCELLATION' if len(terms) >= 2 and tot == 0 else ''}")
    OUT["T_exact"] = {"block_solved": str(e0), "denominator": denom,
                      "pures": [str(v) for v in pc],
                      "audit": {k: v for k, v in a2.items()},
                      "cancellation": canc,
                      "source": w10.src_repr(cand, N)}
else:
    say("  not exactified at these denominators (reported as float-certified)")
    OUT["T_exact"] = None
with open(os.path.join(HERE, "results_t_sharp_exact.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_t_sharp_exact.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say("T DONE")
