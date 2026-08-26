#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- exact torus reduction of a template value system.

WHY THIS IS SOUND.  Let x in (C*)^Sigma be the cell values.  Divide each
fibre equation by its first monomial x^{a_1} (legitimate: all cells are
nonzero).  Every equation becomes

        1 + sum_{k >= 2} x^{a_k - a_1}  =  0        (mixed)
        1 + sum_{k >= 2} x^{a_k - a_1} !=  0        (constant),

so the system only sees the characters x^lambda for lambda in the DIFFERENCE
LATTICE  Lambda = <a_k - a_1>  (rank d).  Pick a Z-basis lambda_1..lambda_d.
Because C* is a divisible (hence injective) Z-module, the injection
Z^d --> Z^Sigma dualises to a SURJECTION (C*)^Sigma --> (C*)^d, so

        z = (x^{lambda_1}, ..., x^{lambda_d})

ranges over ALL of (C*)^d, and conversely every z lifts to an x with all
coordinates nonzero.  Therefore

    an exact source with template T exists
      <=>  there is z in (C*)^d with all mixed Laurent equations = 0 and all
           three constant Laurent expressions != 0.

That equivalence is exact and loses nothing; the diagonal gauge is exactly
the kernel that has been quotiented out.
"""

from __future__ import annotations

from fractions import Fraction

import w12_lattice as LAT


# ------------------------------------------------------------ integer LA


def hnf_basis(rows, chunk=300):
    """Row HNF basis of the lattice spanned by `rows`, computed incrementally
    so the working matrix never exceeds (chunk + ncols) rows."""
    basis = []
    for start in range(0, len(rows), chunk):
        basis, _ = LAT.hnf(basis + [list(r) for r in rows[start:start + chunk]])
    return basis


def pivots_of(basis):
    return [next(j for j, x in enumerate(row) if x != 0) for row in basis]


def solve_in_basis(basis, vector, pivots=None):
    """Integer coordinates of `vector` in the HNF `basis`, or None."""
    if pivots is None:
        pivots = pivots_of(basis)
    v = list(vector)
    coeffs = [0] * len(basis)
    for i, row in enumerate(basis):
        piv = pivots[i]
        if v[piv] == 0:
            continue
        if v[piv] % row[piv] != 0:
            return None
        c = v[piv] // row[piv]
        coeffs[i] = c
        for j in range(piv, len(v)):
            if row[j]:
                v[j] -= c * row[j]
    return coeffs if not any(v) else None


def smith(matrix):
    """Smith normal form.  Returns (D, U, V) with U*matrix*V = D."""
    A = [list(r) for r in matrix]
    m = len(A)
    n = len(A[0]) if m else 0
    U = [[int(i == j) for j in range(m)] for i in range(m)]
    V = [[int(i == j) for j in range(n)] for i in range(n)]

    def swap_rows(i, j):
        A[i], A[j] = A[j], A[i]
        U[i], U[j] = U[j], U[i]

    def swap_cols(i, j):
        for r in A:
            r[i], r[j] = r[j], r[i]
        for r in V:
            r[i], r[j] = r[j], r[i]

    def addrow(dst, src, f):
        for c in range(n):
            A[dst][c] += f * A[src][c]
        for c in range(m):
            U[dst][c] += f * U[src][c]

    def addcol(dst, src, f):
        for r in range(m):
            A[r][dst] += f * A[r][src]
        for r in range(n):
            V[r][dst] += f * V[r][src]

    t = 0
    while t < min(m, n):
        # find a nonzero pivot in the submatrix
        piv = None
        for i in range(t, m):
            for j in range(t, n):
                if A[i][j] != 0:
                    piv = (i, j)
                    break
            if piv:
                break
        if piv is None:
            break
        swap_rows(t, piv[0])
        swap_cols(t, piv[1])
        while True:
            for i in range(t + 1, m):
                while A[i][t] != 0:
                    f = A[i][t] // A[t][t]
                    addrow(i, t, -f)
                    if A[i][t] != 0:
                        swap_rows(i, t)
            for j in range(t + 1, n):
                while A[t][j] != 0:
                    f = A[t][j] // A[t][t]
                    addcol(j, t, -f)
                    if A[t][j] != 0:
                        swap_cols(j, t)
            if all(A[i][t] == 0 for i in range(t + 1, m)):
                break
        if A[t][t] < 0:
            for c in range(n):
                A[t][c] = -A[t][c]
            for c in range(m):
                U[t][c] = -U[t][c]
        t += 1
    return A, U, V


def mat_mul(A, B):
    n = len(A)
    k = len(B)
    p = len(B[0])
    out = [[0] * p for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        for t in range(k):
            a = Ai[t]
            if a:
                Bt = B[t]
                Oi = out[i]
                for j in range(p):
                    Oi[j] += a * Bt[j]
    return out


def mat_inv_unimodular(M):
    """Inverse of a unimodular integer matrix (exact, via Fraction Gauss)."""
    n = len(M)
    A = [[Fraction(x) for x in row] + [Fraction(int(i == j)) for j in range(n)]
         for i, row in enumerate(M)]
    for c in range(n):
        piv = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[piv] = A[piv], A[c]
        inv = A[c][c]
        A[c] = [x / inv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    out = [[x for x in row[n:]] for row in A]
    for row in out:
        for x in row:
            assert x.denominator == 1, "matrix was not unimodular"
    return [[int(x) for x in row] for row in out]


# ----------------------------------------------------- reduced system


class ReducedSystem:
    """The template's value system as Laurent equations on (C*)^d."""

    def __init__(self, system):
        self.system = system
        rows = []
        for monos in list(system.mixed_eqs.values()) + \
                list(system.const_eqs.values()):
            base = LAT.exponent_vector(monos[0], system.nvars)
            for mono in monos[1:]:
                cur = LAT.exponent_vector(mono, system.nvars)
                rows.append([a - b for a, b in zip(cur, base)])
        self.basis = hnf_basis(rows)
        self.d = len(self.basis)
        self.pivots = pivots_of(self.basis)
        self.mixed = {}   # word -> list of exponent rows (len = size-1)
        self.const = {}
        for src, dst in ((system.mixed_eqs, self.mixed),
                         (system.const_eqs, self.const)):
            for w, monos in src.items():
                base = LAT.exponent_vector(monos[0], system.nvars)
                exps = []
                for mono in monos[1:]:
                    cur = LAT.exponent_vector(mono, system.nvars)
                    diff = [a - b for a, b in zip(cur, base)]
                    c = solve_in_basis(self.basis, diff, self.pivots)
                    assert c is not None, "difference not in its own lattice"
                    exps.append(c)
                dst[w] = exps

    def character(self, values, row):
        """Evaluate the character z^row at cell values `values` (Fractions):
        row is in BASIS coordinates, so lift it back to Z^Sigma first."""
        lift = [0] * self.system.nvars
        for c, b in zip(row, self.basis):
            if c:
                for j, x in enumerate(b):
                    if x:
                        lift[j] += c * x
        out = Fraction(1)
        for j, e in enumerate(lift):
            if e:
                out *= Fraction(values[j]) ** e
        return out

    def binomial_rows(self):
        """[(exponent row in Z^d, value)] from the two-term mixed fibres."""
        return [(exps[0], Fraction(-1)) for exps in self.mixed.values()
                if len(exps) == 1]

    def summary(self):
        sizes = {}
        for exps in self.mixed.values():
            sizes[len(exps) + 1] = sizes.get(len(exps) + 1, 0) + 1
        return {"d": self.d, "mixed": len(self.mixed),
                "const": len(self.const), "sizes": sizes}


