#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- independent core for the N=8, d=3 template layer.

Pinned HEAD: see PINNED_HEAD.txt.
NOTHING HERE IS A PROVED CLAIM OF THE PROJECT -- it is probe output.

Written from the mathematical definitions (notes/slice-cover.md sec.2 for (SC);
the master plan for the model).  No code is copied from W8/W11/W12; the numeric
conventions are deliberately the same so that cross-checks are meaningful.

MODEL
-----
N = 8 sites, colour alphabet {0,1,2}.  One 3x3 block A_uv per edge uv of K_8
(u < v; row = colour at u, column = colour at v).  For a word w in {0,1,2}^8

    H(A)_w = sum over the 105 perfect matchings M of K_8 of
             prod_{uv in M} A_uv[w_u][w_v].

EXACT source: H_w = 1 on the 3 constant words, 0 on the 6558 mixed words.
Diagonal gauge => "exact" is equivalent to: values nonzero on the occupied
cells, every mixed fibre sum = 0, every constant fibre sum != 0.

TEMPLATE: tuple of 28 nine-bit masks; bit 3*i+j of mask[e] = cell (i,j) of
edge e is occupied.  m = #nonzero blocks, Sigma = #cells.

ADMISSIBILITY (the space this probe exhausts)
  (SC)  every (vertex p, colour r) slot is served: some incident edge pj has
        T[pj] != 0 and every occupied cell of T[pj] carries colour r at j.
  (C)   each of the three constant words has a nonempty fibre.
  (Z)   no mixed word has fibre of size exactly 1  (O2 / singleton kill).
