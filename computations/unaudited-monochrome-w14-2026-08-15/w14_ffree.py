#!/usr/bin/env python3
"""UNAUDITED PROBE W14 -- fraction-free exact span membership.

Rows are integer vectors.  Elimination is kept INTEGRAL: to reduce r against a
pivot row b with pivot column p we replace r by (b[p]*r - r[p]*b) and divide by
the content.  Membership of a target t in the Q-row-space is unchanged by these
operations (each step multiplies the vector by a nonzero rational), so
"t reduces to 0" decides membership over Q exactly, with no denominators and no
coefficient blow-up.
"""

from __future__ import annotations

from math import gcd


def _primitive(vec):
    g = 0
    for x in vec:
        if x:
            g = gcd(g, abs(x))
    if g > 1:
        vec = [x // g for x in vec]
    if g == 0:
        return vec
    for x in vec:
        if x:
            return [-y for y in vec] if x < 0 else vec
    return vec


class IntSpan:
    """Row space over Q of integer rows, kept in integral echelon form."""

    def __init__(self, ncols):
        self.ncols = ncols
        self.piv = []          # pivot columns, increasing
        self.rows = []         # matching integral rows

    def reduce(self, vec):
        vec = list(vec)
        for p, b in zip(self.piv, self.rows):
            if vec[p]:
                f, g = b[p], vec[p]
                vec = [f * x - g * y for x, y in zip(vec, b)]
                vec = _primitive(vec)
        return vec

    def add(self, vec):
        vec = self.reduce(vec)
        p = next((n for n, x in enumerate(vec) if x), None)
        if p is None:
            return False
        # insert keeping pivot columns increasing
        idx = 0
        while idx < len(self.piv) and self.piv[idx] < p:
            idx += 1
        self.piv.insert(idx, p)
        self.rows.insert(idx, vec)
        return True

    def contains(self, vec):
        return all(x == 0 for x in self.reduce(vec))

    def dim(self):
        return len(self.piv)
