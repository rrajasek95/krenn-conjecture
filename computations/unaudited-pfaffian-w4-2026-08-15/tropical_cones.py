#!/usr/bin/env python3
"""UNAUDITED PROBE (W4 / Route T.1 scouting, addendum) -- the no-singleton locus.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

tropical_scout.py found that generic weight vectors always give a mixed word
with a unique minimal matching (a singleton initial form), but that the
S_6-invariant weight cone often does not.  This script pins that down:

  1. fixed spaces of the natural SUBGROUPS (not just cyclic ones): the full
     S_6 on sites, the full S_3 on colours, S_6 x S_3, and mixtures;
  2. for weight vectors with NO singleton, the maximal LINEAR space of
     perturbations that preserves no-singleton-ness,
         Lin(w) = {v : for every mixed word, all w-minimal matchings have the
                   same v-weight},
     which contains the 18-dimensional gauge lineality and lower-bounds the
     local dimension of the no-singleton locus;
  3. whether the pure (Laurent) mechanism rescues those points.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product
import json
import random

from tropical_scout import (EDGES, MATCHINGS, MIXED, NCELL, PURE, SUPPORT,
                            act, cell, fixed_space, gauge_basis,
                            has_singleton, matching_weights, nullspace,
                            random_point, row_reduce, singleton_count, slack)

SITES = tuple(range(6))


def transposition(n, a, b):
    perm = list(range(n))
    perm[a], perm[b] = perm[b], perm[a]
    return perm


def identity(n):
    return list(range(n))


SUBGROUPS = {
    "S_6 on sites": [(transposition(6, 0, 1), identity(3)),
                     (list(range(1, 6)) + [0], identity(3))],
    "S_3 on colours": [(identity(6), transposition(3, 0, 1)),
                       (identity(6), [1, 2, 0])],
    "S_6 x S_3": [(transposition(6, 0, 1), identity(3)),
                  (list(range(1, 6)) + [0], identity(3)),
                  (identity(6), transposition(3, 0, 1)),
                  (identity(6), [1, 2, 0])],
    "C_6 x C_3": [(list(range(1, 6)) + [0], [1, 2, 0])],
    "C_6 sites": [(list(range(1, 6)) + [0], identity(3))],
    "C_3 colours": [(identity(6), [1, 2, 0])],
    "A_4-ish (3,3) x C_3": [([1, 2, 0, 4, 5, 3], [1, 2, 0])],
    "S_3 diagonal (sites 3+3, colours)": [([1, 2, 0, 4, 5, 3], [1, 2, 0]),
                                          ([1, 0, 2, 4, 3, 5],
                                           transposition(3, 0, 1))],
}


def linear_no_singleton_space(w):
    """{v : every mixed word's w-minimal matchings all have equal v-weight}."""
    equations = []
    for chi in MIXED:
        values = matching_weights(w, chi)
        best = min(values)
        minimal = [n for n, value in enumerate(values) if value == best]
        first = SUPPORT[chi][minimal[0]]
        for other_index in minimal[1:]:
            other = SUPPORT[chi][other_index]
            equation = [0] * NCELL
            for index in first:
                equation[index] += 1
            for index in other:
                equation[index] -= 1
            equations.append(equation)
    return nullspace(equations, NCELL)


def pure_mechanism(w):
    for chi in PURE:
        values = matching_weights(w, chi)
        best = min(values)
        if best > 0:
            return "unit"
        if best < 0 and values.count(best) == 1:
            return "monomial"
    return "neither"


def main():
    print("UNAUDITED PROBE (W4, T.1 addendum) -- the no-singleton locus at K_6")
    print("pinned HEAD 26ba69f7e643694c6a58464af6e9e1de9ec92f01")
    rng = random.Random(4242)
    gauge_dim = len(row_reduce(gauge_basis()))
    print("gauge lineality dim:", gauge_dim)
    print()
    report = {"gauge_dim": gauge_dim, "subgroups": []}
    witnesses = []
    for name, generators in SUBGROUPS.items():
        basis = fixed_space([act(sigma, tau) for sigma, tau in generators])
        hits, trials = 0, 40
        example = None
        for _ in range(trials):
            w = random_point(basis, rng)
            ok, _ = has_singleton(w)
            hits += ok
            if not ok and example is None and any(x for x in w):
                example = w
        entry = {"name": name, "dim": len(basis), "with_singleton": hits,
                 "trials": trials}
        if example is not None:
            witnesses.append((name, example))
        report["subgroups"].append(entry)
        print("  %-34s dim %3d   singleton %2d/%2d %s"
              % (name, len(basis), hits, trials,
                 "" if hits == trials else "<<< NO-SINGLETON POINTS"))
    print()
    print("local linear no-singleton spaces through the witnesses found")
    report["witnesses"] = []
    for name, w in witnesses[:6]:
        space = linear_no_singleton_space(w)
        pure = pure_mechanism(w)
        ties = []
        for chi in MIXED[:0]:
            pass
        entry = {"cone": name, "linear_dim": len(space),
                 "pure_mechanism": pure,
                 "mixed_words_with_singleton": singleton_count(w)}
        report["witnesses"].append(entry)
        print("  from %-30s Lin(w) dim %3d (gauge %d);"
              " pure mechanism: %s" % (name, len(space), gauge_dim, pure))
    print()
    print("robustness: perturb a no-singleton witness inside/outside Lin(w)")
    if witnesses:
        name, w = witnesses[0]
        space = linear_no_singleton_space(w)
        inside = 0
        for _ in range(40):
            v = random_point(space, rng)
            perturbed = [a + b for a, b in zip(w, v)]
            ok, _ = has_singleton(perturbed)
            inside += (not ok)
        outside = 0
        for _ in range(40):
            v = [Fraction(rng.randint(-3, 3)) for _ in range(NCELL)]
            perturbed = [a + b for a, b in zip(w, v)]
            ok, _ = has_singleton(perturbed)
            outside += (not ok)
        print("   inside Lin(w):  %2d/40 stay no-singleton" % inside)
        print("   random ambient: %2d/40 stay no-singleton" % outside)
        report["robustness"] = {"inside": inside, "outside": outside,
                                "linear_dim": len(space)}
    with open("results_tropical_cones.json", "w") as handle:
        json.dump(report, handle, indent=1, default=str)
    print()
    print("wrote results_tropical_cones.json")


if __name__ == "__main__":
    main()
