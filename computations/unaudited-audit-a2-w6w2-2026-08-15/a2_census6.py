#!/usr/bin/env python3
"""AUDIT A2 / claim B.8 -- third independent code path for W2's B.3:
the exhaustive six-site R_cell census, and in particular the minimum number of
mixed singleton fibres at FULL support (|F| = 0).

Route: the three constant matchings are fixed to an orbit representative
(orbit list recomputed here, not imported); the remaining 6 edges range over
{absent} u {9 cells}; for each of the 10^6 templates the fibres are obtained
by grouping the supported perfect matchings by their induced word.  A random
sample is cross-checked against the independent subset-DP counter of a2_core.
"""

from __future__ import annotations

import json
import random
from collections import Counter
from itertools import combinations, permutations, product

from a2_core import audit_template, geom, normalise_template
from a2_rcell_exhaust import perfect_matchings

N = 6
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}
MATCHINGS = perfect_matchings(tuple(range(N)))
STATES = [None] + [(a, b) for a in range(3) for b in range(3)]


def orbit_reps6():
    first = tuple((2 * i, 2 * i + 1) for i in range(N // 2))
    fset = set(first)
    half = N // 2
    stab = []
    for perm in permutations(range(half)):
        for flips in product((0, 1), repeat=half):
            p = [0] * N
            for k in range(half):
                for b in (0, 1):
                    p[2 * k + b] = 2 * perm[k] + (b ^ flips[k])
            stab.append(tuple(p))

    def relabel(M, p):
        return tuple(sorted((min(p[u], p[v]), max(p[u], p[v])) for u, v in M))

    reps = set()
    others = [M for M in MATCHINGS if not (fset & set(M))]
    for a in others:
        for b in others:
            if set(a) & set(b):
                continue
            forms = []
            for p in stab:
                ia, ib = relabel(a, p), relabel(b, p)
                forms.append((ia, ib))
                forms.append((ib, ia))
            reps.add(min(forms))
    return tuple((first,) + pair for pair in sorted(reps))


def bipartite(targets):
    adj = {v: set() for v in range(N)}
    for M in targets:
        for u, v in M:
            adj[u].add(v)
            adj[v].add(u)
    colour = {0: 0}
    stack = [0]
    ok = True
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if w not in colour:
                colour[w] = 1 - colour[v]
                stack.append(w)
            elif colour[w] == colour[v]:
                ok = False
    return ok


def census(targets):
    base = [None] * len(EDGES)
    for c, M in enumerate(targets):
        for e in M:
            base[EIDX[e]] = (c, c)
    free = [i for i, x in enumerate(base) if x is None]
    assert len(free) == len(EDGES) - 3 * (N // 2)
    mlist = [tuple(EIDX[e] for e in M) for M in MATCHINGS]
    vlist = [tuple((e[0], e[1]) for e in M) for M in MATCHINGS]
    dist = Counter()
    best_full = None
    best_any = None
    labels = list(base)
    for assign in product(STATES, repeat=len(free)):
        for i, s in zip(free, assign):
            labels[i] = s
        support = 9 + sum(1 for s in assign if s is not None)
        words = {}
        for mi, idxs in enumerate(mlist):
            w = [0] * N
            ok = True
            for k, ei in enumerate(idxs):
                lab = labels[ei]
                if lab is None:
                    ok = False
                    break
                u, v = vlist[mi][k]
                w[u], w[v] = lab
            if ok:
                words.setdefault(tuple(w), 0)
                words[tuple(w)] += 1
        if any(tuple([r] * N) not in words for r in range(3)):
            continue
        singles = sum(1 for w, k in words.items()
                      if k == 1 and len(set(w)) > 1)
        dist[(support, singles)] += 1
        if best_any is None or singles < best_any:
            best_any = singles
        if support == len(EDGES):
            if best_full is None or singles < best_full:
                best_full = singles
    return dist, best_full, best_any


def main():
    reps = orbit_reps6()
    print(f"n=6 colour-triple orbits recomputed: {len(reps)} (claim 2)")
    out = {"orbits": len(reps), "rows": []}
    g = geom(N)
    rng = random.Random(7)
    for oi, targets in enumerate(reps):
        kind = "K33" if bipartite(targets) else "prism"
        dist, full, anyv = census(targets)
        total = sum(dist.values())
        print(f"  orbit {oi} ({kind}): {total} valid templates, "
              f"min singletons at FULL support = {full}, min at any support "
              f"= {anyv}")
        out["rows"].append({"orbit": oi, "kind": kind, "valid": total,
                            "min_singletons_full_support": full,
                            "min_singletons_any_support": anyv,
                            "distribution": {f"{s}:{k}": v
                                             for (s, k), v in sorted(dist.items())}})
    print(f"OVERALL minimum at full support (|F| = 0): "
          f"{min(r['min_singletons_full_support'] for r in out['rows'])} "
          f"(claim 4)")

    # cross-check a random sample against the subset-DP counter
    mismatches = 0
    for _ in range(200):
        targets = reps[rng.randrange(len(reps))]
        labels = [None] * len(EDGES)
        for c, M in enumerate(targets):
            for e in M:
                labels[EIDX[e]] = (c, c)
        for i in [i for i, x in enumerate(labels) if x is None]:
            labels[i] = rng.choice(STATES)
        t = normalise_template(g, [frozenset() if x is None
                                   else frozenset({tuple(x)}) for x in labels])
        rep = audit_template(g, t, exact=True)
        words = {}
        for M in MATCHINGS:
            w = [0] * N
            ok = True
            for u, v in M:
                lab = labels[EIDX[(u, v)]]
                if lab is None:
                    ok = False
                    break
                w[u], w[v] = lab
            if ok:
                words[tuple(w)] = words.get(tuple(w), 0) + 1
        singles = sum(1 for w, k in words.items()
                      if k == 1 and len(set(w)) > 1)
        if singles != rep["mixed_singletons"]:
            mismatches += 1
    print(f"cross-check against subset-DP counter on 200 random templates: "
          f"{mismatches} mismatches")
    out["dp_crosscheck_mismatches"] = mismatches
    with open("results_census6.json", "w") as h:
        json.dump(out, h, indent=1, default=str)
    print("wrote results_census6.json")


if __name__ == "__main__":
    main()