"""

from __future__ import annotations

from itertools import combinations, product

N = 8
Q = 3
FULL9 = 511

EDGES = tuple((u, v) for u in range(N) for v in range(u + 1, N))
NE = len(EDGES)                                   # 28
EIDX = {e: k for k, e in enumerate(EDGES)}


def _pms(vertices):
    """All perfect matchings of the complete graph on `vertices` (tuple)."""
    if not vertices:
        return [()]
    head = vertices[0]
    out = []
    for k in range(1, len(vertices)):
        rest = vertices[1:k] + vertices[k + 1:]
        for tail in _pms(rest):
            out.append(tuple(sorted(((head, vertices[k]),) + tail)))
    return out


PMS = tuple(_pms(tuple(range(N))))                # 105 matchings as edge-pairs
NM = len(PMS)
PM_EIDX = tuple(tuple(EIDX[e] for e in M) for M in PMS)

WORDS = tuple(product(range(Q), repeat=N))        # 6561
NW = len(WORDS)
WIDX = {w: k for k, w in enumerate(WORDS)}
CONST_WORDS = tuple((c,) * N for c in range(Q))
IS_MIXED = tuple(len(set(w)) > 1 for w in WORDS)

INCIDENT = tuple(tuple(EIDX[(min(p, j), max(p, j))]
                       for j in range(N) if j != p) for p in range(N))

# cell index within a block, as seen from a given endpoint
def cell_bit(i, j):
    return 1 << (3 * i + j)


def cells(mask):
    return [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]


def support(T):
    return sum(1 for mask in T if mask)


def sigma(T):
    return sum(bin(mask).count("1") for mask in T)


def occ(T, e, i, j):
    return (T[e] >> (3 * i + j)) & 1


# ------------------------------------------------------------------ (SC)

def far_colour(mask, p_is_first):
    """The unique far-end colour if the block is thin there, else None.

    p_is_first=True  : we look from endpoint u (the smaller); the far end is v
                       and the far colour is the column index j.
    p_is_first=False : we look from v; the far colour is the row index i.
    """
    if not mask:
        return None
    seen = {(j if p_is_first else i) for (i, j) in cells(mask)}
    return seen.pop() if len(seen) == 1 else None


def sc_servers(T):
    """{(p, r): [edge indices serving the slot]} for the 24 slots."""
    out = {}
    for p in range(N):
        for r in range(Q):
            srv = []
            for e in INCIDENT[p]:
                u, v = EDGES[e]
                if far_colour(T[e], p_is_first=(u == p)) == r:
                    srv.append(e)
            out[(p, r)] = srv
    return out


def sc_failures(T):
    return [k for k, v in sc_servers(T).items() if not v]


def sc_ok(T):
    for p in range(N):
        for r in range(Q):
            ok = False
            for e in INCIDENT[p]:
                u, v = EDGES[e]
                if far_colour(T[e], p_is_first=(u == p)) == r:
                    ok = True
                    break
            if not ok:
                return False
    return True


# ---------------------------------------------------------------- fibres

def fibre(T, w):
    """Indices of the perfect matchings of K_8 supporting the word w."""
    out = []
    for n, M in enumerate(PMS):
        for (u, v) in M:
            if not (T[EIDX[(u, v)]] >> (3 * w[u] + w[v])) & 1:
                break
        else:
            out.append(n)
    return out


def all_fibres(T):
    """{word: [matching indices]} over the words with a NONEMPTY fibre."""
    occtab = [[[(mask >> (3 * i + j)) & 1 for j in range(Q)] for i in range(Q)]
              for mask in T]
    out = {}
    for w in WORDS:
        got = []
        for n, M in enumerate(PMS):
            for (u, v) in M:
                if not occtab[EIDX[(u, v)]][w[u]][w[v]]:
                    break
            else:
                got.append(n)
        if got:
            out[w] = got
    return out


def constants_ok(T):
    return all(fibre(T, c) for c in CONST_WORDS)


def singleton_words(T, limit=None):
    """Mixed words whose fibre has size exactly 1."""
    occtab = [[[(mask >> (3 * i + j)) & 1 for j in range(Q)] for i in range(Q)]
              for mask in T]
    out = []
    for k, w in enumerate(WORDS):
        if not IS_MIXED[k]:
            continue
        cnt = 0
        for M in PMS:
            for (u, v) in M:
                if not occtab[EIDX[(u, v)]][w[u]][w[v]]:
                    break
            else:
                cnt += 1
                if cnt > 1:
                    break
        if cnt == 1:
            out.append(w)
            if limit is not None and len(out) >= limit:
                break
    return out


def admissible(T):
    """(SC) + three constant fibres nonempty + zero mixed singletons."""
    return (sc_ok(T) and constants_ok(T)
            and not singleton_words(T, limit=1))


def audit(T):
    fib = all_fibres(T)
    hist = {}
    for w, ms in fib.items():
        if len(set(w)) > 1:
            hist[len(ms)] = hist.get(len(ms), 0) + 1
    full = [e for e, mask in enumerate(T) if mask == FULL9]
    singles = [e for e, mask in enumerate(T) if bin(mask).count("1") == 1]
    return {
        "m": support(T),
        "sigma": sigma(T),
        "sc_ok": sc_ok(T),
        "sc_failures": [list(x) for x in sc_failures(T)],
        "constants": {c: len(fib.get(CONST_WORDS[c], [])) for c in range(Q)},
        "mixed_singletons": sum(1 for w, ms in fib.items()
                                if len(set(w)) > 1 and len(ms) == 1),
        "fibre_histogram": {int(k): int(v) for k, v in sorted(hist.items())},
        "single_cell_blocks": len(singles),
        "full_blocks": full,
        "mixed_words_live": sum(1 for w in fib if len(set(w)) > 1),
    }


# ------------------------------------------------------------- json i/o

def template_to_list(T):
    return [int(x) for x in T]


def template_from_list(x):
    return tuple(int(v) for v in x)


# --------------------------------------------------------------- groups

def apply_perm(T, pi, sigma_colour):
    """Relabel sites by pi (site p -> pi[p]) and colours by sigma_colour."""
    out = [0] * NE
    for e, (u, v) in enumerate(EDGES):
        mask = T[e]
        if not mask:
            continue
        a, b = pi[u], pi[v]
        flip = a > b
        tgt = EIDX[(min(a, b), max(a, b))]
        acc = 0
        for (i, j) in cells(mask):
            ii, jj = sigma_colour[i], sigma_colour[j]
            if flip:
                ii, jj = jj, ii
            acc |= 1 << (3 * ii + jj)
        out[tgt] = acc
    return tuple(out)
