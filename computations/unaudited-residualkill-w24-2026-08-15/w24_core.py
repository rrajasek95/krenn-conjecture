#!/usr/bin/env python3
"""W24 -- THE RESIDUAL-LINEAR-KILL THEOREM.  UNAUDITED PROBE.

Pinned HEAD: see PINNED_HEAD.txt.  Nothing here is a proved claim of the
repository.  EXACT ARITHMETIC ONLY (int / Fraction / exact sparse
polynomials / Singular over Q).  No floats anywhere.

This core is written FROM THE MODEL DEFINITION and is independent of
w20_core / w21_core (which are imported only in the control scripts for
cross-checking).

MODEL.  N = 8 vertices, alphabet {0,1,2}; a 3x3 complex block A_uv per edge
uv of K_8.  For a word w in {0,1,2}^8,
    H_w(A) = sum over the 105 perfect matchings M of K_8 of
             prod_{(u,v) in M} A_uv[w_u][w_v].
EXACT source  <=>  H_w = 1 on the three constant words and H_w = 0 on all
6,558 mixed words.  A TEMPLATE T assigns to each edge a 9-bit mask of the
cells allowed to be nonzero; support m = number of edges with a nonzero
mask.  A source realises T if every cell outside the mask is zero and every
cell inside is nonzero.

TEMPLATE STRUCTURE at m = 25..28 (verified in w24_struct.py):
  Gamma  = edges with the FULL mask;
  twelve SINGLE edges, each carrying one cell (alpha_e, beta_e).
Writing z_e for the single cell's value, for a mixed word w
    H_w(z) = sum_{S a partial matching of singles ACTIVE at w}
               (prod_{e in S} z_e) * haf_Gamma(V \\ V(S))(w),
where a single e = (i,j) is ACTIVE at w iff (w_i, w_j) = (alpha_e, beta_e).
Degree of H_w in z = max |S| over such S with haf_Gamma(V \\ V(S)) a
nonempty sum (i.e. the complement has a Gamma perfect matching).
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations, product

sys.dont_write_bytecode = True

N = 8
Q = 3
FULL = 511

EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}


def _perfect_matchings(vs):
    if not vs:
        return [()]
    a, rest = vs[0], vs[1:]
    out = []
    for i, b in enumerate(rest):
        for mm in _perfect_matchings(rest[:i] + rest[i + 1:]):
            out.append(((a, b),) + mm)
    return out


PMS = tuple(tuple(sorted(m)) for m in _perfect_matchings(tuple(range(N))))
assert len(PMS) == 105

WORDS = tuple(product(range(Q), repeat=N))
MIXED = tuple(w for w in WORDS if len(set(w)) > 1)
assert len(MIXED) == 6558

# templates: identical literal encoding to W8/W19/W20/W21 (independently
# re-typed here; w24_ctrl.py asserts equality with w21_core.W8_IMMUNE).
TEMPLATES = {
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


def gamma_edges(T):
    return tuple(EDGES[i] for i, t in enumerate(T) if t == FULL)


def single_edges(T):
    """{edge: (alpha, beta)} for the one-cell blocks."""
    out = {}
    for i, t in enumerate(T):
        if t in (0, FULL):
            continue
        cs = [c for c in range(9) if (t >> c) & 1]
        assert len(cs) == 1, (EDGES[i], t, cs)
        out[EDGES[i]] = (cs[0] // 3, cs[0] % 3)
    return out


def active_singles(T, w):
    """the single edges active at the word w."""
    return tuple(e for e, (a, b) in single_edges(T).items()
                 if w[e[0]] == a and w[e[1]] == b)


# --------------------------------------------------------------- hafnians
def haf_on(blocks, gam_set, verts, w):
    """sum over perfect matchings of Gamma restricted to `verts`."""
    verts = tuple(sorted(verts))
    if not verts:
        return Fraction(1)
    a = verts[0]
    tot = Fraction(0)
    for i in range(1, len(verts)):
        b = verts[i]
        e = (a, b) if a < b else (b, a)
        if e not in gam_set:
            continue
        c = blocks[e][w[e[0]]][w[e[1]]]
        if c == 0:
            continue
        tot += c * haf_on(blocks, gam_set, verts[1:i] + verts[i + 1:], w)
    return tot


def phi(blocks, gam_set, w):
    return haf_on(blocks, gam_set, tuple(range(N)), w)


def has_pm(gam_set, verts):
    """does Gamma restricted to `verts` have a perfect matching?"""
    verts = tuple(sorted(verts))
    if not verts:
        return True
    a = verts[0]
    for i in range(1, len(verts)):
        b = verts[i]
        e = (a, b) if a < b else (b, a)
        if e in gam_set and has_pm(gam_set, verts[1:i] + verts[i + 1:]):
            return True
    return False


def H_word(blocks, T, z, w):
    """H_w from the definition: sum over ALL 105 matchings, using the
    template-restricted blocks (Gamma blocks from `blocks`, singles from
    `z`, everything else zero)."""
    sing = single_edges(T)
    gam_set = set(gamma_edges(T))
    tot = Fraction(0)
    for M in PMS:
        p = Fraction(1)
        for (u, v) in M:
            if (u, v) in gam_set:
                p *= blocks[(u, v)][w[u]][w[v]]
            elif (u, v) in sing and (w[u], w[v]) == sing[(u, v)]:
                p *= z[(u, v)]
            else:
                p = Fraction(0)
            if p == 0:
                break
        tot += p
    return tot


def clean_words(T):
    """mixed words with NO active single (all supported matchings inside
    Gamma).  NOTE: the equivalence 'no active single <=> every supported
    matching lies in Gamma' needs every active single to extend; checked
    in w24_struct.py per m."""
    return tuple(w for w in MIXED if not active_singles(T, w))


# ---------------------------------------------------------- linear algebra
def rref(rows, ncols):
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
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return M[:r], piv


def kernel_basis(rows, ncols):
    if not rows:
        return [[Fraction(int(i == k)) for i in range(ncols)]
                for k in range(ncols)]
    R, piv = rref(rows, ncols)
    out = []
    for f in [c for c in range(ncols) if c not in piv]:
        v = [Fraction(0)] * ncols
        v[f] = Fraction(1)
        for i, p in enumerate(piv):
            v[p] = -R[i][f]
        out.append(v)
    return out
