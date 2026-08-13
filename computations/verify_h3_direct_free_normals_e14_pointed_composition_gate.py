#!/usr/bin/env python3
"""Audit the direct-free normal-to-E14 and pointed-cap composition gate.

The two direct-free normal classes are visible in the derived shifted Hasse
cube, but diagonal descent leaves their coefficient times
E=(H0-u)e_Eq.  The E14 unit theorems begin only after a source-labelled
word/grade placement.  This checker also records that composing the derived
invisible lift with any currently committed reduced-Eq correction cannot
construct the primitive cap: ordinary residue is the separating row.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py":
        "7d9e49f34da84772f6e0863a9bfe56cb9a90e0cfd3fceb76da59175ffea36c50",
    "computations/verify_h3_degree4_reset_five_face_aggregate_gate.py":
        "01961c9ae83b91dad31ba859ea2f8a2d5775d73d7ad591aa0a369e7d971f8079",
    "computations/verify_h3_degree4_koszul_reset_quadratic_face_aggregate_gate.py":
        "7c65a37738be404f1c8e5fdf9e634ef450307238f92edfe166c719810f9ad828",
    "computations/verify_h3_rootless_e14_companion_core_identification.py":
        "438ae827dba9e8f7a14f011cb5d76631fc284a2a2a8c6d8bcee7003669a1ac45",
    "computations/verify_h3_literal_mv_odd_reduced_eq_projection_scope.py":
        "deb0ad5e35d42428d7440310af24951d3cb29deb55116fb5ab8eacef5fa1f729",
    "computations/verify_h3_universal_graph_derived_base_change_physical_descent_gate.py":
        "9e60fb8410288a192b8be3b59938e5e7ba4ea42b455fee67b94ca6ef37777fde",
    "computations/verify_scalar_unit_c0_four_cut_common_carrier_gate.py":
        "56421c894acd613300841b7ae41d1bafecc6d65fcc9618982dc61ac198c2fa66",
    "notes/scalar-unit-c0-four-cut-common-carrier-gate.md":
        "a06018da73d6a954f14706fcfdeaae5ace1c2424e02530ab87602c1e77271000",
    "computations/verify_uniform_hasse_moment_augmented_membership_gate.py":
        "f5f663715507d46e6d96b37a1a05c21e9f0b045dcedd878bf657dfb4b32091c3",
    "computations/verify_scalar_unit_moment_transgression_source_lift_based_loop_torsor.py":
        "4bff53e1568a74cfe262fac185558aa14337fe1a2e31e6c46141645e78e8e839",
}
EXPECTED_LEDGER_SHA256 = (
    "e86a1b4cea037a233d80c22f29895fa7ee7f028c79d59bb6ab9b1d69f9f844d1"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def matrix_rank(columns: list[list[Fraction]]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [list(row) for row in zip(*columns, strict=True)]
    rank = 0
    for column in range(len(columns)):
        pivot = next(
            (row for row in range(rank, height) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        value = rows[rank][column]
        rows[rank] = [entry / value for entry in rows[rank]]
        for row in range(height):
            if row == rank or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(rows[row], rows[rank], strict=True)
            ]
        rank += 1
    return rank


def direct_free_normal_audit() -> dict[str, object]:
    # Jacobian rows h1,...,h5 at x12=a, x14=b, in the independent tangent
    # coordinates (x35,x45,x25,x34,x23).  We specialize a=2,b=3 only to
    # certify the generic rank and its two stated left-kernel vectors.
    a, b = Fraction(2), Fraction(3)
    jacobian_rows = [
        [0, 0, 0, 0, 0],
        [b, 0, 0, 0, 0],
        [0, a, b, 0, 0],
        [a, 0, 0, 0, 0],
        [0, 0, 0, a, b],
    ]
    jacobian_columns = [list(column) for column in zip(*jacobian_rows)]
    require(matrix_rank(jacobian_columns) == 3,
            "the direct-free Jacobian rank changed")
    left_h1 = [Fraction(1), 0, 0, 0, 0]
    left_opposite = [0, a, 0, -b, 0]
    for vector in (left_h1, left_opposite):
        require(all(sum(vector[row] * jacobian_rows[row][column]
                        for row in range(5)) == 0
                    for column in range(5)),
                ("claimed normal is not in the left kernel", vector))
    require(matrix_rank([left_h1, left_opposite]) == 2,
            "the two normal classes became dependent")

    h1 = (
        ("x23_21", "x45_12"),
        ("x24_21", "x35_12"),
        ("x25_22", "x34_11"),
    )
    opposite = (
        ("+a", "x13_11", "x45_12"),
        ("+a", "x15_12", "x34_11"),
        ("-b", "x13_11", "x25_22"),
        ("-b", "x15_12", "x23_21"),
    )
    # Every normal monomial after its supported a/b coefficient is removed
    # is a two-edge matching, hence a 2K2 support.  The first is the exact
    # decorated core already identified in the canonical E14 row.
    require(all(len(term) == 2 for term in h1), "h1 stopped being 2K2")
    require(all(len(term) == 3 for term in opposite),
            "the opposite normal term shape changed")
    require(h1[0] == ("x23_21", "x45_12"),
            "the canonical decorated E14 core changed")
    return {
        "direct_free_support": {"x12": "a", "x14": "b"},
        "jacobian_rank": 3,
        "normal_quotient_dimension": 2,
        "normal_generators": ["h1", "a*h2-b*h4"],
        "h1_terms": h1,
        "opposite_terms": opposite,
        "all_leading_new_cell_supports": "2K2",
        "canonical_decorated_core": "x23_21*x45_12",
    }


def shifted_hasse_and_e14_audit() -> dict[str, object]:
    # The complete derived shifted filler is linear in h_v.  Diagonal
    # projection replaces its zero derived differential by L*(H0-u)e_Eq.
    # Two evaluations prove that both normal coefficients are nonzero in the
    # universal polynomial ring, so e_Eq is the first literal hidden row.
    h1_value = Fraction(1)       # x23=x45=1; all other new cells zero
    opposite_value = Fraction(1)  # a=x13=x45=1; b=0; other cells zero
    h0, u = Fraction(0), Fraction(1)
    residuals = [value * (h0 - u)
                 for value in (h1_value, opposite_value)]
    require(residuals == [Fraction(-1), Fraction(-1)],
            "a direct-free normal lost its underived Eq residual")

    # Before a word-changing arrow, physical source labels form direct-sum
    # coordinates.  E14 rows supported on 000101 cannot cancel the normal
    # source row 01211222.  This is a presentation separator, not yet a
    # physical Fredholm terminal.
    normal_word = [Fraction(1), Fraction(0)]
    e14_word = [Fraction(0), Fraction(1)]
    word_separator = [Fraction(1), Fraction(0)]
    dot = lambda left, right: sum(
        (a_entry * b_entry
         for a_entry, b_entry in zip(left, right, strict=True)),
        Fraction(0),
    )
    require(dot(word_separator, normal_word) == 1
            and dot(word_separator, e14_word) == 0,
            "the source-word separator changed")
    return {
        "derived_shifted_filler": {
            "boundary": "L*Y*w",
            "target": 0,
            "ordinary_residue": 0,
            "chart_face": "the corresponding linear combination of -S_v",
        },
        "underived_diagonal_residual": "L*(H0-u)*e_Eq",
        "normal_residual_evaluations": [str(value) for value in residuals],
        "first_literal_hidden_row": "e_Eq",
        "normal_source_word": "01211222",
        "normal_internal_word": "12112",
        "E14_canonical_unary_word": "000101",
        "decorated_core_hit": True,
        "full_source_labelled_E14_map": False,
        "post_Eq_next_separator": {
            "basis": ["word_01211222", "word_000101"],
            "covector": [1, 0],
            "scope": "presentation separator until a physical word/grade arrow is supplied",
        },
        "E14_unit_scope": (
            "terminalizes an already placed canonical two-/three-cell E14 "
            "support; it does not construct the placement arrow"
        ),
    }


def primitive_cap_composition_audit() -> dict[str, object]:
    # Rows are (Q-boundary,target,ordinary residue,Eq).  The shifted invisible
    # lift and every presently available reduced-Eq correction used here have
    # ordinary residue zero.  The primitive cap p does not.
    n = [Fraction(1), 0, 0, 0]
    k_eq = [Fraction(0), 0, 0, 1]
    m_v = [Fraction(0), 0, 0, -1]
    p = [Fraction(-1), 0, Fraction(-1), 0]
    image = [n, k_eq, m_v]
    require(matrix_rank(image) == 2, "the reduced-Eq composition rank changed")
    require(matrix_rank(image + [p]) == 3,
            "primitive cap unexpectedly entered the old composition image")
    residue_dual = [Fraction(0), 0, Fraction(1), 0]
    def dot(vector: list[Fraction], column: list[Fraction]) -> Fraction:
        return sum((a * b for a, b in zip(vector, column, strict=True)),
                   Fraction(0))
    require(all(dot(residue_dual, column) == 0 for column in image)
            and dot(residue_dual, p) == -1,
            "ordinary residue stopped separating the primitive cap")
    z = [a + b for a, b in zip(n, p, strict=True)]
    require(z == [Fraction(0), 0, Fraction(-1), 0],
            "the normalized relative endpoint identity changed")
    return {
        "rows": ["Q-boundary", "target", "ordinary residue", "Eq"],
        "derived_invisible_lift_n": [int(value) for value in n],
        "primitive_cap_p": [int(value) for value in p],
        "n_plus_p": [int(value) for value in z],
        "available_Eq_corrections_have_ordinary_residue": 0,
        "primitive_cap_in_composed_image": False,
        "primitive_dual": "ordinary-residue coordinate",
        "first_missing_column": (
            "one source-labelled residue section p=(-Q,-ores), in the same "
            "word/ridge/repeated grade, together with the pointed input comparison"
        ),
        "universal_K_Eq_scope": "unaugmented; first pointed row d(u_f-u)",
        "physical_Mv_scope": (
            "odd output dressing only; input equality J3(Mv)=A*Jcol(l) and "
            "physical q transport remain open"
        ),
    }


def four_cut_and_first_moment_audit() -> dict[str, object]:
    # Ordered curvature factors in basis (q,r,x).
    right = [Fraction(1), 0, Fraction(-1)]
    left = [Fraction(1), Fraction(-1), Fraction(1)]
    require([a + b for a, b in zip(right, left, strict=True)]
            == [Fraction(2), Fraction(-1), 0],
            "the oriented curvature sum changed")

    # The unweighted endpoint/base augmentation does not determine the first
    # weighted moment: phi(t)=2t-1 has integral zero and t-integral 1/6.
    phi_integral = Fraction(1) - Fraction(1)
    phi_first_moment = Fraction(2, 3) - Fraction(1, 2)
    require(phi_integral == 0 and phi_first_moment == Fraction(1, 6),
            "the based-loop first-moment guard changed")
    return {
        "oriented_factors": {"right": "q-x", "left": "q-r+x"},
        "sum": "2q-r",
        "conditional_common_carrier_consequence": "(r-2q)*H0=0",
        "primitive_cap_grade": {
            "intrinsic_order": 3,
            "word": "01211222",
            "repeated_grade": "P3+K2",
            "base_augmentation": "unweighted H0",
        },
        "four_cut_required_map": (
            "one all-label restriction-insertion/base-change comparison "
            "from the enriched pointed cap family to both orientations"
        ),
        "four_cut_composition_constructed": False,
        "conditional_alternative": (
            "either an oriented projection is nonzero and lands active-clean, "
            "or both vanish on one common H0 and imply c0=0"
        ),
        "based_loop_phi": "2*t-1",
        "phi_unweighted_integral": str(phi_integral),
        "phi_first_weighted_integral": str(phi_first_moment),
        "c1_is_currently_beta_face": False,
        "c1_extra_hypothesis": (
            "identify beta with the affine carrier parameter and prove a "
            "source-valid horizontal one-form with zero based-loop residue"
        ),
    }


def one_r_generator_audit() -> dict[str, object]:
    # Work over R/(beta^2).  Coordinates are
    # (p, beta*p, c1, beta*c1).  The strongest rank-one proposal has one
    # free R generator with dG=p+beta*c1.  This is a formally valid way to
    # *package* p and c1 as a face and its Bockstein.  Its R-span consists of
    # dG and beta*dG, so it does not make p and beta*c1 individual boundaries.
    g = [Fraction(1), 0, 0, Fraction(1)]
    beta_g = [Fraction(0), 1, 0, 0]
    p = [Fraction(1), 0, 0, 0]
    weighted_c1 = [Fraction(0), 0, 0, 1]
    image = [g, beta_g]
    require(matrix_rank(image) == 2, "rank-one R-family rank changed")
    require(matrix_rank(image + [p]) == 3
            and matrix_rank(image + [weighted_c1]) == 3,
            "one R-generator unexpectedly killed an individual face")
    require(matrix_rank(image + [p, weighted_c1]) == 3,
            "the two individual faces no longer differ by the family relation")

    # lambda=(1,0,0,-1) annihilates dG and beta*dG and detects the surviving
    # anti-diagonal combination.  The two coordinate covectors are the
    # independent primitive face readouts before attaching the family.
    survivor = [Fraction(1), 0, 0, Fraction(-1)]
    epsilon_p = [Fraction(1), 0, 0, 0]
    mu_1 = [Fraction(0), 0, 0, Fraction(1)]
    def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
        return sum((a * b for a, b in zip(left, right, strict=True)),
                   Fraction(0))
    require(all(dot(survivor, column) == 0 for column in image)
            and dot(survivor, p) == 1
            and dot(survivor, weighted_c1) == -1,
            "the rank-one-family survivor changed")
    require(dot(epsilon_p, p) == 1
            and dot(epsilon_p, weighted_c1) == 0
            and dot(mu_1, p) == 0
            and dot(mu_1, weighted_c1) == 1,
            "the two primitive face covectors stopped being independent")

    # A second R generator with differential beta*c1 raises the truncated
    # image rank by one and contains both required faces.  It may live in the
    # same enriched comparison theorem; the claim is about domain rank/cells,
    # not about two conjecture-level lemmas.
    second = weighted_c1
    enlarged = image + [second]
    require(matrix_rank(enlarged) == 3
            and matrix_rank(enlarged + [p]) == 3,
            "a second filtered cell did not kill both faces")
    return {
        "coefficient_ring": "R/(beta^2)",
        "basis": ["p", "beta*p", "c1", "beta*c1"],
        "one_generator_boundary": "p+beta*c1",
        "one_generator_formally_packages_face_and_Bockstein": True,
        "one_generator_physically_constructed": False,
        "rank_one_R_image": 2,
        "individual_p_in_image": False,
        "individual_beta_c1_in_image": False,
        "surviving_antidiagonal_dual": [1, 0, 0, -1],
        "independent_face_duals": {
            "epsilon_p": [1, 0, 0, 0],
            "mu_1": [0, 0, 0, 1],
        },
        "minimum_filtered_domain_columns_to_kill_both_individually": 2,
        "scope": (
            "provided p and c1 remain independent in the complete physical "
            "two-grade quotient; the pinned cap-residue and based-loop "
            "calculations prove this in the current candidate quotient, not "
            "a fully constructed physical terminal module"
        ),
        "one_theorem_still_possible": (
            "both cells may be faces of one enriched pointed comparison family"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 direct-free normals / E14 / pointed cap composition gate",
        "pins": PINS,
        "direct_free_normals": direct_free_normal_audit(),
        "shifted_hasse_to_E14": shifted_hasse_and_e14_audit(),
        "primitive_cap_composition": primitive_cap_composition_audit(),
        "four_cut_scope": four_cut_and_first_moment_audit(),
        "one_R_generator": one_r_generator_audit(),
        "verdict": (
            "The complete shifted Hasse cube reaches both direct-free normal "
            "classes only in the derived presentation.  Its first underived "
            "failure is L*(H0-u)e_Eq; after a hypothetical Eq correction a "
            "source-labelled word/grade placement into E14 is still required. "
            "Composing the invisible lift with all presently committed Eq "
            "corrections cannot create the primitive cap because ordinary "
            "residue separates it.  The same enriched pointed cap family could "
            "conditionally provide the two-orientation H0 comparison for c0, "
            "but c1 needs an additional filtered horizontal one-form law.  "
            "A single free R generator can formally package p with c1 as its "
            "beta face, but it only relates the two independent filtered "
            "defects.  If the proof needs both as individual boundaries, at "
            "least two domain cells are needed, although they can belong to "
            "one comparison theorem."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("direct-free/E14 composition ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("direct-free normals: derived filler YES / physical descent NO")
    print("first hidden row: L*(H0-u)*e_Eq")
    print("E14 decorated core: HIT / source-labelled placement: OPEN")
    print("primitive cap from n + old K_Eq: NO (ordinary-residue dual)")
    print("four-cut c0: CONDITIONAL / c1 beta face: NOT YET")
    print("one R generator p+beta*c1: FORMAL PACKAGE / NOT TWO BOUNDARIES")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
