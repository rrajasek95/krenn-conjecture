#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- thick-fibre kill engine at N = 8, d = 3.

Pinned HEAD: see PINNED_HEAD.txt.
Plan: notes/2026-08-15-resolution-master-plan.md, v14 addendum (W12 mission).
NOTHING HERE IS A PROVED CLAIM OF THE PROJECT -- it is probe output.

Independent re-implementation (pure Python ints / Fraction; no numpy anywhere
in this file) of the model conventions of W8's w8_core.py.  Every fibre
number produced here is computed from scratch and is cross-checked against
W8's published histograms in run_t4_controls.py.

MODEL.  N = 8 sites, V_v = C^3, one 3x3 block A_uv per edge uv of K_8 with
u < v (rows = colour at u, columns = colour at v).  For a word w in {0,1,2}^8

    H(A)_w = sum over the 105 perfect matchings M of K_8 of
             prod_{uv in M} A_uv[w_u][w_v].

EXACT: H_w = 1 on the three constant words, 0 on the 6558 mixed words.
Diagonal gauge rescales the three constant values independently, so

    EXACT SOURCE with template T  <=>  values x on the occupied cells, all
    NONZERO, with (mixed) fibre sum = 0 and (constant) fibre sum != 0.

TEMPLATE.  T[e] is a 9-bit mask; bit 3*i+j set means cell (i,j) of edge e is
occupied.  m = supp(T) = # nonzero blocks (EDGES).  Sigma(T) = # cells.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import os
import subprocess
import tempfile

N = 8
Q = 3
FULL9 = (1 << 9) - 1


def require(condition, message):
    if not condition:
        raise ValueError(message)


# ------------------------------------------------------------- geometry


def perfect_matchings(vertices):
    """All perfect matchings of the complete graph on `vertices` (a tuple)."""
    if not vertices:
        return [()]
    first = vertices[0]
    out = []
    for index in range(1, len(vertices)):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            out.append(tuple(sorted(((first, vertices[index]),) + tail)))
    return out


class Geometry:
    """Edges, matchings, words -- all pure Python."""

    def __init__(self, size=N):
        self.size = size
        self.edges = tuple(combinations(range(size), 2))
        self.eindex = {e: n for n, e in enumerate(self.edges)}
        self.matchings = tuple(perfect_matchings(tuple(range(size))))
        self.medges = tuple(tuple(self.eindex[e] for e in m)
                            for m in self.matchings)
        self.words = tuple(product(range(Q), repeat=size))
        self.windex = {w: n for n, w in enumerate(self.words)}
        self.constant_words = tuple((c,) * size for c in range(Q))
        self.incident = tuple(tuple(self.eindex[tuple(sorted((p, j)))]
                                    for j in range(size) if j != p)
                              for p in range(size))

    def is_mixed(self, word):
        return any(c != word[0] for c in word)

    def cell_of(self, edge_index, word):
        u, v = self.edges[edge_index]
        return (word[u], word[v])


_GEO = {}


def geometry(size=N):
    if size not in _GEO:
        _GEO[size] = Geometry(size)
    return _GEO[size]


# ------------------------------------------------------------- templates


def cells(mask):
    return [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]


def bit(i, j):
    return 1 << (3 * i + j)


def support(template):
    return sum(1 for mask in template if mask)


def sigma(template):
    return sum(bin(mask).count("1") for mask in template)


def far_thin_colour(mask, at_second):
    """Unique far-end colour if the block is thin at that endpoint, else None.

    at_second=True asks about the SECOND endpoint (i.e. the block, seen from
    the FIRST endpoint, is supported in a single column colour)."""
    if not mask:
        return None
    seen = {(j if at_second else i) for i, j in cells(mask)}
    return seen.pop() if len(seen) == 1 else None


def block_class(mask):
    if not mask:
        return "zero"
    if bin(mask).count("1") == 1:
        return "single"
    a = far_thin_colour(mask, False) is not None
    b = far_thin_colour(mask, True) is not None
    return "thin" if (a or b) else "fat"


def fie_demands(geo, template):
    """{(p,r): [edges serving demand (p,r)]} for the 24 (vertex,colour) slots.

    (SC)/(FIE): for every vertex p and colour r some incident block must be
    nonzero and supported in the single FAR-END colour r."""
    out = {}
    for p in range(geo.size):
        for r in range(Q):
            servers = []
            for e in geo.incident[p]:
                u, v = geo.edges[e]
                colour = far_thin_colour(template[e], at_second=(u == p))
                if colour == r:
                    servers.append(e)
            out[(p, r)] = servers
    return out


def fie_ok(geo, template):
    return all(v for v in fie_demands(geo, template).values())


# ------------------------------------------------------------- fibres


def fibre(geo, template, word):
    """Matching indices whose every edge has the word's cell occupied."""
    out = []
    for n, medges in enumerate(geo.medges):
        good = True
        for e in medges:
            u, v = geo.edges[e]
            if not ((template[e] >> (3 * word[u] + word[v])) & 1):
                good = False
                break
        if good:
            out.append(n)
    return out


