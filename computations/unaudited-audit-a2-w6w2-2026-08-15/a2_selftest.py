#!/usr/bin/env python3
"""AUDIT A2 -- self-test + mutation controls for the independent core."""

from __future__ import annotations

import json
import random

import numpy as np

from a2_core import (COLORS, audit_template, fibre_counts_bruteforce,
                     fibre_counts_dp_numpy, fibre_counts_dp_python, geom,
                     normalise_template)

CELLS = [(a, b) for a in COLORS for b in COLORS]
out = {}


def random_template(g, rng, m=None, maxcells=9):
    m = m if m is not None else rng.randrange(1, len(g.edges) + 1)
    chosen = rng.sample(range(len(g.edges)), m)
    t = [frozenset() for _ in g.edges]
    for i in chosen:
        k = rng.randrange(1, maxcells + 1)
        t[i] = frozenset(rng.sample(CELLS, k))
    return t


def main():
    rng = random.Random(20260815)

    # (1) three routes agree: python DP, numpy DP, brute-force matchings
    for n in (4, 6, 8):
        g = geom(n)
        bad = 0
        for _ in range(6 if n == 8 else 25):
            t = normalise_template(g, random_template(g, rng))
            a = fibre_counts_dp_python(g, t)
            b = [int(x) for x in fibre_counts_dp_numpy(g, t)]
            c = fibre_counts_bruteforce(g, t)
            if not (a == b == c):
                bad += 1
        out[f"three_routes_agree_N{n}"] = {"mismatches": bad}
        print(f"N={n}: DP-python == DP-numpy == brute force, mismatches={bad}")

    # (2) sanity: the FULL template (all 9 cells on all edges) gives every word
    #     fibre = #perfect matchings of K_N
    for n, expect in ((4, 3), (6, 15), (8, 105)):
        g = geom(n)
        t = normalise_template(g, [CELLS] * len(g.edges))
        counts = fibre_counts_dp_python(g, t)
        ok = all(c == expect for c in counts)
        out[f"full_template_N{n}"] = {"expected": expect, "all_equal": ok}
        print(f"N={n}: full template fibre == {expect} everywhere: {ok}")

    # (3) sanity: a single perfect matching with constant cells (r,r)
    #     -> fibre 1 on word r^N, 0 elsewhere.
    g = geom(8)
    t = [frozenset() for _ in g.edges]
    for u, v in ((0, 1), (2, 3), (4, 5), (6, 7)):
        t[g.eidx[(u, v)]] = frozenset({(0, 0)})
    counts = fibre_counts_dp_python(g, normalise_template(g, t))
    ok = (counts[g.const_rows[0]] == 1 and sum(counts) == 1)
    out["single_constant_matching"] = {"ok": ok}
    print(f"N=8: one constant matching -> exactly one nonzero fibre: {ok}")

    # (4) MUTATION CONTROL A: the checker must SEE singletons.  Build a
    #     template whose fibre structure is known to contain singletons:
    #     three disjoint constant matchings (0,0)/(1,1)/(2,2) only.
    t = [frozenset() for _ in g.edges]
    trip = (((0, 1), (2, 3), (4, 5), (6, 7)),
            ((0, 2), (1, 3), (4, 6), (5, 7)),
            ((0, 3), (1, 2), (4, 7), (5, 6)))
    for c, M in enumerate(trip):
        for e in M:
            t[g.eidx[e]] = frozenset({(c, c)})
    rep = audit_template(g, t)
    out["mutation_A_three_matchings"] = rep
    print("mutation A (3 disjoint constant matchings): m=%d sigma=%d "
          "singletons=%d const=%s" % (rep["m"], rep["sigma"],
                                      rep["mixed_singletons"],
                                      rep["const_fibres"]))

    # (5) MUTATION CONTROL B: take a template with zero singletons and
    #     delete one cell / add one cell; the verdict must move.
    #     (done in a2_sigmamin_audit.py on the real certificates)

    # (6) MUTATION CONTROL C: fibre counts are invariant under a global
    #     site permutation + colour permutation (gauge sanity).
    def permute(g, t, perm, colperm):
        out_t = [frozenset() for _ in g.edges]
        for i, (u, v) in enumerate(g.edges):
            pu, pv = perm[u], perm[v]
            cells = set()
            for a, b in t[i]:
                ca, cb = colperm[a], colperm[b]
                if pu < pv:
                    cells.add((ca, cb))
                else:
                    cells.add((cb, ca))
            key = (pu, pv) if pu < pv else (pv, pu)
            out_t[g.eidx[key]] = frozenset(cells)
        return out_t

    bad = 0
    for _ in range(8):
        t = normalise_template(g, random_template(g, rng, m=20))
        perm = list(range(8))
        rng.shuffle(perm)
        colperm = [0, 1, 2]
        rng.shuffle(colperm)
        a = sorted(fibre_counts_dp_python(g, t))
        b = sorted(fibre_counts_dp_python(g, normalise_template(
            g, permute(g, t, perm, colperm))))
        if a != b:
            bad += 1
    out["mutation_C_gauge_invariance"] = {"mismatches": bad}
    print(f"mutation C (S_8 x S_3 relabelling invariance): mismatches={bad}")

    with open("results_selftest.json", "w") as h:
        json.dump(out, h, indent=1, default=str)
    print("wrote results_selftest.json")


if __name__ == "__main__":
    main()
