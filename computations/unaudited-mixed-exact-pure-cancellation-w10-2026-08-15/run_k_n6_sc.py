#!/usr/bin/env python3
"""W10 task K -- the layer-2 question at SIX sites, where it is cheap:

  ADM+ (N=6) := (T4) + (T5) + (T6) + (S) + (SC)

K1  Is ADM+ nonempty at N=6?  Exhaustive-ish randomised template search over
    m = 9..15 (integer objective; every hit re-audited exactly).
    Counting note: an edge serves at most 2 (vertex,colour) demands and only
    if it is a SINGLE cell, so beta >= 3N - m = 18 - m is forced by (SC).
K2  If ADM+ is nonempty, does a MIXED-EXACT source live on such a template?
    (FLOAT SEARCH with analytic Jacobian; hits re-verified exactly.)
    Positive control: the same solver on a task-B witness template.
"""
from __future__ import annotations
import json, os, random, sys
from fractions import Fraction as F
import numpy as np
from scipy.optimize import least_squares
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (HERE, os.path.join(REPO, "computations",
                             "unaudited-template-kill-w8-2026-08-15")):
    if p not in sys.path:
        sys.path.insert(0, p)
import w10_core as w10                                            # noqa: E402
import w10_numeric as wn                                          # noqa: E402
from w10_core import COLORS, require                              # noqa: E402
import w8_core as w8                                              # noqa: E402

N = 6
EDGES = w10.edges(N)
GEO = w8.geometry(N)
OUT = {}; log = []
def say(s="", flush=True):
    print(s, flush=flush); log.append(s)

def masks_of(tpl):
    out = []
    for e in EDGES:
        mk = 0
        for (i, j) in tpl[e]:
            mk |= 1 << (3 * i + j)
        out.append(mk)
    return out

def cost(masks):
    tpl = {EDGES[n]: frozenset(w8.cells(masks[n])) for n in range(len(EDGES))}
    a = w10.audit(tpl, N)
    fd = w8.fie_demands(GEO, masks)
    unserved = sum(1 for k, v in fd.items() if not v)
    miss = sum(1 for x in a["T4_pure_fibres"] if x == 0)
    return (10 * miss + 10 * unserved + 5 * max(0, 3 - a["min_degree"])
            + 5 * (3 * N - a["slots_covered"]) + a["n_mixed_singletons"]), a

def anneal(m, seed, steps=20000):
    rng = random.Random(seed)
    live = rng.sample(range(len(EDGES)), m)
    masks = [0] * len(EDGES)
    for e in live:
        masks[e] = rng.randrange(1, 512)
    c, _ = cost(masks)
    best = None
    for step in range(steps):
        T = 3.0 * (1 - step / steps) + 0.02
        n = rng.choice(live)
        old = masks[n]
        r = rng.random()
        if r < 0.35:
            new = old ^ (1 << rng.randrange(9))
        elif r < 0.55:
            new = 1 << rng.randrange(9)                       # single cell
        elif r < 0.8:
            end = rng.randrange(2); col = rng.randrange(3); new = 0
            for k in range(3):
                if rng.random() < 0.7:
                    new |= 1 << ((3 * k + col) if end else (3 * col + k))
        else:
            new = rng.randrange(1, 512)
        if new == 0 or new == old:
            continue
        masks[n] = new
        c2, a2 = cost(masks)
        if c2 <= c or rng.random() < pow(2.718281828, -(c2 - c) / T):
            c = c2
            if c2 == 0 and (best is None or a2["Sigma"] < best[0]):
                best = (a2["Sigma"], list(masks))
        else:
            masks[n] = old
    return best

say("=" * 92)
say("K1  is ADM+ = (T4)+(T5)+(T6)+(S)+(SC) nonempty at N=6?   [SEARCH]")
say("=" * 92)
say(f"  counting note: (SC) forces beta >= 3N - m = 18 - m at six sites")
say(f"{'m':>3} {'min Sigma in ADM+':>18} {'beta':>5} {'18-m':>5}   re-audit")
found = {}
for m in range(9, 16):
    best = None
    for seed in range(10):
        b = anneal(m, 7000 * m + seed)
        if b is not None and (best is None or b[0] < best[0]):
            best = b
    if best is None:
        say(f"{m:>3} {'NOT FOUND':>18}")
        continue
    S, masks = best
    tpl = {EDGES[n]: frozenset(w8.cells(masks[n])) for n in range(len(EDGES))}
    a = w10.audit(tpl, N)
    ok = a["ADMISSIBLE"] and w8.fie_ok(GEO, masks) and a["Sigma"] == S
    say(f"{m:>3} {S:>18} {a['beta']:>5} {max(0,18-m):>5}   "
        f"{'OK' if ok else 'MISMATCH'} fibres {a['T4_pure_fibres']}")
    require(ok, f"K1 re-audit failed at m={m}")
    found[m] = tpl
OUT["K1"] = {str(m): {"Sigma": sum(len(v) for v in t.values()),
                      "template": {f"{u},{v}": sorted(map(list, t[(u, v)]))
                                   for (u, v) in EDGES if t[(u, v)]}}
             for m, t in found.items()}

say()
say("=" * 92)
say("K2  do those ADM+ templates carry a MIXED-EXACT source?   [FLOAT SEARCH]")
say("=" * 92)

def probe(label, tpl, starts=400, seed=5):
    s = wn.System(N, d=3, template=tpl)
    rs = np.random.default_rng(seed)
    best = None; hits = 0
    for t in range(starts):
        x0 = rs.normal(size=s.nv) * (0.4 + 1.6 * rs.random())
        sol = least_squares(lambda x: s.residual(x), x0,
                            jac=lambda x: s.jacobian(x), method="lm",
                            xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=2000)
        c = float(np.max(np.abs(sol.fun)))
        nz = int((np.abs(sol.x) > 1e-6).sum())
        if best is None or (c, -nz) < (best[0], -best[2]):
            best = (c, sol.x.copy(), nz)
        if c < 1e-10:
            hits += 1
    c, x, nz = best
    src = w10.zero_source(N)
    for (e, i, j), k in s.vidx.items():
        if abs(x[k]) > 1e-6:
            src[e][i][j] = F(x[k]).limit_denominator(10 ** 7)
    a = w10.audit(w10.template_of(src, N), N)
    say(f"  {label:34s} vars {s.nv:3d} | supp mixed words {len(s.mixed):4d} | "
        f"best max|res| {c:.3e} | hits {hits}/{starts} | nonzero cells "
        f"{nz}/{s.nv} | achieved admissible {a['ADMISSIBLE']}")
    return {"label": label, "n_vars": s.nv, "supported_mixed": len(s.mixed),
            "best_max_residual": c, "hits": hits, "nonzero_cells": nz,
            "achieved_admissible": a["ADMISSIBLE"], "achieved_Sigma": a["Sigma"]}

rows = []
# positive control: a task-B witness template (mixed-exact source EXISTS)
b = json.load(open(os.path.join(HERE, "results_b_witness_n6.json")))
srcA = w10.src_from_repr(b["WA"]["source"], 6)
rows.append(probe("[CONTROL] task-B template m=15",
                  w10.template_of(srcA, N), starts=60))
for m, tpl in sorted(found.items()):
    rows.append(probe(f"ADM+ template m={m}", tpl, starts=400, seed=200 + m))
OUT["K2"] = rows

with open(os.path.join(HERE, "results_k_n6_sc.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_k_n6_sc.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say("K DONE")
