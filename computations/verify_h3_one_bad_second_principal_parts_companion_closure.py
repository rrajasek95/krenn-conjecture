#!/usr/bin/env python3
"""Exact smallest h=3 common-q principal-parts/companion closure.

The partial common-q guard of f7c15e8 can be completed by the selected
``(t,t)`` target row and the ``(c,a)`` mixed common-hole row.  Their five
localized scalar equations have a unimodular tangent block, but the
off-one-edge self-square still has the primitive residue ``S-O``.

The residue is not a new formal face: it is the literal mixed output word
21000121 in the diagonal companion chart.  Adding that already mandatory
coefficient kills the cokernel integrally and concentrates the only
multisite endpoint star in this literal packet.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib
import json
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_one_bad_common_q_cap_extraction_boundary.py":
        "02517a037d7dfc273d2eee63dd85e8228d88cd4824397b7ac478c013624afe5e",
}
EXPECTED_LEDGER_SHA256 = (
    "87e9978e92d561380eca2e0dc50ecc70d1d21ae6daebb52a71d545b8239440e5"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def determinant(matrix):
    matrix = [[Fraction(entry) for entry in row] for row in matrix]
    result = Fraction(1)
    for column in range(len(matrix)):
        pivot = next((row for row in range(column, len(matrix))
                      if matrix[row][column]), None)
        require(pivot is not None, "singular determinant block")
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            result *= -1
        value = matrix[column][column]
        result *= value
        matrix[column] = [entry / value for entry in matrix[column]]
        for row in range(column + 1, len(matrix)):
            factor = matrix[row][column]
            if factor:
                matrix[row] = [left - factor * right
                               for left, right in zip(
                                   matrix[row], matrix[column], strict=True)]
    return result


def dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def build_common_q(base, t=Fraction(1)):
    cell = base.cell
    return Counter({
        cell(1, 3, 1, 1): Fraction(1),  # A
        cell(2, 4, 1, 1): Fraction(1),  # B
        cell(1, 2, 1, 0): t,            # C
        cell(0, 2, 1, 0): Fraction(-1), # E
        cell(3, 4, 0, 0): Fraction(1),  # D
        cell(0, 1, 0, 0): Fraction(1),  # F
        cell(2, 3, 2, 2): Fraction(1),  # G
    })


def build_eight_site_source(base, t=Fraction(1)):
    cell = base.cell
    source = build_common_q(base, t)
    source.update({
        cell(5, 6, 0, 0): Fraction(1),  # pq direct anchor
        cell(5, 7, 1, 1): Fraction(1),  # pr diagonal companion anchor
        cell(6, 7, 1, 0): Fraction(1),  # D_ca
        cell(1, 5, 2, 2): Fraction(1),  # P_t
        cell(0, 6, 1, 1): Fraction(1),  # Q_c first summand
        cell(1, 6, 1, 1): t,            # Q_c second summand
        cell(0, 6, 2, 2): Fraction(1),  # Q_t
        cell(2, 7, 0, 0): Fraction(1),  # R_a
        cell(4, 7, 2, 2): Fraction(1),  # R_t
    })
    return source


def main():
    pin_dependencies()
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")

    one = Fraction(1)
    q = build_common_q(base)
    Q_c = ((0, 1, one), (1, 1, one))
    R_a = ((2, 0, one),)
    P_t = ((1, 2, one),)
    Q_t = ((0, 2, one),)
    R_t = ((4, 2, one),)

    X_a, X_c, X_t = (0,) * 5, (1,) * 5, (2,) * 5
    require(base.odd_star_response(q, Q_c) == Counter({X_c: one}),
            "the c-diagonal target row changed")
    require(base.odd_star_response(q, R_a) == Counter({X_a: one}),
            "the a-diagonal target row changed")
    ca_chord = base.odd_star_response(q, P_t)
    ca_cubic = base.triple_star_response(q, P_t, Q_c, R_a)
    require(ca_chord == Counter({(1, 2, 0, 0, 0): -one})
            and ca_cubic == Counter({(1, 2, 0, 0, 0): one}),
            "the ca mixed common-hole cancellation changed")
    require(base.triple_star_response(q, P_t, Q_t, R_t)
            == Counter({X_t: one}), "the tt target row changed")

    # Scalar equations, at the displayed point, in variables
    # A,B,C,E,D,F,G,Q0,Q1,Ra,Pt,Qt,Rt,Dca,Dtt.
    # g1=Q0AB-1; g2=Q0C+Q1E; g3=RaFD-1;
    # g4=DcaE+Q0Ra; g5=PtQtRtG-1.
    jacobian = [
        [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, -1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0],
    ]
    names = ("A", "B", "C", "E", "D", "F", "G", "Q0", "Q1",
             "Ra", "Pt", "Qt", "Rt", "Dca", "Dtt")
    pivot_names = ("B", "E", "F", "Dca", "G")
    pivot_indices = tuple(names.index(name) for name in pivot_names)
    pivot_block = [[row[index] for index in pivot_indices]
                   for row in jacobian]
    pivot_det = determinant(pivot_block)
    require(abs(pivot_det) == 1, f"the tangent block is not unimodular: {pivot_det}")
    require(not set(pivot_names) & {"Q0", "Q1", "C"},
            "the correction block changes a residue readout")

    # S=Q0*Q1 and O=C.  The exact equation g2 gives
    # E*S+Q0^2*O=Q0*g2, hence S=O at the displayed point.
    available = (Fraction(1), Fraction(1))
    desired = (Fraction(1), Fraction(0))
    companion = (Fraction(0), Fraction(1))
    primitive = (Fraction(1), Fraction(-1))
    require(dot(primitive, available) == 0
            and dot(primitive, desired) == 1,
            "the primitive S-O cokernel changed")
    require(abs(determinant([available, companion])) == 1,
            "the companion face no longer kills the cokernel integrally")
    require(gcd(*(abs(int(value)) for value in primitive)) == 1,
            "the cokernel covector stopped being primitive")

    # The missing residue is an actual physical mixed coefficient.  In the
    # sparse source it has one matching and is exactly C=t.
    companion_word = tuple(map(int, "21000121"))
    matching_label = "06:22|12:10|34:00|57:11"
    for t in (Fraction(0), Fraction(1), Fraction(2)):
        source = build_eight_site_source(base, t)
        tensor = base.hafnian_tensor(source, tuple(range(8)))
        require(tensor[companion_word] == t,
                f"the physical companion coefficient changed at t={t}")

        q_t = build_common_q(base, t)
        Q_c_t = ((0, 1, one), (1, 1, t))
        require(base.odd_star_response(q_t, Q_c_t)
                == Counter({X_c: one}),
                f"the response-preserving degeneration failed at t={t}")
        require(base.odd_star_response(q_t, R_a)
                == Counter({X_a: one}),
                f"the a target moved at t={t}")
        require(base.odd_star_response(q_t, P_t)
                + base.triple_star_response(q_t, P_t, Q_c_t, R_a)
                == Counter(), f"the ca row moved at t={t}")
        require(base.triple_star_response(q_t, P_t, Q_t, R_t)
                == Counter({X_t: one}), f"the tt row moved at t={t}")

    concentrated_q = build_common_q(base, Fraction(0))
    concentrated_Qc = ((0, 1, one),)
    four_squares = {
        "Q_c": base.divided_square_of_star(concentrated_Qc),
        "Q_t": base.divided_square_of_star(Q_t),
        "R_a": base.divided_square_of_star(R_a),
        "R_t": base.divided_square_of_star(R_t),
    }
    require(all(not square for square in four_squares.values()),
            f"a concentrated endpoint square survived: {four_squares}")
    require(base.odd_star_response(concentrated_q, concentrated_Qc)
            == Counter({X_c: one}), "concentration lost the c target")

    ledger = {
        "dependencies": PINS,
        "scalar_module": {
            "variables": names,
            "equations": (
                "Q0*A*B-1", "Q0*C+Q1*E", "Ra*F*D-1",
                "Dca*E+Q0*Ra", "Pt*Qt*Rt*G-1",
            ),
            "pivot_columns": pivot_names,
            "pivot_determinant": str(pivot_det),
            "readouts": ("S=Q0*Q1", "O=C"),
            "primitive_cokernel": "lambda(S,O)=S-O",
            "tt_changes_cokernel": False,
        },
        "companion": {
            "output_word": "21000121",
            "outer_label": "(c,t,c)=(1,2,1)",
            "matching": matching_label,
            "coefficient_on_family": "C=t",
            "physical_status": (
                "mandatory mixed coefficient in the pr-diagonal companion sector"
            ),
            "module_column": (0, 1),
            "augmented_determinant": "1",
        },
        "closure": {
            "C": 0,
            "Q1": 0,
            "all_four_endpoint_divided_squares": 0,
            "ca_row": 0,
            "tt_target": "X_t",
        },
        "verdict": (
            "the tt and ca rows alone leave the primitive S-O cokernel; "
            "the already mandatory (c,t,c) companion coefficient supplies "
            "the O face and kills it unimodularly in the literal packet"
        ),
        "scope": (
            "exact smallest localized h=3 literal packet; the t=1 partial "
            "point violates the companion row and is not a full source. "
            "For arbitrary source support, cancellation mates in that same "
            "mixed word must still be classified before this becomes a "
            "uniform one-bad extraction theorem"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the companion closure ledger changed: {digest}")

    print("h=3 one-bad second-principal-parts companion closure: PASS")
    print(f"minimal Jacobian: 5x15; pivot minor {pivot_names} det={pivot_det}")
    print("tt+ca cokernel: Z generated by lambda(S,O)=S-O")
    print(f"mandatory companion: {''.join(map(str, companion_word))} = C")
    print("augmented (S,O) determinant: 1; all four endpoint squares: zero")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
