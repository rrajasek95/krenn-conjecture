#!/usr/bin/env python3
"""AUDIT A2 / claim B.6 -- independent exhaustion of R_cell at N = 8.

CLAIM UNDER AUDIT (W2): in R_cell at N <= 8, mixed singletons kill every
support <= 27; exactly 28 no-singleton templates exist, all at full support.

SETUP (re-derived).  In R_cell every edge carries at most one cell, so an edge
that carries a constant cell (r,r) carries no other; the three constant fibres
are nonempty iff there are three EDGE-DISJOINT perfect matchings M_0, M_1, M_2
with M_r inside the (r,r) cells.  Up to relabelling sites (S_8) and colours we
may fix (M_0, M_1, M_2) to an orbit representative; the orbit list is
recomputed here from scratch and compared with the committed one.

ENCODING (mine; the committed script uses 10-state edge variables and pairwise
"same colouring" witnesses -- here the variables are HALF-EDGE COLOURS, which
makes the "same word" condition a direct equality of half-edge literals):

  present[e]                     edge e is in the support
  h[e][side][c]                  the colour of e at its `side` endpoint
  sup[M]        <->  all four edges of M present
  same[M][M']    ->  sup[M] & sup[M'] & (same colour at every vertex)
  con[M][c]      ->  every half-edge of M is coloured c
  sup[M]         ->  con[M][0] | con[M][1] | con[M][2] | OR_{M'} same[M][M']

Enumeration blocks the exact (present, h) assignment, so termination in UNSAT
is a complete enumeration.  Every model found is re-verified independently by
the subset-DP fibre counter of a2_core.
"""

from __future__ import annotations

import json
import sys
from itertools import combinations, permutations, product

from pysat.formula import IDPool
from pysat.solvers import Solver

from a2_core import audit_template, geom, normalise_template

N = 8
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}


def perfect_matchings(vs):
    if not vs:
        return [()]
    first, out = vs[0], []
    for i in range(1, len(vs)):
        rest = vs[1:i] + vs[i + 1:]
        for tail in perfect_matchings(rest):
            out.append(tuple(sorted(((first, vs[i]),) + tail)))
    return out


MATCHINGS = perfect_matchings(tuple(range(N)))


# ------------------------------------------------------------ orbit census