def all_fibres(geo, template):
    """{word: [matching indices]} over every word with a NONEMPTY fibre."""
    # cell-occupancy lookup per edge, per (colour_u, colour_v)
    occ = [[[(mask >> (3 * i + j)) & 1 for j in range(Q)] for i in range(Q)]
           for mask in template]
    out = {}
    for word in geo.words:
        got = []
        for n, medges in enumerate(geo.medges):
            for e in medges:
                u, v = geo.edges[e]
                if not occ[e][word[u]][word[v]]:
                    break
            else:
                got.append(n)
        if got:
            out[word] = got
    return out


def fibre_histogram(geo, template, fib=None):
    """{size: count} over MIXED words with nonempty fibre."""
    if fib is None:
        fib = all_fibres(geo, template)
    hist = {}
    for word, ms in fib.items():
        if geo.is_mixed(word):
            hist[len(ms)] = hist.get(len(ms), 0) + 1
    return hist


def audit(geo, template, fib=None):
    if fib is None:
        fib = all_fibres(geo, template)
    classes = [block_class(mask) for mask in template]
    hist = fibre_histogram(geo, template, fib)
    return {
        "m": support(template),
        "sigma": sigma(template),
        "beta": classes.count("single"),
        "thin": classes.count("thin"),
        "fat": classes.count("fat"),
        "fie": fie_ok(geo, template),
        "constants": all(w in fib for w in geo.constant_words),
        "mixed_singletons": sum(1 for w, ms in fib.items()
                                if geo.is_mixed(w) and len(ms) == 1),
        "fibre_histogram": {int(k): int(v) for k, v in sorted(hist.items())},
        "min_mixed_fibre": min([len(ms) for w, ms in fib.items()
                                if geo.is_mixed(w)] or [0]),
        "mixed_words_live": sum(1 for w in fib if geo.is_mixed(w)),
    }


# ------------------------------------------------- the polynomial system


class ValueSystem:
    """Monomial system attached to a template.

    Variables: occupied cells, indexed 0..Sigma-1 as (edge, i, j).
    A word's fibre becomes a sum of squarefree degree-4 monomials in those
    variables (one variable per matching edge).  Mixed words: sum = 0.
    Constant words: sum != 0.  Every variable is required NONZERO.
    """

    def __init__(self, geo, template):
        self.geo = geo
        self.template = tuple(template)
        self.vars = []           # (edge, i, j)
        self.varindex = {}
        for e, mask in enumerate(template):
            for (i, j) in cells(mask):
                self.varindex[(e, i, j)] = len(self.vars)
                self.vars.append((e, i, j))
        self.nvars = len(self.vars)
        self.fib = all_fibres(geo, template)
        self.mixed_eqs = {}      # word -> list of monomials (tuples of vars)
        self.const_eqs = {}
        for word, ms in self.fib.items():
            monomials = []
            for n in ms:
                mono = []
                for e in geo.medges[n]:
                    u, v = geo.edges[e]
                    mono.append(self.varindex[(e, word[u], word[v])])
                monomials.append(tuple(sorted(mono)))
            monomials.sort()
            if geo.is_mixed(word):
                self.mixed_eqs[word] = monomials
            else:
                self.const_eqs[word] = monomials

    def varname(self, n):
        e, i, j = self.vars[n]
        u, v = self.geo.edges[e]
        return f"x_{u}{v}_{i}{j}"

    def evaluate(self, values, word):
        """Exact fibre sum at a rational/complex-rational assignment."""
        total = 0
        for mono in (self.mixed_eqs.get(word) or self.const_eqs.get(word) or []):
            term = 1
            for v in mono:
                term *= values[v]
            total += term
        return total

    def check_exact(self, values):
        """(mixed_defects, constant_values) at an assignment."""
        defects = [w for w in self.mixed_eqs if self.evaluate(values, w) != 0]
        consts = {w: self.evaluate(values, w) for w in self.geo.constant_words}
        return defects, consts


# ------------------------------------------------------------- Singular


def run_singular(script, timeout=1800, quiet=True):
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script + "\nquit;\n")
        path = fh.name
    try:
        proc = subprocess.run(["Singular", "-q", "--no-warn", path],
                              capture_output=True, text=True, timeout=timeout)
    finally:
        os.unlink(path)
    if proc.returncode != 0:
        raise RuntimeError(f"Singular failed: {proc.stderr[:4000]}")
    return proc.stdout


def poly_from_monomials(monomials, names, coeffs=None):
    """Sum of monomials as a Singular polynomial string."""
    parts = []
    for k, mono in enumerate(monomials):
        c = 1 if coeffs is None else coeffs[k]
        body = "*".join(names[v] for v in mono)
        parts.append(f"{c}*{body}" if c != 1 else body)
    return "+".join(parts) if parts else "0"
