"""AUDIT A1 / CLAIM 2: W3's THEOREM A.1 (corrected form).

W3: for a cell support S, exactly one of

  (D)  there is w with  sum_v w_{v,c} = 0 for each colour c  and
       <w, m_s> >= 0 for all s in S, strict for at least one s;
       then a|_{S_0(w)} is again an exact source with the SAME values;
  (P)  the gauge orbit contains a balanced representative:
       load(v,c) = mu_c  (21 real conditions at n = 8).

INDEPENDENT ROUTE.  Both sides are decided here by an EXACT rational
simplex (a1_lp.py) run on feasibility problems built from a dict-keyed
incidence -- no scipy, no floating point, and infeasibility is *proved*, not
inferred from a failed float solve.  A third, completely different route
(numerical Kempf-Ness minimisation of F(r) = sum_s |a_s|^2 e^{2<r,m_s>} over
U) is used to triangulate.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction

from a1_core import COLS, all_cells, nodes_of
from a1_lp import ZERO, feasible, solve


# ------------------------------------------------------------------ (D)


def build_D(n, S):
    S = sorted(S)
    nodes = [(v, c) for v in range(n) for c in COLS]
    nid = {x: i for i, x in enumerate(nodes)}
    NN = len(nodes)
    nvar = 2 * NN + len(S)          # w+, w-, t
    rows, rhs = [], []
    for si, s in enumerate(S):
        row = [ZERO] * nvar
        for p in nodes_of(s):
            row[nid[p]] += 1
            row[NN + nid[p]] -= 1
        row[2 * NN + si] = Fraction(-1)
        rows.append(row)
        rhs.append(ZERO)
    for c in COLS:
        row = [ZERO] * nvar
        for v in range(n):
            row[nid[(v, c)]] += 1
            row[NN + nid[(v, c)]] -= 1
        rows.append(row)
        rhs.append(ZERO)
    row = [ZERO] * nvar
    for si in range(len(S)):
        row[2 * NN + si] = Fraction(1)
    rows.append(row)
    rhs.append(Fraction(1))
    return rows, rhs, S, nodes


def decide_D(n, S):
    rows, rhs, Sl, nodes = build_D(n, S)
    ok, x = feasible(rows, rhs)
    if not ok:
        return False, None
    NN = len(nodes)
    w = {nodes[i]: x[i] - x[NN + i] for i in range(NN)}
    return True, w


def verify_D(n, S, w):
    """Independent exact re-verification of a (D) certificate."""
    for c in COLS:
        if sum(w[(v, c)] for v in range(n)) != 0:
            return False, "pure-neutrality fails"
    pos = 0
    for s in S:
        p, q = nodes_of(s)
        val = w[p] + w[q]
        if val < 0:
            return False, "not admissible"
        if val > 0:
            pos += 1
    if pos == 0:
        return False, "S_0 = S (trivial)"
    return True, f"{pos} cells killed"


# ------------------------------------------------------------------ (P)


def build_P(n, S):
    S = sorted(S)
    nodes = [(v, c) for v in range(n) for c in COLS]
    nid = {x: i for i, x in enumerate(nodes)}
    NN = len(nodes)
    nvar = len(S) + 6               # z (y = 1 + z), mu+, mu-
    deg = {p: 0 for p in nodes}
    for s in S:
        for p in nodes_of(s):
            deg[p] += 1
    rows, rhs = [], []
    for p in nodes:
        row = [ZERO] * nvar
        for si, s in enumerate(S):
            if p in nodes_of(s):
                row[si] += 1
        row[len(S) + p[1]] = Fraction(-1)
        row[len(S) + 3 + p[1]] = Fraction(1)
        rows.append(row)
        rhs.append(Fraction(-deg[p]))
    return rows, rhs, S, nodes


def decide_P(n, S):
    rows, rhs, Sl, nodes = build_P(n, S)
    ok, x = feasible(rows, rhs)
    if not ok:
        return False, None
    y = {s: Fraction(1) + x[i] for i, s in enumerate(Sl)}
    mu = [x[len(Sl) + c] - x[len(Sl) + 3 + c] for c in COLS]
    return True, (y, mu)


def verify_P(n, S, cert):
    y, mu = cert
    L = {(v, c): Fraction(0) for v in range(n) for c in COLS}
    for s in S:
        if y[s] <= 0:
            return False, "non-positive weight"
        for p in nodes_of(s):
            L[p] += y[s]
    for v in range(n):
        for c in COLS:
            if L[(v, c)] != mu[c]:
                return False, f"load({v},{c}) = {L[(v,c)]} != mu_{c} = {mu[c]}"
    return True, f"mu = {[str(m) for m in mu]}"


# ------------------------------------------------- third route: Kempf-Ness


def kempf_ness(n, S, iters=200):
    """Damped-Newton minimisation of F(r) = sum_{s in S} exp(2<r,m_s>) over
    U = {r : sum_v r_{v,c} = 0}.  Convex, so Newton converges globally with
    backtracking.  Returns (max|r|, relative load defect).  (P) <=> the min
    is attained <=> the load defect goes to 0 at bounded |r|."""
    import numpy as np

    S = sorted(S)
    nodes = [(v, c) for v in range(n) for c in COLS]
    nid = {x: i for i, x in enumerate(nodes)}
    P = np.zeros((len(S), len(nodes)))
    for i, s in enumerate(S):
        for p in nodes_of(s):
            P[i, nid[p]] += 1.0
    C = np.zeros((3, len(nodes)))
    for c in COLS:
        for v in range(n):
            C[c, nid[(v, c)]] = 1.0
    B = np.linalg.svd(C)[2][3:].T            # basis of U
    M = P @ B
    z = np.zeros(M.shape[1])

    def F(zz):
        return float(np.sum(np.exp(np.clip(2 * (M @ zz), -600, 600))))

    for _ in range(iters):
        e = np.exp(np.clip(2 * (M @ z), -600, 600))
        g = 2 * M.T @ e
        H = 4 * M.T @ (e[:, None] * M)
        try:
            d = -np.linalg.pinv(H, rcond=1e-12) @ g
        except np.linalg.LinAlgError:
            break
        if not np.all(np.isfinite(d)) or np.linalg.norm(d) < 1e-14:
            break
        t = 1.0
        f0 = F(z)
        while t > 1e-12 and F(z + t * d) > f0 - 1e-4 * t * float(g @ d) * -1e-9:
            if F(z + t * d) < f0:
                break
            t *= 0.5
        z = z + t * d
        if np.max(np.abs(g)) < 1e-11:
            break
    r = B @ z
    e = np.exp(np.clip(2 * (M @ z), -600, 600))
    load = P.T @ e
    defect = 0.0
    for c in COLS:
        vals = np.array([load[nid[(v, c)]] for v in range(n)])
        defect = max(defect, float((vals.max() - vals.min()) /
                                   max(vals.mean(), 1e-300)))
    return float(np.max(np.abs(r))), defect


# --------------------------------------------------------------- driver


def classify(n, S):
    dD, wD = decide_D(n, S)
    dP, cP = decide_P(n, S)
    if dD:
        ok, msg = verify_D(n, S, wD)
        if not ok:
            return "D-BAD:" + msg, None
    if dP:
        ok, msg = verify_P(n, S, cP)
        if not ok:
            return "P-BAD:" + msg, None
    if dD and dP:
        return "BOTH", (wD, cP)
    if dD:
        return "D", wD
    if dP:
        return "P", cP
    return "NEITHER", None


def random_support(n, rng, density):
    return frozenset(k for k in all_cells(n) if rng.random() < density)
