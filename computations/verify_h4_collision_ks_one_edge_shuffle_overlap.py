#!/usr/bin/env python3
"""Audit the intrinsic h=4 one-edge prolongation of the h=3 collision/KS map.

For one six-site tail T={e0,e1,e2}, each of its three two-edge subtails is
an h=3 window and the omitted edge is the one-edge factor.  There are four
collision families, hence twelve presentation-specific new Leibniz faces.

The checker proves two exact statements over Q.

* With the exterior shuffle sign, every window presentation has the same
  intrinsic three-edge Hasse boundary.  Its two old h=3 faces and its one
  new spectator face are exactly the three restrictions of T.
* The three-presentation Cech complex is the augmented oriented triangle.
  It is exact, and the Laplacian contraction is canonical and S3-equivariant
  over Q.  Thus the coefficient/Koszul--PP source has no overlap covector at
  h=4.  An integral equivariant contraction would require division by 3.

This constructs the source-resolution structure map.  It does not assert
that the h=3 collision-to-Kodaira--Spencer comparison itself exists in the
complete physical word/fine/readout complex, nor that those physical rows
factor through this intrinsic source map.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_hyperbolic_collision_pp_augp2_spectator_naturality_gate.py":
        "0eedcb3f03e98ea18b549e2b6e21d7082cf368d8e3bc77fd3f104a178104c25a",
    "notes/uniform-hyperbolic-collision-pp-augp2-spectator-naturality-gate.md":
        "73fd2ff870db0d5344255cee1f2b4008bc19ba5058114f51b312d5a011eb760d",
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    "notes/h3-hasse-coproduct-cosimplicial-totalization.md":
        "9bb749b3b45a6b0248699bf54364cb304f89e01a4a4ad654963aad3534893ba4",
}
EXPECTED_LEDGER_SHA256 = (
    "70faa2e944b33c20099132ebee35661cdb854c28a44ef47ad3f3668d0877e4be"
)

FAMILIES = (
    "forward_01=-D*s1",
    "reverse_01=+p0*q01",
    "forward_02=-D*s0",
    "reverse_02=+p1*q01",
)
TAIL = (0, 1, 2)  # globally oriented edge slots e0<e1<e2

Vector = tuple[Q, ...]
Matrix = tuple[Vector, ...]
Feature = tuple[str, str, tuple[int, ...]]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add_to(answer: dict[Feature, Q], feature: Feature, value: Q) -> None:
    answer[feature] = answer.get(feature, Q(0)) + value
    if not answer[feature]:
        del answer[feature]


def wedge(left: tuple[int, ...], right: tuple[int, ...]) \
        -> tuple[Q, tuple[int, ...]]:
    """Exterior multiplication, with both inputs already ordered."""
    require(not set(left).intersection(right), ("repeated edge slot", left,
                                                right))
    inversions = sum(a > b for a in left for b in right)
    return Q(-1 if inversions % 2 else 1), tuple(sorted(left + right))


def intrinsic_boundary(family: str, parity: int) -> dict[Feature, Q]:
    """d(x*T)=dx*T+(-1)^|x| x*dT for T=(e0,e1,e2)."""
    answer: dict[Feature, Q] = {}
    add_to(answer, ("local_boundary", family, TAIL), Q(1))
    for position in range(3):
        face = TAIL[:position] + TAIL[position + 1:]
        add_to(answer, ("tail_restriction", family, face),
               Q(-1 if (parity + position) % 2 else 1))
    return answer


def presentation_boundary(family: str, spectator: int, parity: int) \
        -> tuple[dict[Feature, Q], Feature, Q]:
    """Map d((x*window) tensor e_i) through the global shuffle.

    The raw presentation orders the two window edges before its spectator.
    Multiplying the entire presentation by the shuffle sign makes its top
    equal to the intrinsically oriented x*e0*e1*e2.
    """
    window = tuple(edge for edge in TAIL if edge != spectator)
    shuffle, full = wedge(window, (spectator,))
    require(full == TAIL, ("shuffle target", spectator, full))
    outer = shuffle
    answer: dict[Feature, Q] = {}

    # The local boundary of x, then the unchanged two-edge window.
    local_shuffle, local_full = wedge(window, (spectator,))
    require(local_full == TAIL, "local shuffle")
    add_to(answer, ("local_boundary", family, TAIL),
           outer * local_shuffle)

    # The two Hasse faces already present in the h=3 window.
    for position, removed in enumerate(window):
        old_face = window[:position] + window[position + 1:]
        face_shuffle, face = wedge(old_face, (spectator,))
        coefficient = (outer
                       * Q(-1 if (parity + position) % 2 else 1)
                       * face_shuffle)
        add_to(answer, ("tail_restriction", family, face), coefficient)

    # The new h=4 Leibniz face from d(e_i)=1.
    new_coefficient = outer * Q(-1 if parity % 2 else 1)
    new_feature = ("tail_restriction", family, window)
    add_to(answer, new_feature, new_coefficient)
    return answer, new_feature, new_coefficient


def one_edge_structure_audit() -> dict[str, object]:
    records = []
    new_faces: set[Feature] = set()
    for parity in (0, 1):
        parity_new_faces: set[Feature] = set()
        for family in FAMILIES:
            expected = intrinsic_boundary(family, parity)
            presentation_records = []
            for spectator in TAIL:
                actual, new_feature, coefficient = presentation_boundary(
                    family, spectator, parity
                )
                require(actual == expected,
                        ("presentation is not the intrinsic boundary",
                         family, parity, spectator, actual, expected))
                parity_new_faces.add(new_feature)
                presentation_records.append({
                    "spectator_edge_slot": spectator,
                    "h3_window_edge_slots": [
                        edge for edge in TAIL if edge != spectator
                    ],
                    "shuffle_sign": (-1) ** (2 - spectator),
                    "new_Leibniz_face": list(new_feature[2]),
                    "new_Leibniz_coefficient": int(coefficient),
                    "inherited_h3_tail_faces": 2,
                    "total_intrinsic_tail_faces": 3,
                })
            require(len({
                tuple(sorted(presentation_boundary(
                    family, spectator, parity
                )[0].items())) for spectator in TAIL
            }) == 1, ("window boundaries differ", family, parity))
            records.append({
                "carrier_parity": parity,
                "collision_family": family,
                "presentations": presentation_records,
                "all_three_presentations_have_one_common_boundary": True,
            })
        require(len(parity_new_faces) == 12,
                ("h4 new-face census", parity, len(parity_new_faces)))
        if parity == 0:
            new_faces = parity_new_faces
        else:
            require(parity_new_faces == new_faces,
                    "parity changed the labelled face set")

    return {
        "six_site_tail": ["e0", "e1", "e2"],
        "collision_families": len(FAMILIES),
        "h3_window_presentations_per_intrinsic_h4_cell": 3,
        "presentation_tops": 12,
        "distinct_new_Leibniz_faces": len(new_faces),
        "new_face_signs_for_even_carrier": [1, -1, 1],
        "new_face_signs_for_odd_carrier": [-1, 1, -1],
        "per_presentation_boundary":
            "two inherited h3 restrictions plus one new spectator restriction",
        "common_intrinsic_boundary":
            "local KS/collision boundary plus all three oriented tail restrictions",
        "records": records,
    }


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


def global_h4_window_census() -> dict[str, object]:
    """Separate the literal fixed-window 12-packet from full h4 descent."""
    vertices = tuple(range(6))
    tails = tuple(perfect_matchings(vertices))
    require(len(tails) == len(set(tails)) == 15, "six-site matchings")

    presentation_count: dict[tuple[str, tuple[tuple[int, int], ...]], int] = {}
    new_face_labels = set()
    for tail in tails:
        for family in FAMILIES:
            key = (family, tail)
            presentation_count[key] = 0
            for spectator in tail:
                window = tuple(edge for edge in tail if edge != spectator)
                presentation_count[key] += 1
                # On a fixed six-site universe the complementary spectator
                # is determined by the two-edge window, but retain it in the
                # audit label to make provenance literal.
                new_face_labels.add((family, window, spectator))
    require(set(presentation_count.values()) == {3}
            and len(presentation_count) == 60,
            "global three-window cover")
    require(len(new_face_labels) == 180, "global h4 Leibniz flags")

    fixed_spectator = (4, 5)
    fixed_windows = tuple(perfect_matchings((0, 1, 2, 3)))
    fixed_packet = {
        (family, window, fixed_spectator)
        for family in FAMILIES for window in fixed_windows
    }
    require(len(fixed_windows) == 3 and len(fixed_packet) == 12,
            "fixed-window twelve-face packet")
    require(fixed_packet.issubset(new_face_labels),
            "fixed-window packet not intrinsic")

    return {
        "six_site_tail_matchings": 15,
        "intrinsic_four_family_h4_cells": 60,
        "h3_window_presentations_per_cell": 3,
        "global_presentation_tops": 180,
        "global_new_Leibniz_flags": 180,
        "fixed_old_four_sites_plus_edge_cells": 12,
        "fixed_old_four_sites_plus_edge_new_faces": 12,
        "fixed_packet_is_subset_of_intrinsic_h4_census": True,
        "clarification": (
            "the requested fixed-window 12-packet is 4 families times the "
            "3 matchings on its old four sites; the overlap triangle is "
            "instead fibrewise over each of the 60 intrinsic h4 cells"
        ),
    }


def transpose(matrix: Matrix) -> Matrix:
    require(matrix, "transpose empty")
    return tuple(tuple(matrix[row][column] for row in range(len(matrix)))
                 for column in range(len(matrix[0])))


def matmul(left: Matrix, right: Matrix) -> Matrix:
    require(left and right and len(left[0]) == len(right),
            ("matrix dimensions", len(left), len(left[0]), len(right),
             len(right[0]) if right else 0))
    return tuple(tuple(sum((left[i][k] * right[k][j]
                            for k in range(len(right))), Q(0))
                           for j in range(len(right[0])))
                 for i in range(len(left)))


def madd(left: Matrix, right: Matrix) -> Matrix:
    require(len(left) == len(right)
            and all(len(a) == len(b) for a, b in zip(left, right,
                                                      strict=True)),
            "matrix add dimensions")
    return tuple(tuple(a + b for a, b in zip(left_row, right_row,
                                             strict=True))
                 for left_row, right_row in zip(left, right, strict=True))


def mscale(value: int | Q, matrix: Matrix) -> Matrix:
    return tuple(tuple(Q(value) * entry for entry in row) for row in matrix)


def identity(size: int) -> Matrix:
    return tuple(tuple(Q(i == j) for j in range(size)) for i in range(size))


def matrix_rank(matrix: Matrix) -> int:
    rows = [list(row) for row in matrix]
    if not rows:
        return 0
    width = len(rows[0])
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        value = rows[pivot_row][column]
        rows[pivot_row] = [entry / value for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [a - value * b for a, b in
                         zip(rows[row], rows[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


# Oriented augmented triangle:
# C2 --B2--> C1{01,02,12} --B1--> C0{0,1,2} --EPS--> Q.
B1: Matrix = (
    (Q(-1), Q(-1), Q(0)),
    (Q(1), Q(0), Q(-1)),
    (Q(0), Q(1), Q(1)),
)
B2: Matrix = ((Q(1),), (Q(-1),), (Q(1),))
EPS: Matrix = ((Q(1), Q(1), Q(1)),)


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(permutation[i] > permutation[j]
                     for i in range(len(permutation))
                     for j in range(i + 1, len(permutation)))
    return -1 if inversions % 2 else 1


def simplex_actions(permutation: tuple[int, int, int]) \
        -> tuple[Matrix, Matrix, Matrix]:
    # Vertices.
    a0 = [[Q(0)] * 3 for _ in range(3)]
    for old in range(3):
        a0[permutation[old]][old] = Q(1)

    # Oriented edges 01,02,12.
    edge_basis = ((0, 1), (0, 2), (1, 2))
    edge_index = {edge: index for index, edge in enumerate(edge_basis)}
    a1 = [[Q(0)] * 3 for _ in range(3)]
    for old, edge in enumerate(edge_basis):
        image = (permutation[edge[0]], permutation[edge[1]])
        ordered = tuple(sorted(image))
        sign = Q(1 if image == ordered else -1)
        a1[edge_index[ordered]][old] = sign

    # The oriented triangle carries the sign representation.
    a2 = ((Q(permutation_sign(permutation)),),)
    return tuple(map(tuple, a0)), tuple(map(tuple, a1)), a2


def overlap_triangle_audit() -> dict[str, object]:
    zero_02 = ((Q(0),), (Q(0),), (Q(0),))
    require(matmul(EPS, B1) == ((Q(0), Q(0), Q(0)),),
            "epsilon B1")
    require(matmul(B1, B2) == zero_02, "B1 B2")
    require(matrix_rank(B1) == 2 and matrix_rank(B2) == 1,
            "triangle ranks")

    # Canonical rational Laplacian contraction.
    section: Matrix = ((Q(1, 3),), (Q(1, 3),), (Q(1, 3),))
    h0 = mscale(Q(1, 3), transpose(B1))       # C0 -> C1
    h1 = ((Q(1, 3), Q(-1, 3), Q(1, 3)),)     # C1 -> C2
    require(matmul(EPS, section) == ((Q(1),),), "epsilon section")
    require(madd(matmul(B1, h0), matmul(section, EPS)) == identity(3),
            "C0 contraction")
    require(madd(matmul(h0, B1), matmul(B2, h1)) == identity(3),
            "C1 contraction")
    require(matmul(h1, B2) == ((Q(1),),), "C2 contraction")

    # Naturality for every relabelling of the three tail edges.
    for permutation in permutations(range(3)):
        a0, a1, a2 = simplex_actions(permutation)
        require(matmul(a0, B1) == matmul(B1, a1),
                ("B1 equivariance", permutation))
        require(matmul(a1, B2) == matmul(B2, a2),
                ("B2 equivariance", permutation))
        require(matmul(a0, section) == section,
                ("section equivariance", permutation))
        require(matmul(a1, h0) == matmul(h0, a0),
                ("h0 equivariance", permutation))
        require(matmul(a2, h1) == matmul(h1, a1),
                ("h1 equivariance", permutation))

    # Four independent collision-family blocks.
    return {
        "one_family_dimensions_C2_C1_C0_target": [1, 3, 3, 1],
        "one_family_ranks_B2_B1_augmentation": [1, 2, 1],
        "four_family_dimensions_C2_C1_C0_target": [4, 12, 12, 4],
        "four_family_ranks_B2_B1_augmentation": [4, 8, 4],
        "homology": [0, 0, 0],
        "canonical_Q_contraction": {
            "section": "(q0+q1+q2)/3",
            "h0": "B1^T/3",
            "h1_on_(a01,a02,a12)": "(a01-a02+a12)/3 times triangle",
            "S3_equivariant": True,
        },
        "integral_resolution_exact": True,
        "integral_S3_equivariant_contraction": False,
        "integral_reason": (
            "an S3-fixed section is a(q0+q1+q2), whose augmentation is 3a"
        ),
    }


def protected_row_counterguard() -> dict[str, object]:
    # A row on the three presentations descends precisely when its centered
    # component vanishes.  These two primitive differences span the test.
    difference_rows = ((1, -1, 0), (1, 0, -1))
    for values in ((0, 0, 0), (5, 5, 5), (2, -1, 7)):
        centered = tuple(Q(value) - sum(map(Q, values), Q(0)) / 3
                         for value in values)
        descends = not any(centered)
        expected = values[0] == values[1] == values[2]
        require(descends == expected, ("descent criterion", values))
    return {
        "criterion": (
            "a protected row descends iff its values on the three shuffled "
            "window presentations are equal"
        ),
        "primitive_mismatch_tests": difference_rows,
        "canonical_mismatch": "a-(sum(a)/3)*(1,1,1)",
        "source_Hasse_value": [0, 0, 0],
        "source_Hasse_stable_covector": False,
        "physical_warning": (
            "word/fine/repeated, target, q, anchor, residue, W and ridge "
            "must each be checked against this criterion; the source "
            "shuffle theorem does not assign those readouts"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h4 collision/KS one-edge shuffle-overlap structure map",
        "pins": PINS,
        "one_edge_structure": one_edge_structure_audit(),
        "global_h4_census": global_h4_window_census(),
        "three_window_overlap": overlap_triangle_audit(),
        "protected_row_counterguard": protected_row_counterguard(),
        "verdict": (
            "For each intrinsic six-site tail and each of the four collision "
            "families, the three h3-window times one-edge presentations map "
            "by the exterior shuffle to one h4 source cell.  Their two old "
            "window restrictions plus one new Leibniz restriction give the "
            "same full three-edge boundary.  The twelve new faces are the "
            "four-by-three intrinsic tail restrictions.  The presentation "
            "overlap is the exact augmented triangle, with a canonical "
            "S3-equivariant rational contraction.  Hence no source-Hasse "
            "overlap covector survives at h4."
        ),
        "scope": (
            "This is an intrinsic coefficient/Koszul--principal-parts "
            "source theorem, using the actual six-site tail and no tensor "
            "factorization of the GHZ target.  It conditionally prolongs a "
            "relabeling-covariant h3 collision-to-Kodaira--Spencer chain.  "
            "It neither constructs that missing physical h3 chain nor "
            "proves equality of its word/fine/repeated and protected "
            "target/q/anchor/residue/W/ridge values across the three windows."
        ),
        "next_exact_test": (
            "evaluate every protected physical row on the three h4 window "
            "presentations; unequal values are detected by (1,-1,0) or "
            "(1,0,-1), while equal values descend through the constructed "
            "shuffle triangle"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("h4 collision/KS one-edge structure: PASS")
    print("new Leibniz faces: 12 = 4 families x 3 omitted edges")
    print("three-window overlap: augmented triangle, exact")
    print("canonical S3-equivariant contraction: YES over Q")
    print("source-Hasse stable covector: NONE")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
