"""UNAUDITED PROBE (W3, Route A, 2026-08-15). HEAD 26ba69f7.

The balance criterion on ANCHOR CHARTS, and the band 18-20 analysis.

Structure used by the committed support-16/17/18 censuses: every
non-distinguished support edge carries a single live *mutual coordinate
anchor* cell (uv, x, x) with x in {0,1,2}; distinguished blocks carry a
declared colour-support subset.

For an ALL-ANCHOR chart the cell graph splits by colour: the cell
(uv,c,c) joins nodes (u,c) and (v,c), so the balance system decouples into
three independent problems, one per colour class

        H_c  =  { uv : the anchor at uv has colour c }  <= K_n .

Balance on colour c is exactly: positive edge weights on H_c with ALL
vertex degrees equal (= mu_c).  Hence

   BAL(anchor chart) holds  <=>  for every colour c, every edge of H_c
   lies in the support of a fractional perfect matching of H_c.

and by half-integrality of the fractional matching polytope this is

   <=>  for every c and every edge uv of H_c, H_c - {u,v} has a
        fractional perfect matching,

which is decided by the fractional Tutte condition  i(H-S) <= |S| for all
S <= V  (Scheinerman-Ullman, Fractional Graph Theory, Thm 2.1.4).

If some colour class fails, the source degenerates and every failing
anchor cell dies -- which kills the WHOLE aggregate block, so the
aggregate support graph strictly shrinks.  This is the floor lift.
"""

from __future__ import annotations

import itertools
import random
from fractions import Fraction

N = 8
VERTS = tuple(range(N))
ALL_EDGES = tuple(itertools.combinations(VERTS, 2))


# ------------------------------------------------ fractional perfect matching


def fpm_exists(edges_set, verts=VERTS) -> bool:
    """Fractional Tutte: i(H - S) <= |S| for every S <= V."""
    adj = {v: set() for v in verts}
    for (u, v) in edges_set:
        adj[u].add(v)
        adj[v].add(u)
    vl = list(verts)
    for mask in range(1 << len(vl)):
        S = {vl[i] for i in range(len(vl)) if mask >> i & 1}
        iso = 0
        for v in vl:
            if v in S:
                continue
            if not (adj[v] - S):
                iso += 1
        if iso > len(S):
            return False
    return True


def _induced(edges_set, removed):
    verts = tuple(x for x in VERTS if x not in removed)
    rest = [f for f in edges_set if f[0] not in removed and f[1] not in removed]
    return rest, verts


def _odd_cycles_through(edges_set, e):
    """All odd cycles (as vertex sets) of the 8-vertex graph containing e."""
    u, v = e
    adj = {x: set() for x in VERTS}
    for (a, b) in edges_set:
        adj[a].add(b)
        adj[b].add(a)
    out = []
    # paths v -> u of even length >= 2 (so the cycle length is odd)
    stack = [(v, [v], {v, u})]
    while stack:
        cur, path, seen = stack.pop()
        for nxt in adj[cur]:
            if nxt == u:
                if len(path) >= 2 and len(path) % 2 == 0:
                    out.append(frozenset(path) | {u})
                continue
            if nxt in seen:
                continue
            if len(path) >= 7:
                continue
            stack.append((nxt, path + [nxt], seen | {nxt}))
    return set(out)


def edge_in_some_fpm(edges_set, e) -> bool:
    """A vertex of the fractional matching polytope is a set of disjoint
    edges (value 1) plus disjoint odd cycles (value 1/2) covering V.  So e
    lies in the support of some fpm iff either H-{u,v} has an fpm (e used
    with value 1) or some odd cycle C through e has H-V(C) with an fpm
    (e used with value 1/2)."""
    u, v = e
    rest, verts = _induced(edges_set, {u, v})
    if fpm_exists(rest, verts):
        return True
    for C in _odd_cycles_through(edges_set, e):
        rest, verts = _induced(edges_set, C)
        if fpm_exists(rest, verts):
            return True
    return False


def passes_balance(edges_set) -> bool:
    """H admits positive edge weights with all 8 vertex degrees equal."""
    es = list(edges_set)
    if not es:
        return False
    cover = set()
    for (u, v) in es:
        cover.add(u)
        cover.add(v)
    if len(cover) < N:                       # isolated node => mu_c = 0
        return False
    if not fpm_exists(es):
        return False
    return all(edge_in_some_fpm(es, e) for e in es)


def failing_edges(edges_set):
    es = list(edges_set)
    cover = set()
    for (u, v) in es:
        cover.add(u)
        cover.add(v)
    if len(cover) < N or not fpm_exists(es):
        return list(es)
    return [e for e in es if not edge_in_some_fpm(es, e)]


# ------------------------------------------------------ cross-check vs the LP


