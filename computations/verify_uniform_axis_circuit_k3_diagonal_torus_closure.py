#!/usr/bin/env python3
"""Close the coefficient torus of the primitive diagonal k=3 transfer.

The seven internal 11-cells and three occupied p-star components of the
common-q transfer form a non-bipartite incidence graph with ten edges and
eight vertices.  Its multiplicative quotient has rank two.  The two
characters are exactly the Y- and Z-response cancellation ratios, both -1.
Thus every nonzero coefficient realization of the same source support and
aggregate X1 response is coordinate-torus equivalent to the normalized
family used by efac2b2.

The second audit extends efac2b2 by every decorated cell having at least one
endpoint colour 2 (five ordered types on all 28 physical edges).  Its 22-row
integral unit survives literally because every certified source word is
binary 0/1.  Hence neither an arbitrary pure-00 unary slice nor any
colour-2 companion can attach to this k=3 transfer.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
import json
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNIT_PATH = (
    "computations/verify_uniform_axis_circuit_k3_pure_unary_attachment_unit.py"
)
PINS = {
    UNIT_PATH:
        "432b19fa7ad03a57caa64fc90243443406bc3d37bd51db3a32fe477e38394636",
    "notes/uniform-axis-circuit-k3-pure-unary-attachment-unit.md":
        "0668a5186e209a05388b73391583cb3229e1792679bba19ade69eca44b3b6a7c",
    "computations/verify_uniform_axis_circuit_k3_common_q_transfer_guard.py":
        "fe8dc76d8f42dd7ae35ea19934ee12da2c114bfd7d9a7590d33cf821bd0b8065",
    "notes/uniform-axis-circuit-k3-common-q-transfer-guard.md":
        "62f879a04a2d0830a3a870d8ff578b91f62eafe8d9a0248291b9c9d89a6bd7be",
}
EXPECTED_LEDGER_SHA256 = (
    "946a373cdaf91d0bff2816cc96efada5ba6258b1f0acfa2d8b5c46a0a206ef2f"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def load_unit():
    path = ROOT / UNIT_PATH
    spec = spec_from_file_location("k3_pure_unary_unit", path)
    require(spec is not None and spec.loader is not None,
            f"cannot load {UNIT_PATH}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VERTICES = ("P", 0, 1, 2, 3, 4, 5, 6)
EDGES = (
    ("p0", "P", 0),
    ("p1", "P", 1),
    ("p2", "P", 2),
    ("a12", 1, 2),
    ("b02", 0, 2),
    ("c56", 5, 6),
    ("d25", 2, 5),
    ("e36", 3, 6),
    ("f13", 1, 3),
    ("g14", 1, 4),
)

# Two primitive multiplicative characters.  A character is an exponent
# vector on EDGES and lies in the left kernel of the unsigned incidence
# matrix precisely when it is invariant under vertex-coordinate scaling.
CHARACTERS = (
    (-1, 1, 0, -1, 1, 0, 0, 0, 0, 0),
    (0, -1, 1, 0, 0, 1, -1, -1, 1, 0),
)


def incidence_matrix():
    matrix = []
    for _, left, right in EDGES:
        matrix.append(tuple(
            int(vertex == left) + int(vertex == right)
            for vertex in VERTICES
        ))
    return tuple(matrix)


def rank(matrix):
    work = [[Q(entry) for entry in row] for row in matrix]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [entry - value * pivot_entry
                         for entry, pivot_entry
                         in zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def determinant(matrix):
    work = [[int(entry) for entry in row] for row in matrix]
    size = len(work)
    require(all(len(row) == size for row in work), "determinant is not square")
    sign = 1
    previous = 1
    for column in range(size - 1):
        pivot = next((row for row in range(column, size)
                      if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        for row in range(column + 1, size):
            for other in range(column + 1, size):
                numerator = (work[row][other] * pivot_value
                             - work[row][column] * work[column][other])
                require(numerator % previous == 0,
                        "Bareiss division stopped being exact")
                work[row][other] = numerator // previous
        previous = pivot_value
    return sign * work[-1][-1]


def audit_torus_characters():
    matrix = incidence_matrix()
    matrix_rank = rank(matrix)
    require(matrix_rank == len(VERTICES),
            "the carrier incidence torus lost full vertex rank")
    require(len(EDGES) - matrix_rank == 2,
            "the carrier torus quotient stopped being two-dimensional")

    for character in CHARACTERS:
        require(all(sum(character[row] * matrix[row][column]
                        for row in range(len(EDGES))) == 0
                    for column in range(len(VERTICES))),
                "a displayed response character left the incidence kernel")
    require(rank(CHARACTERS) == 2,
            "the two response characters became dependent")

    # The gcd of the maximal minors is the torsion order of the incidence
    # cokernel.  It is 2 because the graph is connected and non-bipartite.
    # Over C this finite square-root ambiguity is harmless: the power map is
    # surjective, so the two character values classify torus orbits.
    maximal_minors = []
    for rows in combinations(range(len(EDGES)), len(VERTICES)):
        minor = [[matrix[row][column] for column in range(len(VERTICES))]
                 for row in rows]
        value = abs(determinant(minor))
        if value:
            maximal_minors.append(value)
    require(maximal_minors, "all maximal incidence minors vanished")
    torsion = 0
    for value in maximal_minors:
        torsion = gcd(torsion, value)
    require(torsion == 2,
            f"the non-bipartite incidence torsion changed: {torsion}")

    canonical = {
        "p0": Q(1), "p1": Q(1), "p2": Q(1),
        "a12": Q(1), "b02": Q(-1), "c56": Q(1),
        "d25": Q(1), "e36": Q(1), "f13": Q(-1),
        "g14": Q(1),
    }

    def character_value(character, weights):
        numerator = Q(1)
        denominator = Q(1)
        for exponent, (name, _, _) in zip(character, EDGES, strict=True):
            if exponent > 0:
                numerator *= weights[name] ** exponent
            elif exponent < 0:
                denominator *= weights[name] ** (-exponent)
        return numerator / denominator

    values = tuple(character_value(character, canonical)
                   for character in CHARACTERS)
    require(values == (Q(-1), Q(-1)),
            "the normalized response cancellation characters changed")

    # The two values are exactly the ratios forced by the literal Y and Z
    # coefficient equations:
    #   p0*a12 + p1*b02 = 0,
    #   p1*d25*e36 + p2*f13*c56 = 0.
    samples = (
        {
            "p0": Q(2), "p1": Q(3), "p2": Q(5),
            "a12": Q(7), "b02": Q(-14, 3), "c56": Q(11),
            "d25": Q(13), "e36": Q(17),
            "f13": Q(-3 * 13 * 17, 5 * 11), "g14": Q(19),
        },
        {
            "p0": Q(-2), "p1": Q(5), "p2": Q(-7),
            "a12": Q(3), "b02": Q(6, 5), "c56": Q(-11),
            "d25": Q(2), "e36": Q(-13),
            "f13": Q(-5 * 2 * -13, -7 * -11), "g14": Q(17),
        },
    )
    for weights in samples:
        require(weights["p0"] * weights["a12"]
                + weights["p1"] * weights["b02"] == 0,
                "sample left the Y cancellation locus")
        require(weights["p1"] * weights["d25"] * weights["e36"]
                + weights["p2"] * weights["f13"] * weights["c56"] == 0,
                "sample left the Z cancellation locus")
        require(tuple(character_value(character, weights)
                      for character in CHARACTERS) == (Q(-1), Q(-1)),
                "response cancellation stopped fixing the torus orbit")

    return {
        "vertices": len(VERTICES),
        "occupied_coefficient_edges": len(EDGES),
        "incidence_rank": matrix_rank,
        "torus_quotient_rank": len(EDGES) - matrix_rank,
        "primitive_character_values": [str(value) for value in values],
        "maximal_minor_gcd": torsion,
        "algebraically_closed_torsion_effect": "none (square roots exist)",
        "response_equations": [
            "p0*a12+p1*b02=0",
            "p1*d25*e36+p2*f13*c56=0",
        ],
    }


def audit_arbitrary_colour_two_cells(unit):
    original_q_data = unit.q_data

    def extended_q_data():
        q = original_q_data()
        for edge in unit.EDGES:
            for left_colour, right_colour in (
                    (0, 2), (1, 2), (2, 0), (2, 1), (2, 2)):
                q[(edge[0], edge[1], left_colour, right_colour)] = (
                    unit.variable(
                        f"y{edge[0]}{edge[1]}_{left_colour}{right_colour}"
                    )
                )
        return q

    unit.q_data = extended_q_data
    try:
        generators = unit.build_source_generators()
    finally:
        unit.q_data = original_q_data

    total = Counter()
    for label, multiplier_text in unit.CERTIFICATE.items():
        require(label in generators,
                f"a certified binary source row disappeared: {label}")
        total = unit.add(total, unit.multiply(
            unit.parse_polynomial(multiplier_text), generators[label]
        ))
    require(total == unit.constant(1),
            "the unary source unit acquired a colour-2 defect")

    certified_words = [label[1] for label in unit.CERTIFICATE]
    require(all(set(word) <= {0, 1} for word in certified_words),
            "a certified source word unexpectedly used colour 2")
    return {
        "arbitrary_zero_slice_variables": len(unit.EDGES),
        "arbitrary_cells_with_endpoint_colour_two": 5 * len(unit.EDGES),
        "ordered_colour_types": ["02", "12", "20", "21", "22"],
        "fixed_one_slice_cells": len(unit.ONE_SLICE),
        "certificate_rows": len(unit.CERTIFICATE),
        "certificate_word_alphabet": [0, 1],
        "expanded_value": 1,
        "colour_two_defect_terms": 0,
        "uses_second_response_rows": False,
    }


def main():
    pin_dependencies()
    unit = load_unit()
    ledger = {
        "coefficient_torus": audit_torus_characters(),
        "arbitrary_colour_two_companion":
            audit_arbitrary_colour_two_cells(unit),
        "theorem": (
            "every nonzero coefficient realization of the primitive k3 "
            "diagonal transfer support satisfying its two mixed response "
            "cancellations is coordinate-torus equivalent over C to the "
            "normalized efac2b2 chart; arbitrary 00 cells and all cells "
            "having an endpoint colour 2 still give the same literal unit"
        ),
        "consequence": (
            "the nonzero primitive k3 diagonal lock cannot occur in a full "
            "one-bad packet; its normalized t=0 fibre is also in the unit, "
            "while a minimum-support k2 landing is consumed by the separate "
            "committed k2 closure"
        ),
        "remaining_boundary": (
            "a surviving diagonal lock must change the occupied 11 carrier "
            "topology/support (or leave its nonzero torus), or use an "
            "off-diagonal decoration on a selected anchor edge; arbitrary "
            "larger lock webs are not reduced to this primitive chart"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                f"ledger digest changed: {digest}")
    print(payload)
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
