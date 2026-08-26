"""UNAUDITED (W11, 2026-08-15).  Independent core for the N=8, d=3 bicoloured
cell-template decision.  Written from scratch from the mathematical definitions
and notes/slice-cover.md sec.2; no code reuse from any other lane.

Conventions
-----------
Vertices        0..7.
Edge            unordered pair (u, v) with u < v; EDGES is the sorted list of
                all 28 such pairs, EIDX maps a pair to its index.
Cell            (i, j) with i = colour at the SMALLER endpoint u,
                j = colour at the LARGER endpoint v.  Read from v's side the
                block is the transpose, which is what `far_cells` implements.
Template        list of 28 frozensets of (i, j) pairs (S_uv per edge).
Word            tuple w of length 8 over {0,1,2}; w[p] is the colour at p.
Matching        frozenset of 4 edge indices forming a perfect matching of K_8.

M supports w  <=>  for every edge (u,v) in M, (w[u], w[v]) in S_uv.
fibre(w)      =  set of matchings supporting w.
constant word =  all eight letters equal (3 of them); mixed = the other 6558.
singleton     =  mixed word whose fibre has size exactly 1.
"""

from itertools import product

N = 8
D = 3

EDGES = [(u, v) for u in range(N) for v in range(u + 1, N)]
EIDX = {e: k for k, e in enumerate(EDGES)}
NE = len(EDGES)  # 28

CELLS = [(i, j) for i in range(D) for j in range(D)]  # 9


def all_perfect_matchings():
    """All perfect matchings of K_N, each as a frozenset of edge indices."""
    out = []

    def rec(remaining, acc):
        if not remaining:
            out.append(frozenset(acc))
            return
        u = remaining[0]
        for k in range(1, len(remaining)):
            v = remaining[k]
            rest = remaining[1:k] + remaining[k + 1:]
            rec(rest, acc + [EIDX[(min(u, v), max(u, v))]])

    rec(list(range(N)), [])
    return out


MATCHINGS = all_perfect_matchings()
NM = len(MATCHINGS)  # 105
MATCH_EDGELIST = [sorted(M) for M in MATCHINGS]

# incident edges, as (edge index, other endpoint)
INCIDENT = [[] for _ in range(N)]
for k, (u, v) in enumerate(EDGES):
    INCIDENT[u].append((k, v))
    INCIDENT[v].append((k, u))


def far_cells(p, j, r):
    """Cells (i,j)-indexed in the u<v convention on edge {p,j} whose colour at
    the FAR endpoint j equals r.  Returns (matching_cells, other_cells)."""
    same, other = [], []
    for c in CELLS:
        a, b = c
        far = b if p < j else a
        (same if far == r else other).append(c)
    return same, other


ALL_WORDS = [tuple(w) for w in product(range(D), repeat=N)]
CONSTANT_WORDS = [tuple([c] * N) for c in range(D)]
MIXED_WORDS = [w for w in ALL_WORDS if len(set(w)) > 1]
assert len(ALL_WORDS) == 6561 and len(MIXED_WORDS) == 6558


# --------------------------------------------------------------------------
# Standalone exact checker: direct fibre enumeration.  Deliberately naive and
# independent of anything the encoder does.
# --------------------------------------------------------------------------

def fibre(template, w):
    """List of indices of matchings supporting word w under `template`."""
    out = []
    for mi, M in enumerate(MATCHINGS):
        ok = True
        for ei in M:
            u, v = EDGES[ei]
            if (w[u], w[v]) not in template[ei]:
                ok = False
                break
        if ok:
            out.append(mi)
    return out


def support_size(template):
    return sum(1 for S in template if S)


def sigma(template):
    return sum(len(S) for S in template)


def sc_slots(template):
    """Return the list of (p, r) slots for which condition (SC) FAILS.

    (SC), as forced by notes/slice-cover.md sec.2 (Forced incident-edge
    theorem): for every vertex p and colour r there is an incident edge pj
    with S_pj nonempty and every cell of S_pj carrying colour r at j.
    """
    bad = []
    for p in range(N):
        for r in range(D):
            served = False
            for (ei, j) in INCIDENT[p]:
                S = template[ei]
                if not S:
                    continue
                same, _other = far_cells(p, j, r)
                if S.issubset(set(same)):
                    served = True
                    break
            if not served:
                bad.append((p, r))
    return bad


def constant_fibres(template):
    return {c: fibre(template, CONSTANT_WORDS[c]) for c in range(D)}


def singleton_words(template, limit=None):
    """Mixed words whose fibre has size exactly 1."""
    out = []
    for w in MIXED_WORDS:
        f = fibre(template, w)
        if len(f) == 1:
            out.append(w)
            if limit is not None and len(out) >= limit:
                break
    return out


def audit(template):
    """Full independent audit of a template.  Returns a dict."""
    cf = constant_fibres(template)
    sings = singleton_words(template)
    return {
        "support": support_size(template),
        "sigma": sigma(template),
        "sc_failures": sc_slots(template),
        "constant_fibre_sizes": {c: len(cf[c]) for c in range(D)},
        "constant_fibres_all_nonempty": all(len(cf[c]) > 0 for c in range(D)),
        "n_singletons": len(sings),
        "singleton_examples": sings[:5],
        "admissible": (not sc_slots(template))
        and all(len(cf[c]) > 0 for c in range(D)),
        "zero_singleton": len(sings) == 0,
    }


def template_from_sets(sets):
    return [frozenset(s) for s in sets]


def template_to_json(template):
    return {
        "edges": [list(e) for e in EDGES],
        "blocks": [sorted([list(c) for c in sorted(S)]) for S in template],
    }


def template_from_json(obj):
    assert [tuple(e) for e in obj["edges"]] == EDGES
    return [frozenset(tuple(c) for c in blk) for blk in obj["blocks"]]