def orbit_reps():
    """Triples of pairwise disjoint perfect matchings, first one canonical,
    quotiented by the stabiliser of the first and by swapping colours 1,2.
    Recomputed from scratch (no import from the committed script)."""
    first = tuple((2 * i, 2 * i + 1) for i in range(N // 2))
    fset = set(first)
    stab = []
    half = N // 2
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
        aset = set(a)
        for b in others:
            if aset & set(b):
                continue
            forms = []
            for p in stab:
                ia, ib = relabel(a, p), relabel(b, p)
                forms.append((ia, ib))
                forms.append((ib, ia))
            reps.add(min(forms))
    return tuple((first,) + pair for pair in sorted(reps))


# ------------------------------------------------------------ the formula


def build(targets):
    pool = IDPool()
    present = {e: pool.id(("p", e)) for e in range(len(EDGES))}
    h = {(e, s, c): pool.id(("h", e, s, c))
         for e in range(len(EDGES)) for s in (0, 1) for c in range(3)}
    cl = []
    for e in range(len(EDGES)):
        for s in (0, 1):
            lits = [h[(e, s, c)] for c in range(3)]
            cl.append([-present[e]] + lits)                 # present -> some
            for c in range(3):
                cl.append([-h[(e, s, c)], present[e]])      # colour -> present
            for c1, c2 in combinations(range(3), 2):        # at most one
                cl.append([-h[(e, s, c1)], -h[(e, s, c2)]])

    for c, M in enumerate(targets):                          # fixed constants
        for e in M:
            cl.append([present[EIDX[e]]])
            for s in (0, 1):
                cl.append([h[(EIDX[e], s, c)]])

    sup = {}
    con = {}
    inc = []
    for mi, M in enumerate(MATCHINGS):
        s_ = sup[mi] = pool.id(("s", mi))
        for e in M:
            cl.append([-s_, present[EIDX[e]]])
        cl.append([s_] + [-present[EIDX[e]] for e in M])
        side = {}
        for e in M:
            side[e[0]] = (EIDX[e], 0)
            side[e[1]] = (EIDX[e], 1)
        inc.append(side)
        for c in range(3):
            v = con[(mi, c)] = pool.id(("c", mi, c))
            for u in range(N):
                ei, sd = side[u]
                cl.append([-v, h[(ei, sd, c)]])

    same = {}
    for i, j in combinations(range(len(MATCHINGS)), 2):
        v = same[(i, j)] = pool.id(("m", i, j))
        cl.append([-v, sup[i]])
        cl.append([-v, sup[j]])
        for u in range(N):
            ea, sa = inc[i][u]
            eb, sb = inc[j][u]
            if (ea, sa) == (eb, sb):
                continue
            for c in range(3):
                cl.append([-v, -h[(ea, sa, c)], h[(eb, sb, c)]])
                cl.append([-v, -h[(eb, sb, c)], h[(ea, sa, c)]])

    for i in range(len(MATCHINGS)):
        mates = [same[(min(i, j), max(i, j))]
                 for j in range(len(MATCHINGS)) if j != i]
        cl.append([-sup[i]] + [con[(i, c)] for c in range(3)] + mates)
    return cl, present, h, pool


def decode(model, present, h):
    pos = {l for l in model if l > 0}
    labels = []
    for e in range(len(EDGES)):
        if present[e] not in pos:
            labels.append(None)
            continue
        a = next(c for c in range(3) if h[(e, 0, c)] in pos)
        b = next(c for c in range(3) if h[(e, 1, c)] in pos)
        labels.append((a, b))
    return labels


def main():
    g = geom(N)
    reps = orbit_reps()
    print(f"orbit representatives recomputed independently: {len(reps)} "
          f"(W2/committed claim: 13)")
    try:
        sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations")
        from search_monomial_no_singleton_sat import colored_triple_orbits
        same = tuple(colored_triple_orbits(N)) == reps
        print(f"  identical to the committed list: {same}")
    except Exception as exc:                       # pragma: no cover
        same = f"comparison failed: {exc}"
        print(f"  {same}")

    total = 0
    rows = []
    for oi, targets in enumerate(reps):
        cl, present, h, pool = build(targets)
        models = []
        with Solver(name="cadical195", bootstrap_with=cl) as s:
            while s.solve():
                model = s.get_model()
                labels = decode(model, present, h)
                models.append(labels)
                block = []
                for e in range(len(EDGES)):
                    if labels[e] is None:
                        block.append(present[e])
                    else:
                        block.append(-h[(e, 0, labels[e][0])])
                        block.append(-h[(e, 1, labels[e][1])])
                s.add_clause(block)
        checked = []
        for labels in models:
            t = normalise_template(
                g, [frozenset() if x is None else frozenset({tuple(x)})
                    for x in labels])
            rep = audit_template(g, t, exact=False)
            checked.append({"support": rep["m"],
                            "mixed_singletons": rep["mixed_singletons"],
                            "const_fibres": rep["const_fibres"],
                            "diagonal": all(x is None or x[0] == x[1]
                                            for x in labels),
                            "labels": [None if x is None else list(x)
                                       for x in labels]})
        total += len(models)
        supports = sorted({c["support"] for c in checked})
        bad = [c for c in checked if c["mixed_singletons"] != 0
               or not all(c["const_fibres"])]
        rows.append({"orbit": oi, "targets": [[list(e) for e in M]
                                              for M in targets],
                     "models": len(models), "supports": supports,
                     "independent_check_failures": len(bad),
                     "detail": checked})
        print(f"  orbit {oi}: {len(models)} models, supports {supports}, "
              f"independent-check failures {len(bad)}", flush=True)
    ndiag = sum(1 for r in rows for c in r["detail"] if c["diagonal"])
    print(f"TOTAL MODELS: {total} (claim 28); diagonal {ndiag} (claim 22), "
          f"off-diagonal {total - ndiag} (claim 6)")
    with open("results_rcell_exhaust.json", "w") as fh:
        json.dump({"orbits": len(reps), "identical_to_committed": same,
                   "total_models": total, "diagonal": ndiag, "rows": rows},
                  fh, indent=1, default=str)
    print("wrote results_rcell_exhaust.json")


if __name__ == "__main__":
    main()
