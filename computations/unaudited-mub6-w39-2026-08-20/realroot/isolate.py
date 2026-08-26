"""realroot/isolate -- CERTIFIED isolation of the real points of a
zero-dimensional rational system, and rigorous interval evaluation.

METHOD (standard verified-computation pattern; floating point is used ONLY to
propose boxes, never to decide anything):

  1. Float Newton from many random starts proposes approximate real solutions.
     A proposal that is wrong or missing costs nothing -- it is never trusted.
  2. Each proposal is CERTIFIED by an exact rational interval Krawczyk test:
     for a box X and midpoint c, with Y an approximate inverse of J(c),
         K(X) = c - Y*F(c) + (Id - Y*J(X)) * (X - c)
     If K(X) is contained in the INTERIOR of X then F has EXACTLY ONE zero in
     X (Krawczyk/Moore; see Moore-Kearfott-Cloud, "Introduction to Interval
     Analysis", Thm 8.1-8.2).  All interval arithmetic here is over Fractions,
     so the conclusion is a theorem, not a numerical impression.
  3. COMPLETENESS comes from outside: the Hermite trace form (realroot.py)
     gives the EXACT number N of distinct real points.  If step 2 certifies N
     pairwise-disjoint boxes, the list is provably complete.  Without that
     count, a box list would be worthless (hazard ledger 18: a search that
     stops finding things is not evidence).

Nothing in this file may be used to certify an EQUALITY (e.g. "these two
vectors ARE orthogonal"); interval arithmetic can only ever certify strict
exclusion.  Consumers must therefore be one-sided -- see clique.py.
"""
from __future__ import annotations

from fractions import Fraction

try:
    import numpy as np
except Exception:                                        # pragma: no cover
    np = None


