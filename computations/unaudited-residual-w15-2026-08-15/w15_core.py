#!/usr/bin/env python3
"""UNAUDITED PROBE (W15) -- residual family (R) at N = 8.

Pinned HEAD: see PINNED_HEAD.txt.
Nothing here is a proved claim of the repository.  Every verdict uses
exact arithmetic (Python int / Fraction / exact sparse polynomials).
No floats anywhere in this file.

INDEPENDENT RE-IMPLEMENTATION of the model (deliberately not importing
W8/W12 code, so that the calibration against W8's stored audit numbers
is a genuine cross-check).

MODEL.  N = 8 sites, V_v = C^3, one 3x3 block A_uv per edge uv of K_8
with u < v; rows indexed by the colour at u, columns by the colour at v.
For a word w in {0,1,2}^8

    H(A)_w = sum over perfect matchings M of K_8 of
             prod_{uv in M} A_uv[w_u][w_v].

EXACT SOURCE: H_w = 0 on all 6558 mixed words, H_w != 0 on the three
constant words (W10-G: nonzero pures + mixed-exact => gauge-equivalent
to fully exact with the SAME template).

TEMPLATE: T[e] a 9-bit mask, bit 3*i+j set  <=>  cell (i,j) occupied.
Edges are enumerate(combinations(range(8),2)) -- lexicographic.
An exact source WITH TEMPLATE T has all occupied cells nonzero and all
unoccupied cells zero.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

N = 8
Q = 3
FULL = (1 << 9) - 1

EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}


def perfect_matchings(vertices):
    """All perfect matchings of the complete graph on `vertices`."""
    if not vertices:
        return [()]
    first = vertices[0]
    out = []
    for k in range(1, len(vertices)):
        rest = vertices[1:k] + vertices[k + 1:]
        for tail in perfect_matchings(rest):
            out.append(tuple(sorted(((first, vertices[k]),) + tail)))
    return out


MATCHINGS = tuple(perfect_matchings(tuple(range(N))))          # 105
MATCH_EIDX = tuple(tuple(EIDX[e] for e in m) for m in MATCHINGS)

WORDS = tuple(product(range(Q), repeat=N))                      # 6561
CONST_WORDS = tuple(tuple([c] * N) for c in range(Q))
MIXED_WORDS = tuple(w for w in WORDS if len(set(w)) > 1)         # 6558


def cell_of(edge_index, word):
    u, v = EDGES[edge_index]
    return 3 * word[u] + word[v]


def occupied(template, edge_index, cell):
    return (template[edge_index] >> cell) & 1


def supported_matchings(template, word):
    """Indices of the perfect matchings all of whose cells are occupied."""
    out = []
    for mi, eids in enumerate(MATCH_EIDX):
        ok = True
        for e in eids:
            if not occupied(template, e, cell_of(e, word)):
                ok = False
                break
        if ok:
            out.append(mi)
    return out


def fibre_sizes(template):
    """word -> number of supported matchings (the 'fibre')."""
    return {w: len(supported_matchings(template, w)) for w in WORDS}


def audit(template):
    """Reproduce W8's audit fields independently."""
    m = sum(1 for t in template if t)
    sigma = sum(bin(t).count("1") for t in template)
    hist = {}
    min_mixed = None
    for w in MIXED_WORDS:
        s = len(supported_matchings(template, w))
        hist[s] = hist.get(s, 0) + 1
        if min_mixed is None or s < min_mixed:
            min_mixed = s
    consts = [len(supported_matchings(template, w)) for w in CONST_WORDS]
    full = [i for i, t in enumerate(template) if t == FULL]
    singles = [i for i, t in enumerate(template)
               if t and bin(t).count("1") == 1]
    return dict(m=m, sigma=sigma, fibre_histogram=hist,
                min_mixed_fibre=min_mixed, constant_fibres=consts,
                n_full=len(full), n_single=len(singles),
                full_edges=[EDGES[i] for i in full],
                single_cells={EDGES[i]: (template[i].bit_length() - 1)
                              for i in singles})


# --------------------------------------------------------------- Gamma

def gamma_graph(template):
    return [EDGES[i] for i, t in enumerate(template) if t == FULL]


def is_spanning_2_connected(edges, n=N):
    verts = set()
    for u, v in edges:
        verts.add(u)
        verts.add(v)
    if verts != set(range(n)):
        return False, "not spanning"

    def connected(skip):
        adj = {v: set() for v in range(n) if v != skip}
        for u, v in edges:
            if u != skip and v != skip:
                adj[u].add(v)
                adj[v].add(u)
        start = next(iter(adj))
        seen = {start}
        stack = [start]
        while stack:
            a = stack.pop()
            for b in adj[a]:
                if b not in seen:
                    seen.add(b)
                    stack.append(b)
        return len(seen) == len(adj)

    if not connected(None if False else -1):
        return False, "disconnected"
    for s in range(n):
        if not connected(s):
            return False, f"cut vertex {s}"
    return True, "spanning 2-connected"


