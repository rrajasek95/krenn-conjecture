#!/usr/bin/env python3
"""UNAUDITED PROBE (A3, node 4: uniform-in-N groundwork).

Pinned HEAD: see PINNED_HEAD.txt.  Nothing here is a committed claim.
Exact arithmetic everywhere (Python ints / Fractions).  No floats.

SETTING (monomial / R_cell regime, general even N).
  Sites V = {0..N-1}, V_v = C^3.  A *monomial template* assigns to each
  unordered pair uv (u<v) either ABSENT or an ordered colour label (a,b),
  meaning A_uv = w_uv * e_a^{(u)} (x) e_b^{(v)} with w_uv in C^*.
  A supported perfect matching M then induces exactly one word c(M) in
  {0,1,2}^V, and

      H_N(A)_c = sum_{M : c(M) = c} prod_{uv in M} w_uv .

  *Exactness*: H_c = 0 for every mixed (non-constant) c, and H_{r^N} != 0
  for r = 0,1,2.  (Diagonal site gauge rescales the three constants
  independently, so "!= 0" is the right normalisation.)

FIBRE REFORMULATION (uniform in N; see REPORT section 1).
  For a word c let  H_c := { uv in E : label(uv) = (c_u, c_v) }  (ordered by
  the vertex order).  Then fibre(c) = PM(H_c) and the GHZ value at c is the
  weighted hafnian  haf(H_c) = sum_{M in PM(H_c)} prod_e w_e.
  For a *diagonal* template (every label of the form (r,r)) this factors:
      H_c = disjoint union over r of G_r[S_r],   S_r = c^{-1}(r),
      |fibre(c)| = prod_r pm(G_r[S_r]),
      value(c)   = prod_r f_r(S_r),  f_r(S) := weighted hafnian of G_r[S].

MECHANISMS used for verdicts:
  (O2) a mixed fibre of size 1  -> a single nonzero monomial = 0, impossible.
  (O1) an odd circuit among binomial fibres: binomial fibre {M+,M-} forces
       x^{d} = -1 with d = chi(M+) - chi(M-); an integer relation
       sum n_i d_i = 0 with sum n_i odd is a "1 = -1" certificate.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

Q = 3
ABSENT = None


# ------------------------------------------------------------ combinatorics

def perfect_matchings(vertices):
    """All perfect matchings of the complete graph on `vertices` (tuple)."""
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for pos in range(1, len(vertices)):
        second = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1:]
        for m in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + m))


def edge_list(n):
    return tuple(combinations(range(n), 2))


class Geometry:
    """Edges / matchings / incidence of K_n, cached."""

    def __init__(self, n):
        self.n = n
        self.edges = edge_list(n)
        self.index = {e: i for i, e in enumerate(self.edges)}
        self.matchings = tuple(perfect_matchings(tuple(range(n))))
        self.matching_edges = tuple(
            tuple(self.index[e] for e in m) for m in self.matchings)

    def exponent(self, k):
        row = [0] * len(self.edges)
        for e in self.matching_edges[k]:
            row[e] += 1
        return tuple(row)


_GEO = {}


def geometry(n):
    if n not in _GEO:
        _GEO[n] = Geometry(n)
    return _GEO[n]


# ------------------------------------------------- fibres of a general template

def fibres(geo, labels):
    """labels[e] = None or (a,b), a the colour at the SMALLER endpoint.

    Returns {word: [matching indices]}.  Direct enumeration -- the honest,
    definition-level computation (used as the control for the fast diagonal
    product formula below)."""
    out = {}
    for k, m in enumerate(geo.matchings):
        word = [-1] * geo.n
        ok = True
        for u, v in m:
            lab = labels[geo.index[(u, v)]]
            if lab is None:
                ok = False
                break
            word[u], word[v] = lab
        if ok:
            out.setdefault(tuple(word), []).append(k)
    return out


def is_mixed(word):
    return len(set(word)) > 1


def fibre_profile(table):
    """(#mixed singleton fibres, histogram of mixed fibre sizes)."""
    hist, singles = {}, 0
    for word, mem in table.items():
        if not is_mixed(word):
            continue
        hist[len(mem)] = hist.get(len(mem), 0) + 1
        if len(mem) == 1:
            singles += 1
    return singles, dict(sorted(hist.items()))


# ------------------------------------------- diagonal templates: product formula

def pm_table(n, adj):
    """pm[S] = number of perfect matchings of the induced subgraph on the
    vertex set given by bitmask S.  adj[v] = bitmask of neighbours of v.

    Exact integer subset DP; pm[0] = 1, odd |S| gives 0 automatically."""
    size = 1 << n
    pm = [0] * size
    pm[0] = 1
    for S in range(1, size):
        v = (S & -S).bit_length() - 1
        rest = S & ~(1 << v)
        total = 0
        cand = adj[v] & rest
        while cand:
            b = cand & -cand
            u = b.bit_length() - 1
            total += pm[rest & ~b]
            cand ^= b
        pm[S] = total
    return pm


def adjacency(n, edges):
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return adj


def colour_partitions(n):
    """All 3^n words as (word, mask0, mask1, mask2)."""
    out = []
    for k in range(3 ** n):
        w, t = [], k
        m = [0, 0, 0]
        for v in range(n):
            r = t % 3
            t //= 3
            w.append(r)
            m[r] |= 1 << v
        out.append((tuple(w), m[0], m[1], m[2]))
    return out


class DiagonalTemplate:
    """G_0, G_1, G_2 pairwise disjoint edge sets on [n] (absent = the rest)."""

    def __init__(self, n, colour_edges):
        self.n = n
        self.colour_edges = [set(map(tuple, es)) for es in colour_edges]
        allе = [e for es in self.colour_edges for e in es]
        assert len(allе) == len(set(allе)), "colour classes must be disjoint"
        self.pm = [pm_table(n, adjacency(n, es)) for es in self.colour_edges]
        self.full = (1 << n) - 1

    def pures(self):
        return [self.pm[r][self.full] for r in range(3)]

    def fibre_size(self, word):
        m = [0, 0, 0]
        for v, r in enumerate(word):
            m[r] |= 1 << v
        return self.pm[0][m[0]] * self.pm[1][m[1]] * self.pm[2][m[2]]

    def census(self, parts=None):
        """(singletons, histogram of mixed fibre sizes, pure sizes)."""
        if parts is None:
            parts = colour_partitions(self.n)
        hist, singles, singleton_words = {}, 0, []
        for word, m0, m1, m2 in parts:
            if not is_mixed(word):
                continue
            size = self.pm[0][m0] * self.pm[1][m1] * self.pm[2][m2]
            if size == 0:
                continue
            hist[size] = hist.get(size, 0) + 1
            if size == 1:
                singles += 1
                singleton_words.append(word)
        return singles, dict(sorted(hist.items())), self.pures(), singleton_words

    def labels(self):
        """Ordered-label form, for the direct-enumeration control."""
        geo = geometry(self.n)
        lab = [None] * len(geo.edges)
        for r, es in enumerate(self.colour_edges):
            for e in es:
                lab[geo.index[tuple(sorted(e))]] = (r, r)
        return lab


# ---------------------------------------------------- odd-circuit certificates

def hermite_with_transform(rows):
    """(H, U, pivots, rank) with U unimodular, U*rows = H row-echelon."""
    m = len(rows)
    n = len(rows[0]) if m else 0
    H = [list(r) for r in rows]
    U = [[1 if i == j else 0 for j in range(m)] for i in range(m)]
    pr, pivots = 0, []
    for col in range(n):
        tgt = None
        for r in range(pr, m):
            if H[r][col] != 0:
                tgt = r
                break
        if tgt is None:
            continue
        H[pr], H[tgt] = H[tgt], H[pr]
        U[pr], U[tgt] = U[tgt], U[pr]
        for r in range(pr + 1, m):
            while H[r][col] != 0:
                a, b = H[pr][col], H[r][col]
                if abs(b) >= abs(a):
                    f = b // a
                    for c in range(n):
                        H[r][c] -= f * H[pr][c]
                    for c in range(m):
                        U[r][c] -= f * U[pr][c]
                else:
                    H[pr], H[r] = H[r], H[pr]
                    U[pr], U[r] = U[r], U[pr]
        if H[pr][col] < 0:
            H[pr] = [-x for x in H[pr]]
            U[pr] = [-x for x in U[pr]]
        pivots.append(col)
        pr += 1
        if pr == m:
            break
    return H, U, pivots, pr


def odd_circuit(diffs):
    """Given integer difference vectors d_i (each carrying the value -1),
    return an integer relation sum n_i d_i = 0 with sum n_i ODD, or None.

    Such a relation is a '1 = -1' certificate (O1)."""
    if not diffs:
        return None
    H, U, piv, rank = hermite_with_transform([list(d) for d in diffs])
    for r in range(rank, len(diffs)):
        rel = U[r]
        if sum(rel) % 2:
            return rel
    return None


def binomial_diffs(geo, table):
    """[(word, difference vector)] over mixed fibres of size exactly 2."""
    out = []
    for word, mem in sorted(table.items()):
        if is_mixed(word) and len(mem) == 2:
            a, b = geo.exponent(mem[0]), geo.exponent(mem[1])
            out.append((word, tuple(x - y for x, y in zip(a, b))))
    return out
