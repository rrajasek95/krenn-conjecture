#!/usr/bin/env python3
"""UNAUDITED PROBE (W4 / Route T.1 scouting, gap sweep).

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

The singleton mechanism alone does NOT cover every weight vector: the
S_6-invariant cone contains no-singleton points, and through such a point there
is a 21-dimensional LINEAR no-singleton space (the 18-dimensional gauge
lineality plus three further directions, identified here).

This sweep asks the decisive T.1 question: at the no-singleton weight vectors,
does the PURE (Laurent-saturation) mechanism fire?  in_w(Phi_c - 1) is
  * the unit -1              if min_M W(M, c-word) > 0
  * a single monomial        if min < 0 and attained once,
either of which puts a monomial (indeed a unit, in the first case) in the
initial ideal.  A weight vector with NO mixed singleton and NO pure mechanism
would be a genuine gap in T.1's coverage.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import json
import random

from tropical_scout import (MIXED, NCELL, PURE, SUPPORT, act, cell, EDGES,
                            fixed_space, gauge_basis, has_singleton,
                            matching_weights, nullspace, random_point,
                            row_reduce, singleton_count)
from tropical_cones import (SUBGROUPS, identity, linear_no_singleton_space,
                            pure_mechanism, transposition)


def describe_direction(vector):
    """Human-readable summary of a cell-weight direction."""
    pattern = {}
    for edge in EDGES:
        for i in range(3):
            for j in range(3):
                pattern.setdefault(vector[cell(edge, i, j)], []).append(
                    (edge, i, j))
    summary = []
    for value, cells in sorted(pattern.items(), key=lambda kv: -len(kv[1])):
        colours = sorted({(i, j) for _e, i, j in cells})
        edges = sorted({e for e, _i, _j in cells})
        summary.append({"value": str(value), "cells": len(cells),
                        "colour_pairs": colours if len(colours) <= 9 else "all",
                        "edges": "all" if len(edges) == 15 else edges})
    return summary


def main():
    print("UNAUDITED PROBE (W4, T.1 gap sweep)")
    print("pinned HEAD 26ba69f7e643694c6a58464af6e9e1de9ec92f01")
    rng = random.Random(31337)
    gauge = gauge_basis()
    gauge_reduced = row_reduce(gauge)
    report = {}

    # collect no-singleton weight vectors from every source we know
    pool = []
    for name in ("S_6 on sites", "S_6 x S_3"):
        basis = fixed_space([act(sigma, tau) for sigma, tau in SUBGROUPS[name]])
        for _ in range(200):
            w = random_point(basis, rng, -12, 12)
            if any(w) and not has_singleton(w)[0]:
                pool.append((name, w))
    print("no-singleton points from the symmetric cones:", len(pool))

    # grow the pool inside the local linear spaces
    grown = []
    for name, w in pool[:12]:
        space = linear_no_singleton_space(w)
        for _ in range(60):
            v = random_point(space, rng, -6, 6)
            candidate = [a + b for a, b in zip(w, v)]
            if not has_singleton(candidate)[0]:
                grown.append(("Lin(%s)" % name, candidate))
    pool.extend(grown)
    print("after growing inside the local linear spaces :", len(pool))

    # the decisive question
    counts = {"unit": 0, "monomial": 0, "neither": 0}
    gaps = []
    for name, w in pool:
        kind = pure_mechanism(w)
        counts[kind] += 1
        if kind == "neither":
            gaps.append((name, w))
    print("pure mechanism at those points: unit %d, monomial %d, NEITHER %d"
          % (counts["unit"], counts["monomial"], counts["neither"]))
    report["pool"] = len(pool)
    report["pure_at_no_singleton"] = counts

    # are the gaps inside the gauge lineality (where T.1 is vacuous anyway)?
    def in_gauge(w):
        row = list(w)
        for pivot, brow in gauge_reduced:
            if row[pivot]:
                factor = row[pivot] / brow[pivot]
                row = [a - factor * b for a, b in zip(row, brow)]
        return not any(row)

    if gaps:
        inside = sum(1 for _n, w in gaps if in_gauge(w))
        print("   of the %d gaps, %d lie in the 18-dim gauge lineality"
              " (where in_w(I) is a gauge translate of I, so T.1 is vacuous)"
              % (len(gaps), inside))
        report["gaps"] = {"total": len(gaps), "in_gauge": inside}
        outside = [(n, w) for n, w in gaps if not in_gauge(w)]
        if outside:
            name, w = outside[0]
            print("   GENUINE GAP found in cone %s; mixed singleton words: %d"
                  % (name, singleton_count(w)))
            report["gap_example"] = {"cone": name,
                                     "weights": [str(x) for x in w]}
            for chi in PURE:
                values = matching_weights(w, chi)
                print("     pure word %s: min %s attained %d times"
                      % (str(chi[0]) * 6, min(values),
                         values.count(min(values))))
    else:
        report["gaps"] = {"total": 0}

    # what are the three extra directions of the 21-dim space?
    print()
    print("the extra directions of the 21-dimensional linear no-singleton space")
    name, w = pool[0]
    space = linear_no_singleton_space(w)
    print("   dim Lin(w) =", len(space), " (gauge = %d)" % len(gauge_reduced))
    extra = []
    combined = row_reduce([list(v) for v in gauge] )
    for vector in space:
        row = list(vector)
        for pivot, brow in combined:
            if row[pivot]:
                factor = row[pivot] / brow[pivot]
                row = [a - factor * b for a, b in zip(row, brow)]
        if any(row):
            extra.append(row)
            combined = row_reduce([list(b) for _p, b in combined] + [row])
    print("   extra dimensions beyond the gauge lineality:", len(extra))
    report["extra_directions"] = []
    for vector in extra:
        summary = describe_direction(vector)
        report["extra_directions"].append(summary)
        print("     direction with value pattern:",
              json.dumps(summary)[:400])

    with open("results_tropical_gap.json", "w") as handle:
        json.dump(report, handle, indent=1, default=str)
    print()
    print("wrote results_tropical_gap.json")


if __name__ == "__main__":
    main()
