"""UNAUDITED PROBE (W3, Route A, 2026-08-15). HEAD 26ba69f7.

THE FLOOR-LIFT GAP.

On an all-anchor chart (every support edge carries one live diagonal cell
(uv, x_uv, x_uv)) the committed support-only kills specialise to

  M8 "missed pure row" : some colour class H_c = {uv : x_uv = c} contains
                         no perfect matching  =>  Phi_{c^8} = 0 != 1;
  M9 "singleton mixed" : some mixed word has exactly one live matching;

and the new gauge mechanism of Theorem A.1 specialises to

  O5 "gauge imbalance" : some edge of some H_c lies in no fractional
                         perfect matching of H_c  =>  the source
                         degenerates, that anchor cell dies, hence the
                         whole aggregate block dies and the aggregate
                         support strictly shrinks.

CHART GENERATION.  Because Phi_{c^8}=1 forces a monochromatic-c perfect
matching, an M8-surviving all-anchor chart is exactly

     three PAIRWISE EDGE-DISJOINT perfect matchings P_0,P_1,P_2  (12 edges)
     plus  |E|-12  further edges, each given an arbitrary anchor colour.

That construction automatically has minimum degree 3 and every site seeing
all three colours, so it is sampled without rejection.

We also run a "thickened" variant in which some blocks carry all nine
cells rather than a single anchor, using the general balance LP, to check
that the effect is not an artifact of the one-cell-per-edge idealisation.
"""

from __future__ import annotations

import itertools
import random
from collections import Counter

from w3_band import ALL_EDGES, N, VERTS, failing_edges, min_degree

_M8 = None


def all_pms():
    global _M8
    if _M8 is None:
        from w3_core import matchings

        _M8 = [tuple(tuple(sorted(e)) for e in M) for M in matchings(N)]
    return _M8


def three_disjoint_pms(rng, tries=400):
    Ms = all_pms()
    for _ in range(tries):
        P0 = rng.choice(Ms)
        s0 = set(P0)
        c1 = [M for M in Ms if not (set(M) & s0)]
        if not c1:
            continue
        P1 = rng.choice(c1)
        s1 = s0 | set(P1)
        c2 = [M for M in Ms if not (set(M) & s1)]
        if not c2:
            continue
        return P0, P1, rng.choice(c2)
    return None


def make_chart(rng, nedges):
    tri = three_disjoint_pms(rng)
    if tri is None:
        return None
    edges = []
    colour = []
    for c, P in enumerate(tri):
        for e in P:
            edges.append(e)
            colour.append(c)
    used = set(edges)
    extra = [e for e in ALL_EDGES if e not in used]
    k = nedges - 12
    if k < 0 or k > len(extra):
        return None
    for e in rng.sample(extra, k):
        edges.append(e)
        colour.append(rng.randrange(3))
    return tuple(edges), tuple(colour)


def chart_words(es, colour):
    col = dict(zip(es, colour))
    eset = set(es)
    counts = Counter()
    for M in all_pms():
        if all(e in eset for e in M):
            w = [None] * N
            for (u, v) in M:
                w[u] = w[v] = col[(u, v)]
            counts[tuple(w)] += 1
    return counts


def kill_M8(counts):
    return [c for c in range(3) if counts.get((c,) * N, 0) == 0]


def kill_M9(counts):
    return [w for w, m in counts.items() if len(set(w)) > 1 and m == 1]


def kill_O5(es, colour):
    dead = set()
    for cc in range(3):
        h = tuple(e for e, c in zip(es, colour) if c == cc)
        dead.update(failing_edges(h))
    return dead


def survey(nedges, trials=4000, seed=17):
    rng = random.Random(seed)
    st = Counter()
    removed = []
    stable = []
    for _ in range(trials):
        ch = make_chart(rng, nedges)
        if ch is None:
            continue
        es, colour = ch
        st["charts"] += 1
        counts = chart_words(es, colour)
        assert not kill_M8(counts), "construction guarantees pure rows"
        m9 = kill_M9(counts)
        if m9:
            st["m9"] += 1
        dead = kill_O5(es, colour)
        if dead:
            st["o5"] += 1
        if m9 and dead:
            st["both"] += 1
        if not m9:
            st["survive_M9"] += 1
            if dead:
                st["o5_on_M9_survivors"] += 1
                removed.append(len(dead))
            else:
                st["fully_stable"] += 1
                if len(stable) < 3:
                    stable.append((es, colour))
    return st, removed, stable


def thickened_check(nedges, nthick, trials=120, seed=23):
    """Same charts, but `nthick` of the non-matching blocks carry all nine
    cells.  Uses the general exact balance LP."""
    from w3_balance import classify
    from w3_core import cell_index, edge_index

    EI, CI = edge_index(N), cell_index(N)
    rng = random.Random(seed)
    tally = Counter()
    for _ in range(trials):
        ch = make_chart(rng, nedges)
        if ch is None:
            continue
        es, colour = ch
        thick = set(rng.sample(range(12, len(es)), min(nthick, len(es) - 12)))
        S = set()
        for i, (e, c) in enumerate(zip(es, colour)):
            if i in thick:
                for a in range(3):
                    for b in range(3):
                        S.add(CI[(EI[e], a, b)])
            else:
                S.add(CI[(EI[e], c, c)])
        tag, _ = classify(N, frozenset(S))
        tally[tag] += 1
    return tally


if __name__ == "__main__":
    print("UNAUDITED PROBE  W3 / Route A  HEAD 26ba69f7")
    print("FLOOR-LIFT GAP: committed support kills (M8,M9) vs gauge imbalance (O5)")
    print("all-anchor charts = 3 disjoint pure matchings + extra coloured edges")
    print("=" * 78)
    print(f"{'|E|':>4} {'charts':>7} {'M9':>7} {'O5':>7} {'M9-survivors':>13} "
          f"{'O5 on those':>12} {'fully stable':>13} {'blocks cut':>11}")
    for ne in (13, 14, 15, 16, 17, 18, 19, 20, 21, 22):
        st, removed, stable = survey(ne, trials=2500)
        n = st["charts"]
        if not n:
            continue
        sv = st["survive_M9"]
        avg = sum(removed) / max(1, len(removed))
        print(
            f"{ne:>4} {n:>7} {st['m9']:>7} {st['o5']:>7} {sv:>13} "
            f"{st['o5_on_M9_survivors']:>12} {st['fully_stable']:>13} {avg:>11.2f}"
        )
    print()
    print("thickened variant (some blocks carry all 9 cells), exact balance LP:")
    for ne, nt in ((18, 2), (18, 4), (18, 6), (20, 4), (20, 8)):
        t = thickened_check(ne, nt, trials=80)
        print(f"   |E|={ne} thick={nt}:  {dict(t)}")
