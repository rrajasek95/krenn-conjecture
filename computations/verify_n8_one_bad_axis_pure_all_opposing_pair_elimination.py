#!/usr/bin/env python3
"""Eliminate all two-cell torus-opposing carriers on the pure chart.

The chart-character quotient has 22 opposing pairs among its 90 mixed
residual cells.  They form seven orbits under the exact coloured-chart
stabilizer.  For every pair, expand q^[3] and all four literal response
tensors with all fifteen pure z coefficients retained.  Two source rows,
successively specialized after the first carrier vanishes, have a single
carrier times known chart units.  Hence every pair is coefficient-empty.

Only two mixed carriers are adjoined at once.  Three-carrier cancellation
mates are deliberately outside this bounded theorem.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_one_bad_axis_pure_chart_torus_accessibility.py":
        "327dbf6ac8f2d617f78433f25859d8760bec1253d557158425ec8649babd28e9",
    "computations/verify_n8_one_bad_axis_pure_opposing_pair_top_elimination.py":
        "5d79643d55c4d1589e088187d287b8928e448d02b1f93b63001b9fc9ce97de93",
    "computations/verify_n8_one_bad_endpoint_minor_arbitrary_pure_unary_completion.py":
        "f77b99d56d817689e55f4790e000799bc34c9b6960d2b9f035300d407562f20a",
    "computations/verify_n8_one_bad_endpoint_minor_unary_top_completion.py":
        "f0d4c5382cce1ccb8bed5a5ac0afa8cf8662c905bd0c675a56b51f2be7d0b574",
}
EXPECTED_LEDGER_SHA256 = (
    "55fffaa8acc9e7eb399967c0e85ba6e17ebe073e6a7d80e802d16b64cd6087b5"
)

SITES = tuple(range(6))
COLOURS = tuple(range(3))
PURE0 = (0,) * 6
OLD_Q_UNITS = frozenset(("A", "B", "C", "D"))
PURE_Z_UNITS = frozenset(("z03", "z12", "z45"))
STAR_UNITS = frozenset(("p0", "p2", "s1", "s2"))
KNOWN_UNITS = OLD_Q_UNITS | PURE_Z_UNITS | STAR_UNITS


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def variable(name):
    return Counter({(name,): Fraction(1)})


def opposing_pairs(torus, basis):
    cells = tuple(
        (left, right, left_colour, right_colour)
        for left, right in itertools.combinations(SITES, 2)
        for left_colour, right_colour in itertools.product(COLOURS, repeat=2)
        if left_colour != right_colour
    )
    rays = {
        cell: torus.primitive(torus.quotient_character(cell, basis))
        for cell in cells
    }
    pairs = []
    for index, left in enumerate(cells):
        for right in cells[index + 1:]:
            left_ray, right_ray = rays[left], rays[right]
            pivot = next(position for position, value
                         in enumerate(left_ray) if value)
            if (all(left_ray[position] * right_ray[pivot]
                    == right_ray[position] * left_ray[pivot]
                    for position in range(len(left_ray)))
                    and left_ray[pivot] * right_ray[pivot] < 0):
                pairs.append((left, right))
    return tuple(pairs)


def chart_stabilizer(torus):
    anchors = frozenset(torus.ANCHORS)
    group = []
    for site_permutation in itertools.permutations(range(8)):
        site_map = dict(enumerate(site_permutation))
        for colour_permutation in itertools.permutations(COLOURS):
            colour_map = dict(enumerate(colour_permutation))

            def act(cell):
                left, right, left_colour, right_colour = cell
                return torus.canonical_cell(
                    site_map[left], site_map[right],
                    colour_map[left_colour], colour_map[right_colour]
                )

            if frozenset(act(cell) for cell in anchors) == anchors:
                group.append((site_map, colour_map))
    return tuple(group)


def act_cell(torus, cell, group_element):
    site_map, colour_map = group_element
    left, right, left_colour, right_colour = cell
    return torus.canonical_cell(
        site_map[left], site_map[right],
        colour_map[left_colour], colour_map[right_colour]
    )


def pair_orbits(torus, pairs, group):
    remaining = set(pairs)
    pair_set = frozenset(pairs)
    orbits = []
    while remaining:
        seed = min(remaining)
        orbit = frozenset(
            tuple(sorted((act_cell(torus, seed[0], element),
                          act_cell(torus, seed[1], element))))
            for element in group
        ) & pair_set
        require(orbit, f"the orbit of {seed} left the pair set")
        orbits.append(tuple(sorted(orbit)))
        remaining -= orbit
    return tuple(orbits)


def build_q(module, pair):
    q_cells = {
        module.source_cell(2, 4, 1, 1): variable("A"),
        module.source_cell(3, 5, 1, 1): variable("B"),
        module.source_cell(0, 5, 2, 2): variable("C"),
        module.source_cell(1, 4, 2, 2): variable("D"),
    }
    for left, right in itertools.combinations(SITES, 2):
        q_cells[module.source_cell(left, right, 0, 0)] = variable(
            f"z{left}{right}"
        )
    q_cells[module.source_cell(*pair[0])] = variable("x")
    q_cells[module.source_cell(*pair[1])] = variable("y")
    return q_cells


def source_equations(completion, module, q_cells):
    top = completion.symbolic_matching_tensor(module, q_cells, SITES)
    equations = [("top", word, polynomial)
                 for word, polynomial in top.items() if word != PURE0]
    stars = {
        "p1": {0: (1, "p0"), 5: (1, "p5")},
        "p2": {2: (2, "p2")},
        "s1": {1: (1, "s1")},
        "s2": {3: (2, "s2")},
    }
    responses = {}
    for sector, left, right in (
            ("11", "p1", "s1"), ("12", "p1", "s2"),
            ("21", "p2", "s1"), ("22", "p2", "s2")):
        tensor = completion.symbolic_star_product(
            module, stars[left], stars[right], q_cells
        )
        responses[sector] = tensor
        target = ((1,) * 6 if sector == "11"
                  else ((2,) * 6 if sector == "22" else None))
        equations.extend((sector, word, polynomial)
                         for word, polynomial in tensor.items()
                         if word != target)
    return top, responses, tuple(equations)


def specialize(polynomial, killed):
    return Counter({term: coefficient for term, coefficient in polynomial.items()
                    if not any(variable in term for variable in killed)})


def factor_class(term, carrier):
    factors = set(term) - {carrier}
    if factors <= OLD_Q_UNITS:
        return "old-q-pair"
    if factors & PURE_Z_UNITS:
        require(factors <= PURE_Z_UNITS | STAR_UNITS,
                f"a pure-unit killer acquired another factor: {term}")
        return "pure-unit+stars"
    require(factors <= OLD_Q_UNITS | STAR_UNITS,
            f"an old-q killer acquired another factor: {term}")
    return "old-q+stars"


def eliminate_pair(equations, top):
    alive = {"x", "y"}
    killed = set()
    ledger = []
    while alive:
        found = None
        for sector, word, polynomial in sorted(
                equations, key=lambda item: (item[0], item[1])):
            reduced = specialize(polynomial, killed)
            if len(reduced) != 1:
                continue
            term, coefficient = next(iter(reduced.items()))
            carriers = tuple(variable for variable in sorted(alive)
                             if variable in term)
            if len(carriers) != 1:
                continue
            carrier = carriers[0]
            if not set(term) - {carrier} <= KNOWN_UNITS:
                continue
            # A direct binary source cell would add d_ij*q^[3](word) to a
            # response equation.  Every selected residual word is non-pure;
            # that top coefficient is itself zero in the source ideal.
            direct_safe = sector == "top" or word != PURE0
            require(direct_safe, "a response killer used the pure top word")
            found = {
                "carrier": carrier,
                "sector": sector,
                "word": "".join(map(str, word)),
                "monomial": "*".join(term),
                "coefficient": str(coefficient),
                "factor_class": factor_class(term, carrier),
                "direct_safe_mod_top": direct_safe,
            }
            break
        require(found is not None,
                f"the pair did not eliminate after {sorted(killed)}")
        ledger.append(found)
        killed.add(found["carrier"])
        alive.remove(found["carrier"])
    require(len(ledger) == 2, "the pair elimination length changed")
    return tuple(ledger)


def main():
    pin_dependencies()
    torus = importlib.import_module(
        "verify_n8_one_bad_axis_pure_chart_torus_accessibility")
    completion = importlib.import_module(
        "verify_n8_one_bad_endpoint_minor_unary_top_completion")
    module = importlib.import_module(
        "verify_n8_one_bad_multisite_permanent_null_defect")

    basis, _pivots = torus.nullspace(torus.equation_matrix())
    pairs = opposing_pairs(torus, basis)
    require(len(pairs) == 22,
            f"the opposing mixed-pair count changed: {len(pairs)}")
    group = chart_stabilizer(torus)
    orbits = pair_orbits(torus, pairs, group)
    expected_representatives = (
        ((0, 1, 0, 2), (3, 4, 0, 2)),
        ((0, 2, 0, 1), (3, 4, 0, 1)),
        ((0, 2, 2, 1), (4, 5, 1, 2)),
        ((0, 3, 0, 1), (3, 5, 0, 1)),
        ((0, 4, 2, 1), (2, 5, 1, 2)),
        ((0, 5, 2, 0), (4, 5, 0, 2)),
        ((0, 5, 2, 1), (3, 5, 1, 2)),
    )
    require(len(group) == 4
            and tuple(len(orbit) for orbit in orbits) == (4, 4, 2, 4, 2, 4, 2)
            and tuple(orbit[0] for orbit in orbits) == expected_representatives,
            "the chart-stabilizer orbit census changed")

    eliminations = {}
    pattern_histogram = Counter()
    for pair in pairs:
        q_cells = build_q(module, pair)
        top, _responses, equations = source_equations(
            completion, module, q_cells
        )
        elimination = eliminate_pair(equations, top)
        eliminations[str(pair)] = elimination
        pattern = tuple(sorted(step["factor_class"] for step in elimination))
        pattern_histogram[pattern] += 1
    expected_patterns = Counter({
        ("old-q+stars", "pure-unit+stars"): 12,
        ("old-q+stars", "old-q-pair"): 4,
        ("old-q+stars", "old-q+stars"): 4,
        ("old-q-pair", "pure-unit+stars"): 2,
    })
    require(pattern_histogram == expected_patterns,
            f"the unit-row pattern census changed: {pattern_histogram}")

    ledger = {
        "dependencies": PINS,
        "pair_universe": {
            "mixed_cells": 90,
            "opposing_pairs": len(pairs),
        },
        "chart_stabilizer": {
            "size": len(group),
            "orbit_count": len(orbits),
            "orbit_sizes": tuple(len(orbit) for orbit in orbits),
            "representatives": expected_representatives,
            "transported_c821e58_top_top_pairs": len(orbits[0]),
            "nontransported_pairs": len(pairs) - len(orbits[0]),
        },
        "unit_sources": {
            "old_q": sorted(OLD_Q_UNITS),
            "pure_z": sorted(PURE_Z_UNITS),
            "endpoint_stars": sorted(STAR_UNITS),
            "justification": (
                "the two diagonal response anchors make A,B,C,D and the "
                "four displayed star factors units; 260bb94 makes "
                "z03,z12,z45 units"
            ),
        },
        "kill_pattern_histogram": {
            "+".join(pattern): count
            for pattern, count in sorted(pattern_histogram.items())
        },
        "pair_eliminations": eliminations,
        "verdict": (
            "all 22 two-cell mixed carrier circuits are killed by two "
            "successive literal top/response rows; axis-pure chart "
            "accessibility has no pairwise torus obstruction surviving the "
            "complete source equations"
        ),
        "scope": (
            "all fifteen pure z coefficients and exactly one opposing pair "
            "at a time, with complete top and four pinned response tensors; "
            "arbitrary direct binary rows are harmless modulo the selected "
            "mixed top rows; three or more mixed carriers are not classified"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the all-pair elimination ledger changed: {digest}")

    print("N=8 axis-pure all opposing-pair elimination: PASS")
    print("opposing mixed pairs: 22; chart-stabilizer orbits: 7")
    print("all pairs eliminated by two successive literal unit rows")
    print("unit-row pattern classes: 4")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
