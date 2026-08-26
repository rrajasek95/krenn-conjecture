"""A7 sub-audit: independent re-implementation of the N=8 template/fibre model.

Written from the written specification only.  Nothing here is imported from or
copied out of computations/unaudited-forcing-w19-2026-08-15/.

Exact integer arithmetic only: every quantity in a verdict path is a Python int
or a numpy integer.  No floats anywhere.
"""

import itertools

import numpy as np

N = 8
EDGES = list(itertools.combinations(range(N), 2))          # 28 pairs, lex order
NE = len(EDGES)
EIDX = {e: i for i, e in enumerate(EDGES)}
FULL = 511


def edge_index(u, v):
    return EIDX[(u, v)] if u < v else EIDX[(v, u)]


# ---------------------------------------------------------------- 3x3 blocks

def cells_of(mask):
    """{(i,j) : bit 3i+j of mask is set}."""
    return [(i, j) for i in range(3) for j in range(3) if (mask >> (3 * i + j)) & 1]


def far_thin_colour(mask, at_second):
    """Single column index (at_second=True) or single row index, else None."""
    if mask == 0:
        return None
    cs = cells_of(mask)
    S = {j for (i, j) in cs} if at_second else {i for (i, j) in cs}
    if len(S) == 1:
        return next(iter(S))
    return None


def cell_mask(i, j):
    return 1 << (3 * i + j)


def col_mask(c):
    return cell_mask(0, c) | cell_mask(1, c) | cell_mask(2, c)


def row_mask(r):
    return 7 << (3 * r)


# ---------------------------------------------------------------- (SC)

def servers_of(T):
    """dict (p, r) -> sorted list of edge indices serving that demand."""
    out = {(p, r): [] for p in range(N) for r in range(3)}
    for ei, (u, v) in enumerate(EDGES):
        cu = far_thin_colour(T[ei], True)     # p == u  =>  at_second True
        if cu is not None:
            out[(u, cu)].append(ei)
        cv = far_thin_colour(T[ei], False)    # p == v  =>  at_second False
        if cv is not None:
            out[(v, cv)].append(ei)
    return out


def sc_ok(T):
    srv = servers_of(T)
    return all(len(srv[(p, r)]) > 0 for p in range(N) for r in range(3))


def sc_ok_slow(T):
    """Literal transcription of the definition (independent of servers_of)."""
    for p in range(N):
        for r in range(3):
            hit = False
            for ei, (u, v) in enumerate(EDGES):
                if p != u and p != v:
                    continue
                if far_thin_colour(T[ei], at_second=(u == p)) == r:
                    hit = True
                    break
            if not hit:
                return False
    return True


# ---------------------------------------------------------------- graphs

def gamma_edges(T):
    return [ei for ei in range(NE) if T[ei] == FULL]


def adj_from_edgeidx(edge_idx):
    adj = [0] * N
    for ei in edge_idx:
        u, v = EDGES[ei]
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return adj


def _connected_on(adj, allowed_mask):
    """Is the induced graph on the vertex set `allowed_mask` connected?"""
    verts = [x for x in range(N) if (allowed_mask >> x) & 1]
    if not verts:
        return True
    start = verts[0]
    seen = 1 << start
    stack = [start]
    while stack:
        x = stack.pop()
        nb = adj[x] & allowed_mask & ~seen
        while nb:
            b = nb & -nb
            y = b.bit_length() - 1
            seen |= b
            stack.append(y)
            nb &= ~b
    return seen == allowed_mask


def spanning_2conn(edge_idx):
    """Spans all 8 vertices, connected, and connected after deleting any vertex."""
    adj = adj_from_edgeidx(edge_idx)
    if any(adj[x] == 0 for x in range(N)):
        return False
    allv = (1 << N) - 1
    if not _connected_on(adj, allv):
        return False
    for v in range(N):
        if not _connected_on(adj, allv & ~(1 << v)):
            return False
    return True


def degrees(edge_idx):
    d = [0] * N
    for ei in edge_idx:
        u, v = EDGES[ei]
        d[u] += 1
        d[v] += 1
    return d


# ---------------------------------------------------------------- matchings

def _all_perfect_matchings():
    res = []

    def rec(rem, acc):
        if not rem:
            res.append(tuple(sorted(acc)))
            return
        u = rem[0]
        for k in range(1, len(rem)):
            v = rem[k]
            rec(rem[1:k] + rem[k + 1:], acc + [EIDX[(u, v)]])

    rec(tuple(range(N)), [])
    return res


MATCHINGS = _all_perfect_matchings()          # 105 tuples of 4 edge indices
NM = len(MATCHINGS)
assert NM == 105
MATCH_ARR = np.array(MATCHINGS, dtype=np.int64)

# matchings-as-bitmask over edges, for F(Gamma)
MATCH_EDGEMASK = []
for M in MATCHINGS:
    m = 0
    for ei in M:
        m |= 1 << ei
    MATCH_EDGEMASK.append(m)


