#!/usr/bin/env python3
"""Audit whether H0-u can source-validly restrict to 1-v04 in E14.

In the canonical universal E14 chart, the genuine normalized pure unary row
is

    U_000000 - 1 = v04*v13,

whereas 1-v04 is minus the coefficient of the pivot u35 in the complete
mixed row U_000101.  Coefficient extraction is linear but not multiplicative,
so this equality of one selected coefficient does not define an algebra or
source-presentation map from H0-u.

The localization split is also exact.  On D(1-v04), the first-hit target is
equivalent to the still nonzero private class; if an ideal-preserving map did
send H0-u to this unit, that branch would instead be the scalar-unit arm.  On
V(1-v04), the target reduces to the old unary column, but the private class
survives and the conormal placement vanishes under ordinary restriction.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py":
        "893f000e37e4bcfc78973cb042cc0858087cb25605d6cf070a1bf8dfa7a76b7a",
    "notes/h3-c6-e14-unary-spair-first-reduction-boundary.md":
        "9d3af91f0e97079c8e2bd2dd76db110fdde45e71eed0d21805bdd4575a683c4f",
    "computations/verify_h3_direct_free_normals_e14_pointed_composition_gate.py":
        "ea8cb46d5ee84b1973cb062df73b75c0704a0a31823b53e7187e737175964d53",
    "notes/h3-direct-free-normals-e14-pointed-composition-gate.md":
        "aa927470ffc926bc5639be94c76ab66c00cdabfa0082a0b94f6d117d7add0942",
    "computations/verify_h3_c6_e14_minimal_enlargement_unit.py":
        "d5682f9134ff3dafddb4908707e5ceaacb25ff8b37632e57d9f9f3a4b62f84a8",
    "notes/h3-c6-e14-minimal-enlargement-unit.md":
        "552adf8a24410d4b8a09e61809c9a40c40274ad9c49a7ffe01b7ceb0d5ea22a7",
    "computations/verify_h3_c6_e14_two_cell_unit_frontier.py":
        "b5a2609b64f5a0bf1720a3c571c6c4d28aa316df00129f5b4574e0f32b8c3971",
    "notes/h3-c6-e14-two-cell-unit-frontier.md":
        "07593c3ebeb95b76461792c9835810f2b81e2b2ba701a9c910ea75c2b63809f1",
    "computations/verify_h3_c6_e14_three_cell_top_degree_boundary.py":
        "ac4ae4b8e2a351f4666cc2e196073663da94634ed4aac4c3f4e6b5dd92169313",
    "notes/h3-c6-e14-three-cell-top-degree-boundary.md":
        "75dc1e2d82e9b390fcf172eb3181f000c54b955e20a1b067fd11484df947f629",
    "computations/verify_h3_four_base_silent_c6_response_lock.py":
        "dc4daa2d200f184b5d00d29c4db175320935a189f5590836afa0c724d3fdac8a",
    "notes/h3-four-base-silent-c6-response-lock.md":
        "54d7278e49e8195ed2262fa37cc89936f718b3bcd192884c6473c736a68354b8",
    "computations/verify_h3_e14_keq_private_placement_residue_identification_gate.py":
        "89b0b694b525dba502314e61922cb884ef6ddd2f14fea68b3bafd5215aa40c70",
    "notes/h3-e14-keq-private-placement-residue-identification-gate.md":
        "36828d8503d929427eef55886cb68cbfe7c2431649c38382907835365bd5ed38",
    "computations/verify_h3_e14_keq_private_placement_pointedness_gate.py":
        "5eef4dff45be6e8993808ef5bcb533d62143dd4bc833a16e2015b48e7bc408d8",
    "notes/h3-e14-keq-private-placement-pointedness-gate.md":
        "59111d6a2dda8a16785cab6c6d129c806ea7e01a2a6d54e092c8841f6521c6c0",
}
EXPECTED_LEDGER_SHA256 = (
    "1055ec63a7f6bcbef1025afa0108121473f4891095b14712e8505544028d5a70"
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


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add_polynomials(*terms):
    answer = {}
    for coefficient, polynomial in terms:
        for monomial, value in polynomial.items():
            total = answer.get(monomial, Q(0)) + Q(coefficient) * Q(value)
            if total:
                answer[monomial] = total
            elif monomial in answer:
                del answer[monomial]
    return answer


def evaluate(polynomial, **values):
    answer = Q(0)
    for monomial, coefficient in polynomial.items():
        term = Q(coefficient)
        for variable in monomial:
            term *= Q(values.get(variable, 0))
        answer += term
    return answer


def source_row_vs_coefficient_audit() -> dict[str, object]:
    first = load(
        "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py",
        "factor_provenance_first",
    )
    first_ledger, first_digest = first.audit()
    require(first_digest == first.EXPECTED_LEDGER_SHA256,
            "E14 first reduction changed")

    rewrite = first.load(first.REWRITE_PATH, "factor_provenance_rewrite")
    top = rewrite.load(rewrite.TOP_PATH, "factor_provenance_top")
    two = top.load(top.TWO_CELL_PATH, "factor_provenance_two")
    e14 = two.load(two.E14_PATH, "factor_provenance_e14")
    b4 = e14.load(e14.B4_PATH, "factor_provenance_b4")
    _candidates, _names, _responses, unary = two.universal(e14, b4, 1, 1)

    pure_word = (0,) * 6
    mixed_word = (0, 0, 0, 1, 0, 1)
    pure_coefficient = unary[pure_word]
    require(pure_coefficient == {
                (): Q(1), ("v0400", "v1300"): Q(1)
            }, ("pure E14 unary coefficient changed", pure_coefficient))
    pure_source_row = add_polynomials(
        (1, pure_coefficient), (-1, {(): Q(1)}))
    require(pure_source_row == {("v0400", "v1300"): Q(1)},
            "normalized pure source row changed")

    pivot_factor, mixed_remainder = first.factor_unary(
        unary[mixed_word], ("u35_11",))
    require(pivot_factor == {(): Q(-1), ("v0400",): Q(1)}
            and len(mixed_remainder) == 12,
            ("mixed pivot factor changed", pivot_factor, mixed_remainder))
    a = {(): Q(1), ("v0400",): Q(-1)}
    require(add_polynomials((1, a), (1, pivot_factor)) == {},
            "A stopped being minus the mixed pivot factor")

    # The two polynomials are not restrictions of one another.  At v04=0,
    # the genuine pure source row vanishes while A=1.  At v04=v13=1, A=0
    # while the pure source row is one.
    require(evaluate(pure_source_row, v0400=0, v1300=7) == 0
            and evaluate(a, v0400=0, v1300=7) == 1
            and evaluate(pure_source_row, v0400=1, v1300=1) == 1
            and evaluate(a, v0400=1, v1300=1) == 0,
            "pure/mixed polynomial separation changed")

    # Coefficient extraction at a pivot is not an algebra homomorphism:
    # coeff_u(u)=1, but coeff_u(u^2)=0 while 1*1=1.  Therefore selecting the
    # u35 coefficient cannot be the pullback of a source algebra map.
    coeff_u_on_u = Q(1)
    coeff_u_on_u_squared = Q(0)
    require(coeff_u_on_u_squared != coeff_u_on_u * coeff_u_on_u,
            "coefficient extraction accidentally became multiplicative")

    canonical = first_ledger["canonical_first_reduction"]
    require(canonical["unary_word"] == "000101"
            and canonical["unary_unit_factor"] == [
                [[], "-1"], [["v0400"], "1"]
            ], ("first reduction ledger changed", canonical))
    pointed = load(
        "computations/verify_h3_e14_keq_private_placement_pointedness_gate.py",
        "factor_provenance_pointed",
    )
    pointed_ledger, pointed_digest = pointed.audit()
    require(pointed_digest == pointed.EXPECTED_LEDGER_SHA256,
            "private placement pointedness gate changed")
    guard = pointed_ledger["pointedness"]["sharp_guard"]
    require(guard["pointed_but_trivial_private_face"]["raw_assignment_pointed"]
                is True
            and guard["pointed_but_trivial_private_face"]["R_E14"] == "0"
            and guard["nonzero_private_face_but_nonpointed"]["R_E14"] == "1"
            and guard["nonzero_private_face_but_nonpointed"]
                ["raw_assignment_pointed"] is False,
            ("raw factor assignment became pointed and nonzero",
             pointed_ledger))

    return {
        "genuine_normalized_pure_unary_row": {
            "word": "000000",
            "formula": "U_000000-1=v04_00*v13_00",
            "role": "six-site pure matching/cofactor source equation",
        },
        "selected_mixed_pivot_factor": {
            "word": "000101",
            "complete_row_terms": len(unary[mixed_word]),
            "pivot": "u35_11",
            "coefficient": "-1+v04_00",
            "placement_factor": "1-v04_00",
            "nonpivot_tail_terms": len(mixed_remainder),
        },
        "coefficient_extraction_is_algebra_map": False,
        "independent_pointedness_audit": (
            "a pointed raw assignment forces 1-v04=0 and hence R_E14=0"
        ),
        "separating_specializations": [
            "v04=0: pure row=0, 1-v04=1",
            "v04=v13=1: pure row=1, 1-v04=0",
        ],
        "verdict": (
            "1-v04 is a selected coefficient of a mixed complete row, not "
            "the restriction/cofactor of the pure source relation H0-u"
        ),
    }


def localization_strata_audit() -> dict[str, object]:
    first = load(
        "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py",
        "factor_localization_first",
    )
    ledger, digest = first.audit()
    require(digest == first.EXPECTED_LEDGER_SHA256,
            "E14 localization dependency changed")
    special = ledger["canonical_first_reduction"]["v04_specializations"]
    require(special == {
        "0": {
            "rank_Q": 224,
            "B_remainder_support": 10,
            "private_remainder_support": 10,
            "B_equals_private_remainder": True,
        },
        "1": {
            "rank_Q": 257,
            "B_remainder_support": 0,
            "private_remainder_support": 89,
            "B_equals_private_remainder": False,
        },
    }, ("v04 strata changed", special))

    # Ideal-theoretic consequence of a hypothetical source-presentation map.
    # If F=H0-u belongs to the source ideal and Phi(F)=A, then after inverting
    # A the target source ideal contains the unit A/A=1.  This is the scalar
    # unit arm, not a nontrivial comparison cell.
    a_is_unit_on_d = True
    image_of_source_relation_is_a = True
    localized_source_ideal_is_unit = (
        a_is_unit_on_d and image_of_source_relation_is_a
    )
    require(localized_source_ideal_is_unit,
            "hypothetical D(A) source map stopped forcing a unit")

    # On V(A), the ordinary function A is zero.  It cannot carry the desired
    # nonzero conormal/private placement unless A is itself installed as a
    # target source equation and its derived conormal retained.  The exact
    # first-hit module instead leaves the private class free.
    ordinary_image_on_v = Q(0)
    require(ordinary_image_on_v == 0
            and special["1"]["private_remainder_support"] == 89,
            "V(A) private branch changed")

    lock = load(
        "computations/verify_h3_four_base_silent_c6_response_lock.py",
        "factor_localization_lock",
    )
    crossed = lock.audit_augmented_cycle()
    require("O11--C21(q04)--O22" in crossed["crossed_paths"],
            ("q04 crossed response route changed", crossed))

    return {
        "D(1-v04)": {
            "exact_witness": "v04=0",
            "first_hit_rank": 224,
            "target_remainder": "the same nonzero private generator",
            "localization_alone_closes": False,
            "if_Phi(H0-u)=1-v04_in_source_ideal": (
                "localized source ideal contains 1; scalar-unit branch"
            ),
        },
        "V(1-v04)": {
            "exact_witness": "v04=1",
            "first_hit_rank": 257,
            "target_remainder": 0,
            "private_remainder_support": 89,
            "ordinary_image_of_H0-u_under_proposed_formula": 0,
            "derived_conormal_supplied": False,
            "physical_q04_consequence_under_silent_lock_hypotheses":
                "crossed response path O11--C21(q04)--O22",
        },
        "cover_verdict": (
            "the two strata do not furnish a nontrivial source comparison: "
            "D is either the still-open private class or, under the desired "
            "ideal map, a scalar unit; V closes the target shadow but kills "
            "the ordinary placement and leaves the private class"
        ),
    }


def word_grade_and_unit_scope_audit() -> dict[str, object]:
    direct = load(
        "computations/verify_h3_direct_free_normals_e14_pointed_composition_gate.py",
        "factor_provenance_direct",
    )
    direct_ledger, direct_digest = direct.audit()
    require(direct_digest == direct.EXPECTED_LEDGER_SHA256,
            "direct-free E14 comparison changed")
    word = direct_ledger["shifted_hasse_to_E14"]
    require(word["normal_source_word"] == "01211222"
            and word["normal_internal_word"] == "12112"
            and word["E14_canonical_unary_word"] == "000101"
            and not word["full_source_labelled_E14_map"],
            ("word/grade separator changed", word))

    # Pin and read the exact promotion boundary rather than rerunning the
    # 2.1-million-triple census inside every mode of this wrapper.
    three_note = (ROOT / "notes/h3-c6-e14-three-cell-top-degree-boundary.md").read_text()
    require("All **2,126,208** unordered triples" in three_note
            and "does not yet prove emptiness after allowing every internal cell"
                in three_note
            and "no single universal" in three_note
            and "two-row comparison" in three_note,
            "three-cell unit/exhaustivity scope changed")
    two_note = (ROOT / "notes/h3-c6-e14-two-cell-unit-frontier.md").read_text()
    require("All 57,291" in two_note
            and "ordinary two-row source units" in two_note,
            "two-cell unit scope changed")

    return {
        "source_words": {
            "reduced_Eq_normal": "01211222 (internal 12112)",
            "E14_mixed_unary": "000101",
            "current_word_grade_map": False,
        },
        "known_E14_units": {
            "already_placed_one_cell_supports": "ordinary source units",
            "already_placed_two_cell_supports": 57291,
            "already_placed_three_cell_supports": 2126208,
            "local_internal_monomial_types_exhausted": True,
            "arbitrary_simultaneous_full_support_exhausted": False,
            "universal_two_row_identity": False,
        },
        "consequence": (
            "after an exact physical word/fine/repeated placement, supports "
            "with at most three new internal cells terminalize by the E14 "
            "unit theorems.  Those theorems neither construct the placement "
            "nor close D/V for arbitrary simultaneous contamination"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "E14 K_Eq private-factor localization provenance gate",
        "pins": PINS,
        "source_row_vs_selected_coefficient":
            source_row_vs_coefficient_audit(),
        "localization_strata": localization_strata_audit(),
        "word_grade_and_unit_scope": word_grade_and_unit_scope_audit(),
        "shortest_positive_alternative": {
            "sparse_E14_support": (
                "construct the exact P2/iota word/fine/repeated map; once "
                "placed, the <=3-new-cell E14 unit theorem closes the branch"
            ),
            "D_branch": (
                "an ideal-preserving map with Phi(H0-u)=1-v04 forces the "
                "localized scalar unit, so it is a terminal arm rather than "
                "the desired nontrivial K_Eq comparison"
            ),
            "V_branch": (
                "use the nonzero q04 crossed-C4 response landing where its "
                "silent-lock hypotheses apply, or construct a derived excess "
                "conormal; ordinary restriction supplies no private face"
            ),
            "full_support": (
                "requires the still-missing universal triangular/standard-"
                "basis E14 exhaustivity together with physical placement"
            ),
        },
        "verdict": (
            "The formula H0-u -> 1-v04 is not induced by any committed "
            "source-valid restriction/cofactor.  The genuine normalized pure "
            "E14 cofactor row is v04*v13; 1-v04 is only the u35 coefficient "
            "of the mixed word-000101 row, and coefficient extraction is not "
            "an algebra map.  Localization does not repair this: D retains "
            "the private class unless the hypothetical ideal map makes the "
            "branch a scalar unit, while V closes only the target shadow and "
            "leaves the private/conormal problem.  Existing E14 unit theorems "
            "close sparse supports only after the missing word/grade placement."
        ),
        "scope": (
            "Canonical chart (1,1), the exact first-hit module and its v04=0/1 "
            "strata, the direct-free normal/E14 word separator, and pinned "
            "one-/two-/three-cell E14 unit scope.  This is not a no-go against "
            "a new derived excess/P2 map or a future full-support standard basis."
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("private-factor provenance ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("H0-u -> 1-v04 source-valid cofactor map: NO")
    print("actual pure E14 row: v04*v13; 1-v04: mixed u35 coefficient")
    print("D(1-v04): private survives, or hypothetical ideal map gives unit")
    print("V(1-v04): target shadow closes, private/conormal survives")
    print("E14 units: sparse placed support YES / full support NO")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
