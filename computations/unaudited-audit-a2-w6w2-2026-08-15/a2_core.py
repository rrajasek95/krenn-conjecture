#!/usr/bin/env python3
"""AUDIT A2 -- independent core.  Pinned HEAD 81beedf.

Nothing is imported from W6 or W2.  The fibre counter is re-derived from the
definition and implemented by a DIFFERENT algorithm than either probe:

    A template T assigns to every edge e = {u,v} of K_N (u < v) a set
    S_e subset {0,1,2}^2 of occupied cells (row index = colour at u).
    The support is {e : S_e nonempty}; m = |support|; Sigma = sum |S_e|.

    For a word (colouring) c : [N] -> {0,1,2} and a perfect matching M of
    [N], the monomial prod_{uv in M} A_uv[c_u][c_v] is nonzero in the
    template iff (c_u, c_v) in S_uv for every uv in M.  Hence

        fibre_T(c) = # { M perfect matching of K_N : M subset support and
                         (c_u,c_v) in S_uv for all uv in M }
                   = haf( W_c ),  W_c[u][v] = [ (c_u,c_v) in S_uv ].

W6 computes this by enumerating the 105 matchings and AND-ing boolean masks.
Here it is computed as a HAFNIAN BY SUBSET DYNAMIC PROGRAMMING over the 2^N
vertex subsets (dp[S] = # perfect matchings of the induced allowed graph on
S), which never enumerates matchings at all.  Two variants:

    fibre_counts_dp_python : pure python integers, one word at a time
                             (used for every CERTIFICATE verdict);
    fibre_counts_dp_numpy  : same recursion vectorised over all 3^N words
                             (used for searches only).

A brute-force matching enumerator is included ONLY as an internal
cross-check of the DP (never as the verdict path).
"""

from __future__ import annotations

from itertools import combinations, product

import numpy as np

COLORS = (0, 1, 2)


class Geom:
    """Edge indexing convention: sorted(combinations(range(N), 2))."""

    def __init__(self, n: int):
        self.n = n
        self.edges = tuple(combinations(range(n), 2))
        self.eidx = {e: i for i, e in enumerate(self.edges)}
        self.words = tuple(product(COLORS, repeat=n))
        self.widx = {w: i for i, w in enumerate(self.words)}
        # numpy word table
        self.W = np.array(self.words, dtype=np.int8)
        self.mixed = np.array([len(set(w)) > 1 for w in self.words])
        self.const_rows = [self.widx[tuple([r] * n)] for r in COLORS]
        # even subsets of [n], ordered by popcount
        self.subsets = sorted((s for s in range(1 << n) if bin(s).count("1") % 2 == 0),
                              key=lambda s: bin(s).count("1"))


_GEOM: dict[int, Geom] = {}


def geom(n: int) -> Geom:
    if n not in _GEOM:
        _GEOM[n] = Geom(n)
    return _GEOM[n]


def normalise_template(g: Geom, template) -> tuple:
    """Accept list-of-iterables of cells (per edge, in g.edges order)."""
    out = []
    for s in template:
        cells = frozenset((int(a), int(b)) for a, b in (s or ()))
        for a, b in cells:
            assert a in COLORS and b in COLORS, "cell out of range"
        out.append(cells)
    assert len(out) == len(g.edges), "template length != #edges"
    return tuple(out)


# --------------------------------------------------------------- verdict path


def fibre_one_word_dp(g: Geom, template, word) -> int:
    """haf of the allowed 0/1 adjacency for a single word, by subset DP."""
    n = g.n
    allowed = [[False] * n for _ in range(n)]
    for idx, (u, v) in enumerate(g.edges):
        if (word[u], word[v]) in template[idx]:
            allowed[u][v] = allowed[v][u] = True
    dp = [0] * (1 << n)
    dp[0] = 1
    for s in g.subsets:
        if s == 0:
            continue
        u = (s & -s).bit_length() - 1
        rest = s & ~(1 << u)
        total = 0
        r = rest
        while r:
            vb = r & -r
            v = vb.bit_length() - 1
            r ^= vb
            if allowed[u][v]:
                total += dp[rest & ~vb]
        dp[s] = total
    return dp[(1 << n) - 1]


def fibre_counts_dp_python(g: Geom, template) -> list:
    """Exact integer fibre count for every word.  Slow, authoritative."""
    return [fibre_one_word_dp(g, template, w) for w in g.words]


