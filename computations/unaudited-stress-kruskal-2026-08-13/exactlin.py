#!/usr/bin/env python3
"""UNAUDITED stress-test support library: exact linear algebra + fusion predicates.

Everything here is exact: Fraction arithmetic over Q, or integer arithmetic
mod a prime.  No floating point is used anywhere in this directory.

Formalization (matched to notes/simultaneous-diagonal-flattening-palette-fusion-gate.md
at sha256 473cabecb4c0d168dae4c0d0bdf172faee998c33e0d404d95924833782c53179 and its
checker verify_simultaneous_diagonal_flattening_palette_fusion_gate.py at
sha256 750ff2094c0a1c6e8b767ca7bf9323a41942f37eecf3cdc773a5295d445be1ab):

  * palette embeddings  U (m x r), V (n x r) with columns u_a, v_a.
    In the note U = D_S, V = D_T with m = r^|S|, n = r^|T| and
    u_a = e_a^{tensor S}; those are always linearly independent.
  * shore factors       A (m x r), B (n x r) with columns a_c, b_c
    (note: F_S = D_S G_S, F_T = D_T G_T).
  * Khatri-Rao product  (A o B) (mn x r), column c = vec(a_c b_c^T).
  * fusion square (9)   A o B = (U o V) C  with C in GL_r.
  * fusion defect (7)   Omega_{(a,b),c} = G_{ac} H_{bc} for a != b.

The checker's `fusion_zero(G, H)` is exactly Omega(G, H) == 0; the checker's
`monomial_permutation` is exactly `monomial_map` below specialized to square
matrices with the identity palette.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


# --------------------------------------------------------------------------
# exact rational linear algebra
# --------------------------------------------------------------------------

def zeros(rows, cols):
    return [[Fraction(0)] * cols for _ in range(rows)]


def mat(rows):
    return [[Fraction(entry) for entry in row] for row in rows]


def transpose(matrix):
    if not matrix:
        return []
    return [[matrix[i][j] for i in range(len(matrix))]
            for j in range(len(matrix[0]))]


def matmul(left, right):
    require(len(left[0]) == len(right), ("shape", len(left[0]), len(right)))
    inner = len(right)
    return [[sum(left[i][k] * right[k][j] for k in range(inner))
             for j in range(len(right[0]))]
            for i in range(len(left))]


def rref(matrix):
    """Exact reduced row echelon form.  Returns (R, pivot_columns)."""
    work = [list(row) for row in matrix]
    if not work:
        return work, []
    rows, cols = len(work), len(work[0])
    pivots = []
    row = 0
    for col in range(cols):
        sel = next((r for r in range(row, rows) if work[r][col] != 0), None)
        if sel is None:
            continue
        work[row], work[sel] = work[sel], work[row]
        scale = work[row][col]
        work[row] = [entry / scale for entry in work[row]]
        for other in range(rows):
            if other == row or work[other][col] == 0:
                continue
            factor = work[other][col]
            work[other] = [e - factor * p for e, p in zip(work[other], work[row])]
        pivots.append(col)
        row += 1
        if row == rows:
            break
    return work, pivots


def rank(matrix):
    if not matrix or not matrix[0]:
        return 0
    return len(rref(matrix)[1])


def column_rank(matrix):
    return rank(matrix)


def solve(matrix, rhs):
    """One exact solution x of matrix @ x = rhs, or None if inconsistent."""
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    augmented = [list(matrix[i]) + [rhs[i]] for i in range(rows)]
    reduced, pivots = rref(augmented)
    if cols in pivots:
        return None
    solution = [Fraction(0)] * cols
    for index, col in enumerate(pivots):
        solution[col] = reduced[index][cols]
    return solution


def nullspace(matrix):
    """Exact basis of the right kernel."""
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    reduced, pivots = rref(matrix)
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for f in free:
        vector = [Fraction(0)] * cols
        vector[f] = Fraction(1)
        for index, col in enumerate(pivots):
            vector[col] = -reduced[index][f]
        basis.append(vector)
    return basis


def det(matrix):
    size = len(matrix)
    work = [list(row) for row in matrix]
    result = Fraction(1)
    for col in range(size):
        sel = next((r for r in range(col, size) if work[r][col] != 0), None)
        if sel is None:
            return Fraction(0)
        if sel != col:
            work[col], work[sel] = work[sel], work[col]
            result = -result
        result *= work[col][col]
        inv = work[col][col]
        work[col] = [e / inv for e in work[col]]
        for other in range(col + 1, size):
            if work[other][col] == 0:
                continue
            factor = work[other][col]
            work[other] = [e - factor * p for e, p in zip(work[other], work[col])]
    return result


# --------------------------------------------------------------------------
# k-rank
# --------------------------------------------------------------------------

def krank(matrix, rank_fn=rank):
    """Kruskal rank: largest k such that EVERY k columns are independent.

    Returns 0 if some column is zero.
    """
    cols = len(matrix[0]) if matrix else 0
    best = 0
    for size in range(1, cols + 1):
        ok = True
        for chosen in combinations(range(cols), size):
            sub = [[row[c] for c in chosen] for row in matrix]
            if rank_fn(sub) < size:
                ok = False
                break
        if not ok:
            break
        best = size
    return best


# --------------------------------------------------------------------------
# palettes and Khatri-Rao
# --------------------------------------------------------------------------

def diagonal_embedding(shore_size, palette=3):
    """D_S: columns e_a^{tensor S}, rows indexed by palette words.  (r^|S| x r)"""
    words = list(product(range(palette), repeat=shore_size))
    return [[Fraction(int(word == (colour,) * shore_size))
             for colour in range(palette)] for word in words]


def khatri_rao(left, right):
    """Columnwise Kronecker product.  Row (i, j) -> i * n + j."""
    rows_l, rows_r = len(left), len(right)
    cols = len(left[0])
    require(len(right[0]) == cols, ("khatri-rao column mismatch",))
    return [[left[i][c] * right[j][c] for c in range(cols)]
            for i in range(rows_l) for j in range(rows_r)]


def outer(vec_a, vec_b):
    return [[x * y for y in vec_b] for x in vec_a]


# --------------------------------------------------------------------------
# fusion-square predicates
# --------------------------------------------------------------------------

def factors_through(A, B, U, V):
    """Return C with A o B = (U o V) C, or None.  (The square (9) of the note.)"""
    left = khatri_rao(A, B)
    palette = khatri_rao(U, V)
    columns = []
    for c in range(len(left[0])):
        rhs = [row[c] for row in left]
        sol = solve(palette, rhs)
        if sol is None:
            return None
        # verify (solve returns a particular solution of a consistent system)
        check = matmul(palette, [[x] for x in sol])
        if any(check[i][0] != rhs[i] for i in range(len(rhs))):
            return None
        columns.append(sol)
    return transpose(columns)


def parallel(vec_x, vec_y):
    """True iff the 2 x len matrix [x y] has rank <= 1 (both may be nonzero)."""
    nz_x = [i for i, v in enumerate(vec_x) if v != 0]
    nz_y = [i for i, v in enumerate(vec_y) if v != 0]
    if not nz_x or not nz_y:
        return True
    if nz_x != nz_y:
        return False
    ratio = vec_x[nz_x[0]] / vec_y[nz_x[0]]
    return all(vec_x[i] == ratio * vec_y[i] for i in nz_x)


def monomial_map(A, U):
    """If every column of A is a nonzero multiple of some column of U, return
    the map pi (as a tuple) with a_c ~ u_{pi(c)}; else None."""
    cols = len(A[0])
    pal = len(U[0])
    pi = []
    for c in range(cols):
        a_c = [row[c] for row in A]
        if all(v == 0 for v in a_c):
            return None
        hits = [p for p in range(pal)
                if parallel(a_c, [row[p] for row in U])
                and any(row[p] != 0 for row in U)]
        if len(hits) != 1:
            return None
        pi.append(hits[0])
    return tuple(pi)


def aligned_monomial(A, B, U, V):
    """The note's conclusion (10): a common permutation pi with
    a_c = lambda_c u_{pi(c)} and b_c = mu_c v_{pi(c)}."""
    pi_a = monomial_map(A, U)
    pi_b = monomial_map(B, V)
    if pi_a is None or pi_b is None:
        return None
    if pi_a != pi_b:
        return None
    if len(set(pi_a)) != len(pi_a):
        return None
    return pi_a


def omega_defect(G, H):
    """The note's Omega (7): rows (a,b) with a != b, entries G_ac H_bc."""
    size = len(G)
    return [[G[a][c] * H[b][c] for c in range(size)]
            for a in range(size) for b in range(size) if a != b]


