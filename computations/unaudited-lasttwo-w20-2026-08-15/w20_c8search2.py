#!/usr/bin/env python3
"""W20 -- RESIDUAL 2: the NORMALISED feasibility probe of the C_8 member.
UNAUDITED.  FLOATS FOR SEARCH ONLY -- no verdict rests on them.

The plain alternating least squares of w20_c8search.py always drove the
residual to zero by sending cells (and the three constants) to zero -- the
trivial degenerate point.  Here the three constant words are PINNED:

    H_{c^8} = 1  for c = 0,1,2

which is a legitimate normalisation (the torus gauge scales H_{c^8} by
prod_u lambda_{u,c}, three independent factors, so any exact source can be
rescaled to it).  Since H_{c^8} is linear in the "row c at site t" cells, the
pin is an AFFINE constraint on exactly the same unknowns as the mixed
equations, so each alternating step is a constrained linear least-squares
problem, solved in closed form.

CONTROLS
  * NEGATIVE (known-dead) templates: W8's m = 24 (killed by W15/A6) and
    m = 25 (killed by W19) -- the probe must NOT converge there;
  * POSITIVE (planted-feasible): the same template with only a random
    UNDER-determined subset of the mixed words -- the probe must converge
    with the constants pinned at 1 and the cells bounded away from 0.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w20_core as C                                            # noqa: E402
from w20_c8search import site_unknowns, build_index              # noqa: E402


def linear_rows(T, t, c, vals, idx, unk, words):
    pos = {u: k for k, u in enumerate(unk)}
    out = []
    for w in words:
        row = np.zeros(len(unk))
        hit = False
        for mi in C.support(T, w):
            p = 1.0
            key = None
            for e in C.PM_E[mi]:
                cc = C.cell_index(e, w)
                if (e, cc) in pos:
                    key = (e, cc)
                else:
                    p *= vals[idx[(e, cc)]]
            if key is not None:
                row[pos[key]] += p
                hit = True
        if hit:
            out.append(row)
    return np.array(out) if out else np.zeros((0, len(unk)))


def residual(vals, T, idx, words):
    tot = 0.0
    for w in words:
        s = 0.0
        for mi in C.support(T, w):
            p = 1.0
            for e in C.PM_E[mi]:
                p *= vals[idx[(e, C.cell_index(e, w))]]
            s += p
        tot += s * s
    return tot


def als_pinned(T, words, seed, iters=200, ridge=1e-10):
    idx = build_index(T)
    n = len(idx)
    rng = np.random.default_rng(seed)
    vals = rng.normal(size=n)
    vals[np.abs(vals) < 0.3] = 0.7
    su = {t: site_unknowns(T, t) for t in range(8)}
    bycol = {}
    for w in words:
        bycol.setdefault(w[0], []).append(w)
    hist = []
    for it in range(iters):
        for t in range(8):
            for c in range(3):
                unk = su[t][c]
                if not unk:
                    continue
                ws = [w for w in words if w[t] == c]
                M = linear_rows(T, t, c, vals, idx, unk, ws)
                a = linear_rows(T, t, c, vals, idx, unk, [(c,) * 8])
                if a.shape[0] == 0 or not np.any(a):
                    continue
                a = a[0]
                A = M.T @ M + ridge * np.eye(len(unk))
                try:
                    z = np.linalg.solve(A, a)
                except np.linalg.LinAlgError:
                    continue
                den = a @ z
                if abs(den) < 1e-300:
                    continue
                v = z / den
                if not np.all(np.isfinite(v)):
                    continue
                for u, k in {u: k for k, u in enumerate(unk)}.items():
                    vals[idx[u]] = v[k]
        r = residual(vals, T, idx, words)
        hist.append(r)
        if r < 1e-22:
            break
    consts = [sum(np.prod([vals[idx[(e, C.cell_index(e, w))]]
                           for e in C.PM_E[mi]])
                  for mi in C.support(T, w)) for w in C.CONSTS]
    return dict(seed=seed, final_residual=float(hist[-1]),
                min_residual=float(min(hist)), n_iters=len(hist),
                min_abs_cell=float(np.min(np.abs(vals))),
                constants=[float(x) for x in consts],
                converged=bool(min(hist) < 1e-18))


def run(T, words, tag, seeds, iters=200):
    out = []
    for s in seeds:
        r = als_pinned(T, words, s, iters=iters)
        out.append(r)
        print("   %-28s seed %d: min residual %.4e (final %.4e, %d iters) | "
              "min|cell| %.2e | constants %s | converged=%s"
              % (tag, s, r["min_residual"], r["final_residual"], r["n_iters"],
                 r["min_abs_cell"], ["%.3f" % x for x in r["constants"]],
                 r["converged"]), flush=True)
    return out


def main():
    res = {"_header": "UNAUDITED W20 normalised feasibility probe. FLOATS FOR "
                      "SEARCH ONLY."}
    T = C.C8_MEMBER
    rng = np.random.default_rng(0)
    print("POSITIVE CONTROL (planted-feasible: 60 random mixed words only):",
          flush=True)
    sub = [C.MIXED[i] for i in rng.choice(len(C.MIXED), 60, replace=False)]
    res["positive_control"] = run(T, sub, "C8 / 60 random words", (1, 2, 3),
                                  iters=120)
    print("NEGATIVE CONTROLS (templates already proved dead):", flush=True)
    res["neg_m24"] = run(C.W8_IMMUNE[24], list(C.MIXED), "m=24 (dead, W15/A6)",
                         (1, 2, 3))
    res["neg_m25"] = run(C.W8_IMMUNE[25], list(C.MIXED), "m=25 (dead, W19)",
                         (1, 2, 3))
    print("THE C_8 MEMBER (all 6558 mixed words, constants pinned to 1):",
          flush=True)
    res["C8"] = run(T, list(C.MIXED), "C_8 member",
                    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    best = min(r["min_residual"] for r in res["C8"])
    res["C8_best_residual"] = best
    res["C8_any_converged"] = any(r["converged"] for r in res["C8"])
    print("C_8 member: best normalised mixed residual over 10 restarts = "
          "%.4e ; any converged = %s" % (best, res["C8_any_converged"]),
          flush=True)
    if res["C8_any_converged"]:
        print("*** candidate feasible point found -- MUST be re-derived "
              "exactly before any claim ***", flush=True)
    json.dump(res, open(os.path.join(HERE, "results_c8search2.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
