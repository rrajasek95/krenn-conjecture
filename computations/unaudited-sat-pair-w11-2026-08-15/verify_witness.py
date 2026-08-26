"""UNAUDITED (W11).  THIRD, deliberately different verifier for a witness.

Nothing here is shared with krenn_core / per_graph beyond reading the template:

* perfect matchings are re-derived by brute force over all 8! vertex orders
  (pair up positions 0-1, 2-3, 4-5, 6-7) and deduplicated -- not by the
  recursive routine in krenn_core;
* fibre sizes are computed by a bitmask DP over vertex subsets that counts
  perfect matchings of the word's live graph, never enumerating matchings;
* (SC) is checked by materialising the 3x3 matrix A_{p->j} for each ORDERED
  pair (with the transpose applied when reading from the far side) and asking
  whether it is nonzero with support inside a single column.

Every count is an exact Python integer.
"""

import json
import sys
from itertools import permutations, product

N = 8
D = 3
EDGES = [(u, v) for u in range(N) for v in range(u + 1, N)]
EIDX = {e: k for k, e in enumerate(EDGES)}


def matchings_bruteforce():
    """All perfect matchings of K_8 as frozensets of vertex pairs."""
    out = set()
    for perm in permutations(range(N)):
        M = frozenset(frozenset((perm[2 * i], perm[2 * i + 1]))
                      for i in range(N // 2))
        out.add(M)
    return sorted(sorted(tuple(sorted(p)) for p in M) for M in out)


def load(path):
    obj = json.load(open(path))
    assert [tuple(e) for e in obj["edges"]] == EDGES, "edge order mismatch"
    return {EDGES[k]: set(map(tuple, blk))
            for k, blk in enumerate(obj["blocks"])}


def matrix(T, p, j):
    """A_{p->j}: 3x3 with rows = colour at p, cols = colour at j."""
    if p < j:
        S = T[(p, j)]
        return [[1 if (a, b) in S else 0 for b in range(D)] for a in range(D)]
    S = T[(j, p)]
    return [[1 if (b, a) in S else 0 for b in range(D)] for a in range(D)]


def sc_ok(T):
    """(SC): for every (p, r) some incident edge pj has A_{p->j} nonzero with
    all its support in column r."""
    fails = []
    for p in range(N):
        for r in range(D):
            served = False
            for j in range(N):
                if j == p:
                    continue
                A = matrix(T, p, j)
                if all(A[a][b] == 0 for a in range(D) for b in range(D)):
                    continue
                if any(A[a][b] for a in range(D) for b in range(D) if b != r):
                    continue
                served = True
                break
            if not served:
                fails.append((p, r))
    return fails


def live_pairs(T, w):
    """Vertex pairs (u,v) whose block contains the cell that w selects."""
    out = set()
    for (u, v), S in T.items():
        if (w[u], w[v]) in S:
            out.add((u, v))
            out.add((v, u))
    return out


def count_pm(live):
    """Number of perfect matchings of the graph `live` on vertices 0..7,
    by a bitmask DP over subsets.  Exact integer."""
    full = (1 << N) - 1
    memo = {}

    def rec(mask):
        if mask == 0:
            return 1
        if mask in memo:
            return memo[mask]
        # lowest set vertex must be matched
        p = (mask & -mask).bit_length() - 1
        tot = 0
        rest = mask & ~(1 << p)
        m = rest
        while m:
            q = (m & -m).bit_length() - 1
            m &= m - 1
            if (p, q) in live:
                tot += rec(rest & ~(1 << q))
        memo[mask] = tot
        return tot

    return rec(full)


def report(path, verbose=True):
    T = load(path)
    words = list(product(range(D), repeat=N))
    consts = [tuple([c] * N) for c in range(D)]

    support = sum(1 for S in T.values() if S)
    sigma = sum(len(S) for S in T.values())
    fails = sc_ok(T)

    hist = {}
    singles = []
    const_sizes = {}
    for w in words:
        n = count_pm(live_pairs(T, w))
        if w in consts:
            const_sizes[w[0]] = n
            continue
        hist[n] = hist.get(n, 0) + 1
        if n == 1:
            singles.append(w)

    ok = (not fails) and all(const_sizes[c] > 0 for c in range(D)) \
        and not singles
    out = dict(path=path, support=support, sigma=sigma,
               sc_failures=fails, constant_fibre_sizes=const_sizes,
               n_singletons=len(singles),
               mixed_fibre_histogram=dict(sorted(hist.items())),
               n_mixed_with_nonempty_fibre=sum(v for k, v in hist.items()
                                               if k > 0),
               ADMISSIBLE_ZERO_SINGLETON=ok)
    if verbose:
        print(json.dumps(out, indent=1, default=str))
    return out


def selfcheck():
    """The brute-force matching list must be the 105 expected ones, and the
    DP must reproduce a hand-computable case (the complete graph: 105)."""
    Ms = matchings_bruteforce()
    assert len(Ms) == 105, len(Ms)
    live = set()
    for u in range(N):
        for v in range(N):
            if u != v:
                live.add((u, v))
    assert count_pm(live) == 105
    # cube chart: 3-regular, one diagonal cell per direction -> 6 singletons
    T = {e: set() for e in EDGES}
    for u in range(8):
        for b in range(3):
            v = u ^ (1 << b)
            if u < v:
                T[(u, v)] = {(b, b)}
    sing = [w for w in product(range(D), repeat=N)
            if len(set(w)) > 1 and count_pm(live_pairs(T, w)) == 1]
    assert len(sing) == 6, len(sing)
    assert count_pm(live_pairs(T, (0,) * 8)) == 1
    assert sc_ok(T) == []
    return True


if __name__ == "__main__":
    print("selfcheck:", selfcheck())
    for p in sys.argv[1:]:
        report(p)