# ------------------------------------------------- monomial propagation


class MonomialValues:
    """A partial character phi: Lambda' -> Q*  on a sublattice of Z^d.

    Stored as an HNF basis with attached values; membership + evaluation are
    exact.  `learn` adds a relation and reports CONTRADICTION if the new
    relation conflicts with the stored ones (that is a KILL certificate)."""

    def __init__(self, d):
        self.d = d
        self.rows = []       # HNF rows
        self.vals = []       # Fraction values, phi(row)
        self._pivots = None
        self.contradiction = None
        self.log = []

    def _eval_exact(self, vec):
        """phi(vec) if vec lies in the stored sublattice, else None."""
        if not self.rows:
            return Fraction(1) if not any(vec) else None
        if self._pivots is None:
            self._pivots = pivots_of(self.rows)
        coeffs = solve_in_basis(self.rows, vec, self._pivots)
        if coeffs is None:
            return None
        out = Fraction(1)
        for c, rv in zip(coeffs, self.vals):
            out *= rv ** c
        return out

    def learn(self, vec, val):
        """Impose phi(vec) = val.  Returns 'new' | 'known' | 'contradiction'."""
        if self.contradiction:
            return "contradiction"
        if val == 0:
            self.contradiction = ("zero-value", list(vec))
            return "contradiction"
        cur = self._eval_exact(vec)
        if cur is not None:
            if cur != val:
                self.contradiction = ("value-clash", list(vec),
                                      str(cur), str(val))
                return "contradiction"
            return "known"
        # insert and re-HNF, carrying values multiplicatively
        rows = self.rows + [list(vec)]
        vals = self.vals + [val]
        H, U = LAT.hnf(rows)
        newvals = []
        for urow in U:
            v = Fraction(1)
            for coef, base in zip(urow, vals):
                if coef:
                    v *= base ** coef
            newvals.append(v)
        self.rows, self.vals = H, newvals
        self._pivots = None
        return "new"


