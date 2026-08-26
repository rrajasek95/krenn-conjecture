#!/usr/bin/env python3
"""UNAUDITED PROBE (W6) -- bridge lemmas J.1c / J.1d: shared exact core.

Pinned HEAD: 31cefe2b247450d1168abc07f6dc73318c068e44
Plan: notes/2026-08-15-resolution-master-plan.md (v3 addendum, J.1c and J.1d).
NOTHING HERE IS A PROVED CLAIM.  Exact integer/Fraction arithmetic only.

Two exact objects are built here.

(1) THE EDGE EXPANSION AT A PAIR.  For a source A on N named sites and a pair
    (p, q), split every perfect matching of B = {0..N-1} according to whether
    it uses the edge pq.  With U = B \\ {p, q}, v a colouring of U, and
    i, j the colours at p, q:

        H_B(A)_{(i,j,v)} = A_pq[i][j] * C(v)  +  D(v)[i][j],          (EXP)

        C(v)    = H_U(A|_U)(v)                     complementary hafnian
        D(v)    = P(v) M(v) Q(v)^T                 3x3 matrix
        P(v)    = 3 x |U| matrix, column u = A_pu[.][v_u]
        Q(v)    = 3 x |U| matrix, column u = A_qu[.][v_u]
        M(v)    = |U| x |U| symmetric, zero diagonal,
                  M(v)[u][u'] = H_{U \\ {u,u'}}(A)(v)

    (EXP) is a combinatorial identity valid for EVERY source; it is verified
    exactly here against brute-force hafnians.

(2) THE EXACTNESS CONSEQUENCE.  If H_B(A) = Delta_{B,3} then for every
    NON-CONSTANT colouring v of U every word (i, j, v) is mixed, so

        C(v) * A_pq  =  - P(v) M(v) Q(v)^T   for all non-constant v.   (STAR)

    So on an exact source the pair block is pinned, entry by entry, by its
    neighbourhood: if C(v) != 0 for one non-constant v then A_pq is
    DETERMINED by the rest of the source.  This is the mechanism J.1c(b)
    asks for.

Conventions match the p1/p2/w2 probe directories: blocks are keyed by the
sorted pair (u, v) with row index the colour at u.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product

COLORS = (0, 1, 2)


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


# ------------------------------------------------------------- combinatorics


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple) -> tuple:
    if not vertices:
        return ((),)
    first = vertices[0]
    out = []
    for index in range(1, len(vertices)):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            out.append(((first, vertices[index]),) + tail)
    return tuple(out)


def edge_key(u, v):
    return (u, v) if u < v else (v, u)


def oriented(source, u, v):
    """3x3 table with row index = colour at u, column index = colour at v."""
    if u < v:
        return source[(u, v)]
    table = source[(v, u)]
    return [[table[b][a] for b in COLORS] for a in COLORS]


def zero_source(size):
    return {(u, v): [[0] * 3 for _ in range(3)]
            for u, v in combinations(range(size), 2)}


def hafnian(source, vertices: tuple, colour) -> Fraction:
    """H_S(A)(colour); ``colour`` is a dict site -> colour on ``vertices``."""
    if not vertices:
        return Fraction(1)
    total = Fraction(0)
    for matching in perfect_matchings(tuple(sorted(vertices))):
        term = Fraction(1)
        for u, v in matching:
            term *= oriented(source, u, v)[colour[u]][colour[v]]
            if term == 0:
                break
        total += term
    return total


def full_tensor(source, size):
    """{word: coefficient} over all 3^size words (word[u] is the colour at u)."""
    sites = tuple(range(size))
    out = {}
    for word in product(COLORS, repeat=size):
        colour = {u: word[u] for u in sites}
        out[word] = hafnian(source, sites, colour)
    return out


def ghz_defect(source, size):
    """Number of words where H != Delta (0 == exact)."""
    bad = 0
    for word, value in full_tensor(source, size).items():
        target = 1 if len(set(word)) == 1 else 0
        if value != target:
            bad += 1
    return bad


# ---------------------------------------------------------- the edge expansion


def pair_expansion(source, size, p, q, v):
    """(C(v), M(v), P(v), Q(v), D(v)) for a colouring v of U = B\\{p,q}.

    ``v`` is a dict site -> colour defined on U.
    """
    U = tuple(sorted(site for site in range(size) if site not in (p, q)))
    C = hafnian(source, U, v)
    P = [[oriented(source, p, u)[i][v[u]] for u in U] for i in COLORS]
    Q = [[oriented(source, q, u)[j][v[u]] for u in U] for j in COLORS]
    M = [[Fraction(0)] * len(U) for _ in U]
    for a in range(len(U)):
        for b in range(len(U)):
            if a == b:
                continue
            rest = tuple(x for x in U if x not in (U[a], U[b]))
            M[a][b] = hafnian(source, rest, v)
    D = [[sum(P[i][a] * M[a][b] * Q[j][b]
              for a in range(len(U)) for b in range(len(U)))
          for j in COLORS] for i in COLORS]
    return C, M, P, Q, D


def verify_edge_expansion(source, size, p, q, words=None):
    """Check (EXP) exactly.  Returns (#checked, #violations)."""
    U = tuple(sorted(site for site in range(size) if site not in (p, q)))
    tensor = full_tensor(source, size)
    checked = violations = 0
    universe = words if words is not None else list(product(COLORS, repeat=len(U)))
    for vword in universe:
        v = {u: vword[n] for n, u in enumerate(U)}
        C, _M, _P, _Q, D = pair_expansion(source, size, p, q, v)
        block = oriented(source, p, q)
        for i in COLORS:
            for j in COLORS:
                colour = dict(v)
                colour[p], colour[q] = i, j
                word = tuple(colour[u] for u in range(size))
                lhs = tensor[word]
                rhs = block[i][j] * C + D[i][j]
                checked += 1
                if lhs != rhs:
                    violations += 1
    return checked, violations


# --------------------------------------------------------- block classification


def matrix_rank(matrix):
    rows = [[Fraction(x) for x in row] for row in matrix]
    rank = 0
    for column in range(3):
        pivot = None
        for index in range(rank, len(rows)):
            if rows[index][column] != 0:
                pivot = index
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        head = rows[rank]
        for index in range(len(rows)):
            if index != rank and rows[index][column] != 0:
                factor = rows[index][column] / head[column]
                rows[index] = [a - factor * b for a, b in zip(rows[index], head)]
        rank += 1
    return rank


def cells(matrix):
    return [(i, j) for i in COLORS for j in COLORS if matrix[i][j]]


def rank_one_factors(matrix):
    """(a, b) with matrix = a (x) b, or None if rank != 1."""
    if matrix_rank(matrix) != 1:
        return None
    pivot = next((i, j) for i in COLORS for j in COLORS if matrix[i][j])
    i0, j0 = pivot
    a = [Fraction(matrix[i][j0]) for i in COLORS]
    b = [Fraction(matrix[i0][j]) / Fraction(matrix[i0][j0]) for j in COLORS]
    require(all(matrix[i][j] == a[i] * b[j] for i in COLORS for j in COLORS),
            "rank-one factorisation failed")
    return a, b


def is_coordinate(vector):
    return sum(1 for x in vector if x) == 1


def classify_block(matrix):
    """'zero' | 'basis' | 'rank1-one-coordinate' | 'rank1-noncoordinate'
       | 'rank2' | 'rank3'."""
    support = cells(matrix)
    if not support:
        return "zero"
    rank = matrix_rank(matrix)
    if rank >= 2:
        return f"rank{rank}"
    a, b = rank_one_factors(matrix)
    ca, cb = is_coordinate(a), is_coordinate(b)
    if ca and cb:
        return "basis"
    if ca or cb:
        return "rank1-one-coordinate"
    return "rank1-noncoordinate"


def block_census(source, size):
    """Counts used by the J.1d budget."""
    census = {"zero": 0, "basis": 0, "rank1-one-coordinate": 0,
              "rank1-noncoordinate": 0, "rank2": 0, "rank3": 0}
    total_cells = 0
    for u, v in combinations(range(size), 2):
        matrix = source[(u, v)]
        census[classify_block(matrix)] += 1
        total_cells += len(cells(matrix))
    census["cells"] = total_cells
    census["m"] = sum(census[k] for k in
                      ("basis", "rank1-one-coordinate", "rank1-noncoordinate",
                       "rank2", "rank3"))
    census["R"] = sum(census[k] for k in
                      ("basis", "rank1-one-coordinate", "rank1-noncoordinate"))
    census["H"] = census["rank2"] + census["rank3"]
    return census


def rank_one_degree(source, size):
    """d_R(v) for every vertex."""
    degree = [0] * size
    for u, v in combinations(range(size), 2):
        if matrix_rank(source[(u, v)]) == 1:
            degree[u] += 1
            degree[v] += 1
    return degree
