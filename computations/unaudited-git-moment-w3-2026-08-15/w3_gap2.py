"""UNAUDITED PROBE (W3, Route A, 2026-08-15). HEAD 26ba69f7.

THE FLOOR-LIFT GAP, in the declared-colour-subset (coordinate) regime.

A census chart gives each support block uv a declared colour-support
subset T_uv <= {0,1,2}; in the coordinate regime the live cells of that
block are the diagonal cells (uv,c,c) for c in T_uv.

KEY STRUCTURAL FACT.  For any DIAGONAL-ONLY cell support the cell graph
decouples by colour: the cell (uv,c,c) joins the nodes (u,c) and (v,c).
Hence the balance system splits into three independent problems, and

    BAL(S) holds  <=>  for every colour c, every edge of
                       H_c = { uv : c in T_uv }
                       lies in the support of a fractional perfect
                       matching of H_c.

Kills compared:
   M8  some H_c has no perfect matching                       (committed)
   M9  some mixed word has exactly one live matching          (committed)
   O5  some H_c has an edge in no fractional perfect matching (Theorem A.1)

O5 removes cells; when the last cell of a block dies the aggregate
support strictly shrinks, which is the floor lift.
"""

from __future__ import annotations

import itertools
import random
from collections import Counter

from w3_band import ALL_EDGES, N, failing_edges, fpm_exists

_PMS = None


def all_pms():
    global _PMS
    if _PMS is None:
        from w3_core import matchings

        _PMS = [tuple(tuple(sorted(e)) for e in M) for M in matchings(N)]
    return _PMS


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


SUBSETS = [frozenset(t) for k in (1, 2, 3)
           for t in itertools.combinations((0, 1, 2), k)]


def make_chart(rng, nedges, thick_bias=0.5):
    tri = three_disjoint_pms(rng)
    if tri is None:
        return None
    T: dict[tuple[int, int], set[int]] = {}
    for c, P in enumerate(tri):
        for e in P:
            T.setdefault(e, set()).add(c)
    extra = [e for e in ALL_EDGES if e not in T]
    k = nedges - len(T)
    if k < 0 or k > len(extra):
        return None
    for e in rng.sample(extra, k):
        if rng.random() < thick_bias:
            t = rng.choice([s for s in SUBSETS if len(s) >= 2])
        else:
            t = rng.choice([s for s in SUBSETS if len(s) == 1])
        T[e] = set(t)
    return T


def word_multiplicities(T):
    counts = Counter()
    for M in all_pms():
        if any(e not in T for e in M):
            continue
        for choice in itertools.product(*[sorted(T[e]) for e in M]):
            w = [None] * N
            for (u, v), c in zip(M, choice):
                w[u] = w[v] = c
            counts[tuple(w)] += 1
    return counts


def colour_classes(T):
    return [tuple(e for e in T if c in T[e]) for c in range(3)]


def kill_M8(counts):
    return [c for c in range(3) if counts.get((c,) * N, 0) == 0]


def kill_M9(counts):
    return [w for w, m in counts.items() if len(set(w)) > 1 and m == 1]


def kill_O5(T):
    dead_cells = []
    for c, H in enumerate(colour_classes(T)):
        for e in failing_edges(H):
            dead_cells.append((e, c))
    return dead_cells


def blocks_emptied(T, dead_cells):
    lost = Counter()
    for e, c in dead_cells:
        lost[e] += 1
    return [e for e, k in lost.items() if k == len(T[e])]


def survey(nedges, trials=1500, seed=17, thick_bias=0.5):
    rng = random.Random(seed)
    st = Counter()
    cut = []
    survivors = []
    for _ in range(trials):
        T = make_chart(rng, nedges, thick_bias)
        if T is None:
            continue
        st["charts"] += 1
        counts = word_multiplicities(T)
        m8 = kill_M8(counts)
        m9 = kill_M9(counts)
        if m8:
            st["m8"] += 1
        if m9:
            st["m9"] += 1
        dead = kill_O5(T)
        if dead:
            st["o5"] += 1
        if m8 or m9:
            continue
        st["survive_committed"] += 1
        if dead:
            st["o5_on_survivors"] += 1
            st["blocks_emptied"] += bool(blocks_emptied(T, dead))
            cut.append(len(blocks_emptied(T, dead)))
        else:
            st["fully_stable"] += 1
            if len(survivors) < 5:
                survivors.append(T)
    return st, cut, survivors


if __name__ == "__main__":
    print("UNAUDITED PROBE  W3 / Route A  HEAD 26ba69f7")
    print("FLOOR-LIFT GAP, coordinate/declared-subset charts")
    print("=" * 92)
    for bias in (0.5, 0.85):
        print(f"\nthick_bias={bias} (probability an extra block declares >=2 colours)")
        print(f"{'|E|':>4} {'charts':>7} {'M8':>6} {'M9':>7} {'O5':>7} "
              f"{'surv M8+M9':>11} {'O5 on surv':>11} {'blocks cut':>11} "
              f"{'FULLY STABLE':>13}")
        for ne in (14, 16, 18, 20, 22, 24):
            st, cut, surv = survey(ne, trials=1200, thick_bias=bias)
            n = st["charts"]
            if not n:
                continue
            sv = st["survive_committed"]
            avg = sum(cut) / max(1, len(cut))
            print(
                f"{ne:>4} {n:>7} {st['m8']:>6} {st['m9']:>7} {st['o5']:>7} "
                f"{sv:>11} {st['o5_on_survivors']:>11} {avg:>11.2f} "
                f"{st['fully_stable']:>13}"
            )