def F_gamma_count(gamma_edge_idx):
    gm = 0
    for ei in gamma_edge_idx:
        gm |= 1 << ei
    return sum(1 for m in MATCH_EDGEMASK if (m & ~gm) == 0)


def perfect_matchings_of(edge_idx):
    gm = 0
    for ei in edge_idx:
        gm |= 1 << ei
    return [M for M, m in zip(MATCHINGS, MATCH_EDGEMASK) if (m & ~gm) == 0]


# ---------------------------------------------------------------- words

NW = 3 ** N                                   # 6561
# word index w  <->  digits w_p with p-th digit weight 3**p
_digits = np.zeros((NW, N), dtype=np.int64)
for _p in range(N):
    _digits[:, _p] = (np.arange(NW) // (3 ** _p)) % 3

# CELLIDX[ei][w] = 3*w_u + w_v  for edge ei = (u,v)
CELLIDX = np.zeros((NE, NW), dtype=np.int64)
for _ei, (_u, _v) in enumerate(EDGES):
    CELLIDX[_ei] = 3 * _digits[:, _u] + _digits[:, _v]

CONST_WORDS = [int(sum(r * 3 ** p for p in range(N))) for r in range(3)]  # 0,3280,6560
IS_MIXED = np.ones(NW, dtype=bool)
for _c in CONST_WORDS:
    IS_MIXED[_c] = False
assert int(IS_MIXED.sum()) == 6558


def word_digits(w):
    return tuple(int(_digits[w, p]) for p in range(N))


def fibre_counts(T):
    """Exact integer array of length 6561: |fibre(w)| for every word w."""
    compat = np.empty((NE, NW), dtype=bool)
    for ei in range(NE):
        compat[ei] = ((int(T[ei]) >> CELLIDX[ei]) & 1).astype(bool)
    counts = np.zeros(NW, dtype=np.int64)
    for M in MATCHINGS:
        c = compat[M[0]] & compat[M[1]]
        c &= compat[M[2]]
        c &= compat[M[3]]
        counts += c
    return counts


def fibre_counts_slow(T):
    """Independent pure-Python reference implementation (no numpy)."""
    counts = [0] * NW
    for w in range(NW):
        d = [(w // (3 ** p)) % 3 for p in range(N)]
        tot = 0
        for M in MATCHINGS:
            ok = True
            for ei in M:
                u, v = EDGES[ei]
                if not ((T[ei] >> (3 * d[u] + d[v])) & 1):
                    ok = False
                    break
            if ok:
                tot += 1
        counts[w] = tot
    return counts


def in_R_report(T):
    """Full (R) test.  Returns a dict of exact integers / booleans."""
    T = [int(x) for x in T]
    g = gamma_edges(T)
    cnt = fibre_counts(T)
    const = [int(cnt[c]) for c in CONST_WORDS]
    mixed_min = int(cnt[IS_MIXED].min())
    sc = sc_ok(T)
    tc = spanning_2conn(g)
    rep = {
        "sc_ok": bool(sc),
        "const_fibres": const,
        "const_all_nonempty": all(x >= 1 for x in const),
        "gamma_size": len(g),
        "gamma_edges": [list(EDGES[ei]) for ei in g],
        "gamma_spanning_2conn": bool(tc),
        "F_gamma": F_gamma_count(g),
        "min_mixed_fibre": mixed_min,
        "mixed_ok": mixed_min >= 3,
        "m": sum(1 for x in T if x != 0),
        "Sigma": sum(bin(x).count("1") for x in T),
    }
    rep["in_R"] = bool(sc and rep["const_all_nonempty"] and tc and mixed_min >= 3)
    return rep


def in_R(T):
    return in_R_report(T)["in_R"]


# ---------------------------------------------------------------- group actions

def apply_site_colour_perms(T, sigmas):
    """sigmas[p] is a tuple s with s[c] = image of colour c at site p.

    New block on e=(u,v) has cell (sigmas[u][i], sigmas[v][j]) iff old had (i,j).
    """
    out = []
    for ei, (u, v) in enumerate(EDGES):
        m = 0
        for (i, j) in cells_of(T[ei]):
            m |= cell_mask(sigmas[u][i], sigmas[v][j])
        out.append(m)
    return out


def apply_vertex_perm(T, pi):
    """pi is a permutation of 0..7 (list).  New template T' with
    T'[{pi(u),pi(v)}] = block of T[{u,v}], transposed if pi flips the order."""
    out = [0] * NE
    for ei, (u, v) in enumerate(EDGES):
        a, b = pi[u], pi[v]
        m = 0
        if a < b:
            for (i, j) in cells_of(T[ei]):
                m |= cell_mask(i, j)
            out[EIDX[(a, b)]] = m
        else:
            for (i, j) in cells_of(T[ei]):
                m |= cell_mask(j, i)          # transpose
            out[EIDX[(b, a)]] = m
    return out


W8_M26 = [511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 511,
          128, 32, 64, 128, 511, 256, 511, 0, 511, 511, 0, 511]
W8_M28 = [511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 511,
          128, 32, 64, 128, 511, 256, 511, 511, 511, 511, 511, 511]
