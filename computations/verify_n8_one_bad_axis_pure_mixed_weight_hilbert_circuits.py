#!/usr/bin/env python3
"""Degree-two/three Hilbert circuits of the pure-chart mixed weight cone.

The 90 off-diagonal residual q cells define rational quotient characters on
the 13-dimensional chart-cocharacter kernel (their span has rank 11).
Nonseparability is a nonzero nonnegative dependence among these columns.
Besides the 22 opposing pairs, there are 58 pair-free positive three-cell
circuits.  Every one has primitive raw coefficients (1,1,1) and is the
unique three-edge recombination of one retained anchor in each colour.

These triples are indecomposable nonnegative integer-kernel elements, hence
genuine Hilbert-basis elements.  This checker makes no claim about Hilbert
basis elements of degree four or higher.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib
import itertools
import json
from math import gcd, lcm
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_one_bad_axis_pure_chart_torus_accessibility.py":
        "327dbf6ac8f2d617f78433f25859d8760bec1253d557158425ec8649babd28e9",
    "computations/verify_n8_one_bad_axis_pure_all_opposing_pair_elimination.py":
        "2c7ab786a4b0efeb0a4a02e85268d0decef86de0986c1fb0ae567f013676d97c",
}
EXPECTED_LEDGER_SHA256 = (
    "cf305fb10e70ab9358f3d89a29c220496c5498ee4ec61a204a97bfa9bd6aef3b"
)

SITES = tuple(range(6))
COLOURS = tuple(range(3))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def matrix_rank(columns):
    if not columns:
        return 0
    rows = [list(row) for row in zip(*columns, strict=True)]
    rank = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(rank, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [value - scale * pivot_value
                         for value, pivot_value
                         in zip(rows[row], rows[rank], strict=True)]
        rank += 1
        if rank == len(rows):
            break
    return rank


def positive_three_dependence(left, middle, right):
    """Return positive coefficients for left,middle,right, or None."""
    first = next(index for index, value in enumerate(left) if value)
    second = next((index for index in range(len(left))
                   if left[first] * middle[index]
                   != left[index] * middle[first]), None)
    if second is None:
        return None
    determinant = (left[first] * middle[second]
                   - left[second] * middle[first])
    left_coefficient = Fraction(
        right[first] * middle[second] - right[second] * middle[first],
        determinant,
    )
    middle_coefficient = Fraction(
        left[first] * right[second] - left[second] * right[first],
        determinant,
    )
    if (left_coefficient >= 0 or middle_coefficient >= 0
            or not all(right[index]
                       == left_coefficient * left[index]
                       + middle_coefficient * middle[index]
                       for index in range(len(left)))):
        return None
    return -left_coefficient, -middle_coefficient, Fraction(1)


def primitive_positive(values):
    denominator = 1
    for value in values:
        denominator = lcm(denominator, value.denominator)
    integers = [int(value * denominator) for value in values]
    common = 0
    for value in integers:
        common = gcd(common, abs(value))
    require(common and all(value > 0 for value in integers),
            f"the dependence is not positive primitive: {values}")
    return tuple(value // common for value in integers)


def ray_scale(raw, primitive):
    return next(Fraction(primitive[index], raw[index])
                for index in range(len(raw)) if raw[index])


def row_sum(torus, cells):
    return tuple(sum(torus.cell_character(cell)[index] for cell in cells)
                 for index in range(torus.WIDTH))


def triple_orbits(all_pairs, torus, triples, group):
    triple_set = frozenset(triples)
    remaining = set(triples)
    orbits = []
    while remaining:
        seed = min(remaining)
        orbit = frozenset(
            tuple(sorted(all_pairs.act_cell(torus, cell, element)
                         for cell in seed))
            for element in group
        ) & triple_set
        require(orbit, f"the triple orbit of {seed} vanished")
        orbits.append(tuple(sorted(orbit)))
        remaining -= orbit
    return tuple(orbits)


def main():
    pin_dependencies()
    torus = importlib.import_module(
        "verify_n8_one_bad_axis_pure_chart_torus_accessibility")
    all_pairs = importlib.import_module(
        "verify_n8_one_bad_axis_pure_all_opposing_pair_elimination")

    basis, _pivots = torus.nullspace(torus.equation_matrix())
    cells = tuple(
        (left, right, left_colour, right_colour)
        for left, right in itertools.combinations(SITES, 2)
        for left_colour, right_colour in itertools.product(COLOURS, repeat=2)
        if left_colour != right_colour
    )
    raw = {cell: torus.quotient_character(cell, basis) for cell in cells}
    primitive = {cell: torus.primitive(raw[cell]) for cell in cells}
    require(len(cells) == 90 and all(any(raw[cell]) for cell in cells),
            "the nonzero mixed-ray universe changed")
    require(matrix_rank(tuple(raw[cell] for cell in cells)) == 11,
            "the mixed quotient-character rank changed")

    pairs = all_pairs.opposing_pairs(torus, basis)
    pair_sets = frozenset(frozenset(pair) for pair in pairs)
    require(len(pairs) == 22, "the degree-two Hilbert circuit count changed")

    triples = []
    ray_coefficients = {}
    raw_coefficients = {}
    anchor_recombinations = {}
    anchor_sums = defaultdict(list)
    for anchors in itertools.combinations(torus.ANCHORS, 3):
        anchor_sums[row_sum(torus, anchors)].append(anchors)

    for triple in itertools.combinations(cells, 3):
        dependence = positive_three_dependence(
            *(primitive[cell] for cell in triple)
        )
        if dependence is None:
            continue
        require(not any(frozenset(pair) <= frozenset(triple)
                        for pair in pairs),
                f"a positive triple contains a degree-two circuit: {triple}")
        primitive_ray_coefficients = primitive_positive(dependence)
        coefficients_on_raw = primitive_positive(tuple(
            dependence[index]
            * ray_scale(raw[cell], primitive[cell])
            for index, cell in enumerate(triple)
        ))
        require(coefficients_on_raw == (1, 1, 1),
                f"a raw triple stopped being an equal-weight circuit: "
                f"{triple}: {coefficients_on_raw}")
        require(all(sum(raw[cell][coordinate] for cell in triple) == 0
                    for coordinate in range(len(basis))),
                f"the raw quotient relation failed: {triple}")

        anchor_matches = anchor_sums[row_sum(torus, triple)]
        require(len(anchor_matches) == 1,
                f"the three-edge anchor recombination is not unique: "
                f"{triple}: {anchor_matches}")
        anchors = anchor_matches[0]
        require(tuple(sorted(cell[2] for cell in anchors)) == (0, 1, 2),
                f"the anchor recombination lost one-per-colour: {anchors}")

        triples.append(triple)
        ray_coefficients[str(triple)] = primitive_ray_coefficients
        raw_coefficients[str(triple)] = coefficients_on_raw
        anchor_recombinations[str(triple)] = anchors

    triples = tuple(triples)
    require(len(triples) == 58,
            f"the degree-three positive circuit count changed: {len(triples)}")
    require(Counter(raw_coefficients.values()) == Counter({(1, 1, 1): 58}),
            "the raw Hilbert coefficient histogram changed")

    anchor_histogram = Counter(anchor_recombinations.values())
    require(len(anchor_histogram) == 12
            and Counter(anchor_histogram.values())
            == Counter({6: 6, 5: 2, 4: 2, 2: 2}),
            f"the anchor recombination census changed: {anchor_histogram}")

    group = all_pairs.chart_stabilizer(torus)
    orbits = triple_orbits(all_pairs, torus, triples, group)
    expected_representatives = (
        ((0, 1, 0, 2), (2, 4, 1, 2), (3, 4, 0, 1)),
        ((0, 1, 0, 2), (3, 4, 1, 2), (3, 5, 0, 1)),
        ((0, 2, 0, 1), (0, 3, 2, 0), (4, 5, 1, 2)),
        ((0, 2, 0, 1), (0, 4, 2, 1), (3, 5, 0, 2)),
        ((0, 2, 0, 1), (1, 4, 2, 1), (3, 4, 0, 2)),
        ((0, 2, 2, 1), (0, 4, 0, 1), (3, 5, 0, 2)),
        ((0, 2, 2, 1), (0, 5, 0, 2), (3, 4, 0, 1)),
        ((0, 2, 2, 1), (4, 5, 0, 2), (4, 5, 1, 0)),
        ((0, 3, 0, 1), (0, 5, 2, 1), (3, 5, 0, 2)),
        ((0, 3, 0, 1), (1, 5, 2, 1), (3, 4, 0, 2)),
        ((0, 3, 2, 1), (0, 5, 0, 1), (3, 5, 0, 2)),
        ((0, 3, 2, 1), (0, 5, 0, 2), (3, 5, 0, 1)),
        ((0, 3, 2, 1), (1, 5, 0, 1), (2, 5, 0, 2)),
        ((0, 3, 2, 1), (1, 5, 0, 2), (2, 5, 0, 1)),
        ((0, 4, 2, 0), (2, 5, 1, 0), (4, 5, 1, 2)),
        ((0, 4, 2, 0), (2, 5, 1, 2), (4, 5, 1, 0)),
        ((0, 5, 2, 0), (2, 4, 1, 0), (4, 5, 1, 2)),
        ((0, 5, 2, 0), (3, 5, 1, 2), (4, 5, 0, 1)),
    )
    require(len(group) == 4 and len(orbits) == 18
            and Counter(map(len, orbits)) == Counter({4: 11, 2: 7})
            and tuple(orbit[0] for orbit in orbits)
            == expected_representatives,
            "the degree-three chart-stabilizer orbit census changed")

    first = triples[0]
    first_anchors = anchor_recombinations[str(first)]
    require(first == expected_representatives[0]
            and first_anchors == (
                (0, 3, 0, 0), (2, 4, 1, 1), (1, 4, 2, 2)
            )
            and row_sum(torus, first) == row_sum(torus, first_anchors),
            "the canonical higher circuit changed")

    # An equal-coefficient pair-free positive circuit is support-minimal.
    # Any decomposition in the nonnegative integer kernel would be supported
    # on a proper nonempty subset; sizes one and two have just been excluded.
    # Therefore its incidence vector is an indecomposable Hilbert element.
    ledger = {
        "dependencies": PINS,
        "mixed_weight_configuration": {
            "columns": len(cells),
            "quotient_coordinates": len(basis),
            "rank": 11,
            "zero_columns": 0,
        },
        "positive_circuits": {
            "degree2_opposing_pairs": len(pairs),
            "degree3_pair_free": len(triples),
            "degree3_raw_coefficient_histogram": {"1,1,1": len(triples)},
            "degree3_chart_stabilizer_orbits": len(orbits),
            "degree3_orbit_size_histogram": {
                str(size): count
                for size, count in sorted(Counter(map(len, orbits)).items())
            },
            "degree3_orbit_representatives": expected_representatives,
        },
        "anchor_recombination": {
            "distinct_anchor_triples": len(anchor_histogram),
            "circuits_per_anchor_triple_histogram": {
                str(count): frequency
                for count, frequency
                in sorted(Counter(anchor_histogram.values()).items())
            },
            "every_circuit_has_unique_anchor_triple": True,
            "every_anchor_triple_has_one_anchor_per_colour": True,
        },
        "smallest_higher_hilbert_element": {
            "mixed_cells": first,
            "anchor_cells": first_anchors,
            "raw_coefficients": (1, 1, 1),
            "character_identity": (
                "chi(01:02)+chi(24:12)+chi(34:01)="
                "chi(03:00)+chi(24:11)+chi(14:22)"
            ),
            "relative_weight_identity": "ell1+ell2+ell3=0",
            "pair_free": True,
            "hilbert_indecomposable": True,
        },
        "verdict": (
            "the 22 opposing pairs do not generate all nonseparable mixed "
            "leading supports: 58 primitive pair-free degree-three Hilbert "
            "circuits are the smallest higher obstructions"
        ),
        "scope": (
            "exact oriented-matroid and nonnegative integer-kernel structure "
            "through degree three; no coefficient source packets are "
            "enumerated, and Hilbert elements of degree four or higher are "
            "not classified"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the mixed Hilbert-circuit ledger changed: {digest}")

    print("N=8 axis-pure mixed weight Hilbert circuits: PASS")
    print("mixed rays/rank: 90/11; zero rays: 0")
    print("positive circuits: degree2=22, pair-free degree3=58")
    print("degree3 Hilbert elements: 18 chart-stabilizer orbits")
    print("smallest higher circuit has raw coefficients 1,1,1")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