def crosscheck_with_lp(trials=120, seed=3):
    """The fast combinatorial test must agree with the exact balance LP run on
    the corresponding all-anchor cell support."""
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from w3_balance import classify
    from w3_core import cell_index, edge_index

    EI = edge_index(N)
    CI = cell_index(N)
    rng = random.Random(seed)
    agree = disagree = 0
    for _ in range(trials):
        k = rng.randint(4, 12)
        es = rng.sample(ALL_EDGES, k)
        colour = 0
        S = frozenset(CI[(EI[e], colour, colour)] for e in es)
        # the cell support only meets colour-0 nodes; nodes (v,1),(v,2) are
        # isolated, so the FULL balance problem is infeasible by construction.
        # Test the single-colour sub-problem instead, on n=8 with all three
        # colour classes equal to `es` (so each class is the same graph).
        S = frozenset(
            CI[(EI[e], c, c)] for e in es for c in range(3)
        )
        want = passes_balance(es)
        tag, _ = classify(N, S)
        got = tag == "P"
        if want == got:
            agree += 1
        else:
            disagree += 1
            print("  MISMATCH", sorted(es), "fast=", want, "lp=", tag)
    return agree, disagree


# --------------------------------------------------- classify by class size


def classify_sizes(kmax=8, sample=200000, seed=11):
    """For each class size k: are ALL spanning min-degree-1 graphs on 8
    vertices with k edges balance-feasible, none, or some?"""
    rng = random.Random(seed)
    out = {}
    for k in range(4, kmax + 1):
        total = 0
        good = 0
        bad_example = None
        good_example = None
        combos = itertools.combinations(ALL_EDGES, k)
        n_all = 1
        for i in range(k):
            n_all = n_all * (28 - i) // (i + 1)
        if n_all <= sample:
            it = combos
        else:
            it = (tuple(rng.sample(ALL_EDGES, k)) for _ in range(sample))
        for es in it:
            cover = set()
            for (u, v) in es:
                cover.add(u)
                cover.add(v)
            if len(cover) < N:
                continue
            total += 1
            if passes_balance(es):
                good += 1
                if good_example is None:
                    good_example = es
            elif bad_example is None:
                bad_example = es
        out[k] = dict(
            spanning=total,
            balanced=good,
            exhaustive=n_all <= sample,
            bad=bad_example,
            good=good_example,
        )
    return out


# ------------------------------------------------------ band 18-20 charts


def min_degree(es, n=N):
    deg = [0] * n
    for (u, v) in es:
        deg[u] += 1
        deg[v] += 1
    return min(deg)


def sample_band_charts(nedges, trials=20000, seed=5):
    """Sample anchor charts: a support graph G with |E|=nedges, min degree >=3,
    plus a 3-colouring of E(G) in which every vertex sees all three colours
    (the committed forced-incidence condition).  Report the (O5) kill rate."""
    rng = random.Random(seed)
    stats = dict(charts=0, killed=0, killed_by_size=0, edges_killed=[], part=dict())
    tries = 0
    while stats["charts"] < trials and tries < trials * 200:
        tries += 1
        es = rng.sample(ALL_EDGES, nedges)
        if min_degree(es) < 3:
            continue
        col = [rng.randrange(3) for _ in es]
        seen = [set() for _ in range(N)]
        for e, c in zip(es, col):
            seen[e[0]].add(c)
            seen[e[1]].add(c)
        if any(len(s) < 3 for s in seen):
            continue
        classes = [tuple(e for e, c in zip(es, col) if c == cc) for cc in range(3)]
        stats["charts"] += 1
        sizes = tuple(sorted(len(h) for h in classes))
        rec = stats["part"].setdefault(sizes, [0, 0])
        rec[0] += 1
        dead = []
        for h in classes:
            dead.extend(failing_edges(h))
        if dead:
            stats["killed"] += 1
            rec[1] += 1
            stats["edges_killed"].append(len(set(dead)))
            if any(len(h) == 5 for h in classes):
                stats["killed_by_size"] += 1
    return stats


if __name__ == "__main__":
    print("UNAUDITED PROBE  W3 / Route A  HEAD 26ba69f7")
    print("=" * 74)
    print("0. cross-check of the fast criterion against the exact balance LP")
    a, d = crosscheck_with_lp(trials=60)
    print(f"   agree={a} disagree={d}")
    print()
    print("1. balance feasibility of a single anchor colour class, by size")
    tab = classify_sizes(kmax=7)
    for k, r in sorted(tab.items()):
        mode = "EXHAUSTIVE" if r["exhaustive"] else "sampled"
        pct = 100.0 * r["balanced"] / max(1, r["spanning"])
        print(
            f"   k={k:2d} {mode:10s} spanning={r['spanning']:8d} "
            f"balanced={r['balanced']:8d} ({pct:5.1f}%)"
        )
        if r["bad"]:
            print(f"        first failing class: {sorted(r['bad'])}")
    print()
    print("2. band charts (support graph min-degree 3, all 3 colours at each site)")
    for ne in (18, 19, 20):
        st = sample_band_charts(ne, trials=4000)
        kr = 100.0 * st["killed"] / max(1, st["charts"])
        avg = sum(st["edges_killed"]) / max(1, len(st["edges_killed"]))
        print(
            f"   |E|={ne}: charts={st['charts']} killed={st['killed']} ({kr:5.1f}%)"
            f"  mean aggregate edges removed={avg:.2f}"
        )
        for sizes, (tot, kil) in sorted(st["part"].items()):
            if tot >= 20:
                print(
                    f"        class sizes {sizes}: {kil}/{tot} killed "
                    f"({100.0*kil/tot:5.1f}%)"
                )
