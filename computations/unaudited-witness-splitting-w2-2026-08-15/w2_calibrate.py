#!/usr/bin/env python3
"""UNAUDITED PROBE (W2) -- calibration of the kill engine on committed data.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

Three calibration targets, all from committed artifacts:

  C1  notes/monomial-fiber-counterexample.md eq. (1) = the orbit-40 monomial
      boundary of notes/n8-toric-binomial-lattice-audit.md.  Expected fibre
      census {1:1, 2:38, 4:1, 24:1} with the size-1/4/24 fibres CONSTANT;
      expected verdict O1 (odd holonomy), NOT O2.
  C2  a literal singleton template (drop one edge of C1) -> O2.
  C3  the committed six-site claim (notes/counterexample-search.md section 3):
      in the FULL-support monomial ansatz on six vertices every assignment has
      a mixed singleton, with minima 6 (prism) and 4 (K_{3,3}).
"""

from __future__ import annotations

from collections import Counter
from itertools import product
import json
import sys
import time

from w2_monomial import (Q, analyse, fibre_profile, fibres, geometry,
                         is_mixed, support_size)


def orbit40_labels():
    """The committed K_8 monomial boundary, eq. (1) of the counterexample note."""
    geo = geometry(8)
    e1 = {(0, 2), (1, 3), (4, 6), (5, 7)}
    e2 = {(0, 4), (0, 6), (1, 5), (1, 7), (2, 4), (2, 6), (3, 5), (3, 7)}
    labels = []
    for edge in geo.edges:
        if edge in e1:
            labels.append((1, 1))
        elif edge in e2:
            labels.append((2, 2))
        else:
            labels.append((0, 0))
    return geo, labels


def c1_c2():
    geo, labels = orbit40_labels()
    table = fibres(geo, labels)
    census = Counter(len(members) for members in table.values())
    exceptional = {len(members): colouring for colouring, members in table.items()
                   if len(members) != 2}
    singletons, histogram = fibre_profile(table)
    start = time.time()
    verdict = analyse(geo, labels)
    report = {
        "C1_support": support_size(labels),
        "C1_fibre_census": dict(sorted(census.items())),
        "C1_exceptional_are_constant": {
            str(size): [colouring, not is_mixed(colouring)]
            for size, colouring in sorted(exceptional.items())},
        "C1_mixed_singletons": singletons,
        "C1_mixed_histogram": dict(sorted(histogram.items())),
        "C1_verdict": verdict["verdict"],
        "C1_seconds": round(time.time() - start, 2),
    }
    if verdict["verdict"] == "O1-odd-holonomy":
        report["C1_relation_coeffs"] = verdict["coefficients"]
        report["C1_relation_words"] = verdict.get("words")
        report["C1_binomials"] = verdict.get("binomials")

    # C2: delete one edge -> literal singletons must appear.
    dropped = list(labels)
    dropped[geo.index[(0, 1)]] = None
    table2 = fibres(geo, dropped)
    singles2, hist2 = fibre_profile(table2)
    verdict2 = analyse(geo, dropped)
    report.update({
        "C2_support": support_size(dropped),
        "C2_mixed_singletons": singles2,
        "C2_mixed_histogram": dict(sorted(hist2.items())),
        "C2_verdict": verdict2["verdict"],
    })
    return report


def disjoint_triples(size):
    """Ordered triples of pairwise edge-disjoint perfect matchings, up to the
    relabelling used by the committed SAT search (first matching canonical)."""
    sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations")
    from search_monomial_no_singleton_sat import colored_triple_orbits
    return colored_triple_orbits(size)


def c3_full_support_six():
    """Exhaustive: 9^6 label choices on the six non-target edges, all present."""
    geo = geometry(6)
    orbits = disjoint_triples(6)
    out = {}
    for number, targets in enumerate(orbits):
        base = [None] * len(geo.edges)
        used = set()
        for colour, matching in enumerate(targets):
            for edge in matching:
                base[geo.index[edge]] = (colour, colour)
                used.add(geo.index[edge])
        free = [e for e in range(len(geo.edges)) if e not in used]
        assert len(free) == 6, len(free)
        minimum = None
        distribution = Counter()
        for choice in product(range(9), repeat=len(free)):
            labels = list(base)
            for slot, value in zip(free, choice):
                labels[slot] = divmod(value, Q)
            singles, _ = fibre_profile(fibres(geo, labels))
            distribution[singles] += 1
            if minimum is None or singles < minimum:
                minimum = singles
        # Identify the union type of the three target matchings.
        edges = {edge for matching in targets for edge in matching}
        degree_free = Counter()
        for u, v in geo.edges:
            if (u, v) not in edges:
                degree_free[u] += 1
                degree_free[v] += 1
        out[f"orbit{number}"] = {
            "targets": [list(map(list, matching)) for matching in targets],
            "min_mixed_singletons": minimum,
            "complement_degrees": sorted(degree_free.values()),
            "distribution": dict(sorted(distribution.items())),
        }
    return out


def main():
    print("UNAUDITED PROBE (W2) -- calibration, HEAD 26ba69f", flush=True)
    report = {"C1_C2": c1_c2()}
    print(json.dumps(report["C1_C2"], indent=1), flush=True)
    start = time.time()
    report["C3_six_full_support"] = c3_full_support_six()
    print(f"C3 seconds={time.time() - start:.0f}", flush=True)
    print(json.dumps(report["C3_six_full_support"], indent=1)[:2000], flush=True)
    with open("calibration.json", "w") as handle:
        json.dump(report, handle, indent=1)


if __name__ == "__main__":
    main()
