#!/usr/bin/env python3
"""A3 Task 1 -- exhaustive structured sweeps for a singleton-free template
at N = 10 (the first N = 2 mod 4 above the proved N = 6).

Three complete sweeps, all exact:
  (S1) CIRCULANT: colour each of the 5 difference classes of Z_10 by
       {0,1,2,absent}  -> 4^5 = 1024 templates, all diagonal.
  (S2) BIPARTITE-SPLIT: V = X u Y with |X| = 2a; colour 0 = K_{X,Y};
       colours 1,2 arbitrary DISJOINT graphs inside K_X u K_Y.  Exhausted
       only for the sub-family "colour 1 = a perfect matching M of X u Y
       (when it exists), colour 2 = everything else inside" over all
       splits and all M -- this is exactly the A3 family template, tested
       at every unbalanced split of 10.
  (S3) BLOW-UP of the N = 8 family: F_4 with one vertex of X and one of Y
       each SPLIT into two (all 3^2 recolourings of the new internal
       edges x all colourings of the duplicated star), plus the two
       "add a pendant M-pair" variants.

Also: (S4) the general parity statistic -- for every diagonal template on
N = 6 and N = 10 in the sweeps, record the minimum number of singletons.
"""

from __future__ import annotations

import json
import sys
from itertools import combinations, product

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from a3_core import DiagonalTemplate, colour_partitions

N = 10
PARTS = colour_partitions(N)


def census(colour_edges):
    tpl = DiagonalTemplate(N, colour_edges)
    s, hist, pures, sw = tpl.census(PARTS)
    return s, pures, hist


def sweep_circulant():
    diffs = {}
    for d in range(1, 6):
        es = set()
        for i in range(N):
            j = (i + d) % N
            es.add(tuple(sorted((i, j))))
        diffs[d] = es
    best, rows = None, []
    for assign in product([None, 0, 1, 2], repeat=5):
        ce = [set(), set(), set()]
        for d, c in zip(range(1, 6), assign):
            if c is not None:
                ce[c] |= diffs[d]
        if any(not e for e in ce):
            continue
        s, pures, hist = census(ce)
        if 0 in pures:
            continue
        rows.append(dict(assign=list(assign), singletons=s, pures=pures))
        if best is None or s < best["singletons"]:
            best = rows[-1]
    return dict(tested=len(rows), best=best,
                zero_singleton=[r for r in rows if r["singletons"] == 0])


def sweep_bipartite_splits():
    """colour 0 = K_{X,Y}; colour 1 = a perfect matching of X and of Y (if
    they have even size); colour 2 = the rest inside X and inside Y."""
    rows = []
    for a in range(2, 9):
        X = list(range(a))
        Y = list(range(a, N))
        if len(X) % 2 or len(Y) % 2:
            continue
        # all perfect matchings of X and of Y
        def pms(S):
            if not S:
                yield []
                return
            f = S[0]
            for i in range(1, len(S)):
                for r in pms(S[1:i] + S[i + 1:]):
                    yield [tuple(sorted((f, S[i])))] + r
        for MX in pms(X):
            for MY in pms(Y):
                M = set(MX) | set(MY)
                E0 = {tuple(sorted((x, y))) for x in X for y in Y}
                E2 = set()
                for S in (X, Y):
                    for e in combinations(sorted(S), 2):
                        if e not in M:
                            E2.add(e)
                if not E2:
                    continue
                s, pures, hist = census([E0, M, E2])
                rows.append(dict(split=[len(X), len(Y)], singletons=s,
                                 pures=pures, MX=MX, MY=MY))
    ok = [r for r in rows if r["singletons"] == 0 and 0 not in r["pures"]]
    return dict(tested=len(rows), zero_singleton_and_all_pures=ok[:5],
                count_ok=len(ok),
                best=min(rows, key=lambda r: (0 in r["pures"], r["singletons"]))
                if rows else None)


def sweep_blowup():
    """Take F_4 on {0..7} (X = evens, Y = odds) and grow to 10 sites by
    splitting one X-vertex and one Y-vertex; sweep the colours of the two
    new internal edges and of every duplicated cross edge state."""
    X8, Y8 = [0, 2, 4, 6], [1, 3, 5, 7]
    MX8 = [(0, 2), (4, 6)]
    MY8 = [(1, 3), (5, 7)]
    rows, ok = [], []
    # 8 -> new vertices 8 (clone of 0, joins X) and 9 (clone of 1, joins Y)
    for cnew_x in (0, 1, 2, None):        # colour of edge {0,8}
        for cnew_y in (0, 1, 2, None):    # colour of edge {1,9}
            for clone_mode in ("copy", "swap"):
                E = {0: set(), 1: set(), 2: set()}
                X, Y = X8 + [8], Y8 + [9]
                M = set(MX8) | set(MY8)
                for (u, v) in combinations(range(8), 2):
                    if (u in X8) != (v in X8):
                        E[0].add((u, v))
                    elif (u, v) in M:
                        E[1].add((u, v))
                    else:
                        E[2].add((u, v))
                # new cross edges
                for y in Y8:
                    E[0].add(tuple(sorted((8, y))))
                for x in X8:
                    E[0].add(tuple(sorted((9, x))))
                E[0].add((8, 9))
                # 8's edges inside X: copy 0's, or swap 0's roles
                for x in X8:
                    if x == 0:
                        continue
                    src = (0, x) if (0, x) in M else None
                    lab = 1 if (tuple(sorted((0, x))) in M) else 2
                    if clone_mode == "swap":
                        lab = 2 if lab == 1 else 1
                    E[lab].add(tuple(sorted((8, x))))
                for y in Y8:
                    if y == 1:
                        continue
                    lab = 1 if (tuple(sorted((1, y))) in M) else 2
                    if clone_mode == "swap":
                        lab = 2 if lab == 1 else 1
                    E[lab].add(tuple(sorted((9, y))))
                if cnew_x is not None:
                    E[cnew_x].add((0, 8))
                if cnew_y is not None:
                    E[cnew_y].add((1, 9))
                ce = [E[0], E[1], E[2]]
                allе = [e for s in ce for e in s]
                if len(allе) != len(set(allе)):
                    continue
                s, pures, hist = census(ce)
                row = dict(cnew_x=cnew_x, cnew_y=cnew_y, mode=clone_mode,
                           singletons=s, pures=pures)
                rows.append(row)
                if s == 0 and 0 not in pures:
                    ok.append(row)
    return dict(tested=len(rows), zero_singleton_all_pures=ok,
                best=min(rows, key=lambda r: (0 in r["pures"], r["singletons"]))
                if rows else None)


def main():
    out = {}
    out["circulant"] = sweep_circulant()
    print("circulant sweep:", out["circulant"]["tested"], "templates with all "
          "pures live; zero-singleton hits:",
          len(out["circulant"]["zero_singleton"]),
          "; best:", out["circulant"]["best"])
    out["bipartite_splits"] = sweep_bipartite_splits()
    print("bipartite-split sweep:", out["bipartite_splits"]["tested"],
          "templates; zero-singleton+all-pures:",
          out["bipartite_splits"]["count_ok"],
          "; best:", out["bipartite_splits"]["best"])
    out["blowup"] = sweep_blowup()
    print("F_4 blow-up sweep:", out["blowup"]["tested"], "templates; hits:",
          len(out["blowup"]["zero_singleton_all_pures"]),
          "; best:", out["blowup"]["best"])
    with open(__file__.rsplit("/", 1)[0] + "/results_structured10.json",
              "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print("wrote results_structured10.json")


if __name__ == "__main__":
    main()
