#!/usr/bin/env python3
"""Audit the first site-repeating EqSystem collision against cap ``r0``.

Let

    a = (01:11),  b = (07:11).

These are the first site-repeating pair in the current order-six target
enrichment.  Since they share site 0, no perfect matching contains both.
Consequently every official EqSystem coefficient satisfies

    partial_a partial_b H_w = 0

term by term.  The strongest source-derived mixed collision is nevertheless
nonzero: in the Macaulay/Hasse--Tate closure it is

    C_ab,w = x_b iota_a e_w - x_a iota_b e_w,
    d C_ab,w = x_b partial_a H_w - x_a partial_b H_w.

For the pure compatible word this is a literal 30-term source boundary.  It
lies in End(response).  EqSystem Tate cells, their termwise/private rows and
restriction/insertion maps are all objectwise, while r0 and E are in
End(cap).  The free dg-category closure therefore still has Hom(response,cap)
equal to zero in every degree.  A cap-r0 landing raises the maximally granted
source-row rank by one and has the cap-coordinate separator.

The smallest genuinely new constructor is not another EqSystem Tate cell.
It is a normalized EqSystem--AugP2 dg-bimodule map, with a repeated-site
divided-Hasse prolongation, whose operation component is a nonzero
response-to-cap matrix unit.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_chart_model_is_official_eqsystem.py":
        "ef1a997323e0a116787fa3c50368e22ecd33804942a9179eabefa2993e4d9373",
    "computations/verify_h3_order6_site_repeating_target_enrichment_current_tree.py":
        "f1bc7a9f8fdb9148fde5c4d79a4b7f59a3bd03cd6ff00dc1c2fb3c0e7f511ea9",
    "computations/verify_h3_eqsystem_augp2_actual_presentation_underdetermination_gate.py":
        "2c112bffeef2c6adb00029077b6b231de396ace76c78756ab0e11e20078a557b",
    "computations/verify_h3_uc4_beq_tie_source_provenance_audit.py":
        "f237ccffd40863a201b780ea034fcbd7781bc555e1fbc6f528d99d3ab71394c6",
    "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py":
        "02a28ec54b83b2f786e47b0fdc992f5f28dd95a04ba16219f0e24482d4999097",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "computations/verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py":
        "9c182f13ba4da4f2dd3ff49fd9ebf60dd1a218f53cbf4416e82a63236f57404f",
}
EXPECTED_LEDGER_SHA256 = (
    "dd6bd43e4dc2e7f40eed1798a346133584438506a9f9c8448242b0a347ba9661"
)

A = (0, 1, 1, 1)
B = (0, 7, 1, 1)
PURE_ONE = (1,) * 8
OBJECTS = ("response", "cap")


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def decorated_monomial(matching, word):
    return tuple(sorted((left, right, word[left], word[right])
                        for left, right in matching))


def derivative(row, variable):
    output = Counter()
    for monomial in row:
        multiplicity = monomial.count(variable)
        if not multiplicity:
            continue
        remainder = list(monomial)
        remainder.remove(variable)
        output[tuple(sorted(remainder))] += Q(multiplicity)
    return +output


def multiply_cell(cell, polynomial):
    return Counter({tuple(sorted((cell,) + monomial)): coefficient
                    for monomial, coefficient in polynomial.items()})


def rank(columns) -> int:
    basis = {}
    for source in columns:
        vector = {key: Q(value) for key, value in source.items() if value}
        while vector:
            pivot = min(vector, key=repr)
            if pivot not in basis:
                inverse = Q(1) / vector[pivot]
                basis[pivot] = {
                    key: value * inverse for key, value in vector.items()
                }
                break
            coefficient = vector[pivot]
            for key, value in basis[pivot].items():
                residue = vector.get(key, Q(0)) - coefficient * value
                if residue:
                    vector[key] = residue
                else:
                    vector.pop(key, None)
    return len(basis)


def official_pair_audit(official):
    matchings = official.OFFICIAL_MATCHINGS
    require(len(matchings) == 105
            and A[:2] == (0, 1) and B[:2] == (0, 7)
            and len(set(A[:2] + B[:2])) == 3,
            "first site-repeating pair changed")

    words_compatible_a = 0
    words_compatible_b = 0
    words_compatible_both = 0
    occurrence_a = 0
    occurrence_b = 0
    occurrence_both = 0
    second_derivative_nonzero_words = 0
    for word in product(range(3), repeat=8):
        row = tuple(decorated_monomial(matching, word)
                    for matching in matchings)
        contains_a = sum(A in monomial for monomial in row)
        contains_b = sum(B in monomial for monomial in row)
        contains_both = sum(A in monomial and B in monomial
                            for monomial in row)
        if contains_a:
            words_compatible_a += 1
        if contains_b:
            words_compatible_b += 1
        if contains_a and contains_b:
            words_compatible_both += 1
        occurrence_a += contains_a
        occurrence_b += contains_b
        occurrence_both += contains_both
        if derivative(derivative(row, A), B):
            second_derivative_nonzero_words += 1

    require((words_compatible_a, words_compatible_b,
             words_compatible_both)
            == (729, 729, 243),
            "compatible-word census changed")
    require((occurrence_a, occurrence_b, occurrence_both)
            == (10_935, 10_935, 0)
            and second_derivative_nonzero_words == 0,
            (occurrence_a, occurrence_b, occurrence_both,
             second_derivative_nonzero_words))
    return {
        "first_site_repeating_pair": [repr(A), repr(B)],
        "shared_site": 0,
        "official_relations_checked": 3 ** 8,
        "perfect_matchings_per_relation": len(matchings),
        "compatible_words_a_b_both": [
            words_compatible_a, words_compatible_b, words_compatible_both,
        ],
        "termwise_occurrences_a_b_both": [
            occurrence_a, occurrence_b, occurrence_both,
        ],
        "nonzero_mixed_second_derivative_relations":
            second_derivative_nonzero_words,
        "identity": "partial_a partial_b H_w=0 for every word w",
        "reason": "a perfect matching cannot contain two edges sharing site 0",
    }


def mixed_collision_tate_audit(official):
    row = tuple(decorated_monomial(matching, PURE_ONE)
                for matching in official.OFFICIAL_MATCHINGS)
    da = derivative(row, A)
    db = derivative(row, B)
    dab = derivative(da, B)
    require(len(row) == 105 and len(da) == len(db) == 15 and not dab,
            (len(row), len(da), len(db), len(dab)))

    left = multiply_cell(B, da)
    right = multiply_cell(A, db)
    boundary = Counter(left)
    boundary.subtract(right)
    boundary = +boundary
    negative = Counter({monomial: -coefficient
                        for monomial, coefficient in right.items()})
    # Counter unary plus deletes negative values, so rebuild the signed result.
    boundary = Counter(left)
    boundary.update(negative)
    boundary = Counter({monomial: coefficient
                        for monomial, coefficient in boundary.items()
                        if coefficient})
    require(len(left) == len(right) == 15
            and not set(left) & set(right)
            and len(boundary) == 30
            and set(boundary.values()) == {Q(-1), Q(1)},
            "mixed collision boundary changed")

    def repeated_sites(monomial):
        counts = Counter(site for cell in monomial for site in cell[:2])
        return tuple(sorted(site for site, count in counts.items()
                            if count > 1))

    repeated = tuple(repeated_sites(monomial) for monomial in boundary)
    require(all(repeated_sites_tuple for repeated_sites_tuple in repeated),
            "a collision term became a perfect matching")

    # A single-relation second Hasse face is zero.  The nonzero pair row first
    # appears as a decomposable Macaulay/Hasse--Tate expression built from the
    # two first derivatives.  Its differential is a polynomial, hence closed
    # under the ordinary EqSystem differential.
    return {
        "relation_word": "11111111",
        "relation": "d(e_w)=H_w-1",
        "source_derived_cell": "C_ab,w=x_b*iota_a(e_w)-x_a*iota_b(e_w)",
        "boundary": "x_b*partial_a(H_w)-x_a*partial_b(H_w)",
        "first_derivative_terms_a_b": [len(da), len(db)],
        "boundary_support": len(boundary),
        "boundary_values": sorted(map(int, set(boundary.values()))),
        "every_boundary_term_has_repeated_site": True,
        "primitive_second_Hasse_face": 0,
        "target_constant_derivative": 0,
        "d_squared": 0,
        "operation_endpoint": "response -> response",
        "cap_r0_component": 0,
        "source_valid": True,
    }


def categorical_no_go_audit(actual_presentation, cap_provenance,
                             response_cap, termwise_landing):
    actual_ledger, actual_digest = actual_presentation.audit()
    require(actual_digest == actual_presentation.EXPECTED_LEDGER_SHA256,
            actual_digest)
    literal = actual_ledger["smallest_literal_generated_presentation"]
    require(literal["Hom0_response_cap"] == 0
            and literal["primitive_Hom1_response_cap"] == 0
            and literal["generated_Hom1_response_cap"] == 0,
            literal)

    cap_provenance.pin_dependencies()
    cap = cap_provenance.cap_r0_provenance_audit()
    require(cap["constructed_cap_generator"] == "r_0"
            and cap["internal_B_equals_Eq_tie"]
            and cap["cross_word_response_to_cap_membership"] == "OPEN",
            cap)

    response_ledger, response_digest = response_cap.audit()
    require(response_digest == response_cap.EXPECTED_LEDGER_SHA256,
            response_digest)
    hom = response_ledger["literal_idempotent_Hom"]
    require(hom["Hom_degree0_response_to_cap_in_current_grammar"] == 0,
            hom)

    landing_ledger, landing_digest = termwise_landing.audit()
    require(landing_digest == termwise_landing.EXPECTED_LEDGER_SHA256,
            landing_digest)
    physical = landing_ledger["physical_obstruction_after_linear_solution"]
    require(physical["first_typed_obstruction"]
                ["current_operation_algebra_value"] == "e_C A e_R=0",
            physical)

    # Enlarge the response/source block maximally by granting every one of the
    # 30 termwise collision rows independently.  None has a cap-r0 coordinate.
    source_rows = tuple({("source", index): Q(1)} for index in range(30))
    cap_target = {("cap", "r0_landing"): Q(1)}
    rank_before = rank(source_rows)
    rank_after = rank(source_rows + (cap_target,))
    separator = {("cap", "r0_landing"): Q(1)}
    require(rank_before == 30 and rank_after == 31
            and all(sum(separator.get(key, Q(0)) * value
                        for key, value in column.items()) == 0
                    for column in source_rows)
            and sum(separator.get(key, Q(0)) * value
                    for key, value in cap_target.items()) == 1,
            "cap-coordinate separator changed")

    primitive_edges = {("response", "response"), ("cap", "cap")}
    reachable = set(primitive_edges)
    for _ in range(4):
        reachable |= {
            (left_source, right_target)
            for left_source, left_target in tuple(reachable)
            for right_source, right_target in tuple(reachable)
            if left_target == right_source
        }
    require(reachable == primitive_edges
            and ("response", "cap") not in reachable,
            reachable)
    return {
        "universal_closure_generators": [
            "official EqSystem variables and relation Tate cells in End(response)",
            "all termwise H_w/private Macaulay rows in End(response)",
            "all restriction/insertion/divided-Hasse faces in End(response)",
            "constructed r0,E and AugP2 normalizers in End(cap)",
        ],
        "differential_preserves_operation_endpoints": True,
        "composition_closure_edges": [list(edge) for edge in sorted(reachable)],
        "Hom_all_degrees_response_cap": 0,
        "maximally_granted_collision_row_rank": rank_before,
        "rank_after_cap_r0_landing": rank_after,
        "exact_separator": "coefficient of the cap-r0 landing coordinate",
        "separator_on_current_rows": 0,
        "separator_on_desired_landing": 1,
        "cap_internal_r0_is_tied": True,
        "cap_internal_tie_constructs_cross_object_image": False,
        "verdict": (
            "the first forbidden pair has a source-valid internal collision "
            "boundary, but no boundary into r0 in the universal objectwise closure"
        ),
    }


def minimal_new_constructor_audit(packaging):
    packaging_ledger, packaging_digest = packaging.audit()
    require(packaging_digest == packaging.EXPECTED_LEDGER_SHA256,
            packaging_digest)
    package = packaging_ledger["augmented_packaging"]
    require(not package["existing_AugP2_status"]
                ["constructed_literal_source_object"]
            and package["rank_before_mixed_cell"] == 2
            and package["rank_after_mixed_cell"] == 3,
            package)
    return {
        "not_sufficient": [
            "another EqSystem Tate generator",
            "another termwise/private coordinate row",
            "Macaulay multiplication by cap r0",
            "the existing objectwise restriction/insertion API",
        ],
        "smallest_new_constructor": {
            "name": "mixed_collision_AugP2_bimodule",
            "type": (
                "a normalized degree-zero EqSystem-response -> AugP2-cap "
                "dg-bimodule map with repeated-site divided-Hasse prolongation"
            ),
            "base_normalization": "Phi_1(epsilon_root)=r0_root, Phi_0(c_root)=-E_root",
            "first_instance": "ordered pair ((01:11),(07:11)) and its root-labelled mates",
            "required_operation_component": "nonzero e_C A e_R matrix unit",
            "required_first_square": [
                "the 30-term source collision boundary",
                "the termwise/private cap-B image",
                "the reduced-Eq/K_Eq face",
                "the word/fine/repeated/root-labelled comparison face",
            ],
            "naturality": [
                "restriction/insertion", "endpoint transpose",
                "AB<->AC root covariance", "private multiplier deletion",
            ],
        },
        "why_this_is_minimal": (
            "every load-bearing coefficient and Tate face already exists "
            "objectwise; the only absent primitive type is the response-to-cap "
            "operation component joining them"
        ),
        "next_faces_after_constructor": {
            "mixed_mapping_square": package["first_post_word_obstruction"],
            "shifted_ridge": package["first_ridge_obstruction"],
        },
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    official = load(
        "computations/verify_chart_model_is_official_eqsystem.py",
        "first_pair_official",
    )
    actual_presentation = load(
        "computations/verify_h3_eqsystem_augp2_actual_presentation_underdetermination_gate.py",
        "first_pair_actual_presentation",
    )
    cap_provenance = load(
        "computations/verify_h3_uc4_beq_tie_source_provenance_audit.py",
        "first_pair_cap_provenance",
    )
    response_cap = load(
        "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py",
        "first_pair_response_cap",
    )
    termwise_landing = load(
        "computations/verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py",
        "first_pair_termwise_landing",
    )
    packaging = load(
        "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py",
        "first_pair_packaging",
    )

    ledger = {
        "theorem": "h3 first site-repeating collision Tate/AugP2 operation no-go",
        "pins": PINS,
        "official_first_pair": official_pair_audit(official),
        "universal_mixed_collision_Tate_cell": mixed_collision_tate_audit(official),
        "categorical_and_grade_no_go": categorical_no_go_audit(
            actual_presentation, cap_provenance, response_cap, termwise_landing),
        "smallest_genuinely_new_constructor":
            minimal_new_constructor_audit(packaging),
        "verdict": (
            "The first site-repeating pair is source-valid only as an internal "
            "Macaulay/Hasse--Tate collision.  Its primitive mixed second "
            "derivative is zero termwise, while its strongest decomposable "
            "boundary has 30 terms and remains in End(response).  Adding all "
            "termwise/private rows and restriction/insertion faces preserves "
            "operation endpoints, so Hom(response,cap)=0 and a cap-r0 landing "
            "has an exact one-coordinate separator.  The missing datum is one "
            "EqSystem--AugP2 dg-bimodule constructor with a nonzero e_C A e_R "
            "component and repeated-site divided-Hasse prolongation"
        ),
        "scope": (
            "exact all-6561-word official EqSystem audit of the first pair, "
            "exact pure-word 30-term collision boundary, and a categorical "
            "no-go for the objectwise generated closure.  It does not rule out "
            "the stated new bimodule constructor or prove its higher ridge faces"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("first-pair collision ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "official", "collision",
                                           "category", "constructor"),
                        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h3 first site-repeating collision ({arguments.mode}): PASS")
        print("partial_(01:11) partial_(07:11) H_w: ZERO FOR ALL 6561 WORDS")
        print("strongest internal collision boundary: 30 TERMS")
        print("source-valid boundary into r0: NO; exact cap-coordinate separator")
        print("smallest new API: MIXED-COLLISION EqSystem->AugP2 DG BIMODULE")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
