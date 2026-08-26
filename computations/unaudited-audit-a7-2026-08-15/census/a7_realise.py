"""A7: realisability engine.

Given a candidate Gamma (edge-index list) we must decide whether some template T
with gamma_edges(T) = Gamma lies in (R), and if so produce an explicit witness.

STRUCTURE THEOREM (proved in the report, used only to organise the search; every
YES is certified by running the full exact in_R on the produced template):

  A template with gamma_edges(T)=Gamma is (SC)-admissible iff every vertex p has
  3 incident non-Gamma edges carrying pairwise distinct "far colours" at p.  A
  FULL block is thin in neither direction, so it serves nothing; hence
  deg_Gamma(p) <= 4 is necessary.  Conversely, choosing for each vertex p a set
  S_p of 3 incident non-Gamma edges and a bijection c_p : S_p -> {0,1,2} yields a
  template:
      e={u,v} in S_u cap S_v  ->  single cell (c_v(e), c_u(e))     [1 cell]
      e in S_u only           ->  full column c_u(e)               [3 cells]
      e in S_v only           ->  full row    c_v(e)               [3 cells]
      e in neither            ->  FULL minus one cell              [8 cells]
  and these are exactly the componentwise-maximal templates for that choice of
  server assignment.  Fibre sizes are monotone in the masks, so searching over
  (S_p, c_p, deleted cells) is exhaustive for the purposes of realisability.
"""

import random

import a7_core as C

FULL = 511


def complement_edges(gamma_edge_idx):
    g = set(gamma_edge_idx)
    return [e for e in range(28) if e not in g]


def incident_nonG(gamma_edge_idx):
    non = complement_edges(gamma_edge_idx)
    inc = {p: [] for p in range(8)}
    for e in non:
        u, v = C.EDGES[e]
        inc[u].append(e)
        inc[v].append(e)
    return inc, non


def build_template(gamma_edge_idx, sel, free_del):
    """sel[p] = dict {edge_index: colour} with 3 entries, colours a bijection.
    free_del[e] = (i,j) cell removed from an unused non-Gamma edge."""
    gset = set(gamma_edge_idx)
    T = [0] * 28
    for e in range(28):
        if e in gset:
            T[e] = FULL
            continue
        u, v = C.EDGES[e]
        cu = sel[u].get(e)
        cv = sel[v].get(e)
        if cu is not None and cv is not None:
            T[e] = C.cell_mask(cv, cu)
        elif cu is not None:
            T[e] = C.col_mask(cu)
        elif cv is not None:
            T[e] = C.row_mask(cv)
        else:
            i, j = free_del[e]
            T[e] = FULL ^ C.cell_mask(i, j)
    return T


def score(T):
    """0 iff the fibre conditions hold.  Exact integers only."""
    cnt = C.fibre_counts(T)
    bad_mixed = int((cnt[C.IS_MIXED] < 3).sum())
    bad_const = sum(1 for c in C.CONST_WORDS if int(cnt[c]) < 1)
    return 10 * bad_const + bad_mixed


def naive_sel(gamma_edge_idx):
    inc, _ = incident_nonG(gamma_edge_idx)
    return {p: {e: k for k, e in enumerate(sorted(inc[p])[:3])} for p in range(8)}


def find_cubic_subgraphs(non_edges, limit=200, rng=None):
    """All (up to `limit`) 3-regular spanning subgraphs of the complement."""
    inc = {p: [] for p in range(8)}
    for e in non_edges:
        u, v = C.EDGES[e]
        inc[u].append(e)
        inc[v].append(e)
    order = list(non_edges)
    if rng is not None:
        rng.shuffle(order)
    res = []
    deg = [0] * 8

    def rec(i, chosen):
        if len(res) >= limit:
            return
        if all(d == 3 for d in deg):
            res.append(list(chosen))
            return
        if i >= len(order):
            return
        # prune: remaining capacity
        rem = order[i:]
        cap = [0] * 8
        for e in rem:
            u, v = C.EDGES[e]
            cap[u] += 1
            cap[v] += 1
        for p in range(8):
            if deg[p] + cap[p] < 3:
                return
        e = order[i]
        u, v = C.EDGES[e]
        if deg[u] < 3 and deg[v] < 3:
            deg[u] += 1
            deg[v] += 1
            chosen.append(e)
            rec(i + 1, chosen)
            chosen.pop()
            deg[u] -= 1
            deg[v] -= 1
        rec(i + 1, chosen)

    rec(0, [])
    return res


