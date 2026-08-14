#!/usr/bin/env python3
"""Test the five degree-four h_v/Eq cells against Psi_loc.

The five derived reset fillers have underived residual

    h_v * (H0-u) * e_Eq.

Although the full reset word is the canonical cap word 01211222, this is a
central conormal row in raw squarefree 2K2 grade.  Psi_loc instead sees four
operation-corner-resolved reduced-Eq packets in repeated P3+K2 grade.  With
all labels retained, the five literal projections are zero.  An
operation-blind diagonal placement e_Eq -> (1,1,1,1) is also delta-dark.

This checker additionally grants the entire 19-dimensional external
augmentation space of the exhaustive local map.  Since Psi_loc is zero on
that space, no target/q/anchor/W/residue/ridge/eta/sigma decoration can make
the reset candidate bright.  A nonzero value requires the still missing
source-labelled K_Eq/cross-word lift to assign a nonconstant corner vector.
Even then the value is h_v times the corner mismatch, not a primitive unit;
the five denominator hafnians have no denominator-only unit aggregate.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py":
        "6c42cd4dc7dca1544dc0b675f5f4543ec348f1fba34b7ea14bf80cc6a20b9cf1",
    "computations/verify_h3_degree4_reset_five_face_aggregate_gate.py":
        "01961c9ae83b91dad31ba859ea2f8a2d5775d73d7ad591aa0a369e7d971f8079",
    "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py":
        "7d9e49f34da84772f6e0863a9bfe56cb9a90e0cfd3fceb76da59175ffea36c50",
    "computations/verify_h3_four_site_full_source_exhaustiveness_decomposition_gate.py":
        "269a1b775e0790c3e4f1f6390b83673c1118270e491885ce9383e703f07b3278",
    "computations/verify_h3_reduced_eq_spencer_three_projection_gate.py":
        "315508b572fa0d96b33ba83b8ac4905e59dfbf8f484023891618dbb3c6489d83",
    "computations/verify_h3_five_denominator_hafnians_complete_intersection.py":
        "4c87c1db939346e8f1d83a26b5edef19e3143a65cc6d6fd5ea636f99d13b5615",
    "notes/h3-degree4-reset-five-face-aggregate-gate.md":
        "5a19c7b8bfb21cb0c76532accb3af1f0ea4cdb6b13fa6b500124f77f61395100",
    "notes/h3-shifted-denominator-chart-filler-augmented-commutator.md":
        "1d89c1e592fdc723bb58b1b75e2ba846b812401efad33c8cd88d4265dc0a7743",
}
EXPECTED_LEDGER_SHA256 = (
    "c24027f49e9a0ed3b617ad3e8879bb40e8adf39ed8b7a3b13b16a9e550912110"
)


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


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


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


def local_supermap_audit(local):
    local_ledger, local_digest = local.audit()
    require(local_digest == local.EXPECTED_LEDGER_SHA256,
            "the local terminal ledger changed")
    named = (local.top_projection_columns()
             + local.lower_face_and_reinsertion_columns()
             + local.external_augmented_columns())
    columns = tuple(value for _name, value in named)
    dual = scale(Q(1, 12), local.integral_terminal_dual())
    external = tuple(label for label in local.LABELS
                     if label.startswith(("target:", "W:", "ores:"))
                     or label in ("M", "ainc", "q", "P_f", "ridge",
                                  "eta", "sigma"))
    require(len(external) == 19
            and rank(columns) == 126
            and all(dual[local.INDEX[label]] == 0 for label in external)
            and all(dot(dual, value) == 0 for value in columns),
            "the local external grant or terminal changed")

    # Grant one deliberately arbitrary vector in every augmented external
    # row.  This freezes the statement that augmentation decoration cannot
    # alter the deciding private-minus-Eq scalar.
    arbitrary = [Q(0)] * len(local.LABELS)
    for index, label in enumerate(external, 1):
        arbitrary[local.INDEX[label]] = Q((-1) ** index * (index + 2))
    require(dot(dual, tuple(arbitrary)) == 0
            and rank(columns + (tuple(arbitrary),)) == 126,
            "an external augmentation row became Psi-bright")
    return dual, {
        "dimension": len(local.LABELS),
        "rank": rank(columns),
        "cokernel_dimension": 1,
        "normalized_terminal": (
            "Psi_loc=(1/12) sum_(corner,matching) "
            "delta_corner*(B-Eq)"
        ),
        "external_augmented_rows_granted": list(external),
        "external_augmented_dimension": len(external),
        "Psi_coefficients_on_all_external_rows": 0,
        "rank_after_arbitrary_external_decoration":
            rank(columns + (tuple(arbitrary),)),
    }


def local_top_vector(local, *, B=(0, 0, 0, 0), Eq=(0, 0, 0, 0)):
    entries = {}
    for block, values in (("B", B), ("Eq", Eq)):
        for corner, coefficient in enumerate(values):
            for matching in range(3):
                entries[local.top_label(block, corner, matching)] = coefficient
    return local.sparse(entries)


def five_reset_audit(reset, shifted, eq_spencer, complete_intersection):
    faces = reset.denominator_faces()
    monomials = [monomial for face in faces.values() for monomial in face]
    generators = []
    for site in range(1, 6):
        generators.append(complete_intersection.poly(*(
            (coefficient, monomial)
            for monomial, coefficient in faces[site].items()
        )))
    basis = complete_intersection.buchberger(generators)
    leading = [complete_intersection.leading(value)[0] for value in basis]
    height, _cover = complete_intersection.minimal_vertex_cover_size(leading)
    shifted_ledger, shifted_digest = shifted.audit()
    eq_ledger, eq_digest = eq_spencer.audit()
    require(len(faces) == 5
            and all(len(face) == 3 for face in faces.values())
            and len(monomials) == len(set(monomials)) == 15
            and shifted_digest
                == "bdcc6a2734c3bd31f060d56fd88f8f5344f39e43aed03f70f18cfa65eef74b92"
            and eq_digest
                == "ad0fa899252ab48d5df1eb868b1492ecc07619c05cc976fe73526fdfa7fceee3",
            "the five reset/Eq cells changed")
    initial = shifted_ledger["initial_layer"]
    derived = shifted_ledger["two_direction_derived_filler"]
    qzero = shifted_ledger["qzero_top"]
    conormal = eq_ledger["pinned_conormal_identifications"]
    require(initial["isolated_underived_commutator"]
                == "h_v*(H_0-u)*eq"
            and derived["target"] == derived["ordinary_residue"] == 0
            and not qzero["underived_source_descent"]
            and conormal["universal_conormal"] == "E=(H0-u)e_Eq"
            and not conormal["same_physical_source_grade"]
            and len(generators) == height == 5,
            "the underived reset/physical descent frontier changed")
    return {
        "mixed_internal_word": "12112",
        "full_augmented_word": "01211222",
        "cells": 5,
        "terms_per_h_v": 3,
        "distinct_quadratic_terms": len(set(monomials)),
        "derived_filler_boundary": "h_v*Y*w",
        "derived_filler_target": derived["target"],
        "derived_filler_ordinary_residue": derived["ordinary_residue"],
        "underived_residual": "h_v*(H0-u)*e_Eq",
        "qzero_diagonal_residual": qzero[
            "diagonal_projection_commutator"],
        "underived_source_descent_constructed": False,
        "central_conormal": conormal["universal_conormal"],
        "denominator_complete_intersection_height": height,
        "denominator_only_primitive_unit_aggregate": False,
        "denominator_first_syzygies": "Koszul h_i*e_j-h_j*e_i",
    }


def psi_projection_audit(local, dual, decomposition):
    decomposition_ledger, decomposition_digest = decomposition.audit()
    require(decomposition_digest == decomposition.EXPECTED_LEDGER_SHA256
            and decomposition.CORNERS == tuple(
                "A_[a|b]=DQ[a|b] A_[b|a]=DQ[b|a] "
                "B=PS[P0,S1] C=PS[P1,S0]".split(" ", 3)),
            "the operation-corner decomposition changed")

    delta = tuple(map(Q, (1, 1, -1, -1)))
    one = tuple(map(Q, (1, 1, 1, 1)))
    zero = tuple(map(Q, (0, 0, 0, 0)))
    literal_zero = local_top_vector(local)
    diagonal_eq = local_top_vector(local, Eq=one)
    diagonal_tied = local_top_vector(local, B=one, Eq=one)
    bright_eq = local_top_vector(local, Eq=delta)
    require(dot(dual, literal_zero) == 0
            and dot(dual, diagonal_eq) == 0
            and dot(dual, diagonal_tied) == 0
            and dot(dual, bright_eq) == -1,
            "the reset landing controls changed")

    # A generic corner vector e has normalized value
    # -(1/4) delta.e after repeating it over the three matching occurrences.
    basis_values = []
    for corner in range(4):
        basis = tuple(Q(1 if index == corner else 0) for index in range(4))
        observed = dot(dual, local_top_vector(local, Eq=basis))
        expected = -delta[corner] / Q(4)
        require(observed == expected,
                ("generic corner formula changed", corner, observed, expected))
        basis_values.append(str(observed))

    return {
        "local_operation_corners": list(local.CORNERS),
        "reset_operation_parent": "none: central Hasse/Koszul Eq conormal",
        "reset_root_label": "none: neither A/B nor A/C",
        "raw_reset_site_grade": "squarefree 2K2",
        "required_mixed_landing_grade": "repeated P3+K2",
        "literal_projection_to_corner_B_Eq": "zero",
        "literal_Psi_values_on_all_five_cells": ["0"] * 5,
        "operation_blind_diagonal_Eq_vector": [1, 1, 1, 1],
        "Psi_on_diagonal_Eq": "0",
        "Psi_on_diagonal_tied_B_Eq": "0",
        "bright_Eq_only_delta_control": "-1",
        "generic_corner_basis_values": basis_values,
        "formula_after_a_new_corner_resolving_lift": (
            "Psi(reset_v)=-(h_v/4)*delta.e_v"
        ),
        "word_warning": (
            "the full word 01211222 agrees with the cap word, but word "
            "equality does not supply the missing operation/root/corner-Eq "
            "labels or the 2K2-to-P3+K2 grade transport"
        ),
    }


def physical_status_audit(eq_spencer):
    ledger, digest = eq_spencer.audit()
    require(digest
            == "ad0fa899252ab48d5df1eb868b1492ecc07619c05cc976fe73526fdfa7fceee3",
            digest)
    cone = ledger["universal_mapping_cone"]
    require(cone["formal_three_projection_unification"]
            and not cone["physical_three_projection_cell_constructed"],
            cone)
    return {
        "formal_common_Eq_cone": cone["universal_two_term_cone"],
        "formal_projection_unification": True,
        "physical_source_labelled_cone_constructed": False,
        "first_required_datum": (
            "a source-labelled K_Eq(beta)/cross-word comparison which maps "
            "the central e_Eq row into a corner-resolved repeated-grade Eq "
            "packet and totalizes all product-rule faces"
        ),
        "must_retain": [
            "operation parent and A/B versus A/C root label",
            "word 01211222 and the incident response-to-cap arrow",
            "repeated P3+K2 fine degree",
            "private and reduced-Eq matching occurrences",
            "target, W, physical q and anchor",
            "ordinary and labelled residue",
            "ridge and -d(q_xv^01) connection",
            "eta and sigma",
        ],
    }


def audit():
    pin_dependencies()
    local = load(
        "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py",
        "hv_psiloc_local")
    reset = load(
        "computations/verify_h3_degree4_reset_five_face_aggregate_gate.py",
        "hv_psiloc_reset")
    shifted = load(
        "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py",
        "hv_psiloc_shifted")
    decomposition = load(
        "computations/verify_h3_four_site_full_source_exhaustiveness_decomposition_gate.py",
        "hv_psiloc_decomposition")
    eq_spencer = load(
        "computations/verify_h3_reduced_eq_spencer_three_projection_gate.py",
        "hv_psiloc_eq_spencer")
    complete_intersection = load(
        "computations/verify_h3_five_denominator_hafnians_complete_intersection.py",
        "hv_psiloc_complete_intersection")

    dual, local_data = local_supermap_audit(local)
    reset_data = five_reset_audit(
        reset, shifted, eq_spencer, complete_intersection)
    projection_data = psi_projection_audit(local, dual, decomposition)
    physical_data = physical_status_audit(eq_spencer)
    ledger = {
        "theorem": "h3 degree-four five-h_v Psi_loc augmented landing gate",
        "pins": PINS,
        "exhaustive_local_terminal_and_external_grant": local_data,
        "five_degree_four_reset_cells": reset_data,
        "literal_and_formal_projection_to_Psi_loc": projection_data,
        "physical_cross_grade_status": physical_data,
        "verdict": (
            "The five h_v Koszul-with-Eq cells are not a physical "
            "unbalanced reduced-Eq landing.  Their derived filler is "
            "target/residue zero, but underived descent leaves a central Eq "
            "conormal in raw 2K2 grade, with no DQ/PS operation parent, "
            "A/B-or-A/C root label, or corner-resolved Eq occurrence.  Their "
            "strict Psi_loc projection is zero.  Even granting an "
            "operation-blind diagonal Eq placement and the entire external "
            "augmentation space leaves Psi_loc zero.  A nonzero value "
            "requires the missing physical K_Eq/cross-word lift and is then "
            "-(h_v/4)delta.e_v, not a denominator-forced primitive unit."
        ),
        "classification": "UNAugmented physical descent / OFF-GRADE / diagonal-dark",
        "nonclaims": [
            "same full word 01211222 is not treated as same operation/fine/repeated grade",
            "the q-zero contraction h_v->1 is not called an underived source cell",
            "the common scalar Eq conormal is not renamed as a corner Eq_j row",
            "arbitrary external decoration is not allowed to change a B-Eq terminal value",
            "the formal K_Eq cone is not called a constructed physical comparison",
        ],
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("five-h_v Psi_loc ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("five h_v/Eq cells -> Psi_loc: PASS")
    print("literal chart/root/corner-Eq projection: ZERO/OFF-GRADE")
    print("operation-blind diagonal Eq placement: Psi_loc=0")
    print("all 19 external augmentation rows: Psi_loc=0")
    print("physical unbalanced Eq landing: NOT CONSTRUCTED")
    print("possible only after K_Eq lift: -(h_v/4)*delta.e_v")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