# --------------------------------------------------------------------------
# prime-field arithmetic (for exhaustive searches)
# --------------------------------------------------------------------------

def to_int(entry):
    """Exact coercion of an integral Fraction/int to int (no rounding)."""
    if isinstance(entry, Fraction):
        require(entry.denominator == 1, ("non-integral entry mod p", entry))
        return int(entry.numerator)
    return int(entry)


def rank_mod(matrix, prime):
    work = [[to_int(e) % prime for e in row] for row in matrix]
    if not work or not work[0]:
        return 0
    rows, cols = len(work), len(work[0])
    row = 0
    for col in range(cols):
        sel = next((r for r in range(row, rows) if work[r][col] % prime), None)
        if sel is None:
            continue
        work[row], work[sel] = work[sel], work[row]
        inv = pow(work[row][col], -1, prime)
        work[row] = [e * inv % prime for e in work[row]]
        for other in range(rows):
            if other == row or work[other][col] % prime == 0:
                continue
            factor = work[other][col]
            work[other] = [(e - factor * p) % prime
                           for e, p in zip(work[other], work[row])]
        row += 1
        if row == rows:
            break
    return row


def krank_mod(matrix, prime):
    return krank(matrix, rank_fn=lambda m: rank_mod(m, prime))


def in_span_mod(vectors, target, prime):
    """Is target in the span of the given vectors (rows)?  Exact mod p."""
    base = [list(v) for v in vectors]
    return rank_mod(base, prime) == rank_mod(base + [list(target)], prime)


def parallel_mod(vec_x, vec_y, prime):
    return rank_mod([list(vec_x), list(vec_y)], prime) <= 1


def monomial_map_mod(A, U, prime):
    cols = len(A[0])
    pal = len(U[0])
    pi = []
    for c in range(cols):
        a_c = [row[c] % prime for row in A]
        if all(v == 0 for v in a_c):
            return None
        hits = [p for p in range(pal)
                if parallel_mod(a_c, [row[p] for row in U], prime)]
        if len(hits) != 1:
            return None
        pi.append(hits[0])
    return tuple(pi)
