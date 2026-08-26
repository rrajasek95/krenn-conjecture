#!/usr/bin/env python3
"""UNAUDITED PROBE (W2) -- EXHAUSTIVE six-site coordinate-regime census.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

Every coordinate template on six sites whose three constant fibres are
nonempty is covered.  A nonempty constant fibre of colour r needs a perfect
matching all of whose edges carry the label (r, r); distinct colours use
disjoint edge sets, so the three constant matchings are automatically
edge-disjoint.  Fixing them canonically (the committed
`colored_triple_orbits` reduction of computations/search_monomial_no_singleton
_sat.py) leaves 15 - 9 = 6 free pairs, each in one of TEN states: absent, or
one of the nine ordered labels.  10^6 per orbit, both orbits, exhaustive.

Outputs, per orbit and per support:
  * the distribution of the number of MIXED SINGLETON fibres,
  * the verdict census of the full kill engine (K0/O2/O1/K3/survivor).

The committed claim it must reproduce (notes/counterexample-search.md
section 3): in the FULL support case the minimum number of mixed singleton
fibres is 6 for the prism union and 4 for K_{3,3}.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
import sys
import time

from w2_monomial import Q, analyse, geometry, is_mixed

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations")
from search_monomial_no_singleton_sat import colored_triple_orbits  # noqa: E402


def union_type(targets):
    """Prism (two disjoint triangles joined) vs K_{3,3}: bipartite or not."""
    edges = [edge for matching in targets for edge in matching]
    complement = [e for e in geometry(6).edges if e not in set(edges)]
    # The union of three disjoint perfect matchings on six vertices is a cubic
    # graph: either K_{3,3} (bipartite) or the triangular prism.
    adjacency = {v: set() for v in range(6)}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    colour = {0: 0}
    stack = [0]
    bipartite = True
    while stack:
        v = stack.pop()
        for w in adjacency[v]:
            if w not in colour:
                colour[w] = 1 - colour[v]
                stack.append(w)
            elif colour[w] == colour[v]:
                bipartite = False
    return ("K33" if bipartite else "prism"), complement


def build_orbit(targets):
    geo = geometry(6)
    base = [None] * len(geo.edges)
    used = set()
    for colour, matching in enumerate(targets):
        for edge in matching:
            base[geo.index[edge]] = (colour, colour)
            used.add(geo.index[edge])
    free = [e for e in range(len(geo.edges)) if e not in used]
    # Per matching: (free slots used, partial colouring from target edges).
    plans = []
    for matching in geo.matchings:
        slots = []
        fixed = {}
        for u, v in matching:
            index = geo.index[(u, v)]
            if base[index] is None:
                slots.append((index, u, v))
            else:
                fixed[u], fixed[v] = base[index]
        plans.append((tuple(slots), tuple(sorted(fixed.items()))))
    return geo, base, free, plans


LABELS = [None] + [divmod(value, Q) for value in range(9)]


def census_orbit(targets, deep_limit=200000):
    geo, base, free, plans = build_orbit(targets)
    slot_of = {edge: position for position, edge in enumerate(free)}
    singleton_distribution = Counter()
    verdicts = Counter()
    by_support = {}
    survivors = []
    deep_calls = 0

    total = 10 ** len(free)
    for code in range(total):
        choice = []
        rest = code
        for _ in range(len(free)):
            choice.append(rest % 10)
            rest //= 10
        support = 9 + sum(1 for value in choice if value)
        table = {}
        for number, (slots, fixed) in enumerate(plans):
            colouring = [-1] * 6
            ok = True
            for index, u, v in slots:
                value = choice[slot_of[index]]
                if value == 0:
                    ok = False
                    break
                a, b = LABELS[value]
                colouring[u], colouring[v] = a, b
            if not ok:
                continue
            for vertex, value in fixed:
                colouring[vertex] = value
            table.setdefault(tuple(colouring), []).append(number)

        singles = sum(1 for c, m in table.items() if is_mixed(c) and len(m) == 1)
        singleton_distribution[(support, singles)] += 1
        bucket = by_support.setdefault(support, Counter())
        if singles:
            verdicts["O2-literal-singleton"] += 1
            bucket["O2-literal-singleton"] += 1
            continue
        labels = list(base)
        for index in free:
            labels[index] = LABELS[choice[slot_of[index]]]
        deep_calls += 1
        result = analyse(geo, labels, table=table)
        verdicts[result["verdict"]] += 1
        bucket[result["verdict"]] += 1
        if result["verdict"] == "survivor":
            survivors.append({"labels": [list(x) if x else None for x in labels],
                              "support": support, "detail": result})
    return {
        "singleton_distribution": {f"{s}:{k}": v for (s, k), v
                                   in sorted(singleton_distribution.items())},
        "verdicts": dict(verdicts),
        "by_support": {str(k): dict(v) for k, v in sorted(by_support.items())},
        "deep_calls": deep_calls,
        "survivors": survivors,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="census6.json")
    args = parser.parse_args()
    print("UNAUDITED PROBE (W2) -- exhaustive six-site census, HEAD 26ba69f",
          flush=True)
    orbits = colored_triple_orbits(6)
    print(f"colored triple orbits at n=6: {len(orbits)}", flush=True)
    report = {}
    for number, targets in enumerate(orbits):
        kind, _complement = union_type(targets)
        start = time.time()
        result = census_orbit(targets)
        result["union_type"] = kind
        result["targets"] = [list(map(list, matching)) for matching in targets]
        result["seconds"] = round(time.time() - start, 1)
        report[f"orbit{number}"] = result
        full = [k for k in result["singleton_distribution"] if k.startswith("15:")]
        minimum_full = min(int(k.split(":")[1]) for k in full)
        minimum_any = min(int(k.split(":")[1])
                          for k in result["singleton_distribution"])
        result["min_singletons_full_support"] = minimum_full
        result["min_singletons_any_support"] = minimum_any
        print(f"orbit{number} ({kind}): verdicts={dict(result['verdicts'])} "
              f"deep={result['deep_calls']} "
              f"min_singletons_full={minimum_full} min_any={minimum_any} "
              f"survivors={len(result['survivors'])} "
              f"({result['seconds']}s)", flush=True)
    with open(args.out, "w") as handle:
        json.dump(report, handle, indent=1)


if __name__ == "__main__":
    main()
