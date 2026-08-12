#!/usr/bin/env python3
"""Target-normalized transfer gate for the physical cyclic comparison A.

After Laurent normalization, let C_i be the five formal comparison vertices
and let x be the physical target-normalized unary lift.  Their coarse rows are

    C_i : (lower,ainc,W,tgt,ores)=(1,0,0,0,0),
    x   : (lower,ainc,W,tgt,ores)=(1,-1,0,0,0).

Thus g_i=C_i-x has the primitive relative signature with the opposite anchor
sign.  The source-valid adjacent squares give only g_i-g_(i+1).  Their C5
incidence lattice has rank four, and the degree-five top is only the relation
sum_i(g_i-g_(i+1))=0.  It does not construct a base g_i.

The cyclic package and the 0373033 kernel witness are

    A=sum_i C_i,       Z=A-5*x=sum_i g_i.

Modulo the adjacent edges, Z=5*g_0.  Hence, over characteristic zero,
constructing physical A from x is equivalent to constructing one physical
base comparison g_i; the adjacent transfer squares do not do so.

Before even granting clean adjacent edges, the literal PP squares carry the
known reduced pure-Eq defects.  The target-normalized x is killed by the
pure-Eq+anchor separator, so it cannot cancel one defect.  The five defects
do cancel in the degree-five Tate-weighted sum, but that sum is the existing
top relation and still has zero comparison aggregate.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "24bf520cc498f7be06fb001a1187928781e05f05bed3ffbd3729f8cbcc50e3e6"
PINS = {
    "computations/verify_h3_rootless_abcde_target_normalization_generator_dichotomy.py":
        "7abab46d3ae648dd309c2fec3266e70dec5b95c5fd150fea2c8c6035840e9bd3",
    "computations/verify_h3_rootless_endpoint_to_collision_chain_map_boundary.py":
        "be39a61df8e3723983eea7a20d405fba7ff0f3822bc90e8d48b8039177f69cfc",
    "computations/verify_h3_rootless_clean_c5_omega_r_positive_generator_boundary.py":
        "47183bf5c06c0cf0d7c6c73d82776cddca47375ea02d1f6e8a9942d8540a1320",
    "computations/verify_h3_rootless_zero_anchor_collision_edge_source_obstruction.py":
        "8249604a56f7fc8ee8a3c66a33cb905eed6a02202c43ed81283e91c61d748180",
    "computations/verify_h3_rootless_eta_character_source_interface.py":
        "2357e1a4e1c22c4496d99be12b8bf49deea3838337743ea849da29757508517c",
}

FACES = (1, 3, 5, 2, 4)
AUG_ROWS = ("lower_abcde", "ainc", "W", "target", "ores")


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def add(*columns):
    return tuple(sum(column[row] for column in columns)
                 for row in range(len(columns[0])))


def scale(coefficient, column):
    coefficient = Q(coefficient)
    return tuple(coefficient * Q(value) for value in column)


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value
                           for value in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [left - factor * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def multiply(left, right):
    answer = Counter()
    for left_word, left_value in left.items():
        for right_word, right_value in right.items():
            word = tuple(a + b for a, b in
                         zip(left_word, right_word, strict=True))
            answer[word] += left_value * right_value
    return Counter({term: value for term, value in answer.items() if value})


def subtract(left, right):
    answer = Counter(left)
    answer.subtract(right)
    return Counter({term: value for term, value in answer.items() if value})


def monomial(index):
    word = [0] * 5
    word[index] = 1
    return Counter({tuple(word): 1})


def physical_edge_defect_audit():
    # Variables (a,b,c,d,e).  Literal physical adjacent squares have pure-Eq
    # defects a-b,c-d,e-a,b-c,d-e.  Their Tate complements are
    # ce,be,bd,ad,ac and the weighted sum vanishes term by term.
    variables = [monomial(index) for index in range(5)]
    a, b, c, d, e = variables
    defects = (
        subtract(a, b), subtract(c, d), subtract(e, a),
        subtract(b, c), subtract(d, e),
    )
    weights = (
        multiply(c, e), multiply(b, e), multiply(b, d),
        multiply(a, d), multiply(a, c),
    )
    weighted = Counter()
    for weight, defect in zip(weights, defects, strict=True):
        weighted.update(multiply(weight, defect))
    weighted = Counter({term: value for term, value in weighted.items()
                        if value})
    require(not weighted, "Tate-weighted pure-Eq defects stopped cancelling")

    # In (pure_Eq,ainc,W,tgt,ores), x is target-normalized but is killed by
    # pure_Eq+ainc.  Therefore no multiple of x cancels a nonzero reduced
    # pure-Eq face while retaining zero anchor incidence.
    x = (Q(1), Q(-1), Q(0), Q(0), Q(0))
    reduced_eq = (Q(-1), Q(0), Q(0), Q(0), Q(0))
    separator = (Q(1), Q(1), Q(0), Q(0), Q(0))
    require(dot(separator, x) == 0,
            "target-normalized x escaped the Eq+anchor separator")
    require(dot(separator, reduced_eq) == -1,
            "reduced Eq face stopped being separated from x")
    return {
        "physical_edge_defects": ["a-b", "c-d", "e-a", "b-c", "d-e"],
        "degree_five_Tate_weights": ["ce", "be", "bd", "ad", "ac"],
        "weighted_defect_sum": 0,
        "individual_defect_cancelled_by_x_at_zero_anchor": False,
        "separator": "pure_Eq+physical_ainc",
        "meaning": (
            "cyclic cancellation makes the existing top compatibility; it "
            "does not manufacture an individual clean transfer edge"
        ),
    }


def normalized_transfer_audit():
    # Work in the six-dimensional formal coefficient module on
    # (C_0,...,C_4,x).  Only the five adjacent C differences are physical
    # transfer columns.  g_i=C_i-x are the candidate base comparisons.
    vertices = []
    for index in range(5):
        column = [Q(0)] * 6
        column[index] = Q(1)
        vertices.append(tuple(column))
    x_basis = (Q(0), Q(0), Q(0), Q(0), Q(0), Q(1))
    edges = []
    for index in range(5):
        edges.append(add(vertices[index],
                         scale(-1, vertices[(index + 1) % 5])))
    g = [add(vertex, scale(-1, x_basis)) for vertex in vertices]
    A = add(*vertices)
    five_x = scale(5, x_basis)
    Z = add(A, scale(-1, five_x))
    require(Z == add(*g), "A-5x stopped being sum_i(C_i-x)")
    require(rank(edges) == 4, "adjacent transfer lattice lost rank four")
    require(rank(edges + [g[0]]) == 5,
            "one base comparison stopped completing the transfer module")

    epsilon = (Q(1), Q(1), Q(1), Q(1), Q(1), Q(0))
    require(all(dot(epsilon, edge) == 0 for edge in edges),
            "face-sum stopped killing adjacent transfers")
    require(dot(epsilon, x_basis) == 0,
            "x acquired comparison aggregate")
    require(dot(epsilon, A) == dot(epsilon, Z) == 5,
            "A or A-5x lost its comparison aggregate")

    # Integral relation: Z-5*g0=-4E0-3E1-2E2-E3.  Thus Z/5 and one base
    # comparison are equivalent after characteristic-zero localization,
    # but the cyclic aggregate has integral index five.
    right = add(scale(-4, edges[0]), scale(-3, edges[1]),
                scale(-2, edges[2]), scale(-1, edges[3]))
    require(add(Z, scale(-5, g[0])) == right,
            "cyclic aggregate/base comparison relation changed")

    # Coarse augmented signatures, with the comparison aggregate displayed
    # separately from the physical rows.
    C_aug = (Q(1), Q(0), Q(0), Q(0), Q(0))
    x_aug = (Q(1), Q(-1), Q(0), Q(0), Q(0))
    g_aug = add(C_aug, scale(-1, x_aug))
    A_aug = scale(5, C_aug)
    Z_aug = add(A_aug, scale(-5, x_aug))
    require(g_aug == (Q(0), Q(1), Q(0), Q(0), Q(0)),
            "base comparison acquired the wrong augmented signature")
    require(A_aug == (Q(5), Q(0), Q(0), Q(0), Q(0)),
            "physical cyclic A signature changed")
    require(Z_aug == (Q(0), Q(5), Q(0), Q(0), Q(0)),
            "A-5x stopped being the 037 kernel witness")
    require(scale(Q(-1, 5), Z_aug)
            == (Q(0), Q(-1), Q(0), Q(0), Q(0)),
            "037 generator normalization changed")

    return {
        "formal_basis": [f"C_{face}" for face in FACES] + ["x"],
        "physical_transfer_columns": [
            [int(value) for value in column] for column in edges
        ],
        "transfer_rank": rank(edges),
        "primitive_transfer_cokernel": "face-sum epsilon",
        "epsilon_on_x_A_Aminus5x": [0, 5, 5],
        "base_comparisons": "g_i=C_i-x",
        "base_signature_lower_ainc_W_tgt_ores": [0, 1, 0, 0, 0],
        "relative_generator": "-g_i, equivalently -(A-5x)/5",
        "cyclic_to_base_relation": "Z-5g_0=-4E_0-3E_1-2E_2-E_3",
        "integral_index_of_cyclic_aggregate": 5,
        "conclusion": (
            "adjacent transfer plus x constructs neither A nor A-5x; over "
            "characteristic zero either one is equivalent to one new "
            "physical base comparison C_i-x"
        ),
    }


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")
    ledger = {
        "theorem": "target-normalized cyclic comparison transfer gate",
        "literal_adjacent_squares": physical_edge_defect_audit(),
        "normalized_common_degree_transfer": normalized_transfer_audit(),
        "remaining_physical_readout": {
            "individual_comparison_eta":
                "dr_v(eta_z)=1+delta_(vz)*u_z/t",
            "cyclic_aggregate_eta": "5+u_z/t",
            "supplied_by_target_normalized_x": False,
        },
        "verdict": (
            "target normalization solves the unary target/W/ores rows but "
            "does not provide a comparison vertex.  Literal adjacent squares "
            "first retain their reduced pure-Eq defect; even granting its "
            "correction, the source transfer module has rank four and leaves "
            "the primitive base class C_i-x.  This class is exactly the "
            "A-5x relative-generator class of 0373033"
        ),
        "smallest_new_datum": (
            "one source-labelled common-companion comparison C_i-x in a "
            "fixed repeated P3+K2 grade, with the pinned eta/rootless readout"
        ),
        "scope": (
            "exact literal first PP defects and exact Laurent-normalized C5 "
            "transfer module; no no-go against adjoining the stated physical "
            "relative comparison generator"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    print("h3 rootless cyclic comparison target-normalized transfer: GATE")
    print("literal edge cleanup by x: NO (pure Eq + anchor separator)")
    print("after clean edges: rank 4, one base C_i-x remains")
    print("A-5x = sum_i(C_i-x); normalized negative is 037 generator")
    print("next datum: one physical common-companion comparison vertex")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
