"""UNAUDITED PROBE (W3, Route A, 2026-08-15). HEAD 26ba69f7.

TASK D: the 1-PS reading of the numerics.

The master plan asserts "the observed eps^{-1/23} scaling is the
destabilizing 1-PS signature".  This script tests the *structural* half of
that reading on the committed n=6 near-solution data:

  1. is the blow-up direction a GAUGE direction, i.e. is
     log|a| ~ x_0 + t*phi(w) for a single weight vector w?
  2. does that w satisfy the pure-neutrality condition <pi_c, w> = 0
     (which is what Theorem A.1 requires of a degeneration that preserves
     exactness)?
  3. does balancing the point (Kempf-Ness / the convex programme
     F(r) = sum_s |a_s|^2 exp(<r,m_s>) minimised over
     U = {r : sum_v r_{v,c} = 0}) remove the divergence?

If (3) removes it, the divergence is motion along a CLOSED gauge orbit and
is not an instability at all -- which is what notes/finite-obstruction.md
sec 3 already proves for the prism border family.
"""

from __future__ import annotations

import glob
import math
import os

import numpy as np
from scipy.optimize import minimize

from w3_core import cell_index, cell_nodes, cells, edge_index, node

N6 = 6
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def load_matrices(path):
    d = np.load(path)
    if "matrices" in d:
        return np.asarray(d["matrices"]), d
    return None, d


def to_cell_vector(mats, n=N6):
    """(C(n,2),3,3) -> flat cell vector in this module's indexing."""
    EI, CI = edge_index(n), cell_index(n)
    a = np.zeros(len(cells(n)), dtype=complex)
    for k in range(mats.shape[0]):
        for i in range(3):
            for j in range(3):
                a[CI[(k, i, j)]] = mats[k, i, j]
    return a


def balance(a, n=N6, tol=1e-12, iters=4000):
    """Minimise F(r) = sum_s y_s exp(<r,m_s>) over U; returns the balanced
    modulus vector and the gauge r."""
    S = [s for s in range(len(a)) if abs(a[s]) > tol]
    y0 = np.array([abs(a[s]) ** 2 for s in S])
    CN = cell_nodes(n)
    P = np.zeros((len(S), 3 * n))
    for i, s in enumerate(S):
        p, q = CN[s]
        P[i, p] += 1.0
        P[i, q] += 1.0
    # basis of U = {r : sum_v r_{v,c} = 0 for each c}
    C = np.zeros((3, 3 * n))
    for c in range(3):
        for v in range(n):
            C[c, node(v, c)] = 1.0
    _, _, Vt = np.linalg.svd(C)
    B = Vt[3:].T                                   # (3n) x (3n-3)
    M = P @ B

    def F(z):
        e = M @ z
        e = np.clip(e, -300, 300)
        return float(np.sum(y0 * np.exp(e)))

    def G(z):
        e = np.clip(M @ z, -300, 300)
        return M.T @ (y0 * np.exp(e))

    res = minimize(F, np.zeros(M.shape[1]), jac=G, method="L-BFGS-B",
                   options=dict(maxiter=iters, ftol=1e-16, gtol=1e-14))
    r = B @ res.x
    ybal = y0 * np.exp(np.clip(M @ res.x, -300, 300))
    loads = P.T @ ybal
    return S, np.sqrt(ybal), r, loads, res


def load_defect(loads, n=N6):
    """max over colours of (max_v load - min_v load) / mean load."""
    out = []
    for c in range(3):
        vals = np.array([loads[node(v, c)] for v in range(n)])
        m = vals.mean()
        out.append(float((vals.max() - vals.min()) / max(m, 1e-30)))
    return out


def gauge_direction_fit(a, n=N6, tol=1e-12):
    """Best-fit gauge direction for the blow-up: regress log|a| on the
    gauge subspace and report how much of the SPREAD it explains."""
    S = [s for s in range(len(a)) if abs(a[s]) > tol]
    x = np.array([math.log(abs(a[s])) for s in S])
    CN = cell_nodes(n)
    P = np.zeros((len(S), 3 * n))
    for i, s in enumerate(S):
        p, q = CN[s]
        P[i, p] += 1.0
        P[i, q] += 1.0
    sol, *_ = np.linalg.lstsq(P, x, rcond=None)
    resid = x - P @ sol
    return sol, float(np.linalg.norm(resid)), float(np.linalg.norm(x - x.mean()))


if __name__ == "__main__":
    print("UNAUDITED PROBE  W3 / Route A  HEAD 26ba69f7")
    print("TASK D: is the observed amplitude divergence a destabilizing 1-PS?")
    print("=" * 80)
    cands = sorted(glob.glob(os.path.join(REPO, "candidate_*.npz")))
    rows = []
    for path in cands:
        mats, d = load_matrices(path)
        if mats is None or mats.shape != (15, 3, 3):
            continue
        res = d["residual"] if "residual" in d else None
        rmax = float(np.max(np.abs(res))) if res is not None else float("nan")
        a = to_cell_vector(np.asarray(mats, dtype=complex))
        amax = float(np.max(np.abs(a)))
        if amax < 5:
            continue
        S, bal, r, loads, opt = balance(a)
        w, resid, spread = gauge_direction_fit(a)
        rows.append((os.path.basename(path), rmax, amax, float(bal.max()),
                     load_defect(loads), resid, spread, len(S)))
    print(f"{'file':38s} {'res_max':>9} {'max|a|':>9} {'max|a| BAL':>11} "
          f"{'gaugefit resid/spread':>22} {'cells':>6}")
    for name, rmax, amax, bmax, defect, resid, spread, ns in rows:
        print(f"{name:38s} {rmax:9.2e} {amax:9.3g} {bmax:11.4g} "
              f"{resid/max(spread,1e-30):22.4f} {ns:6d}")
        print(f"{'':38s} balanced load defect per colour: "
              f"{[f'{x:.2e}' for x in defect]}")
    print()
    print("Reading: 'max|a| BAL' is the largest modulus after the Kempf-Ness")
    print("balancing gauge.  If it collapses to O(1) the divergence was pure")
    print("gauge motion along a CLOSED orbit, not an instability.")