def propagate(red, extra=None, max_rounds=200):
    """Learn monomial values from the equations until closure.

    Returns (MonomialValues, verdict, log).  verdict in
    {'contradiction', 'closed'}."""
    phi = MonomialValues(red.d)
    log = []
    for vec, val in red.binomial_rows():
        st = phi.learn(vec, val)
        log.append(("binomial", st))
        if st == "contradiction":
            return phi, "contradiction", log
    if extra:
        for vec, val in extra:
            st = phi.learn(vec, val)
            log.append(("extra", st))
            if st == "contradiction":
                return phi, "contradiction", log
    zero = [0] * red.d
    for _ in range(max_rounds):
        progress = False
        for w, exps in red.mixed.items():
            terms = [(zero, Fraction(1))] + [(e, None) for e in exps]
            known = Fraction(1)          # the leading 1
            unknown = []
            for e in exps:
                val = phi._eval_exact(e) if phi.rows else None
                if val is None:
                    unknown.append(e)
                else:
                    known += val
            if not unknown:
                if known != 0:
                    return phi, "contradiction", log + [
                        ("all-known-nonzero-sum", "".join(map(str, w)),
                         str(known))]
            elif len(unknown) == 1:
                st = phi.learn(unknown[0], -known)
                log.append(("solve", "".join(map(str, w)), st))
                if st == "contradiction":
                    return phi, "contradiction", log
                if st == "new":
                    progress = True
        if not progress:
            break
    return phi, "closed", log


def constant_status(red, phi):
    """For each constant word: 'forced-zero' (KILL), 'nonzero', 'unknown'."""
    out = {}
    for w, exps in red.const.items():
        total = Fraction(1)
        unknown = 0
        for e in exps:
            val = phi._eval_exact(e) if phi.rows else None
            if val is None:
                unknown += 1
            else:
                total += val
        if unknown == 0:
            out[w[0]] = "forced-zero" if total == 0 else "nonzero"
        else:
            out[w[0]] = f"unknown({unknown} free of {len(exps)})"
    return out
