#!/usr/bin/env python3
"""W20 -- RESIDUAL 2: an honest FEASIBILITY PROBE of the C_8 member.
UNAUDITED.

FLOATS ARE USED HERE FOR SEARCH ONLY.  No verdict in this probe's report
rests on a float: a hit would be re-derived exactly (rationalised + checked
with Fraction arithmetic), and a miss is reported as evidence, never as a
proof.

METHOD (uses the site-linearity W20-L).  H_w is LINEAR in the blocks at any
single site t (every perfect matching covers t exactly once).  So alternate:
for each site t and each colour c at t, replace the occupied cells of "row c
at t" by the smallest right singular vector of the corresponding coefficient
matrix.  That is exact alternating least squares on a multilinear system;
it converges to 0 residual whenever a solution exists and is reachable.

Calibration: the same routine is run on the m=26 clean layer, where exact
solutions are KNOWN to exist (w20_forcing.py produced them), so a failure to
converge there would indict the method rather than the template.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w20_core as C                                            # noqa: E402


def site_unknowns(T, t):
    """for each colour c at t: the list of (edge index, cell) unknowns."""
    out = {c: [] for c in range(3)}
    for ei, (u, v) in enumerate(C.EDGES):
        if t != u and t != v:
            continue
        for cc in range(9):
            if not (T[ei] >> cc) & 1:
                continue
            i, j = cc // 3, cc % 3
            c = i if u == t else j
            out[c].append((ei, cc))
    return out


def build_index(T):
    idx = {}
    for ei in range(C.NE):
        for cc in range(9):
            if (T[ei] >> cc) & 1:
                idx[(ei, cc)] = len(idx)
    return idx


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


def als(T, words, seed, iters=120, rng_scale=1.0):
    idx = build_index(T)
    n = len(idx)
    rng = np.random.default_rng(seed)
    vals = rng.normal(scale=rng_scale, size=n)
    vals[np.abs(vals) < 0.2] = 0.5
    su = {t: site_unknowns(T, t) for t in range(8)}
    sup = {w: C.support(T, w) for w in words}
    hist = []
    for it in range(iters):
        for t in range(8):
            for c in range(3):
                unk = su[t][c]
                if not unk:
                    continue
                pos = {u: k for k, u in enumerate(unk)}
                rows = []
                for w in words:
                    if w[t] != c:
                        continue
                    row = np.zeros(len(unk))
                    hit = False
                    for mi in sup[w]:
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
                        rows.append(row)
                if not rows:
                    continue
                M = np.array(rows)
                _, _, Vt = np.linalg.svd(M, full_matrices=False)
                v = Vt[-1]
                if np.max(np.abs(v)) == 0:
                    continue
                v = v / np.max(np.abs(v))
                for u, k in pos.items():
                    vals[idx[u]] = v[k]
        r = residual(vals, T, idx, words)
        hist.append(r)
        if r < 1e-24:
            break
    minabs = float(np.min(np.abs(vals)))
    consts = [abs(sum(np.prod([vals[idx[(e, C.cell_index(e, w))]]
                               for e in C.PM_E[mi]])
                      for mi in C.support(T, w))) for w in C.CONSTS]
    return dict(seed=seed, final_residual=float(hist[-1]),
                min_residual=float(min(hist)), n_iters=len(hist),
                min_abs_cell=minabs, constant_values=[float(x) for x in consts],
                converged=bool(hist[-1] < 1e-20))


def main():
    res = {"_header": "UNAUDITED W20 residual-2 feasibility probe. FLOATS FOR "
                      "SEARCH ONLY; no verdict rests on them."}
    # CALIBRATION: the m=26 clean layer, where exact solutions are known
    T26 = C.W8_IMMUNE[26]
    f26 = C.full_pm_indices(T26)
    clean26 = [w for w in C.MIXED if not C.extras_at(T26, w, f26)]
    cal = [als(T26, clean26, s, iters=60) for s in (1, 2, 3)]
    res["calibration_m26_clean_layer"] = cal
    print("CALIBRATION (m=26 clean layer, solutions known to exist):",
          flush=True)
    for r in cal:
        print("   seed %d: residual %.3e (min %.3e) after %d iters, "
              "converged=%s" % (r["seed"], r["final_residual"],
                                r["min_residual"], r["n_iters"],
                                r["converged"]), flush=True)
    # the C_8 member: ALL 6558 mixed equations
    T = C.C8_MEMBER
    out = []
    for s in (1, 2, 3, 4, 5, 6, 7, 8):
        r = als(T, list(C.MIXED), s, iters=140)
        out.append(r)
        print("C_8 member, seed %d: residual %.4e (min %.4e) after %d iters | "
              "min |cell| %.2e | constants %s | converged=%s"
              % (s, r["final_residual"], r["min_residual"], r["n_iters"],
                 r["min_abs_cell"],
                 ["%.2e" % x for x in r["constant_values"]], r["converged"]),
              flush=True)
    res["C8_full_mixed_system"] = out
    res["C8_any_converged"] = any(r["converged"] for r in out)
    # the cross-block subsystem alone (L-free and R-free words only)
    from w20_c8 import LFREE, RFREE
    free = set()
    for x in LFREE:
        for y in C.WORDS:
            pass
    import itertools
    for x in LFREE:
        for y in itertools.product(range(3), repeat=4):
            free.add(tuple(x) + tuple(y))
    for y in RFREE:
        for x in itertools.product(range(3), repeat=4):
            free.add(tuple(x) + tuple(y))
    free = sorted(w for w in free if len(set(w)) > 1)
    res["n_free_words"] = len(free)
    out2 = []
    for s in (1, 2, 3, 4):
        r = als(T, free, s, iters=140)
        out2.append(r)
        print("C_8 free-word (permanent) subsystem, seed %d: residual %.4e "
              "(min %.4e) | min |cell| %.2e | converged=%s"
              % (s, r["final_residual"], r["min_residual"], r["min_abs_cell"],
                 r["converged"]), flush=True)
    res["C8_free_subsystem"] = out2
    json.dump(res, open(os.path.join(HERE, "results_c8search.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
