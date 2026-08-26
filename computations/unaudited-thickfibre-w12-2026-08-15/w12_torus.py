#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- solving the binomial part exactly and handing the
residual to Singular.

Given a ReducedSystem (Laurent equations on (C*)^d) and the binomial
sublattice  C z = eps  (rows c_i in Z^d, values eps_i in {+-1}), compute the
Smith normal form U C V = D.  Setting  z = w^{V^T}  (i.e. an exponent ROW r
becomes r.V) the binomial system becomes  w_j^{D_jj} = eps'_j,  j <= rank,
with  eps'_j = prod_i eps_i^{U_ji},  and  w_{rank+1..d}  free.

Every elementary divisor equal to 1 pins its w_j to +-1 outright; a divisor
delta > 1 forces a case split over the delta-th roots of eps'_j, which we
carry as a cyclotomic parameter.  The residual is a Laurent system in
f = d - rank free variables, which is what goes to Groebner.
"""

from __future__ import annotations

from fractions import Fraction

import w12_reduce as RED


class TorusSolution:
    def __init__(self, d, rows, vals):
        self.d = d
        self.rows = [list(r) for r in rows]
        self.vals = list(vals)
        if not self.rows:
            # no binomial relations at all: the whole torus stays free
            self.D, self.U = [], []
            self.V = [[int(i == j) for j in range(d)] for i in range(d)]
            self.rank = 0
            self.divisors = []
            self.eps = []
            self.free = d
            return
        C = self.rows
        D, U, V = RED.smith(C)
        self.D, self.U, self.V = D, U, V
        self.rank = sum(1 for i in range(len(D)) if D[i][i] != 0) if D else 0
        self.divisors = [D[i][i] for i in range(self.rank)]
        # eps'_j = prod_i eps_i^{U[j][i]}
        self.eps = []
        for j in range(self.rank):
            v = Fraction(1)
            for i, coef in enumerate(U[j]):
                if coef:
                    v *= self.vals[i] ** coef
            self.eps.append(v)
        self.free = d - self.rank

    def transform(self, row):
        """Exponent row r in Z^d -> r.V in Z^d (pinned part | free part)."""
        return [sum(row[j] * self.V[j][k] for j in range(self.d))
                for k in range(self.d)]

    def pinned_factor(self, trow):
        """The scalar contributed by the pinned coordinates, if all divisors
        are 1.  Returns None if a divisor > 1 is actually used."""
        out = Fraction(1)
        for j in range(self.rank):
            e = trow[j]
            if e == 0:
                continue
            if self.divisors[j] != 1:
                return None
            out *= self.eps[j] ** e
        return out

    def free_exponents(self, trow):
        return trow[self.rank:]

    def summary(self):
        return {"d": self.d, "binomial_rank": self.rank,
                "free_dimension": self.free,
                "elementary_divisors": sorted(set(self.divisors)),
                "nontrivial_divisors": [x for x in self.divisors if x != 1],
                "eps_values": sorted(set(str(x) for x in self.eps))}


def laurent_forms(red, sol, which="mixed"):
    """[(word, [(coeff, free-exponent-row)])] for each equation.

    The equation is  sum(coeff * w^{exponent}) = 0   (mixed)  /  != 0 (const);
    the leading 1 is included as coeff 1 with the zero exponent."""
    src = red.mixed if which == "mixed" else red.const
    out = []
    for w, exps in src.items():
        terms = [(Fraction(1), [0] * sol.free)]
        ok = True
        for e in exps:
            t = sol.transform(e)
            c = sol.pinned_factor(t)
            if c is None:
                ok = False
                break
            terms.append((c, sol.free_exponents(t)))
        if not ok:
            raise RuntimeError("nontrivial elementary divisor in use")
        out.append((w, terms))
    return out


def singular_polynomial(terms, names):
    """Clear the Laurent denominators and return a Singular polynomial."""
    f = len(names)
    shift = [0] * f
    for _, exps in terms:
        for k in range(f):
            shift[k] = max(shift[k], -exps[k])
    parts = []
    for coeff, exps in terms:
        mono = []
        for k in range(f):
            e = exps[k] + shift[k]
            if e == 1:
                mono.append(names[k])
            elif e > 1:
                mono.append(f"{names[k]}^{e}")
        body = "*".join(mono) if mono else "1"
        num, den = coeff.numerator, coeff.denominator
        parts.append(f"({num}/{den})*{body}" if den != 1 else f"({num})*{body}")
    return "+".join(parts), shift
