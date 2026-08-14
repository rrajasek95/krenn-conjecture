#!/usr/bin/env python3
"""Project the five degree-four reset Eq residuals toward kappa_AB/kappa_AC.

The five derived reset fillers leave h_v*(H0-u)*e_Eq under physical descent.
Here e_Eq is a central conormal row.  It is not one of the four cornerwise
Eq_j rows in the private-minus-Eq quotient, and the raw h_v coefficient is
in the squarefree 2K2 grade rather than the repeated P3+K2 grade of the
cross-word mixed naturality cells.  Hence the literal projection of all
five reset cells to kappa_AB/kappa_AC is zero/off-grade.

Even granting an operation-blind diagonal placement sends the central Eq
row to (1,1,1,1), whose delta augmentation is zero.  A nonzero projection
would require the still missing source-labelled K_Eq/cross-word comparison.
If that comparison sends e_Eq to a corner vector e_kappa, the exact value
on the v-th reset cell is -h_v*delta.e_kappa.  The complete-intersection
theorem proves that denominator-only Koszul syzygies cannot turn the h_v
coefficients into a primitive unit aggregate.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_degree4_reset_five_face_aggregate_gate.py":
        "01961c9ae83b91dad31ba859ea2f8a2d5775d73d7ad591aa0a369e7d971f8079",
    "notes/h3-degree4-reset-five-face-aggregate-gate.md":
        "5a19c7b8bfb21cb0c76532accb3af1f0ea4cdb6b13fa6b500124f77f61395100",
    "computations/verify_h3_five_denominator_hafnians_complete_intersection.py":
        "4c87c1db939346e8f1d83a26b5edef19e3143a65cc6d6fd5ea636f99d13b5615",
    "notes/h3-five-denominator-hafnians-complete-intersection.md":
        "6ad68e8d26f6e7132857a4c92819eb28133be4562ea76ad63adb09620d1d6646",
    "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py":
        "7d9e49f34da84772f6e0863a9bfe56cb9a90e0cfd3fceb76da59175ffea36c50",
    "notes/h3-shifted-denominator-chart-filler-augmented-commutator.md":
        "1d89c1e592fdc723bb58b1b75e2ba846b812401efad33c8cd88d4265dc0a7743",
    "computations/verify_h3_reduced_eq_spencer_three_projection_gate.py":
        "315508b572fa0d96b33ba83b8ac4905e59dfbf8f484023891618dbb3c6489d83",
    "notes/h3-reduced-eq-spencer-three-projection-gate.md":
        "a3ee90d506f00aa8059e2272dba7992b2348d6187b990aaff27cbc62e92b0071",
    "computations/verify_h3_four_site_full_source_exhaustiveness_decomposition_gate.py":
        "269a1b775e0790c3e4f1f6390b83673c1118270e491885ce9383e703f07b3278",
    "notes/h3-four-site-full-source-exhaustiveness-decomposition-gate.md":
        "703da478db0e60c53f98bdd4835248172872b7412eb884a60d08ac14bef1fb4e",
}
EXPECTED_LEDGER_SHA256 = "f193da45cec98df29ef60c808ba7ba728bd3466df620aa51b59fa84a5ea2bb2f"

DELTA = tuple(map(Q, (1, 1, -1, -1)))
ONE4 = tuple(map(Q, (1, 1, 1, 1)))


def require(condition: bool, detail: object) -> None:
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
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def be_vector(*, B=(0, 0, 0, 0), Eq=(0, 0, 0, 0)):
    return tuple(map(Q, B + Eq))


def chi(value) -> Q:
    return dot(DELTA + scale(-1, DELTA), value)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def pinned_note_claims_audit() -> dict[str, object]:
    reset_note = (ROOT / "notes/h3-degree4-reset-five-face-aggregate-gate.md").read_text()
    ci_note = (ROOT / "notes/h3-five-denominator-hafnians-complete-intersection.md").read_text()
    eq_note = (ROOT / "notes/h3-reduced-eq-spencer-three-projection-gate.md").read_text()
    decomposition_note = (ROOT / (
        "notes/h3-four-site-full-source-exhaustiveness-decomposition-gate.md"
    )).read_text()
    require("h_v(H_0-u)e_{\\rm Eq}" in reset_note
            and "full_word" not in reset_note
            and "form a complete intersection" in ci_note
            and "height five" in ci_note
            and "Betti numbers" in ci_note
            and "same physical source grade" not in eq_note
            and "different parity, word, endpoint, and repeated-label grades"
                in eq_note
            and "chi(\\kappa)=-\\delta\\cdot e_\\kappa" in decomposition_note,
            "a pinned note no longer states the required scope guard")
    return {
        "reset_note_pinned": True,
        "complete_intersection_note_pinned": True,
        "reset_underived_residual": "h_v*(H0-u)*e_Eq",
        "complete_intersection_consequence": (
            "all denominator-only first syzygies are Koszul and have no "
            "primitive unit face coefficient"
        ),
        "reduced_Eq_scope": (
            "common conormal polynomial, but different physical source grades"
        ),
    }


def complete_intersection_audit(ci, reset) -> dict[str, object]:
    # Rebuild the exact five generators using the dependency's own routines.
    faces = reset.denominator_faces()
    generators = []
    for site in range(1, 6):
        terms = []
        for monomial, coefficient in faces[site].items():
            require(coefficient == 1, (site, monomial, coefficient))
            terms.append((1, monomial))
        generators.append(ci.poly(*terms))
    basis = ci.buchberger(generators)
    require(all(not ci.normal_form(ci.s_polynomial(left, right), basis)
                for left_index, left in enumerate(basis)
                for right in basis[left_index + 1:]),
            "Buchberger criterion changed")
    leading = [ci.leading(value)[0] for value in basis]
    height, cover = ci.minimal_vertex_cover_size(leading)
    require(len(generators) == height == 5,
            ("the denominator CI height changed", height))
    betti = [1, 5, 10, 10, 5, 1]
    return {
        "variables": len(ci.VARS),
        "generators": len(generators),
        "terms_per_generator": [len(value) for value in generators],
        "groebner_basis_size": len(basis),
        "height": height,
        "minimum_initial_vertex_cover": list(cover),
        "regular_sequence": True,
        "koszul_betti_numbers": betti,
        "first_syzygy_generators": 10,
        "first_syzygy_type": "h_i*e_j-h_j*e_i",
        "primitive_unit_aggregate_from_denominator_only": False,
    }


def five_reset_cells_audit(reset, shifted, eq_spencer) -> dict[str, object]:
    faces = reset.denominator_faces()
    all_monomials = [monomial for face in faces.values() for monomial in face]
    require(len(faces) == 5
            and all(len(face) == 3 for face in faces.values())
            and len(all_monomials) == len(set(all_monomials)) == 15,
            "the five mixed h_v supports changed")

    shifted_ledger, shifted_digest = shifted.audit()
    eq_ledger, eq_digest = eq_spencer.audit()
    require(shifted_digest == "bdcc6a2734c3bd31f060d56fd88f8f5344f39e43aed03f70f18cfa65eef74b92"
            and eq_digest == "ad0fa899252ab48d5df1eb868b1492ecc07619c05cc976fe73526fdfa7fceee3",
            "a reset/Eq ledger changed")
    initial = shifted_ledger["initial_layer"]
    derived = shifted_ledger["two_direction_derived_filler"]
    qzero = shifted_ledger["qzero_top"]
    conormal = eq_ledger["pinned_conormal_identifications"]
    require(initial["target"] == initial["ordinary_residue"] == 0
            and initial["isolated_underived_commutator"]
                == "h_v*(H_0-u)*eq"
            and derived["target"] == derived["ordinary_residue"] == 0
            and not qzero["underived_source_descent"]
            and conormal["universal_conormal"] == "E=(H0-u)e_Eq"
            and not conormal["same_physical_source_grade"],
            (initial, derived, qzero, conormal))
    return {
        "mixed_internal_word": "12112",
        "full_augmented_word": "01211222",
        "cells": 5,
        "matching_terms_per_h_v": 3,
        "distinct_quadratic_matching_terms": len(set(all_monomials)),
        "raw_coefficient_site_type": "2K2; four internal sites occur once",
        "derived_boundary": "h_v*Y*w",
        "derived_target": derived["target"],
        "derived_ordinary_residue": derived["ordinary_residue"],
        "chart_face": initial["chart_face"],
        "corrected_chart_face": initial["corrected_subtraction"],
        "underived_residual": "h_v*(H0-u)*e_Eq",
        "underived_source_descent_constructed": qzero[
            "underived_source_descent"],
        "physical_augmentation_guard": (
            "target and ordinary residue vanish in the derived filler, but "
            "the missing physical comparison must still totalize word, "
            "repeated grade, ridge, labelled residue, W, anchor, q, eta, "
            "and sigma"
        ),
    }


def literal_kappa_projection_audit(decomposition) -> dict[str, object]:
    # The reset Eq row is a central scalar row indexed by deletion face v.
    # Kappa is indexed by a root label (AB/AC), a DQ/PS operation mate, and
    # the repeated P3+K2 cap grade.  With all labels retained, the Hom block
    # between these objects is zero until K_Eq/cross-word placement is built.
    require(decomposition.DELTA == DELTA
            and len(decomposition.CROSS_EDGES) == 4,
            "the kappa decomposition changed")
    records = []
    for site in range(1, 6):
        records.append({
            "reset_face": f"h_{site}*(H0-u)*e_Eq",
            "source_index": f"deletion site {site}",
            "word": "01211222",
            "raw_repeated_grade": "2K2",
            "operation_parent": "central reset/Eq; no DQ/PS corner label",
            "root_label": "none",
            "projection_to_kappa_AB": "0 (literal direct-sum projection)",
            "projection_to_kappa_AC": "0 (literal direct-sum projection)",
            "chi": "0 in the current typed map",
        })
    return {
        "kappa_required_grade": "repeated P3+K2 after a physical incident-cell lift",
        "kappa_required_labels": [
            "root A/B or A/C",
            "one of four DQ/PS operation mates",
            "corner-resolved Eq_0,...,Eq_3 incidence",
        ],
        "reset_cells": records,
        "literal_projection_rank_to_two_kappas": 0,
        "verdict": (
            "same cap word is insufficient: raw repeated grade, operation "
            "parent, root label, and corner-resolved Eq row all differ"
        ),
    }


def diagonal_and_missing_lift_controls_audit(reset, eq_spencer) \
        -> dict[str, object]:
    # An operation-blind placement of the central Eq row is necessarily the
    # constant vector.  It is delta-dark.  The generic-even formal shadow
    # also has a delta-dark four-entry root coefficient, but it remains in a
    # different label module.
    require(dot(DELTA, ONE4) == 0,
            "the diagonal Eq placement became bright")
    diagonal_eq_only = be_vector(Eq=ONE4)
    tied_arbitrary = be_vector(B=DELTA, Eq=DELTA)
    generic_even_D = tuple(map(Q, (-1, 1, -1, 1)))
    require(chi(diagonal_eq_only) == 0
            and chi(tied_arbitrary) == 0
            and dot(DELTA, generic_even_D) == 0,
            "a formal tied/operation-blind control became bright")

    eq_ledger, _digest = eq_spencer.audit()
    cone = eq_ledger["universal_mapping_cone"]
    require(cone["formal_three_projection_unification"]
            and not cone["physical_three_projection_cell_constructed"],
            cone)

    faces = reset.denominator_faces()
    symbolic = []
    for site, face in faces.items():
        symbolic.append({
            "site": site,
            "coefficient": f"h_{site}",
            "if_missing_lift_sends_e_Eq_to_e_kappa":
                f"chi=-h_{site}*delta.e_kappa",
            "quadratic_terms": len(face),
        })
    return {
        "strongest_operation_blind_diagonal_Eq_lift": [1, 1, 1, 1],
        "diagonal_delta_Eq": "0",
        "diagonal_chi": "0",
        "tied_B_equals_Eq_control_chi": "0",
        "generic_even_formal_root_vector": [-1, 1, -1, 1],
        "generic_even_delta_pairing": "0",
        "formal_common_K_Eq_cone_exists": True,
        "physical_common_K_Eq_cone_constructed": False,
        "only_possible_nonzero_formula_after_new_lift": symbolic,
        "aggregate_formula": (
            "chi(sum_v reset_v)=-(sum_v h_v)*delta.e_kappa"
        ),
        "why_not_primitive": (
            "the h_v form a height-five complete intersection; every "
            "denominator-only first syzygy is Koszul with coefficients in "
            "(h_1,...,h_5), so no unit aggregate is forced"
        ),
    }


def exact_physical_frontier_audit(eq_spencer) -> dict[str, object]:
    ledger, digest = eq_spencer.audit()
    require(digest == "ad0fa899252ab48d5df1eb868b1492ecc07619c05cc976fe73526fdfa7fceee3",
            digest)
    return {
        "first_required_cell": "source-labelled K_Eq(beta) / cross-word mixed Eq lift",
        "must_preserve": [
            "word 01211222 and incident response-to-cap word arrow",
            "P3+K2 repeated fine degree",
            "A/B versus A/C root label",
            "DQ/PS operation parent",
            "corner-resolved private and Eq occurrence rows",
            "target and W",
            "physical q and anchor",
            "ordinary and labelled residue",
            "shifted ridge and -d(q_xv^01) connection",
            "eta and sigma",
        ],
        "current_status": ledger["current_exact_status"],
        "consequence": (
            "the degree-four reset supplies a polynomial coefficient for "
            "the same formal conormal, but neither constructs kappa nor "
            "decides delta.e_kappa"
        ),
    }


def audit():
    pin_dependencies()
    reset = load(
        "computations/verify_h3_degree4_reset_five_face_aggregate_gate.py",
        "reset_kappa_degree4",
    )
    ci = load(
        "computations/verify_h3_five_denominator_hafnians_complete_intersection.py",
        "reset_kappa_ci",
    )
    shifted = load(
        "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py",
        "reset_kappa_shifted",
    )
    eq_spencer = load(
        "computations/verify_h3_reduced_eq_spencer_three_projection_gate.py",
        "reset_kappa_eq_spencer",
    )
    decomposition = load(
        "computations/verify_h3_four_site_full_source_exhaustiveness_decomposition_gate.py",
        "reset_kappa_decomposition",
    )
    ledger = {
        "theorem": "h3 degree-four reset cross-word kappa projection gate",
        "pins": PINS,
        "pinned_note_claims": pinned_note_claims_audit(),
        "denominator_complete_intersection":
            complete_intersection_audit(ci, reset),
        "five_mixed_reset_cells":
            five_reset_cells_audit(reset, shifted, eq_spencer),
        "literal_projection_to_kappa_AB_AC":
            literal_kappa_projection_audit(decomposition),
        "formal_diagonal_and_missing_lift_controls":
            diagonal_and_missing_lift_controls_audit(reset, eq_spencer),
        "physical_augmentation_frontier":
            exact_physical_frontier_audit(eq_spencer),
        "verdict": (
            "The five h_v reset residuals have zero literal projection to "
            "kappa_AB and kappa_AC.  Although they are Eq-only, their Eq row "
            "is the central conormal, not a corner-resolved Eq_j row, and "
            "their raw 2K2 grade is off the repeated P3+K2 kappa grade.  An "
            "operation-blind diagonal lift is delta-dark.  Only the missing "
            "physical K_Eq/cross-word comparison could assign a nonconstant "
            "corner vector e_kappa, in which case the exact v-th value is "
            "-h_v*delta.e_kappa.  Complete intersection prevents the five "
            "denominator coefficients from forcing a primitive unit value."
        ),
        "scope": (
            "Exact canonical h=3 reset, complete-intersection, derived "
            "Hasse/Koszul, reduced-Eq Spencer, and private-minus-Eq typed "
            "projection audit.  It proves off-grade/darkness of the current "
            "cells, not existence or zero value of the missing physical "
            "K_Eq/cross-word lift."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("degree-four reset kappa ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 degree-four reset -> cross-word kappa projection: PASS")
    print("five literal reset projections to kappa_AB/kappa_AC: ZERO/OFF-GRADE")
    print("operation-blind diagonal Eq lift: delta.Eq=0")
    print("nonzero only after missing lift: chi_v=-h_v*delta.e_kappa")
    print("denominator-only primitive unit aggregate: NO (height-five CI)")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
