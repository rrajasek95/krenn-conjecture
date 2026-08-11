#!/usr/bin/env python3
"""Finite carrier cover for the three same-hole Nakayama unit losses.

The diagonal Q_c and R_a response equations, together with the literal tt
block, leave two possible pure-c carrier matchings and three possible pure-a
carrier matchings.  This checker enumerates their six localized charts and
their exact site-relabel orbits.  Besides the proved Nakayama orbit, the two
remaining orbits have a mixed cofactor coefficient containing a carrier-unit
monomial.  Thus they give an ordinary unit unless a displayed crossed
internal-q repair matching is also nonzero.

This is a carrier-chart cover with the endpoint stars/directs fixed.  It does
not identify the forced internal-q repair with the previously studied
endpoint-star crossed quadratic mate.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_one_bad_same_hole_edge03_nakayama_stability.py":
        "98fe42db69aa92e77a81d13171b3892d71e5d3e7cf32d55db527cabe2bad79f9",
}
EXPECTED_LEDGER_SHA256 = (
    "fbc558ff5114069e7847698b46aefb7d04fe82c4d905b36ec97c53110a17cdbe"
)

A, C, T = range(3)
SITES = tuple(range(5))
T_EDGE = frozenset((2, 3))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def q_name(u, v, a, b):
    if u > v:
        u, v, a, b = v, u, b, a
    return f"q{u}{v}:{a}{b}"


def monomial(*factors):
    return tuple(sorted(factors))


def clean(poly):
    return Counter({term: coefficient for term, coefficient in poly.items()
                    if coefficient})


def odd_fixed_star(base, hole, colour, word):
    if word[hole] != colour:
        return Counter()
    vertices = tuple(site for site in SITES if site != hole)
    endpoint_colour = dict(enumerate(word))
    answer = Counter()
    for matching in base.perfect_matchings(vertices):
        answer[monomial(*(q_name(u, v, endpoint_colour[u], endpoint_colour[v])
                          for u, v in matching))] += 1
    return clean(answer)


def reduce_tt(poly):
    """Use q23:22=1 and q23:ab=0 otherwise."""
    answer = Counter()
    for factors, coefficient in poly.items():
        kept = []
        for factor in factors:
            if factor.startswith("q23:"):
                if factor != q_name(2, 3, T, T):
                    break
            else:
                kept.append(factor)
        else:
            answer[tuple(kept)] += coefficient
    return clean(answer)


def edge_set(*edges):
    return frozenset(frozenset(edge) for edge in edges)


def permute_edges(edges, permutation):
    return frozenset(
        frozenset((permutation[min(edge)], permutation[max(edge)]))
        for edge in edges
    )


def chart_orbits(charts):
    permutations = tuple(itertools.permutations(SITES))
    adjacency = {chart: set() for chart in charts}
    for left in charts:
        for right in charts:
            for permutation in permutations:
                if (permute_edges(left[0], permutation) == right[0]
                        and permute_edges(left[1], permutation) == right[1]
                        and permute_edges(edge_set((2, 3)), permutation)
                        == edge_set((2, 3))):
                    adjacency[left].add(right)
                    break
    unseen = set(charts)
    components = []
    while unseen:
        seed = min(unseen, key=lambda chart: chart[2:])
        component = set()
        stack = [seed]
        while stack:
            chart = stack.pop()
            if chart in component:
                continue
            component.add(chart)
            stack.extend(adjacency[chart] - component)
        unseen -= component
        components.append(tuple(sorted((chart[2], chart[3])
                                       for chart in component)))
    return tuple(sorted(components))


def string_poly(poly):
    return ["*".join(term) if term else "1" for term in sorted(poly)]


def main():
    pin_dependencies()
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")

    # The tt target fixes q23:22=1 and every other q23 decoration to zero.
    qc_target = reduce_tt(odd_fixed_star(base, 0, C, (C,) * 5))
    ra_target = reduce_tt(odd_fixed_star(base, 2, A, (A,) * 5))
    expected_qc = Counter({
        monomial(q_name(1, 2, C, C), q_name(3, 4, C, C)): 1,
        monomial(q_name(1, 3, C, C), q_name(2, 4, C, C)): 1,
    })
    expected_ra = Counter({
        monomial(q_name(0, 1, A, A), q_name(3, 4, A, A)): 1,
        monomial(q_name(0, 3, A, A), q_name(1, 4, A, A)): 1,
        monomial(q_name(0, 4, A, A), q_name(1, 3, A, A)): 1,
    })
    require(qc_target == expected_qc, f"Q_c target changed: {qc_target}")
    require(ra_target == expected_ra, f"R_a target changed: {ra_target}")

    c_carriers = {
        "C1": edge_set((1, 2), (3, 4)),
        "C2": edge_set((1, 3), (2, 4)),
    }
    a_carriers = {
        "A1": edge_set((0, 1), (3, 4)),
        "A2": edge_set((0, 3), (1, 4)),
        "A3": edge_set((0, 4), (1, 3)),
    }
    charts = tuple((c_edges, a_edges, c_name, a_name)
                   for c_name, c_edges in c_carriers.items()
                   for a_name, a_edges in a_carriers.items())
    require(len(charts) == 6, "the pure-carrier chart count changed")

    # A sum equal to one in a local ring has a unit summand; a product is a
    # unit exactly when both factors are.  Hence these six charts cover all
    # residue points of the two pure target equations.
    orbits = chart_orbits(charts)
    expected_orbits = (
        (("C1", "A1"), ("C2", "A3")),
        (("C1", "A2"), ("C2", "A2")),
        (("C1", "A3"), ("C2", "A1")),
    )
    require(orbits == expected_orbits, f"carrier orbits changed: {orbits}")

    # The nontrivial member of the Nakayama orbit is obtained by swapping
    # common sites 1 and 4.  The entire source packet (including star holes)
    # is transported, so this is a genuine site relabel, not a row-only one.
    swap_14 = (0, 4, 2, 3, 1)
    require(permute_edges(c_carriers["C2"], swap_14) == c_carriers["C1"]
            and permute_edges(a_carriers["A1"], swap_14)
            == a_carriers["A3"]
            and permute_edges(edge_set((2, 3)), swap_14)
            == edge_set((2, 3)),
            "the alternate Nakayama carrier stopped being a site relabel")

    # Shared C/A carrier orbit.  In the representative C1,A1 chart the
    # mixed Q_c coefficient 11100 consists of a carrier-unit monomial plus
    # exactly one repair product after the tt reduction.
    shared_word = (C, C, C, A, A)
    shared_defect = reduce_tt(odd_fixed_star(base, 0, C, shared_word))
    shared_unit = monomial(q_name(1, 2, C, C), q_name(3, 4, A, A))
    shared_repair = monomial(q_name(1, 3, C, A), q_name(2, 4, C, A))
    require(shared_defect == Counter({shared_unit: 1, shared_repair: 1}),
            f"the shared-carrier defect changed: {shared_defect}")

    # Middle A/T carrier orbit.  The A2 target carrier and the fixed tt
    # carrier create a unit term in Q_c(10220).  Its cancellation requires
    # one of exactly two crossed internal-q repair matchings.
    middle_word = (C, A, T, T, A)
    middle_defect = reduce_tt(odd_fixed_star(base, 0, C, middle_word))
    # q23:22 has already been replaced by one in the reduced polynomial.
    middle_unit = monomial(q_name(1, 4, A, A))
    middle_repairs = (
        monomial(q_name(1, 2, A, T), q_name(3, 4, T, A)),
        monomial(q_name(1, 3, A, T), q_name(2, 4, T, A)),
    )
    require(middle_defect == Counter({middle_unit: 1,
                                      middle_repairs[0]: 1,
                                      middle_repairs[1]: 1}),
            f"the middle-carrier defect changed: {middle_defect}")

    lost_unit_cover = {
        "q24:11_nonunit": (("C1", "A1"), ("C1", "A2"), ("C1", "A3")),
        "q34:00_nonunit": (("C1", "A2"), ("C1", "A3"),
                             ("C2", "A2"), ("C2", "A3")),
        "q01:00_nonunit": (("C1", "A2"), ("C1", "A3"),
                             ("C2", "A2"), ("C2", "A3")),
    }
    require(set().union(*(set(value) for value in lost_unit_cover.values()))
            == {pair for orbit in expected_orbits for pair in orbit}
               - {("C2", "A1")},
            "the three unit-loss covers stopped covering the five alternatives")

    ledger = {
        "dependencies": PINS,
        "pure_target_polynomials_after_tt": {
            "Qc_all_c": string_poly(qc_target),
            "Ra_all_a": string_poly(ra_target),
        },
        "carrier_charts": 6,
        "site_relabel_orbits": orbits,
        "nakayama_orbit": (("C2", "A1"), ("C1", "A3")),
        "nakayama_relabel_old_to_new": swap_14,
        "unit_loss_cover": lost_unit_cover,
        "shared_CA_defect": {
            "representative": ("C1", "A1"),
            "word": "".join(map(str, shared_word)),
            "polynomial": string_poly(shared_defect),
            "conclusion": (
                "ordinary unit unless the unique mixed C/A repair product "
                "q13:10*q24:10 is a unit"
            ),
        },
        "middle_AT_defect": {
            "representatives": (("C1", "A2"), ("C2", "A2")),
            "word": "".join(map(str, middle_word)),
            "polynomial": string_poly(middle_defect),
            "conclusion": (
                "ordinary unit unless at least one of the two displayed "
                "mixed A/T repair products is a unit"
            ),
        },
        "verdict": (
            "the five nonbase carrier charts split into one exact site-relabel "
            "of the Nakayama chart and four charts forcing a crossed internal-q "
            "repair matching (or an ordinary unit)"
        ),
        "scope": (
            "fixed endpoint-star/direct same-hole packet; this finite cover "
            "does not identify the internal-q crossed repairs with the known "
            "endpoint-star crossed quadratic-mate chart and does not allow "
            "arbitrary extra endpoint-star components"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the carrier-cover ledger changed: {digest}")

    print("h=3 same-hole unit-loss carrier cover: PASS")
    print("pure carrier charts/orbits: 6/3")
    print("Nakayama orbit: C2,A1 <-> C1,A3 by site swap 1<->4")
    print("other charts: ordinary unit or crossed internal-q repair")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
