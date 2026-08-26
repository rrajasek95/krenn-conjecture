#!/usr/bin/env python3
"""UNAUDITED PROBE W23 (pure-equation witness core) -- core module.

Pinned HEAD: see PINNED_HEAD.txt.

INDEPENDENT re-implementation of the matching tensor and of the pure-equation
laws.  Nothing here imports W22/W17/W5; those are used only as CROSS-CHECKS in
the runners (inter-probe controls).

SETTING.  B a set of N sites (N even), blocks A_uv in V_u (x) V_v, V = C^3,
oriented so that A_uv[i][j] = coefficient of colour i at u and colour j at v.

    H_B(A)_w = sum_{M in PM(B)} prod_{(u,v) in M} A_uv[w_u][w_v].

EXACT source:  H_B(A)_w = 1 if w is constant, 0 otherwise.

SCALAR COLOUR SLICE  w_c(u,v) := A_uv[c][c];  its hafnian cofactors

    C^(c)_S := haf( w_c | B \\ S )          (S a set of sites),
    C^(c)_ab := C^(c)_{a,b},   C^(c)_ab;uv := C^(c)_{a,b,u,v}.

STAR (co-star) VECTORS  sigma^(c)_au := A_au(., c) in V_a,
    sigma^(c)_au[d] = A_au[d][c].

LAW L1 (W22-S, re-derived here):  for every site a and colour c,

    sum_{y != a} C^(c)_ay sigma^(c)_ay = e_c      in V_a.               (L1)

LAW L2 (THE OBJECT OF THIS PROBE): for every pair a != b and colour c,

    C^(c)_ab A_ab + Phi^(c)_ab = e_c (x) e_c      in V_a (x) V_b,       (L2)
    Phi^(c)_ab := sum_{u != v in B\\{a,b}} C^(c)_ab;uv sigma^(c)_au (x) sigma^(c)_bv.

All arithmetic exact (int / Fraction).  No floats anywhere in this file.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations, product
import os
import subprocess
import tempfile

COLORS3 = (0, 1, 2)


def require(cond, detail):
    if not cond:
        raise AssertionError(detail)


def ekey(a, b):
    return (a, b) if a < b else (b, a)


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple) -> tuple:
    """All perfect matchings of a tuple of sites (independent recursion)."""
    if len(vertices) == 0:
        return ((),)
    if len(vertices) % 2:
        return ()
    head = vertices[0]
    out = []
    for k in range(1, len(vertices)):
        mate = vertices[k]
        rest = vertices[1:k] + vertices[k + 1:]
        for tail in perfect_matchings(rest):
            out.append(((head, mate),) + tail)
    return tuple(out)


# --------------------------------------------------------------- source utils

def oriented(src, u, v, ncol=3):
    """A_uv with row = colour at u, column = colour at v."""
    if u < v:
        return src[(u, v)]
    m = src[(v, u)]
    return [[m[j][i] for j in range(ncol)] for i in range(ncol)]


def zero_source(n, ncol=3):
    return {(a, b): [[0] * ncol for _ in range(ncol)]
            for a, b in combinations(range(n), 2)}


def haf_word(src, word, sites, ncol=3):
    """Haf_{sites}(A) at the given word (word is a dict site -> colour)."""
    total = 0
    for M in perfect_matchings(tuple(sites)):
        term = 1
        for a, b in M:
            term *= oriented(src, a, b, ncol)[word[a]][word[b]]
            if term == 0:
                break
        total += term
    return total


def H(src, word, n, ncol=3):
    """H_B(A)_w for a word given as a tuple over range(n)."""
    return haf_word(src, {i: word[i] for i in range(n)}, tuple(range(n)), ncol)


def exact_defects(src, n, ncol=3):
    bad = []
    for word in product(range(ncol), repeat=n):
        tgt = 1 if len(set(word)) == 1 else 0
        if H(src, word, n, ncol) != tgt:
            bad.append(word)
    return bad


def mixed_defects(src, n, ncol=3):
    bad = []
    for word in product(range(ncol), repeat=n):
        if len(set(word)) == 1:
            continue
        if H(src, word, n, ncol) != 0:
            bad.append(word)
    return bad


def pures(src, n, ncol=3):
    return {c: H(src, (c,) * n, n, ncol) for c in range(ncol)}


# ------------------------------------------------------- scalar colour slices

def colour_slice(src, c, n, ncol=3):
    """w_c(u,v) = A_uv[c][c] as a dict on unordered pairs."""
    return {ekey(a, b): oriented(src, a, b, ncol)[c][c]
            for a, b in combinations(range(n), 2)}


def haf_scalar(w, sites):
    """haf of the symmetric weight w restricted to `sites` (odd -> 0)."""
    sites = tuple(sites)
    if len(sites) % 2:
        return 0
    total = 0
    for M in perfect_matchings(sites):
        term = 1
        for a, b in M:
            term *= w[ekey(a, b)]
            if term == 0:
                break
        total += term
    return total


def cofactor(w, n, drop):
    """C^(c)_drop = haf(w | B \\ drop)."""
    rest = tuple(x for x in range(n) if x not in drop)
    return haf_scalar(w, rest)


def star_vec(src, a, u, c, ncol=3):
    """sigma^(c)_au in V_a:  d -> A_au[d][c]."""
    m = oriented(src, a, u, ncol)
    return [m[d][c] for d in range(ncol)]


# ------------------------------------------------------------------- LAW  L1

def l1_lhs(src, a, c, n, ncol=3):
    """sum_{y != a} C^(c)_ay sigma^(c)_ay  in V_a."""
    w = colour_slice(src, c, n, ncol)
    vec = [0] * ncol
    for y in range(n):
        if y == a:
            continue
        cof = cofactor(w, n, (a, y))
        if cof == 0:
            continue
        sv = star_vec(src, a, y, c, ncol)
        for d in range(ncol):
            vec[d] += cof * sv[d]
    return vec


def l1_residual(src, a, c, n, ncol=3):
    v = l1_lhs(src, a, c, n, ncol)
    return [v[d] - (1 if d == c else 0) for d in range(ncol)]


def l1_words(src, a, c, n, ncol=3):
    """The H-values the L1 identity reproduces: word = c everywhere, d at a."""
    out = []
    for d in range(ncol):
        word = [c] * n
        word[a] = d
        out.append(H(src, tuple(word), n, ncol))
    return out


# ------------------------------------------------------------------- LAW  L2

def l2_Phi(src, a, b, c, n, ncol=3):
    """Phi^(c)_ab = sum_{u != v in B\\{a,b}} C^(c)_ab;uv sigma^(c)_au (x) sigma^(c)_bv."""
    w = colour_slice(src, c, n, ncol)
    rest = [x for x in range(n) if x not in (a, b)]
    out = [[0] * ncol for _ in range(ncol)]
    for u, v in permutations(rest, 2):
        cof = cofactor(w, n, (a, b, u, v))
        if cof == 0:
            continue
        sa = star_vec(src, a, u, c, ncol)
        sb = star_vec(src, b, v, c, ncol)
        for d in range(ncol):
            if sa[d] == 0:
                continue
            for e in range(ncol):
                if sb[e] == 0:
                    continue
                out[d][e] += cof * sa[d] * sb[e]
    return out


def l2_lhs(src, a, b, c, n, ncol=3):
    """C^(c)_ab A_ab + Phi^(c)_ab  in V_a (x) V_b (a 3x3 matrix)."""
    w = colour_slice(src, c, n, ncol)
    cof = cofactor(w, n, (a, b))
    blk = oriented(src, a, b, ncol)
    phi = l2_Phi(src, a, b, c, n, ncol)
    return [[cof * blk[d][e] + phi[d][e] for e in range(ncol)]
            for d in range(ncol)]


def l2_residual(src, a, b, c, n, ncol=3):
    """LHS - e_c (x) e_c."""
    lhs = l2_lhs(src, a, b, c, n, ncol)
    return [[lhs[d][e] - (1 if (d == c and e == c) else 0)
             for e in range(ncol)] for d in range(ncol)]


def l2_words(src, a, b, c, n, ncol=3):
    """The matrix of H-values [ H_B(A)_{w(d,e)} ], w = c everywhere, d at a,
    e at b.  (The independent evaluator of the ALGEBRAIC form of L2.)"""
    out = [[0] * ncol for _ in range(ncol)]
    for d in range(ncol):
        for e in range(ncol):
            word = [c] * n
            word[a] = d
            word[b] = e
            out[d][e] = H(src, tuple(word), n, ncol)
    return out


# ---------------------------------------------- L2 corollaries (see REPORT.md)

def l2_offcolour(mat, c, ncol=3):
    """The (ncol-1)x(ncol-1) off-colour corner: rows/cols != c."""
    idx = [d for d in range(ncol) if d != c]
    return [[mat[d][e] for e in idx] for d in idx]


def l2_consistency_residuals(src, a, b, n, ncol=3):
    """For each colour d, the two colours c != d give two expressions for
    A_ab[d][d].  Cross-multiplied residual:

        C^(c2)_ab * Phi^(c1)_ab[d][d] - C^(c1)_ab * Phi^(c2)_ab[d][d] = 0.

    Returns a dict d -> residual (must vanish on an exact source)."""
    w = {c: colour_slice(src, c, n, ncol) for c in range(ncol)}
    cof = {c: cofactor(w[c], n, (a, b)) for c in range(ncol)}
    phi = {c: l2_Phi(src, a, b, c, n, ncol) for c in range(ncol)}
    out = {}
    for d in range(ncol):
        others = [c for c in range(ncol) if c != d]
        require(len(others) == 2, "consistency relation is a ternary statement")
        c1, c2 = others
        out[d] = cof[c2] * phi[c1][d][d] - cof[c1] * phi[c2][d][d]
    return out


# ------------------------------------------------------ star family / L1 matrix

def star_family(src, p, n, ncol=3):
    """{A_py}_{y != p} as a dict y -> 3x3 (row = colour at p)."""
    return {y: oriented(src, p, y, ncol) for y in range(n) if y != p}


def cofactor_diagonals(src, p, n, ncol=3):
    """D_y = diag(C^(0)_py, ..., C^(ncol-1)_py) as a list per y."""
    out = {}
    for y in range(n):
        if y == p:
            continue
        out[y] = [cofactor(colour_slice(src, c, n, ncol), n, (p, y))
                  for c in range(ncol)]
    return out


def l1_matrix_residual(src, p, n, ncol=3):
    """sum_y A_py D_y - I  (the matrix form of L1)."""
    A = star_family(src, p, n, ncol)
    D = cofactor_diagonals(src, p, n, ncol)
    out = [[0] * ncol for _ in range(ncol)]
    for y, blk in A.items():
        for d in range(ncol):
            for c in range(ncol):
                out[d][c] += blk[d][c] * D[y][c]
    for c in range(ncol):
        out[c][c] -= 1
    return out


# ----------------------------------------------------------------- lin algebra

def matrix_rank(rows):
    m = [[Fraction(x) for x in r] for r in rows]
    if not m:
        return 0
    ncols = len(m[0])
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(m)):
            if m[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        head = m[r]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c] / head[c]
                m[i] = [x - f * y for x, y in zip(m[i], head)]
        r += 1
    return r


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def minor_cc(m, c):
    """The principal 2x2 minor of m obtained by deleting row c and column c."""
    idx = [i for i in range(3) if i != c]
    (i, j) = idx
    return m[i][i] * m[j][j] - m[i][j] * m[j][i]


def nullspace(rows, ncols):
    """Exact basis of the right null space of the given rows."""
    m = [[Fraction(x) for x in r] for r in rows]
    piv = []
    r = 0
    for c in range(ncols):
        p = None
        for i in range(r, len(m)):
            if m[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        inv = Fraction(1) / m[r][c]
        m[r] = [x * inv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[r])]
        piv.append(c)
        r += 1
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for f in free:
        v = [Fraction(0)] * ncols
        v[f] = Fraction(1)
        for i, c in enumerate(piv):
            v[c] = -m[i][f]
        basis.append(v)
    return basis


# -------------------------------------------------- blocking / witness layer

def left_kernel(blk, ncol=3):
    """Basis of {u : A^T u = 0} = the left kernel of blk."""
    rows = [[blk[i][c] for i in range(ncol)] for c in range(ncol)]  # columns of blk
    return nullspace(rows, ncol)


def alpha_of(src, p, u, n, ncol=3):
    """alpha_y = A_py^T u  in V_y, for every y != p."""
    out = {}
    for y in range(n):
        if y == p:
            continue
        blk = oriented(src, p, y, ncol)
        out[y] = [sum(u[i] * blk[i][c] for i in range(ncol)) for c in range(ncol)]
    return out


def W_set(src, p, u, n, ncol=3):
    """W(u) = {y != p : A_py^T u != 0}."""
    al = alpha_of(src, p, u, n, ncol)
    return set(y for y, v in al.items() if any(x != 0 for x in v))


def cap_R(src, p, q, K, sites, ncol=3):
    R = {}
    for a, b in combinations(sorted(sites), 2):
        apa, aqa = oriented(src, p, a, ncol), oriented(src, q, a, ncol)
        apb, aqb = oriented(src, p, b, ncol), oriented(src, q, b, ncol)
        mat = [[0] * ncol for _ in range(ncol)]
        for ca in range(ncol):
            for cb in range(ncol):
                tot = 0
                for i in range(ncol):
                    for j in range(ncol):
                        k = K[i][j]
                        if k == 0:
                            continue
                        tot += k * (apa[i][ca] * aqb[j][cb]
                                    + aqa[j][ca] * apb[i][cb])
                mat[ca][cb] = tot
        R[(a, b)] = mat
    return R


def cap_s(src, p, q, K, ncol=3):
    m = oriented(src, p, q, ncol)
    return sum(K[i][j] * m[i][j] for i in range(ncol) for j in range(ncol))


def _entry(tab, a, b, ca, cb):
    return tab[(a, b)][ca][cb] if a < b else tab[(b, a)][cb][ca]


def cap_error(src, p, q, K, sites, ncol=3):
    """E_pq(K) = sum_M sum_{J subset M, |J|>=2} s^{h-|J|} prod_J R prod_{M\\J} A."""
    sites = tuple(sorted(sites))
    h = len(sites) // 2
    s = cap_s(src, p, q, K, ncol)
    R = cap_R(src, p, q, K, sites, ncol)
    A = {(a, b): oriented(src, a, b, ncol) for a, b in combinations(sites, 2)}
    slot = {a: i for i, a in enumerate(sites)}
    out = {}
    for word in product(range(ncol), repeat=len(sites)):
        tot = 0
        for M in perfect_matchings(sites):
            for size in range(2, h + 1):
                pref = s ** (h - size)
                if pref == 0:
                    continue
                for J in combinations(range(h), size):
                    Js = set(J)
                    term = pref
                    for i, (a, b) in enumerate(M):
                        ca, cb = word[slot[a]], word[slot[b]]
                        term *= _entry(R if i in Js else A, a, b, ca, cb)
                        if term == 0:
                            break
                    tot += term
        if tot != 0:
            out[word] = tot
    return out


def is_admissible(src, p, q, K, ncol=3):
    return cap_s(src, p, q, K, ncol) != 0 and all(K[c][c] != 0 for c in range(ncol))


# -------------------------------------------------------------------- Singular

def run_singular(script: str, timeout: int = 1800):
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script + "\nquit;\n")
        path = fh.name
    try:
        proc = subprocess.run(["Singular", "-q", "--no-warn", path],
                              capture_output=True, text=True, timeout=timeout)
    finally:
        os.unlink(path)
    out = proc.stdout
    bad = [ln for ln in out.splitlines() if ln.strip().startswith("?")]
    if proc.returncode != 0 or bad:
        raise RuntimeError(f"Singular failed rc={proc.returncode}: {bad[:5]} "
                           f"{proc.stderr[:1500]}")
    return out


def no_shadow_guard(script: str, ringvars):
    """Ledger item 13: never name a generator after a ring variable."""
    for ln in script.splitlines():
        t = ln.strip()
        for kw in ("poly ", "ideal ", "int ", "number ", "matrix ", "list ",
                   "vector ", "map "):
            if t.startswith(kw):
                name = t[len(kw):].split("=")[0].split("(")[0].strip()
                if name in ringvars:
                    raise AssertionError(f"shadowing hazard: {ln}")
    return True


# ------------------------------------------------------------ standard sources

def delta43():
    """Delta_{4,3}: the K_4 ternary exception (EXACT at N=4, 3 colours)."""
    src = zero_source(4)
    for c, M in enumerate([((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]):
        for e in M:
            src[e][c][c] = 1
    return src


def delta_n2(n, ncol=2, cycle=None):
    """Delta_{N,2} on the alternating Hamiltonian cycle.  ncol=2 gives the
    GENUINELY EXACT two-colour source; ncol=3 gives the padded source (which
    fails only the colour-2 pure equation)."""
    if cycle is None:
        cycle = list(range(n))
    edges = [(cycle[i], cycle[(i + 1) % n]) for i in range(n)]
    src = zero_source(n, ncol)
    for i in range(0, n, 2):
        src[ekey(*edges[i])][0][0] = 1
    for i in range(1, n, 2):
        src[ekey(*edges[i])][1][1] = 1
    return src


def near_exact_six_site():
    """The committed near-exact six-site source (W17 t2e certificate)."""
    import json
    path = ("/Users/rishi/workplace/krenn-conjecture/computations/"
            "unaudited-scalar-slice-w17-2026-08-15/"
            "results_t2e_nearexact_certificate.json")
    with open(path) as fh:
        C = json.load(fh)
    src = {}
    for k, m in C["blocks"].items():
        a, b = (int(x) for x in k.replace("(", "").replace(")", "").split(","))
        src[(a, b)] = [[Fraction(str(x)) for x in row] for row in m]
    return src


def random_source(rng, n, lo=-3, hi=3, ncol=3):
    return {e: [[rng.randint(lo, hi) for _ in range(ncol)] for _ in range(ncol)]
            for e in combinations(range(n), 2)}
