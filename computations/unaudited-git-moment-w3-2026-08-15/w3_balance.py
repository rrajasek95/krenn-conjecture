"""UNAUDITED PROBE (agent W3, Route A, 2026-08-15).  HEAD 26ba69f7.

The gauge-torus instability alternative, as an exactly certified linear
program on a cell support S.

Theory (proved in REPORT.md, Theorem A.1):

  For w in R^{3n} put W_w(s) = w_{u,i} + w_{v,j} for the cell s=(uv,i,j).
  Let  Adm(S) = {w : W_w(s) >= 0 for all s in S}  and
       U      = {w : sum_v w_{v,c} = 0 for c = 0,1,2}   (pure-preserving).
  Exactly one of

   (D)  there is w in Adm(S) ^ U with S_0(w) = {s : W_w(s)=0} a PROPER
        subset of S    [then a|_{S_0} is again an exact source];
   (P)  there is y in R^S_{>0} and mu_0,mu_1,mu_2 with

              sum_{s incident to node (v,c)} y_s = mu_c   for all (v,c)

        [the BALANCE / zero-moment condition; Kempf-Ness then says the
         gauge orbit contains a point with |a_s|^2 = y_s].

  The alternative is Stiemke's lemma applied to the subspace
  phi(U) <= R^S, phi(w)_s = W_w(s), whose orthogonal complement is
  {y : sum_s y_s m_s in span(pi_0,pi_1,pi_2)} = the balance space.

Both sides are certified in exact rational arithmetic; floating LP is only
used to *find* the candidate certificate.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
from scipy.optimize import linprog

from w3_core import cell_nodes, node


# ----------------------------------------------------------------- helpers


def _incidence(n: int, S):
    """A[(v,c), s] = 1 if cell s meets node (v,c).  Returns (rows, cols, S)."""
    S = sorted(S)
    CN = cell_nodes(n)
    A = np.zeros((3 * n, len(S)), dtype=float)
    for col, s in enumerate(S):
        p, q = CN[s]
        A[p, col] += 1.0
        A[q, col] += 1.0
    return A, S


def _rationalise(x, max_den=10**6):
    return [Fraction(float(v)).limit_denominator(max_den) for v in x]


# ------------------------------------------------------- (D) degeneration


def find_degeneration(n: int, S, max_den: int = 10**6):
    """Search for w in Adm(S) ^ U with S_0(w) proper.  Exactly certified.

    Returns None, or dict(w=..., S0=frozenset, killed=frozenset).
    """
    A, Sl = _incidence(n, S)          # A^T w gives the cell weights W_w
    m = len(Sl)
    N = 3 * n

    # variables w (free, N of them).  Constraints:
    #   W_w(s) >= 0            for s in S        (A^T w >= 0)
    #   sum_v w_{v,c} = 0      for c = 0,1,2
    #   W_w(s) <= 1            (bound the cone; scale is free)
    # objective: maximise sum_s W_w(s).  Optimum > 0  <=>  (D) holds.
    AT = A.T                                     # m x N
    A_ub = np.vstack([-AT, AT])
    b_ub = np.concatenate([np.zeros(m), np.ones(m)])
    A_eq = np.zeros((3, N))
    for c in range(3):
        for v in range(n):
            A_eq[c, node(v, c)] = 1.0
    b_eq = np.zeros(3)
    res = linprog(
        c=-AT.sum(axis=0),
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=[(None, None)] * N,
        method="highs",
    )
    if not res.success or -res.fun <= 1e-9:
        return None

    # ---- exact certification of the found w -------------------------------
    for den in (10**3, 10**4, 10**5, max_den):
        w = _rationalise(res.x, den)
        # project exactly onto U: subtract the colour-block mean
        for c in range(3):
            tot = sum(w[node(v, c)] for v in range(n))
            shift = Fraction(tot, n)
            for v in range(n):
                w[node(v, c)] -= shift
        CN = cell_nodes(n)
        Wv = {s: w[CN[s][0]] + w[CN[s][1]] for s in Sl}
        if any(x < 0 for x in Wv.values()):
            continue
        S0 = frozenset(s for s in Sl if Wv[s] == 0)
        if len(S0) == len(Sl):
            continue
        # exact re-check of the three pure conditions
        assert all(sum(w[node(v, c)] for v in range(n)) == 0 for c in range(3))
        return {
            "w": w,
            "S0": S0,
            "killed": frozenset(Sl) - S0,
            "weights": Wv,
        }
    return None


def verify_degeneration(n: int, S, cert) -> bool:
    """Exact re-verification of a (D) certificate."""
    CN = cell_nodes(n)
    w = cert["w"]
    for c in range(3):
        if sum(w[node(v, c)] for v in range(n)) != 0:
            return False
    S0 = set()
    for s in S:
        val = w[CN[s][0]] + w[CN[s][1]]
        if val < 0:
            return False
        if val == 0:
            S0.add(s)
    return set(S0) == set(cert["S0"]) and len(S0) < len(set(S))


# ------------------------------------------------------------ (P) balance


def find_balance(n: int, S, max_den: int = 10**6):
    """Search for y > 0 on S with colour-constant loads.  Exactly certified.

    Returns None, or dict(y=dict cell->Fraction, mu=[Fraction]*3).
    """
    A, Sl = _incidence(n, S)
    m = len(Sl)
    N = 3 * n

    # variables: y (m) , mu (3) , t (1).   maximise t.
    #   load(v,c) - mu_c = 0
    #   y_s - t >= 0
    #   sum y_s = m         (normalisation)
    nv = m + 3 + 1
    A_eq = np.zeros((3 * n + 1, nv))
    b_eq = np.zeros(3 * n + 1)
    for v in range(n):
        for c in range(3):
            r = node(v, c)
            A_eq[r, :m] = A[r, :]
            A_eq[r, m + c] = -1.0
    A_eq[3 * n, :m] = 1.0
    b_eq[3 * n] = float(m)
    A_ub = np.zeros((m, nv))
    for i in range(m):
        A_ub[i, i] = -1.0
        A_ub[i, m + 3] = 1.0
    b_ub = np.zeros(m)
    obj = np.zeros(nv)
    obj[m + 3] = -1.0
    res = linprog(
        c=obj,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=[(0, None)] * m + [(0, None)] * 3 + [(None, None)],
        method="highs",
    )
    if not res.success or -res.fun <= 1e-9:
        return None

    yf = res.x[:m]
    for den in (10**3, 10**4, 10**5, max_den):
        y = {s: Fraction(float(val)).limit_denominator(den) for s, val in zip(Sl, yf)}
        if any(v <= 0 for v in y.values()):
            continue
        # exact repair of the balance equations by least-squares is not
        # available over Q; instead solve the balance system exactly with the
        # rounded y as a starting guess for the support pattern.
        fixed = _exact_balance_from_guess(n, Sl, y)
        if fixed is not None:
            return fixed
    return _exact_balance_from_guess(n, Sl, None)


def _exact_balance_from_guess(n: int, Sl, guess):
    """Solve the exact rational balance system, seeking a strictly positive
    solution near `guess` (or any strictly positive solution)."""
    import sympy as sp

    m = len(Sl)
    CN = cell_nodes(n)
    # unknowns y_0..y_{m-1}, mu_0..mu_2
    Amat = sp.zeros(3 * n, m + 3)
    for col, s in enumerate(Sl):
        p, q = CN[s]
        Amat[p, col] += 1
        Amat[q, col] += 1
    for v in range(n):
        for c in range(3):
            Amat[node(v, c), m + c] = -1
    ns = Amat.nullspace()
    if not ns:
        return None
    basis = [list(vec) for vec in ns]
    # look for a strictly positive combination: LP over the coefficients
    k = len(basis)
    B = np.array([[float(b[i]) for b in basis] for i in range(m)])  # m x k
    A_ub = np.hstack([-B, np.ones((m, 1))])
    b_ub = np.zeros(m)
    obj = np.zeros(k + 1)
    obj[k] = -1.0
    bnds = [(-1, 1)] * k + [(None, 1)]
    res = linprog(c=obj, A_ub=A_ub, b_ub=b_ub, bounds=bnds, method="highs")
    if not res.success or -res.fun <= 1e-9:
        return None
    for den in (10**3, 10**4, 10**5, 10**6):
        coef = [Fraction(float(v)).limit_denominator(den) for v in res.x[:k]]
        vec = [sum(c * sp.Rational(b[i]) for c, b in zip(coef, basis)) for i in range(m + 3)]
        yv = [Fraction(int(sp.Rational(v).p), int(sp.Rational(v).q)) for v in vec]
        if all(v > 0 for v in yv[:m]):
            y = {s: yv[i] for i, s in enumerate(Sl)}
            mu = yv[m:]
            if verify_balance(n, Sl, y, mu):
                return {"y": y, "mu": mu}
    return None


def verify_balance(n: int, S, y, mu) -> bool:
    """Exact re-verification of a (P) certificate."""
    CN = cell_nodes(n)
    load = [Fraction(0)] * (3 * n)
    for s in S:
        if y[s] <= 0:
            return False
        p, q = CN[s]
        load[p] += y[s]
        load[q] += y[s]
    for v in range(n):
        for c in range(3):
            if load[node(v, c)] != mu[c]:
                return False
    return True


def classify(n: int, S):
    """Return ('D', cert) or ('P', cert) or ('?', None)."""
    S = frozenset(S)
    d = find_degeneration(n, S)
    if d is not None and verify_degeneration(n, S, d):
        return "D", d
    p = find_balance(n, S)
    if p is not None:
        return "P", p
    if d is not None:
        return "D?", d
    return "?", None