# ------------------------------------------ exact sparse polynomials
# A polynomial is a dict: monomial (sorted tuple of variable ids, with
# repetition) -> Fraction coefficient.  Variables are small ints.

def pzero():
    return {}


def pconst(c):
    c = Fraction(c)
    return {} if c == 0 else {(): c}


def pvar(i):
    return {(i,): Fraction(1)}


def padd(a, b):
    out = dict(a)
    for mon, c in b.items():
        nc = out.get(mon, Fraction(0)) + c
        if nc:
            out[mon] = nc
        elif mon in out:
            del out[mon]
    return out


def pneg(a):
    return {m: -c for m, c in a.items()}


def psub(a, b):
    return padd(a, pneg(b))


def pmul(a, b):
    out = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            mon = tuple(sorted(ma + mb))
            nc = out.get(mon, Fraction(0)) + ca * cb
            if nc:
                out[mon] = nc
            elif mon in out:
                del out[mon]
    return out


def pscale(a, c):
    c = Fraction(c)
    if c == 0:
        return {}
    return {m: v * c for m, v in a.items()}


def piszero(a):
    return not a


def peval(a, values):
    """values: dict var id -> Fraction."""
    tot = Fraction(0)
    for mon, c in a.items():
        t = c
        for v in mon:
            t *= values[v]
        tot += t
    return tot


# ------------------------------------------------ variable bookkeeping

class VarMap:
    """Assigns a polynomial variable to every occupied cell of a template."""

    def __init__(self, template):
        self.template = tuple(template)
        self.ids = {}
        self.names = []
        for e in range(len(EDGES)):
            for cell in range(9):
                if occupied(template, e, cell):
                    self.ids[(e, cell)] = len(self.names)
                    u, v = EDGES[e]
                    self.names.append(f"A{u}{v}_{cell // 3}{cell % 3}")

    def var(self, edge_index, cell):
        return self.ids[(edge_index, cell)]

    def __len__(self):
        return len(self.names)


def word_polynomial(template, vmap, word):
    """Exact sparse polynomial H_w in the occupied-cell variables."""
    out = pzero()
    for mi in supported_matchings(template, word):
        mon = []
        for e in MATCH_EIDX[mi]:
            mon.append(vmap.var(e, cell_of(e, word)))
        out = padd(out, {tuple(sorted(mon)): Fraction(1)})
    return out


def word_monomials(template, vmap, word):
    """List of monomials (tuples of var ids), one per supported matching."""
    res = []
    for mi in supported_matchings(template, word):
        res.append(tuple(sorted(vmap.var(e, cell_of(e, word))
                                for e in MATCH_EIDX[mi])))
    return res


# ------------------------------------------------------ (R) instances
# W8's saved immunity templates (computations/unaudited-template-kill-w8
# -2026-08-15/results_immunity.json).  Copied verbatim; a checker in
# w15_task0_calibrate.py re-reads the JSON and asserts equality.

W8_IMMUNE = {
    20: [511, 0, 511, 1, 2, 4, 0, 511, 0, 0, 8, 16, 4, 511, 8, 0, 128, 32,
         64, 128, 0, 256, 511, 0, 511, 511, 0, 511],
    21: [511, 511, 511, 1, 2, 4, 0, 511, 0, 0, 8, 16, 4, 511, 8, 0, 128, 32,
         64, 128, 0, 256, 511, 0, 511, 511, 0, 511],
    22: [511, 511, 511, 1, 2, 4, 511, 511, 0, 0, 8, 16, 4, 511, 8, 0, 128,
         32, 64, 128, 0, 256, 511, 0, 511, 511, 0, 511],
    23: [511, 511, 511, 1, 2, 4, 511, 511, 511, 0, 8, 16, 4, 511, 8, 0, 128,
         32, 64, 128, 0, 256, 511, 0, 511, 511, 0, 511],
    24: [511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 0,
         128, 32, 64, 128, 0, 256, 511, 0, 511, 511, 0, 511],
    25: [511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 511,
         128, 32, 64, 128, 0, 256, 511, 0, 511, 511, 0, 511],
    26: [511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 511,
         128, 32, 64, 128, 511, 256, 511, 0, 511, 511, 0, 511],
    27: [511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 511,
         128, 32, 64, 128, 511, 256, 511, 511, 511, 511, 0, 511],
    28: [511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 511,
         128, 32, 64, 128, 511, 256, 511, 511, 511, 511, 511, 511],
}


def single_cell_activity(template):
    """(edge, cell) -> the pair of (vertex, colour) constraints it needs."""
    out = {}
    for e, t in enumerate(template):
        if t and bin(t).count("1") == 1:
            cell = t.bit_length() - 1
            u, v = EDGES[e]
            out[e] = ((u, cell // 3), (v, cell % 3))
    return out


def is_clean(template, word, activity=None):
    """True iff no single-cell block is active on `word`."""
    if activity is None:
        activity = single_cell_activity(template)
    for e, ((u, cu), (v, cv)) in activity.items():
        if word[u] == cu and word[v] == cv:
            return False
    return True
