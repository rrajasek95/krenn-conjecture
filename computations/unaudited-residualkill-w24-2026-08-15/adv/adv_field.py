#!/usr/bin/env python3
"""ADVERSARIAL W24 -- exact quadratic number fields + a FIELD-GENERIC
from-the-definition hafnian / residual engine.

Fields: Q, Q(omega) = Q[w]/(w^2+w+1), Q(i) = Q[i]/(i^2+1).
Everything is exact (pairs of Fractions).  NO FLOATS.
UNAUDITED probe.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations

N = 8


class Quad:
    """a + b*g  with  g^2 = S + T*g   (class attributes S, T)."""
    __slots__ = ("a", "b")
    S = Fraction(-1)
    T = Fraction(-1)          # default: omega  (w^2 = -1 - w)
    NAME = "omega"

    def __init__(self, a=0, b=0):
        self.a = Fraction(a)
        self.b = Fraction(b)

    # -- coercion
    @classmethod
    def _c(cls, o):
        if isinstance(o, Quad):
            return o
        if isinstance(o, (int, Fraction)):
            return cls(o, 0)
        return NotImplemented

    def __add__(self, o):
        o = self._c(o)
        return NotImplemented if o is NotImplemented else \
            type(self)(self.a + o.a, self.b + o.b)
    __radd__ = __add__

    def __neg__(self):
        return type(self)(-self.a, -self.b)

    def __sub__(self, o):
        o = self._c(o)
        return NotImplemented if o is NotImplemented else \
            type(self)(self.a - o.a, self.b - o.b)

    def __rsub__(self, o):
        o = self._c(o)
        return NotImplemented if o is NotImplemented else \
            type(self)(o.a - self.a, o.b - self.b)

    def __mul__(self, o):
        o = self._c(o)
        if o is NotImplemented:
            return NotImplemented
        cl = type(self)
        # (a+bg)(c+dg) = ac + (ad+bc)g + bd g^2 = ac+bd*S + (ad+bc+bd*T) g
        return cl(self.a * o.a + self.b * o.b * cl.S,
                  self.a * o.b + self.b * o.a + self.b * o.b * cl.T)
    __rmul__ = __mul__

    def conj(self):
        """the nontrivial Galois conjugate: g -> T - g."""
        cl = type(self)
        return cl(self.a + self.b * cl.T, -self.b)

    def norm(self):
        cl = type(self)
        # (a+bg)(a+b(T-g)) = a^2 + abT - b^2 S     [since g(T-g)=Tg-g^2=-S]
        return self.a * self.a + self.a * self.b * cl.T - self.b * self.b * cl.S

    def inv(self):
        n = self.norm()
        if n == 0:
            raise ZeroDivisionError(str(self))
        c = self.conj()
        return type(self)(c.a / n, c.b / n)

    def __truediv__(self, o):
        o = self._c(o)
        return NotImplemented if o is NotImplemented else self * o.inv()

    def __rtruediv__(self, o):
        o = self._c(o)
        return NotImplemented if o is NotImplemented else o * self.inv()

    def __eq__(self, o):
        o = self._c(o)
        if o is NotImplemented:
            return NotImplemented
        return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    def __bool__(self):
        return self.a != 0 or self.b != 0

    def __repr__(self):
        return "(%s+%s*%s)" % (self.a, self.b, type(self).NAME)


class Om(Quad):
    S = Fraction(-1)
    T = Fraction(-1)
    NAME = "w"


class Gi(Quad):
    S = Fraction(-1)
    T = Fraction(0)
    NAME = "i"


ZERO_Q, ONE_Q = Fraction(0), Fraction(1)


# ---------------------------------------------------------------- generic
def haf_gen(bl, gam_set, verts, w, one, zero):
    """sum over perfect matchings of Gamma|verts -- FIELD GENERIC."""
    verts = tuple(sorted(verts))
    if not verts:
        return one
    a = verts[0]
    tot = zero
    for k in range(1, len(verts)):
        b = verts[k]
        e = (a, b) if a < b else (b, a)
        if e not in gam_set:
            continue
        c = bl[e][w[e[0]]][w[e[1]]]
        if not c:
            continue
        r = haf_gen(bl, gam_set, verts[1:k] + verts[k + 1:], w, one, zero)
        if r:
            tot = tot + c * r
    return tot


def rref_gen(rows, ncols, zero, one):
    M = [list(r) for r in rows]
    piv, r = [], 0
    for c in range(ncols):
        sel = None
        for i in range(r, len(M)):
            if M[i][c]:
                sel = i
                break
        if sel is None:
            continue
        M[r], M[sel] = M[sel], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [aa - f * bb for aa, bb in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return M[:r], piv


def kernel_gen(rows, ncols, zero, one):
    if not rows:
        return [[one if i == k else zero for i in range(ncols)]
                for k in range(ncols)]
    R, piv = rref_gen(rows, ncols, zero, one)
    out = []
    for f in [c for c in range(ncols) if c not in piv]:
        v = [zero] * ncols
        v[f] = one
        for i, p in enumerate(piv):
            v[p] = -R[i][f]
        out.append(v)
    return out
