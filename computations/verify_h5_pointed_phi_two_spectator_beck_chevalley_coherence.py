#!/usr/bin/env python3
"""Audit the h=5 two-spectator coherence of the pointed mixed comparison.

Condition on one source-labelled h=3 Phi_KS,r0/P_f schema.  A fixed h=5
tail has two spectator edges beyond an h=3 window.  The two interval factors
give states

    q67*q89, dq67*q89, q67*dq89, dq67*dq89.

The tensor differential squares to zero, both restrictions are chain maps,
the restrictions commute, and the two insertion orders agree on the top.
The mixed face occurs with coefficients -1,+1 and cancels.  Thus the fixed
window has no new two-spectator associator.

There is also a presentation-level test.  Four tail edges have six h=3
two-edge windows.  The twelve one-edge overlaps form the octahedral graph.
Its four inherited h=4 triangles leave H1 of dimension three.  The three
standard disjoint-edge Beck--Chevalley squares add three independent faces;
together their boundary rank is seven, exactly the cycle-space dimension.
The augmented presentation complex is then exact without a higher cell.

This is a conditional local coherence theorem, not full h=5 PAComp.  The
physical protected rows must still be Hasse-linear, and full matching-cover
descent/exhaustivity remains the separate U4 obligation.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h4_pointed_phi01_fixed_tail_h3_restriction_gate.py":
        "db1f9c4ccdf8b95cdbc681427ce5caa473385293f0e49f9817b185707e93e5b2",
    "notes/h4-pointed-phi01-fixed-tail-h3-restriction-gate.md":
        "78a1dc43506279ef639685d6053eaecd683d12937f503a01c3016f62302b46f0",
    "computations/verify_h4_collision_ks_one_edge_shuffle_overlap.py":
        "bf25a8c481ad8e42a14b22ff3f955f5d321289356d9dd11962ffc68d4e06671e",
    "notes/h4-collision-ks-one-edge-shuffle-overlap.md":
        "3b50f4a6e556f3cd760d335910b788b7b16d074d0a5382dc89bae381e2932972",
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    "notes/h3-hasse-coproduct-cosimplicial-totalization.md":
        "9bb749b3b45a6b0248699bf54364cb304f89e01a4a4ad654963aad3534893ba4",
    "computations/verify_uniform_hyperbolic_collision_pp_augp2_spectator_naturality_gate.py":
        "0eedcb3f03e98ea18b549e2b6e21d7082cf368d8e3bc77fd3f104a178104c25a",
    "notes/uniform-hyperbolic-collision-pp-augp2-spectator-naturality-gate.md":
        "73fd2ff870db0d5344255cee1f2b4008bc19ba5058114f51b312d5a011eb760d",
}
EXPECTED_LEDGER_SHA256 = (
    "b88be7f35fba95f171d855ebb82938e80f73b416e12adec0c3c385999dea2087"
)

Vector = tuple[Q, ...]
Matrix = tuple[Vector, ...]  # row-major
ZERO4: Matrix = tuple((Q(0),) * 4 for _ in range(4))
I4: Matrix = tuple(tuple(Q(row == column) for column in range(4))
                   for row in range(4))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def transpose(matrix: Matrix) -> Matrix:
    require(matrix, "empty transpose")
    width = len(matrix[0])
    require(all(len(row) == width for row in matrix), "matrix width")
    return tuple(tuple(row[column] for row in matrix)
                 for column in range(width))


def matmul(left: Matrix, right: Matrix) -> Matrix:
    require(left and right and len(left[0]) == len(right), "matmul shape")
    columns = transpose(right)
    return tuple(tuple(sum((a * b for a, b in zip(row, column, strict=True)),
                           Q(0))
                       for column in columns)
                 for row in left)


def identity(size: int) -> Matrix:
    return tuple(tuple(Q(row == column) for column in range(size))
                 for row in range(size))


def zero(height: int, width: int) -> Matrix:
    return tuple((Q(0),) * width for _ in range(height))


def scale(value: Q, matrix: Matrix) -> Matrix:
    return tuple(tuple(value * entry for entry in row) for row in matrix)


def block_matrix(blocks: tuple[tuple[Matrix, ...], ...]) -> Matrix:
    require(blocks and blocks[0], "empty block matrix")
    block_columns = len(blocks[0])
    require(all(len(row) == block_columns for row in blocks),
            "block row width")
    answer = []
    for block_row in blocks:
        height = len(block_row[0])
        require(all(len(block) == height for block in block_row),
                "block height")
        for inner_row in range(height):
            answer.append(tuple(entry for block in block_row
                                for entry in block[inner_row]))
    return tuple(answer)


def subtract(left: Matrix, right: Matrix) -> Matrix:
    require(len(left) == len(right)
            and all(len(a) == len(b) for a, b in
                    zip(left, right, strict=True)), "subtract shape")
    return tuple(tuple(a - b for a, b in zip(row_left, row_right,
                                             strict=True))
                 for row_left, row_right in zip(left, right, strict=True))


def rank(vectors: tuple[Vector, ...]) -> int:
    if not vectors:
        return 0
    work = [list(map(Q, vector)) for vector in vectors]
    width = len(work[0])
    require(all(len(vector) == width for vector in work), "rank width")
    pivot_row = 0
    for column in range(width):
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
            work[row] = [entry - value * base for entry, base in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def base_and_one_spectator_differentials() -> tuple[Matrix, Matrix]:
    # h3 basis (epsilon_s,r0,c_f,E).
    d3 = (
        (Q(0), Q(0), Q(0), Q(0)),
        (Q(0), Q(0), Q(0), Q(0)),
        (Q(-1), Q(0), Q(0), Q(0)),
        (Q(0), Q(1), Q(0), Q(0)),
    )
    d4 = block_matrix((
        (d3, ZERO4),
        (I4, scale(Q(-1), d3)),
    ))
    require(matmul(d3, d3) == zero(4, 4)
            and matmul(d4, d4) == zero(8, 8),
            "base/one-spectator differential squared")
    return d3, d4


def two_spectator_total_complex_audit() -> dict[str, object]:
    d3, _ = base_and_one_spectator_differentials()
    # State order 00=q67q89, 10=dq67q89, 01=q67dq89,
    # 11=dq67dq89.  Tensor sign convention:
    # d10=-11, d01=+11.
    d5 = block_matrix((
        (d3, ZERO4, ZERO4, ZERO4),
        (I4, scale(Q(-1), d3), ZERO4, ZERO4),
        (I4, ZERO4, scale(Q(-1), d3), ZERO4),
        (ZERO4, scale(Q(-1), I4), I4, d3),
    ))
    require(matmul(d5, d5) == zero(16, 16),
            "two-spectator differential stopped squaring to zero")

    insertion = block_matrix(((I4,), (ZERO4,), (ZERO4,), (ZERO4,)))
    defect = subtract(matmul(d5, insertion), matmul(insertion, d3))
    expected_defect = block_matrix(((ZERO4,), (I4,), (I4,), (ZERO4,)))
    require(defect == expected_defect,
            "two-spectator insertion defect changed")

    # At spectator degree only, d0=(1,1), d1=(-1,1).  The mixed face
    # cancels in d1*d0 and is hit with primitive coefficient one.
    d0 = ((Q(1),), (Q(1),))
    d1 = ((Q(-1), Q(1)),)
    require(matmul(d1, d0) == ((Q(0),),)
            and rank(tuple(transpose(d0))) == 1
            and rank(tuple(d1)) == 1,
            "two-spectator square sign/rank changed")
    return {
        "spectator_state_order": [
            "q67*q89", "dq67*q89", "q67*dq89", "dq67*dq89",
        ],
        "d_q67q89": "dq67*q89 + q67*dq89",
        "d_dq67q89": "-dq67*dq89",
        "d_q67dq89": "+dq67*dq89",
        "total_dimension_over_four_dimensional_h3_complex": 16,
        "total_d_squared": 0,
        "top_insertion_defect": ["dq67*q89", "q67*dq89"],
        "mixed_face_coefficients": [-1, 1],
        "mixed_face_cancellation": 0,
        "primitive_mixed_face_is_hit": True,
        "new_fixed_window_associator_class": False,
    }


def restriction_and_shuffle_audit() -> dict[str, object]:
    _, d4 = base_and_one_spectator_differentials()
    d3, _ = base_and_one_spectator_differentials()
    d5 = block_matrix((
        (d3, ZERO4, ZERO4, ZERO4),
        (I4, scale(Q(-1), d3), ZERO4, ZERO4),
        (I4, ZERO4, scale(Q(-1), d3), ZERO4),
        (ZERO4, scale(Q(-1), I4), I4, d3),
    ))
    # Restrict 67: retain states 00,01.  Restrict 89: retain 00,10.
    rho67 = block_matrix(((I4, ZERO4, ZERO4, ZERO4),
                          (ZERO4, ZERO4, I4, ZERO4)))
    rho89 = block_matrix(((I4, ZERO4, ZERO4, ZERO4),
                          (ZERO4, I4, ZERO4, ZERO4)))
    rho_one = block_matrix(((I4, ZERO4),))
    rho_both = block_matrix(((I4, ZERO4, ZERO4, ZERO4),))
    require(matmul(rho67, d5) == matmul(d4, rho67)
            and matmul(rho89, d5) == matmul(d4, rho89),
            "one of the two restrictions stopped being a chain map")
    route_67_then_89 = matmul(rho_one, rho67)
    route_89_then_67 = matmul(rho_one, rho89)
    require(route_67_then_89 == route_89_then_67 == rho_both,
            "two spectator restrictions stopped commuting")

    # Insert 67 into the 89 complex, or 89 into the 67 complex.
    insert67 = block_matrix(((I4, ZERO4),
                             (ZERO4, ZERO4),
                             (ZERO4, I4),
                             (ZERO4, ZERO4)))
    insert89 = block_matrix(((I4, ZERO4),
                             (ZERO4, I4),
                             (ZERO4, ZERO4),
                             (ZERO4, ZERO4)))
    insert_one = block_matrix(((I4,), (ZERO4,)))
    route_insert_89_then_67 = matmul(insert67, insert_one)
    route_insert_67_then_89 = matmul(insert89, insert_one)
    require(route_insert_89_then_67 == route_insert_67_then_89,
            "top insertion orders stopped agreeing")

    # Graded transposition of the two spectator factors: swap 10 and 01 and
    # negate 11.  It commutes with d5 and squares to one.
    swap = block_matrix((
        (I4, ZERO4, ZERO4, ZERO4),
        (ZERO4, ZERO4, I4, ZERO4),
        (ZERO4, I4, ZERO4, ZERO4),
        (ZERO4, ZERO4, ZERO4, scale(Q(-1), I4)),
    ))
    require(matmul(swap, swap) == identity(16)
            and matmul(swap, d5) == matmul(d5, swap),
            "graded spectator shuffle changed")
    return {
        "rho67": "retain 00,01; kill 10,11",
        "rho89": "retain 00,10; kill 01,11",
        "both_restrictions_are_chain_maps": True,
        "rho89_rho67_equals_rho67_rho89": True,
        "common_value": "rho_{67,89}: q67*q89*z -> z, all dqi states -> 0",
        "two_top_insertion_orders_equal_strictly": True,
        "graded_shuffle": "10 <-> 01; 11 -> -11",
        "graded_shuffle_is_chain_involution": True,
        "Beck_Chevalley_debt": "the standard oriented mixed 11 square only",
    }


WINDOWS = ("01", "02", "03", "12", "13", "23")
EDGES = tuple((left, right) for left, right in combinations(WINDOWS, 2)
              if len(set(left) & set(right)) == 1)
TRIANGLES = (
    ("01", "02", "12"),
    ("01", "03", "13"),
    ("02", "03", "23"),
    ("12", "13", "23"),
)
BC_SQUARES = (
    ("01", "02", "23", "13"),
    ("01", "03", "23", "12"),
    ("02", "03", "13", "12"),
)


def vertex_incidence(left: str, right: str) -> Vector:
    answer = [Q(0)] * len(WINDOWS)
    answer[WINDOWS.index(left)] = Q(-1)
    answer[WINDOWS.index(right)] = Q(1)
    return tuple(answer)


def cycle_boundary(vertices: tuple[str, ...]) -> Vector:
    answer = [Q(0)] * len(EDGES)
    for left, right in zip(vertices, vertices[1:] + vertices[:1]):
        oriented = (left, right)
        edge = tuple(sorted(oriented, key=WINDOWS.index))
        require(edge in EDGES, ("non-overlap cycle edge", vertices, edge))
        answer[EDGES.index(edge)] += Q(1 if edge == oriented else -1)
    return tuple(answer)


def six_window_presentation_audit() -> dict[str, object]:
    edge_boundaries = tuple(vertex_incidence(*edge) for edge in EDGES)
    triangle_boundaries = tuple(cycle_boundary(value) for value in TRIANGLES)
    square_boundaries = tuple(cycle_boundary(value) for value in BC_SQUARES)
    edge_rank = rank(edge_boundaries)
    cycle_dimension = len(EDGES) - edge_rank
    triangle_rank = rank(triangle_boundaries)
    complete_face_rank = rank(triangle_boundaries + square_boundaries)
    require(len(WINDOWS) == 6 and len(EDGES) == 12
            and edge_rank == 5 and cycle_dimension == 7
            and triangle_rank == 4
            and complete_face_rank == 7,
            "six-window octahedral ranks changed")

    h1_after_triangles = cycle_dimension - triangle_rank
    h1_after_bc = cycle_dimension - complete_face_rank
    h2_after_bc = len(TRIANGLES) + len(BC_SQUARES) - complete_face_rank
    require(h1_after_triangles == 3 and h1_after_bc == h2_after_bc == 0,
            "presentation homology changed")
    return {
        "four_tail_edge_indices": [0, 1, 2, 3],
        "h3_window_vertices": list(WINDOWS),
        "one_edge_overlap_graph": "octahedral graph J(4,2)",
        "vertex_edge_counts": [len(WINDOWS), len(EDGES)],
        "edge_boundary_rank": edge_rank,
        "cycle_space_dimension": cycle_dimension,
        "inherited_h4_triangles": [list(value) for value in TRIANGLES],
        "h4_triangle_boundary_rank": triangle_rank,
        "H1_after_h4_triangles_only": h1_after_triangles,
        "standard_disjoint_edge_BC_squares":
            [list(value) for value in BC_SQUARES],
        "face_rank_after_three_BC_squares": complete_face_rank,
        "H1_after_standard_BC_squares": h1_after_bc,
        "H2_after_standard_BC_squares": h2_after_bc,
        "augmented_dimensions": [7, 12, 6, 1],
        "augmented_ranks": [7, 5, 1],
        "higher_associator_cell_needed": False,
        "sharp_warning": (
            "the four h4 triangles alone are insufficient; omitting the "
            "three standard Beck-Chevalley squares leaves H1 dimension 3"
        ),
    }


def selected_faces_and_readouts_audit() -> dict[str, object]:
    matchings = (("23", "45"), ("24", "35"), ("25", "34"))
    local_db01 = tuple(
        f"q67*q89*p0*s1*dq{edge}*q{mate}"
        for left, right in matchings
        for edge, mate in ((left, right), (right, left))
    )
    first67 = tuple(f"dq67*q89*p0*s1*q{left}*q{right}"
                    for left, right in matchings)
    first89 = tuple(f"q67*dq89*p0*s1*q{left}*q{right}"
                    for left, right in matchings)
    mixed = tuple(f"dq67*dq89*p0*s1*q{left}*q{right}"
                  for left, right in matchings)
    require(tuple(map(len, (local_db01, first67, first89, mixed))) ==
                (6, 3, 3, 3),
            "h5 selected face counts changed")

    row_order = (
        "B", "Eq", "target", "M", "ainc", "q", "P_f",
        "ores", "W", "ridge", "eta", "sigma",
    )
    r0 = tuple(map(Q, (1, 1, 1, -1, -1, 0, 1, 0, 0, 0, 0, 0)))
    minus_r0 = tuple(-value for value in r0)
    require(tuple(left + right for left, right in
                  zip(minus_r0, r0, strict=True)) == (Q(0),) * len(r0),
            "protected mixed-face cancellation changed")
    return {
        "fixed_window_local_db01_terms": list(local_db01),
        "first_dq67_faces": list(first67),
        "first_dq89_faces": list(first89),
        "mixed_dq67dq89_faces": list(mixed),
        "support_counts_local_first67_first89_mixed": [6, 3, 3, 3],
        "mixed_face_signs": [-1, 1],
        "conditional_r0_row_order": list(row_order),
        "conditional_readout_on_each_local_db01_term": list(map(int, r0)),
        "conditional_mixed_readout_sum": [0] * len(r0),
        "physical_status": (
            "the cancellation is exact for every Hasse-linear protected "
            "row; Hasse-linearity of the physical Phi/AugP2 comparison is "
            "still a hypothesis, not constructed here"
        ),
    }


def full_h5_scope_audit() -> dict[str, object]:
    # h=5 has four tail edges on eight sites.  There are 7!!=105 matchings,
    # and each has C(4,2)=6 h3-window presentations.  A fixed h3 partition
    # covers only 3*3!!=9 tails.
    return {
        "h": 5,
        "tail_edges": 4,
        "tail_matchings": 105,
        "h3_window_presentations_per_matching": 6,
        "fixed_partition_tail_matchings": 9,
        "cross_partition_tail_matchings": 96,
        "fixed_tail_coherence_proved_here": True,
        "full_matching_cover_descent_proved_here": False,
        "protected_physical_Hasse_linearity_proved_here": False,
        "new_local_operation_generator_beyond_Phi": False,
        "remaining_uniform_inputs": [
            "the one source-valid Phi_KS,r0/P_f schema",
            "physical Hasse-linearity of PP/AugP2 and protected readouts",
            "normalized descent over the complete 105-matching cover",
        ],
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h5 pointed Phi two-spectator Beck-Chevalley coherence",
        "pins": PINS,
        "two_spectator_total_complex": two_spectator_total_complex_audit(),
        "restriction_reinsertion_shuffle": restriction_and_shuffle_audit(),
        "six_window_presentation_complex": six_window_presentation_audit(),
        "selected_faces_and_protected_readouts":
            selected_faces_and_readouts_audit(),
        "full_h5_scope": full_h5_scope_audit(),
        "verdict": (
            "Conditionally on one source-labelled Phi_KS,r0/P_f schema, "
            "two fixed spectators introduce no new local associator.  The "
            "tensor differential squares to zero, restrictions commute, "
            "top insertions agree, and the dq67*dq89 face cancels with "
            "coefficients -1,+1.  Presentation-wise, however, the four "
            "inherited h4 triangles alone leave H1 dimension three.  The "
            "three ordinary disjoint-edge Beck-Chevalley squares supply "
            "exactly those three missing directions, making the augmented "
            "six-window complex exact with no higher cell.  Thus there is "
            "no new operation generator beyond Phi plus the standard "
            "shuffle/Hasse/Beck-Chevalley faces."
        ),
        "scope": (
            "exact rational fixed-tail h5 chain, sign and six-window "
            "presentation computation.  It is conditional on physical Phi "
            "and protected-row Hasse-linearity.  It does not prove the full "
            "105-matching cover descent, physical U4 exhaustivity, uniform "
            "PAComp(h), or existence of Phi itself."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("h5 two-spectator coherence ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "complex", "restriction",
                                           "presentations", "faces", "scope"),
                        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h5 pointed Phi two-spectator coherence ({arguments.mode}): PASS")
        print("fixed-window mixed face: (-1,+1), cancels")
        print("h4 triangles only: H1 dimension 3")
        print("+ three Beck-Chevalley squares: H1=H2=0")
        print("new local operation generator beyond Phi: NO")
        print("full h5 PAComp: OPEN (physical U4 and 105-tail descent)")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