def sel_from_cubic(D, rng):
    """Random bijective colouring of each vertex's 3 D-edges."""
    inc = {p: [] for p in range(8)}
    for e in D:
        u, v = C.EDGES[e]
        inc[u].append(e)
        inc[v].append(e)
    sel = {}
    for p in range(8):
        cs = [0, 1, 2]
        rng.shuffle(cs)
        sel[p] = {e: cs[k] for k, e in enumerate(inc[p])}
    return sel


def random_sel(gamma_edge_idx, rng):
    inc, _ = incident_nonG(gamma_edge_idx)
    sel = {}
    for p in range(8):
        es = rng.sample(inc[p], 3)
        cs = [0, 1, 2]
        rng.shuffle(cs)
        sel[p] = {e: cs[k] for k, e in enumerate(es)}
    return sel


CELLS9 = [(i, j) for i in range(3) for j in range(3)]


def search_witness(gamma_edge_idx, seed=0, tries=400, hill=60, verbose=False):
    """Return (T, info) with in_R(T) True, or (None, info)."""
    rng = random.Random(seed)
    inc, non = incident_nonG(gamma_edge_idx)
    gset = set(gamma_edge_idx)
    # A FULL block is thin in neither direction, so it serves no demand; a vertex
    # with fewer than 3 incident non-Gamma edges can never have all 3 demands met.
    if any(len(inc[p]) < 3 for p in range(8)):
        return None, {"route": "sc_impossible_deg>4", "evals": 0, "seed": seed,
                      "min_nonGamma_degree": min(len(inc[p]) for p in range(8))}
    default_del = {e: (0, 1) for e in range(28)}
    evals = 0
    best = (10 ** 9, None)

    def evaluate(sel, fdel):
        nonlocal evals, best
        T = build_template(gamma_edge_idx, sel, fdel)
        evals += 1
        s = score(T)
        if s < best[0]:
            best = (s, (dict((p, dict(sel[p])) for p in range(8)), dict(fdel)))
        return s, T

    cands = []
    cands.append(("naive", naive_sel(gamma_edge_idx)))
    cubics = find_cubic_subgraphs(non, limit=60, rng=rng)
    for D in cubics[:20]:
        cands.append(("cubic", sel_from_cubic(D, rng)))
    for _ in range(20):
        cands.append(("random", random_sel(gamma_edge_idx, rng)))

    for tag, sel in cands:
        s, T = evaluate(sel, default_del)
        if s == 0 and C.in_R(T):
            return T, {"route": tag, "evals": evals, "seed": seed}

    # randomized restarts with hill climbing
    for t in range(tries):
        if cubics and t % 2 == 0:
            sel = sel_from_cubic(cubics[rng.randrange(len(cubics))], rng)
        else:
            sel = random_sel(gamma_edge_idx, rng)
        fdel = dict(default_del)
        s, T = evaluate(sel, fdel)
        if s == 0 and C.in_R(T):
            return T, {"route": "restart", "evals": evals, "seed": seed}
        for _ in range(hill):
            p = rng.randrange(8)
            move = rng.random()
            newsel = {q: dict(sel[q]) for q in range(8)}
            newdel = dict(fdel)
            if move < 0.45:
                es = list(newsel[p].keys())
                cs = [newsel[p][e] for e in es]
                i, j = rng.sample(range(3), 2)
                cs[i], cs[j] = cs[j], cs[i]
                newsel[p] = {e: c for e, c in zip(es, cs)}
            elif move < 0.9:
                es = list(newsel[p].keys())
                out = rng.choice(es)
                avail = [e for e in inc[p] if e not in newsel[p]]
                if not avail:
                    continue
                new_e = rng.choice(avail)
                col = newsel[p].pop(out)
                newsel[p][new_e] = col
            else:
                free = [e for e in non
                        if e not in newsel[C.EDGES[e][0]] and e not in newsel[C.EDGES[e][1]]]
                if not free:
                    continue
                e = rng.choice(free)
                newdel[e] = rng.choice(CELLS9)
            s2, T2 = evaluate(newsel, newdel)
            if s2 <= s:
                sel, fdel, s = newsel, newdel, s2
            if s == 0 and C.in_R(T2):
                return T2, {"route": "hill", "evals": evals, "seed": seed}
    return None, {"route": "failed", "evals": evals, "seed": seed, "best_score": best[0]}
