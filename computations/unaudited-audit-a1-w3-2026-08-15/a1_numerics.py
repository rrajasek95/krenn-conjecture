"""AUDIT A1 / CLAIM 6 -- the numerics correction.

W3 claims (REPORT item 5):
  (i)  the eps^{-1/23} premise has NO repository backing;
  (ii) the committed near-solution divergence is CLOSED-ORBIT gauge motion:
       "Kempf-Ness balancing collapses candidate_n6_q3_seed2 to exactly the
        prism (nine cells at modulus 1)".

(i) is checked by `git grep` (see REPORT.md).  (ii) is checked here with an
INDEPENDENT balancer: damped Newton on F(r) = sum_s |a_s|^2 exp(2<r,m_s>)
over U = {r : sum_v r_{v,c} = 0}, written from scratch (W3 uses scipy
L-BFGS on the same convex function).  Numerics only -- reported as numerics.
"""

from __future__ import annotations

import itertools
import os
import sys

import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
N = 6
E6 = list(itertools.combinations(range(N), 2))


def cells_from(mats, tol):
    out = {}
    for k, (u, v) in enumerate(E6):
        for i in range(3):
            for j in range(3):
                z = mats[k, i, j]
                if abs(z) > tol:
                    out[(u, v, i, j)] = z
    return out


def balance(cellvals, n=N, iters=400):
    keys = sorted(cellvals)
    nodes = [(v, c) for v in range(n) for c in range(3)]
    nid = {x: i for i, x in enumerate(nodes)}
    P = np.zeros((len(keys), len(nodes)))
    for i, (u, v, a, b) in enumerate(keys):
        P[i, nid[(u, a)]] += 1
        P[i, nid[(v, b)]] += 1
    C = np.zeros((3, len(nodes)))
    for c in range(3):
        for v in range(n):
            C[c, nid[(v, c)]] = 1
    B = np.linalg.svd(C)[2][3:].T
    M = P @ B
    y0 = np.array([abs(cellvals[k]) ** 2 for k in keys])
    z = np.zeros(M.shape[1])
    for _ in range(iters):
        e = y0 * np.exp(np.clip(2 * (M @ z), -600, 600))
        g = 2 * M.T @ e
        H = 4 * M.T @ (e[:, None] * M)
        d = -np.linalg.pinv(H, rcond=1e-13) @ g
        if not np.all(np.isfinite(d)):
            break
        t = 1.0
        f0 = float(e.sum())
        for _ in range(60):
            zz = z + t * d
            f1 = float(np.sum(y0 * np.exp(np.clip(2 * (M @ zz), -600, 600))))
            if f1 < f0:
                break
            t *= 0.5
        z = z + t * d
        if np.max(np.abs(g)) < 1e-12:
            break
    mod = np.sqrt(y0 * np.exp(np.clip(2 * (M @ z), -600, 600)))
    load = P.T @ (mod ** 2)
    defect = 0.0
    for c in range(3):
        vals = np.array([load[nid[(v, c)]] for v in range(n)])
        defect = max(defect, float((vals.max() - vals.min()) /
                                   max(vals.mean(), 1e-300)))
    return keys, mod, float(np.max(np.abs(B @ z))), defect


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "candidate_n6_q3_seed2.npz"
    path = os.path.join(REPO, name)
    d = np.load(path)
    mats = np.asarray(d["matrices"], dtype=complex)
    res = float(np.max(np.abs(d["residual"]))) if "residual" in d else float("nan")
    print(f"AUDIT A1 / claim 6 -- independent balancing of {name}")
    print(f"  system residual (as stored): {res:.3e}")
    for tol in (1e-12, 1e-8, 1e-6, 1e-4, 1e-3):
        cv = cells_from(mats, tol)
        if not cv:
            continue
        keys, mod, rmax, defect = balance(cv)
        big = [(k, m) for k, m in zip(keys, mod) if m > 1e-3 * max(mod)]
        print(f"  tol={tol:8.0e}: cells={len(cv):3d}  max|a| before="
              f"{max(abs(v) for v in cv.values()):10.4g}  after balancing="
              f"{mod.max():8.4g}  |r|max={rmax:7.3f}  load defect={defect:.2e}")
        print(f"              cells with balanced modulus > 1e-3*max: "
              f"{len(big)}; distinct balanced moduli (2 dp): "
              f"{sorted(set(round(float(m), 2) for m in mod))[:12]}")