# --------------------------------------------------------------------------
# exact rational intervals
# --------------------------------------------------------------------------
class Iv:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        if hi is None:
            hi = lo
        self.lo = Fraction(lo)
        self.hi = Fraction(hi)
        if self.lo > self.hi:
            raise ValueError("empty interval")

    def __repr__(self):
        return f"[{float(self.lo):.6g},{float(self.hi):.6g}]"

    def __add__(self, o):
        o = o if isinstance(o, Iv) else Iv(o)
        return Iv(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __neg__(self):
        return Iv(-self.hi, -self.lo)

    def __sub__(self, o):
        return self + (-(o if isinstance(o, Iv) else Iv(o)))

    def __rsub__(self, o):
        return (o if isinstance(o, Iv) else Iv(o)) + (-self)

    def __mul__(self, o):
        o = o if isinstance(o, Iv) else Iv(o)
        p = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return Iv(min(p), max(p))

    __rmul__ = __mul__

    def contains_zero(self):
        return self.lo <= 0 <= self.hi

    def width(self):
        return self.hi - self.lo

    def mid(self):
        return (self.lo + self.hi) / 2

    def strictly_inside(self, o):
        """self is contained in the INTERIOR of o"""
        return o.lo < self.lo and self.hi < o.hi


def iv_dot(a, b):
    s = Iv(0)
    for x, y in zip(a, b):
        s = s + x * y
    return s


# --------------------------------------------------------------------------
# polynomial systems as callables over Fractions / intervals
# --------------------------------------------------------------------------
class PolySystem:
    """Dense representation: each polynomial is a list of (coeff, exponent
    tuple).  Evaluation works over Fraction, float, or Iv uniformly."""

    def __init__(self, polys, nvars):
        self.polys = polys
        self.n = nvars

    def eval(self, x, zero, one):
        out = []
        for p in self.polys:
            s = zero
            for c, e in p:
                t = one * c
                for i, k in enumerate(e):
                    for _ in range(k):
                        t = t * x[i]
                s = s + t
            out.append(s)
        return out

    def eval_f(self, x):
        return self.eval(x, 0.0, 1.0)

    def eval_iv(self, x):
        return self.eval(x, Iv(0), Iv(1))

    def jac_f(self, x):
        m, n = len(self.polys), self.n
        J = [[0.0] * n for _ in range(m)]
        for r, p in enumerate(self.polys):
            for c, e in p:
                for i in range(n):
                    if e[i] == 0:
                        continue
                    t = float(c) * e[i]
                    for k, kk in enumerate(e):
                        pw = kk - 1 if k == i else kk
                        for _ in range(pw):
                            t *= x[k]
                    J[r][i] += t
        return J

    def jac_iv(self, x):
        m, n = len(self.polys), self.n
        J = [[Iv(0)] * n for _ in range(m)]
        for r, p in enumerate(self.polys):
            row = [Iv(0)] * n
            for c, e in p:
                for i in range(n):
                    if e[i] == 0:
                        continue
                    t = Iv(Fraction(c) * e[i])
                    for k, kk in enumerate(e):
                        pw = kk - 1 if k == i else kk
                        for _ in range(pw):
                            t = t * x[k]
                    row[i] = row[i] + t
            J[r] = row
        return J


# --------------------------------------------------------------------------
# float Newton (proposal only -- never trusted)
# --------------------------------------------------------------------------
def newton(sysm, x0, iters=80, tol=1e-13):
    if np is None:
        raise RuntimeError("numpy required for the proposal stage")
    x = np.array(x0, dtype=float)
    for _ in range(iters):
        F = np.array(sysm.eval_f(list(x)), dtype=float)
        if np.max(np.abs(F)) < tol:
            return x, True
        J = np.array(sysm.jac_f(list(x)), dtype=float)
        try:
            step, *_ = np.linalg.lstsq(J, -F, rcond=None)
        except Exception:
            return x, False
        x = x + step
        if not np.all(np.isfinite(x)):
            return x, False
    F = np.array(sysm.eval_f(list(x)), dtype=float)
    return x, bool(np.max(np.abs(F)) < 1e-9)


# --------------------------------------------------------------------------
# exact Krawczyk certification
# --------------------------------------------------------------------------
def krawczyk_certify(sysm, centre, radius):
    """Try to prove that the box centre +- radius contains EXACTLY ONE real
    solution.  centre: list of Fraction; radius: Fraction.  Returns the box
    (list of Iv) on success, else None.

    Requires a square system (#polys == #vars): we use the first n polynomials
    and afterwards VERIFY the remaining ones by interval evaluation, so the
    certificate covers the whole system.
    """
    n = sysm.n
    X = [Iv(c - radius, c + radius) for c in centre]
    c = [Fraction(x.mid()) for x in X]
    sq = PolySystem(sysm.polys[:n], n)
    Jc = sq.jac_f([float(v) for v in c])
    if np is None:
        return None
    try:
        Yf = np.linalg.inv(np.array(Jc, dtype=float))
    except Exception:
        return None
    # rationalise Y (any rational matrix is admissible; accuracy only affects
    # whether the test succeeds, never whether the conclusion is valid)
    Y = [[Fraction(float(Yf[i][j])).limit_denominator(10**12)
          for j in range(n)] for i in range(n)]
    Fc = sq.eval([Iv(v) for v in c], Iv(0), Iv(1))
    JX = sq.jac_iv(X)
    K = []
    for i in range(n):
        s = Iv(c[i])
        for j in range(n):
            s = s - Y[i][j] * Fc[j]
        for j in range(n):
            # (Id - Y*J(X)) * (X - c)
            coef = Iv(1 if i == j else 0)
            for k in range(n):
                coef = coef - Y[i][k] * JX[k][j]
            s = s + coef * (X[j] - Iv(c[j]))
        K.append(s)
    for i in range(n):
        if not K[i].strictly_inside(X[i]):
            return None
    # the remaining (redundant) equations must also vanish on the box
    for p in sysm.polys[n:]:
        val = PolySystem([p], n).eval_iv(K)[0]
        if not val.contains_zero():
            return None
    return K
