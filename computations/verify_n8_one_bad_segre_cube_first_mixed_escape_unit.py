#!/usr/bin/env python3
"""Exclude the first 11/22 carrier escape from the Segre--K4 chart.

Start with the fixed weighted fourteen-cell top-null quadratic H from
commit 772290e, add arbitrary pure-0 cells d on all fifteen physical edges,
and add exactly two disjoint 11 cells and two disjoint 22 cells.  There are
45 two-edge matchings for each colour and the decorated weighted stabilizer
of H is trivial, so this checker audits all 45^2=2025 labelled charts.

In every chart and for each colour c=1,2, a mixed top coefficient is a
single nonzero monomial P_c dividing the product A_c of the two cc carrier
coefficients.  On the other hand the pure diagonal response coefficient is

    A_c * L_c - 1,

where L_c is the exact two-hole endpoint-star pairing.  If g_c=eps*P_c is
the mixed top row, then

    (A_c L_c - 1) - (A_c/P_c) L_c g_c/eps = -1.

This is an ordinary integral unit certificate.  Hence the first forced
mixed escape is impossible before the unary or crossed response rows are
used.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = (
    "computations/verify_n8_one_bad_segre_cube_k4_closure_counterguard.py"
)
DEPENDENCY_SHA256 = (
    "44e2ca27001ef82ed77f73d5c956963b13507f98b4c9a1fd7b6f71b6434e700b"
)
EXPECTED_DIGEST = "cbccd90941108385bcf5a0f9d6035ea7533284fa73874165c097544fbba9a871"
SITES = tuple(range(6))
EDGES = tuple(itertools.combinations(SITES, 2))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_dependency():
    path = ROOT / DEPENDENCY
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            f"dependency changed: {DEPENDENCY}: {actual}")
    spec = spec_from_file_location("segre_k4", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def carrier_pairs():
    result = []
    for holes in EDGES:
        residual = set(SITES) - set(holes)
        for matching in perfect_matchings(residual):
            result.append((holes, tuple(sorted(matching))))
    require(len(result) == 45,
            "the two-disjoint-cell carrier census changed")
    return tuple(result)


def pinned_H(module):
    base_support, base_weights, _rows, exported = module.audit_plucker_square()
    cross = {
        ((2, 5), (0, 1)): Fraction(1),
        ((2, 5), (2, 0)): Fraction(-1),
        ((3, 4), (0, 2)): Fraction(1),
        ((3, 4), (1, 0)): Fraction(-1),
    }
    completion = module.audit_cross_completion(
        base_support, base_weights, exported
    )
    require(completion["full_top_tensor"] == 0,
            "the pinned H quadratic stopped being top-null")
    support = frozenset(set(base_support) | set(cross))
    weights = dict(base_weights)
    weights.update(cross)
    require(len(support) == 14 and set(weights) == set(support),
            "the pinned weighted H support changed")
    return support, weights


def transform_cell(cell, permutation):
    (left, right), (left_colour, right_colour) = cell
    image_left, image_right = permutation[left], permutation[right]
    if image_left < image_right:
        return ((image_left, image_right), (left_colour, right_colour))
    return ((image_right, image_left), (right_colour, left_colour))


def weighted_stabilizer(support, weights):
    stabilizer = []
    for permutation in itertools.permutations(SITES):
        transformed = {transform_cell(cell, permutation) for cell in support}
        if transformed != set(support):
            continue
        if all(weights[transform_cell(cell, permutation)] == value
               for cell, value in weights.items()):
            stabilizer.append(permutation)
    require(stabilizer == [SITES],
            f"the weighted H stabilizer changed: {stabilizer}")
    return stabilizer


def polynomial_add(*values):
    answer = Counter()
    for value in values:
        answer.update(value)
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def polynomial_scale(value, scalar):
    scalar = Fraction(scalar)
    return {monomial: scalar * coefficient
            for monomial, coefficient in value.items()
            if scalar * coefficient}


def polynomial_mul(left, right):
    answer = Counter()
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            answer[monomial] += left_coefficient * right_coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def chart_top_rows(module, H_support, H_weights, carrier_1, carrier_2):
    support = set(H_support)
    cell_data = {cell: ((), Fraction(value))
                 for cell, value in H_weights.items()}
    for index, edge in enumerate(EDGES):
        cell = (edge, (0, 0))
        support.add(cell)
        cell_data[cell] = ((f"d{index}",), Fraction(1))
    for colour, matching, names in (
        (1, carrier_1, ("a", "b")),
        (2, carrier_2, ("c", "e")),
    ):
        for edge, name in zip(matching, names, strict=True):
            cell = (edge, (colour, colour))
            support.add(cell)
            cell_data[cell] = ((name,), Fraction(1))

    rows = {}
    for word in itertools.product(range(3), repeat=6):
        polynomial = Counter()
        for matching in module.MATCHINGS:
            cells = tuple((edge, (word[edge[0]], word[edge[1]]))
                          for edge in matching)
            if not all(cell in support for cell in cells):
                continue
            monomial = tuple(sorted(
                name for cell in cells for name in cell_data[cell][0]
            ))
            coefficient = Fraction(1)
            for cell in cells:
                coefficient *= cell_data[cell][1]
            polynomial[monomial] += coefficient
        polynomial = {monomial: coefficient
                      for monomial, coefficient in polynomial.items()
                      if coefficient}
        if polynomial:
            rows[word] = polynomial
    return rows


def choose_unit_witness(rows, carrier_names):
    allowed = {
        (carrier_names[0],),
        (carrier_names[1],),
        tuple(sorted(carrier_names)),
    }
    candidates = []
    for word, polynomial in rows.items():
        if len(set(word)) == 1 or len(polynomial) != 1:
            continue
        monomial, coefficient = next(iter(polynomial.items()))
        if monomial in allowed:
            candidates.append((len(monomial), word, monomial, coefficient))
    require(candidates,
            f"no literal top unit witness for carriers {carrier_names}")
    return min(candidates)


def verify_unit_identity(carrier_names, L_name, witness):
    _degree, _word, top_monomial, top_coefficient = witness
    full_carrier = tuple(sorted(carrier_names))
    complement = list(full_carrier)
    for name in top_monomial:
        complement.remove(name)
    response = {
        tuple(sorted(full_carrier + (L_name,))): Fraction(1),
        (): Fraction(-1),
    }
    top_row = {top_monomial: top_coefficient}
    multiplier = {
        tuple(sorted(tuple(complement) + (L_name,))):
            Fraction(1, 1) / top_coefficient
    }
    remainder = polynomial_add(
        response,
        polynomial_scale(polynomial_mul(multiplier, top_row), -1),
    )
    require(remainder == {(): Fraction(-1)},
            "the response/top ordinary unit identity changed")
    return {
        "mixed_top_word": "".join(map(str, witness[1])),
        "top_monomial": "*".join(top_monomial),
        "top_coefficient": str(top_coefficient),
        "diagonal_response": (
            "*".join(full_carrier) + f"*{L_name}-1"
        ),
        "unit_remainder": "-1",
    }


def audit_all_charts(module):
    H_support, H_weights = pinned_H(module)
    stabilizer = weighted_stabilizer(H_support, H_weights)
    pairs = carrier_pairs()
    degree_histogram = Counter()
    witness_rows = []

    for holes_1, carrier_1 in pairs:
        for holes_2, carrier_2 in pairs:
            rows = chart_top_rows(
                module, H_support, H_weights, carrier_1, carrier_2
            )
            witness_1 = choose_unit_witness(rows, ("a", "b"))
            witness_2 = choose_unit_witness(rows, ("c", "e"))
            certificate_1 = verify_unit_identity(
                ("a", "b"), "L1", witness_1
            )
            certificate_2 = verify_unit_identity(
                ("c", "e"), "L2", witness_2
            )
            degree_histogram[(witness_1[0], witness_2[0])] += 1
            witness_rows.append({
                "holes_1": list(holes_1),
                "carrier_1": [list(edge) for edge in carrier_1],
                "holes_2": list(holes_2),
                "carrier_2": [list(edge) for edge in carrier_2],
                "colour_1": certificate_1,
                "colour_2": certificate_2,
            })

    require(len(witness_rows) == 2025,
            "the paired first-escape chart count changed")
    require(degree_histogram == Counter({
        (1, 1): 1089,
        (1, 2): 396,
        (2, 1): 396,
        (2, 2): 144,
    }), f"the unit-witness degree histogram changed: {degree_histogram}")
    witness_digest = sha256(json.dumps(
        witness_rows, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()

    return {
        "weighted_H_site_stabilizer_order": len(stabilizer),
        "carrier_placements_per_colour": len(pairs),
        "paired_labelled_charts": len(witness_rows),
        "unit_witness_degree_histogram": {
            f"{left},{right}": count
            for (left, right), count in sorted(degree_histogram.items())
        },
        "all_charts_have_colour_1_unit": True,
        "all_charts_have_colour_2_unit": True,
        "witness_table_sha256": witness_digest,
        "verdict": (
            "every first 11/22 carrier chart has an ordinary unit generated "
            "by a literal mixed top coefficient and either diagonal response"
        ),
    }


def main():
    module = load_dependency()
    ledger = {
        "dependency": {"path": DEPENDENCY, "sha256": DEPENDENCY_SHA256},
        "first_mixed_escape": audit_all_charts(module),
        "scope": (
            "fixed weighted fourteen-cell H, arbitrary fifteen pure-0 "
            "coefficients, and exactly two disjoint 11 plus two disjoint 22 "
            "cells; no claim after further nonzero-colour q-cells are added"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"first-mixed-escape ledger changed: {digest}")
    print("N=8 Segre-K4 first mixed escape: PASS")
    print("carrier charts: 45 x 45 = 2025; weighted stabilizer: trivial")
    print("ordinary top/diagonal-response unit: every chart, both colours")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
