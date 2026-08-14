#!/usr/bin/env python3
"""Refute d^2-forcing of the cross-word mixed-cell augmentation.

The four source-labelled naturality edges have a primitive square cycle
z=(1,-1,1,-1).  Their one-skeleton is already a chain complex: d z=0,
so d^2=0 does not make z a boundary.  A derived-naturality/exactness
hypothesis is required to adjoin a mixed 2-cell kappa with d kappa=z.

Even after kappa is granted, d^2 does not determine its terminal B/Eq
augmentation.  In the projected complex

    d kappa = (z,a),      a in Q^8_B,Eq,

and the B/Eq rows have zero outgoing differential.  Thus every a obeys
d^2=0.  Modulo the old rank-seven cap image, the freedom is exactly

    a = lambda*(delta,0),   Psi(a)=lambda,
    chi(a)=delta.(B-Eq)=4*lambda.

In particular dark lambda=0 and bright lambda=1 fillers have identical
source boundary z.  The db01/dL01 faces are strictly off-grade and have
zero B/Eq image, so they do not remove this freedom.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_db01_dl01_literal_private_eq_conservation_gate.py":
        "1a27b00d28be6334a27e0603a0ef776367d3c71b6f8fa45d3005963f8dff4c6c",
    "notes/h3-db01-dl01-literal-private-eq-conservation-gate.md":
        "6ba7ac1df36e3ed4ed30acc1d219f22bcdff0d673e078aeb3b2e1d327a2737d9",
    "computations/verify_h3_e14_pointed_orbit_keq_mapping_cylinder_gate.py":
        "2e4b1a1b9bb5b5be8d0997132b49b95576a28dc6ccb9cfd83db808ace8f52f3e",
    "notes/h3-e14-pointed-orbit-keq-mapping-cylinder-gate.md":
        "f5008f5b7e892b5ce5270faacee4ec9f2bffc2630b8dd15a55cb8f5c6800cb21",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "notes/h3-shear-collision-augp2-packaging-map-gate.md":
        "9d5918605dd94d08d18c099966e5956fa0f1c62855b97fd81bf9ada54f2f45ad",
    "computations/verify_h3_balanced_square_private_eq_projection_gate.py":
        "bbfb690a73844169574351ad019171a6d9c5fe332e59cc9694a1f67dcf31cf8e",
    "notes/h3-balanced-square-private-eq-projection-gate.md":
        "6d740e7e30231204dbe1b79c4b7c21fe5f5b5ac45122ac714be3c7626afa7c31",
    "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py":
        "c583279d8f4cb7efc24b7fc4784e480b63acb1ca7fe430ae1a7e2db2b854c11b",
    "notes/h3-augmented-p2-section-shortest-conditional-gate.md":
        "ee5da6f0911feb06707106cc6207161bbac7cabd31885f554321698dfbb989d8",
}
EXPECTED_DIGEST = "33894eee4fd4ce7fd5548daa1f5f1ae3386baf1a8b9e56d252c3a013fcffed97"

DELTA = tuple(map(Q, (1, 1, -1, -1)))
ZERO4 = (Q(0),) * 4
ZERO8 = (Q(0),) * 8


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def matvec(matrix, vector):
    require(all(len(row) == len(vector) for row in matrix), "matvec width")
    return tuple(dot(row, vector) for row in matrix)


def rank(columns) -> int:
    columns = tuple(columns)
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def square_data():
    # Vertex order is bottom-left, bottom-right, top-left, top-right.
    # Edge order is bottom P_f, left K_Eq, right K_Eq, top cross-word.
    bottom = tuple(map(Q, (-1, 1, 0, 0)))
    left = tuple(map(Q, (-1, 0, 1, 0)))
    right = tuple(map(Q, (0, -1, 0, 1)))
    top = tuple(map(Q, (0, 0, -1, 1)))
    edges = (bottom, left, right, top)
    d1 = tuple(tuple(edges[column][row] for column in range(4))
               for row in range(4))
    z = tuple(map(Q, (1, -1, 1, -1)))
    return edges, d1, z


def boundary_audit():
    mapping = load(
        "computations/verify_h3_e14_pointed_orbit_keq_mapping_cylinder_gate.py",
        "cross_word_d2_mapping_square",
    )
    pinned = mapping.mapping_cylinder_square_audit()
    edges, d1, z = square_data()
    require(pinned["primitive_boundary_cycle"] == [1, -1, 1, -1]
            and pinned["H1_without_mixed_face"] == "Z"
            and pinned["H1_after_one_mixed_face"] == 0,
            "the pinned mapping-square theorem changed")
    require(rank(edges) == 3 and matvec(d1, z) == ZERO4,
            "the primitive square cycle changed")

    # With no C2 at all, C1 -> C0 is already a valid chain complex.  Its
    # d^2 condition is vacuous in degree two and H1 is one-dimensional.
    # This is the smallest exact countermodel to filler existence by d^2.
    h1_without_c2 = len(edges) - rank(edges)
    require(h1_without_c2 == 1, "the one-skeleton H1 changed")

    # If derived naturality/exactness is added, the normalized filler has
    # boundary z.  Its coefficient is primitive (up to orientation), and
    # it kills H1.  This is forced *after* existence, not by d^2 alone.
    c2_boundary_rank = rank((z,))
    require(c2_boundary_rank == 1
            and h1_without_c2 - c2_boundary_rank == 0,
            "one primitive filler stopped killing square H1")
    return {
        "edge_order": pinned["edge_order"],
        "d1_rank": rank(edges),
        "primitive_cycle_z": list(map(int, z)),
        "d1_z": list(map(int, matvec(d1, z))),
        "one_skeleton_already_satisfies_d_squared_zero": True,
        "H1_without_mixed_cell": 1,
        "d_squared_forces": (
            "the edge debt z is closed and primitive; it does not force z "
            "to be a boundary"
        ),
        "mixed_cell_existence_forced_by_d_squared": False,
        "extra_hypothesis_which_forces_existence": (
            "derived naturality, mapping-square exactness, or an explicit "
            "source 2-cell kappa with d(kappa)=z"
        ),
        "normalized_boundary_if_existence_is_granted": [1, -1, 1, -1],
        "orientation_ambiguity": "simultaneous sign only",
    }


def old_cap_columns():
    diagonal = []
    for corner in range(4):
        basis = tuple(Q(1) if index == corner else Q(0)
                      for index in range(4))
        diagonal.append(basis + basis)
    companions = []
    for positive in (0, 1):
        for negative in (2, 3):
            edge = tuple(Q(1) if index in (positive, negative) else Q(0)
                         for index in range(4))
            companions.append(edge + ZERO4)
    return tuple(diagonal + companions)


def augmentation_audit():
    private_eq = load(
        "computations/verify_h3_balanced_square_private_eq_projection_gate.py",
        "cross_word_d2_private_eq",
    )
    pinned = private_eq.projection_audit()
    require(pinned["old_projection_rank"] == 7
            and pinned["criterion"] == "delta dot (B-Eq) is nonzero",
            "the pinned B/Eq theorem changed")

    edges, d1_square, z = square_data()
    # D1 on C1(square) direct-sum A_BEq is [d1_square | 0].
    d1_total = tuple(d1_square[row] + ZERO8 for row in range(4))
    psi = DELTA + tuple(-value for value in DELTA)
    b_delta = DELTA + ZERO4
    eq_delta = ZERO4 + DELTA
    tied_delta = DELTA + DELTA

    # Check d^2 on a basis of every possible terminal augmentation.  Since
    # d is zero on A_BEq, d^2(kappa)=d1(z,a)=d1_square*z for all a.
    augmentation_basis = tuple(
        tuple(Q(1) if row == column else Q(0) for row in range(8))
        for column in range(8)
    )
    test_augmentations = (ZERO8, b_delta, eq_delta, tied_delta,
                          *augmentation_basis)
    for augmentation in test_augmentations:
        d2_kappa = z + augmentation
        require(matvec(d1_total, d2_kappa) == ZERO4,
                ("augmentation entered d^2", augmentation))

    require(dot(psi, ZERO8) == 0
            and dot(psi, b_delta) == 4
            and dot(psi, eq_delta) == -4
            and dot(psi, tied_delta) == 0,
            "the dark/bright augmentation controls changed")

    # These two exact totalizations have the same source boundary z and all
    # the same off-grade db01/dL01 faces, yet distinct terminal charge.
    dark_boundary = z + ZERO8
    bright_boundary = z + b_delta
    require(dark_boundary[:4] == bright_boundary[:4] == z
            and matvec(d1_total, dark_boundary) == ZERO4
            and matvec(d1_total, bright_boundary) == ZERO4,
            "the two-filler counterguard stopped sharing its source boundary")
    return {
        "projected_total_complex": (
            "C2=<kappa> -> C1(square) direct_sum A_BEq -> C0(vertices), "
            "with d(kappa)=(z,a) and d|A_BEq=0"
        ),
        "d_squared_condition_on_a": "none: every a in Q^8 is allowed",
        "known_db01_dL01_B_Eq_images": {
            "six_db01": "six copies of zero_8",
            "eighteen_dL01": "eighteen copies of zero_8",
        },
        "same_source_boundary_counterguard": {
            "dark_filler": {"a": [0] * 8, "chi": 0, "Psi": 0},
            "bright_filler": {
                "a": list(map(int, b_delta)), "chi": 4, "Psi": 1,
            },
            "both_have_boundary_z": list(map(int, z)),
            "both_satisfy_d_squared_zero": True,
        },
        "other_controls": {
            "Eq_only_delta": {"chi": -4, "Psi": -1},
            "tied_B_Eq_delta": {"chi": 0, "Psi": 0},
        },
        "forced_exact_delta_B_minus_Eq_value": None,
        "reason": (
            "mixed-incidence coefficient one and terminal B/Eq augmentation "
            "are independent coordinates"
        ),
    }


def quotient_audit():
    old = old_cap_columns()
    psi = DELTA + tuple(-value for value in DELTA)
    b_delta = DELTA + ZERO4
    require(rank(old) == 7
            and all(dot(psi, column) == 0 for column in old)
            and dot(psi, b_delta) == 4,
            "the old cap quotient changed")

    # ker(psi) and span(old) both have dimension seven, hence agree.  For
    # every augmentation a, lambda=psi(a)/4 is its unique quotient class.
    # Verify the normal form on a basis, which proves it linearly on Q^8.
    basis = tuple(
        tuple(Q(1) if row == column else Q(0) for row in range(8))
        for column in range(8)
    )
    normal_forms = []
    for augmentation in basis:
        lam = dot(psi, augmentation) / Q(4)
        residual = tuple(value - lam * base
                         for value, base in zip(
                             augmentation, b_delta, strict=True))
        require(dot(psi, residual) == 0
                and rank(old + (residual,)) == rank(old),
                ("the quotient normal form failed", augmentation, lam))
        normal_forms.append(str(lam))

    # The packaging quotient independently records that the mixed cell is a
    # new third direction.  It does not identify that direction with Psi.
    require(rank(((Q(1), Q(0), Q(0), Q(0)),
                  (Q(0), Q(1), Q(0), Q(0)))) == 2
            and rank(((Q(1), Q(0), Q(0), Q(0)),
                      (Q(0), Q(1), Q(0), Q(0)),
                      (Q(0), Q(0), Q(1), Q(0)))) == 3,
            "the abstract packaging rank changed")
    return {
        "old_B_Eq_dimension": 8,
        "old_cap_rank": rank(old),
        "old_cap_cokernel_dimension": 1,
        "primitive_unnormalized_detector": "chi=delta.(B-Eq)",
        "normalized_detector": "Psi=chi/4",
        "unique_normal_form_modulo_old_cap_rows": (
            "a congruent to lambda*(delta,0), lambda=chi(a)/4"
        ),
        "basis_normal_form_lambdas": normal_forms,
        "set_of_d_squared_compatible_values_over_Q": "chi=4*lambda, lambda arbitrary in Q",
        "existence_normalization": (
            "if a mixed filler is granted, d(kappa)=z fixes its square-"
            "incidence coefficient to one up to orientation"
        ),
        "augmentation_normalization": (
            "not fixed; an additional physical cap/descent readout theorem "
            "must specify lambda"
        ),
        "terminal_fork": (
            "lambda=0 conserves Psi; lambda!=0 breaks/fills the unique B/Eq "
            "quotient projection-wise"
        ),
    }


def hypothesis_audit():
    augmented = load(
        "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py",
        "cross_word_d2_augmented_p2",
    )
    independence = augmented.homogeneous_face_independence()
    require(independence["raw_face_rank"] == 7
            and not independence["P_f_implies_primitive_p"],
            "the independent augmented-face theorem changed")
    return {
        "what_the_assumed_top_and_PP_faces_supply": [
            "the top cross-word edge",
            "its literal db01 and dL01 response boundaries",
            "the primitive closed square debt z after objectwise K_Eq edges",
        ],
        "what_they_do_not_supply": [
            "a source 2-cell bounding z",
            "the primitive cap face p",
            "physical K_Eq/invisible-cap descent n",
            "a B/Eq augmentation class lambda",
        ],
        "shortest_existence_hypothesis": (
            "the top extends to a pointed derived-natural PP mapping "
            "cylinder whose square 2-cell has boundary z"
        ),
        "shortest_forced_augmentation_hypothesis": (
            "in addition, give a physical source-labelled cap/K_Eq descent "
            "law computing Pi_BEq(kappa) modulo the old cap image"
        ),
        "one_scalar_form_of_the_extra_law": (
            "specify lambda=Psi(Pi_BEq(kappa)); the exact value is then "
            "chi=4*lambda"
        ),
        "nonzero_terminal_landing_condition": "lambda != 0",
        "primitive_B_only_convention_if_separately_proved": (
            "Pi_BEq(kappa)=(delta,0) modulo old rows, hence chi=4 and Psi=1"
        ),
    }


def run(mode: str) -> str:
    pin_dependencies()
    ledger = {}
    if mode in ("all", "boundary"):
        ledger["square_boundary_and_existence"] = boundary_audit()
    if mode in ("all", "augmentation"):
        ledger["d_squared_augmentation_counterguard"] = augmentation_audit()
    if mode in ("all", "quotient"):
        ledger["private_Eq_affine_quotient"] = quotient_audit()
    if mode in ("all", "hypotheses"):
        ledger["sharp_additional_hypotheses"] = hypothesis_audit()
    if mode == "all":
        ledger["theorem"] = (
            "cross-word PP mapping-cylinder d-squared existence and "
            "augmentation freedom gate"
        )
        ledger["verdict"] = (
            "The proposed d^2-forcing statement is false twice.  The edge "
            "data force a primitive closed square debt z but not a mixed "
            "source 2-cell; the square one-skeleton already has d^2=0 and "
            "H1=Q.  After a filler is separately granted, d^2 fixes its "
            "square boundary to z but leaves its B/Eq augmentation arbitrary. "
            "Modulo old cap rows the exact freedom is lambda in Q, with "
            "delta.(B-Eq)=4 lambda."
        )
        ledger["scope"] = (
            "exact rational minimal mapping-square and terminal B/Eq quotient, "
            "with the committed six db01 and eighteen dL01 zero projections. "
            "The two augmented fillers are logical chain-level counterguards; "
            "the bright one is not claimed to be an already constructed "
            "physical source cell."
        )
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if mode == "all" and EXPECTED_DIGEST != "TO_BE_FROZEN":
        require(digest == EXPECTED_DIGEST,
                ("cross-word d2/augmentation ledger changed", digest))
    print(f"h3 cross-word mapping-cylinder d2 gate ({mode}): PASS")
    if mode in ("all", "boundary"):
        print("d^2 forces closed square debt, not a mixed-cell filler")
    if mode in ("all", "augmentation"):
        print("same source boundary z admits chi=0 and chi=4 augmentations")
    if mode in ("all", "quotient"):
        print("mod old cap rows: chi=4*lambda, lambda arbitrary over Q")
    if mode in ("all", "hypotheses"):
        print("forced value needs an additional physical cap/descent law")
    print("ledger_sha256=" + digest)
    return digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("all", "boundary", "augmentation", "quotient", "hypotheses"),
        default="all",
    )
    arguments = parser.parse_args()
    run(arguments.mode)


if __name__ == "__main__":
    main()