def fibre_counts_bruteforce(g: Geom, template) -> list:
    """Independent cross-check only: enumerate matchings per word."""
    def pms(vs):
        if not vs:
            return [()]
        first, out = vs[0], []
        for i in range(1, len(vs)):
            rest = vs[1:i] + vs[i + 1:]
            for tail in pms(rest):
                out.append(((first, vs[i]),) + tail)
        return out
    matchings = pms(tuple(range(g.n)))
    counts = []
    for w in g.words:
        total = 0
        for M in matchings:
            if all((w[u], w[v]) in template[g.eidx[(u, v)]] for u, v in M):
                total += 1
        counts.append(total)
    return counts


# ------------------------------------------------------------- search path


def allowed_masks(g: Geom, template):
    """boolean array per edge over all words (vectorised)."""
    out = []
    for idx, (u, v) in enumerate(g.edges):
        tbl = np.zeros((3, 3), dtype=bool)
        for a, b in template[idx]:
            tbl[a, b] = True
        out.append(tbl[g.W[:, u], g.W[:, v]])
    return out


def _dp_plan(g: Geom):
    """Precompute the subset-DP recursion once per N (pure bookkeeping)."""
    if getattr(g, "_plan", None) is not None:
        return g._plan
    rank = {s: i for i, s in enumerate(g.subsets)}
    steps = []                       # (target rank, [(edge index, source rank)])
    for s in g.subsets:
        if s == 0:
            continue
        u = (s & -s).bit_length() - 1
        rest = s & ~(1 << u)
        terms = []
        r = rest
        while r:
            vb = r & -r
            v = vb.bit_length() - 1
            r ^= vb
            key = (u, v) if u < v else (v, u)
            terms.append((g.eidx[key], rank[rest & ~vb]))
        steps.append((rank[s], terms))
    g._plan = (rank, steps)
    return g._plan


def fibre_counts_dp_numpy(g: Geom, template) -> np.ndarray:
    """Same subset DP, vectorised over all 3^N words.

    The masked accumulation uses a bitwise AND with the 0/-1 form of the
    allowed mask; identical arithmetic to np.add(..., where=mask), just
    faster.  Cross-checked against fibre_counts_dp_python in a2_selftest.
    """
    rank, steps = _dp_plan(g)
    masks = [-(mask.astype(np.int32)) for mask in allowed_masks(g, template)]
    buf = getattr(g, "_buf", None)
    if buf is None:
        buf = g._buf = np.zeros((len(g.subsets), len(g.words)), dtype=np.int32)
    buf[:] = 0
    buf[0] = 1
    for target, terms in steps:
        acc = buf[target]
        for eidx, src in terms:
            acc += buf[src] & masks[eidx]
    return buf[rank[(1 << g.n) - 1]].copy()


# ------------------------------------------------------------ template audit


def audit_template(g: Geom, template, exact=True) -> dict:
    """Full independent verdict for one template."""
    t = normalise_template(g, template)
    support = [i for i, s in enumerate(t) if s]
    m = len(support)
    sigma = sum(len(s) for s in t)
    beta = sum(1 for s in t if len(s) == 1)
    deg = [0] * g.n
    slots = set()
    for i in support:
        u, v = g.edges[i]
        deg[u] += 1
        deg[v] += 1
        for a, b in t[i]:
            slots.add((u, a))
            slots.add((v, b))
    counts = (fibre_counts_dp_python(g, t) if exact
              else list(map(int, fibre_counts_dp_numpy(g, t))))
    const = [counts[r] for r in g.const_rows]
    singles = [g.words[i] for i in range(len(counts))
               if counts[i] == 1 and g.mixed[i]]
    hist = {}
    for i, c in enumerate(counts):
        if g.mixed[i] and c:
            hist[c] = hist.get(c, 0) + 1
    return {"m": m, "sigma": sigma, "beta": beta, "min_degree": min(deg),
            "slots": len(slots), "const_fibres": const,
            "constants_all_nonempty": all(c > 0 for c in const),
            "mixed_singletons": len(singles),
            "singleton_words": ["".join(map(str, w)) for w in singles[:6]],
            "mixed_fibre_histogram": dict(sorted(hist.items())),
            "support_edges": [list(g.edges[i]) for i in support]}


def diagonal_template(g: Geom, palettes):
    """palettes: per-edge iterable of colours c -> cells {(c,c)}."""
    return [frozenset((c, c) for c in (p or ())) for p in palettes]
