#!/usr/bin/env python3
"""Audit actual divided-Hasse extraction for a retained h=3 pair.

For an actual bivariate source lift

    X(s,t)=x+s*xi+t*zeta+s*t*eta+...,

the coefficient of ``s*t`` in a matching-multiaffine source row is

    J_x F(eta) + B_x F(xi,zeta).

The marked retained pair is only one summand of ``B``.  Minimum occupied
support is a property of the base point; it neither kills the mixed
correction ``eta`` nor the other pair summands.

A literal mixed-word guard makes the distinction sharp.  On word 001122,
retain the diagonal tail q45[22] and use the two matchings

    q01[00] q23[11] q45[22],
    q02[01] q13[01] q45[22].

The bivariate family q01=q02=s, q23=t, q13=-t, q45=1 makes their complete
target sum identically zero.  The marked pair (q01,q23) contributes +1 to
the divided-Hasse coefficient and the second pair contributes -1.  With
D=1 and every endpoint cell zero, the complete direct-response row is the
same zero polynomial.  At the base point all four varied cells are zero;
there is no occupied-coordinate deletion and no nonzero offdiagonal base
cell to which the active-minor theorem applies.

Thus actual coefficient extraction forces the *sum* of all proper pair and
mixed-correction faces, not the selected lower packet.  A positive theorem
must rule out the other same-grade pair faces (and J*eta) using the complete
augmented rows, or promote their first nonzero base incidence separately.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_chart_switch_word_target_affine_gate.py":
        "c0f0eb10c26816d7ad7033fc22f8d8ff8fe45a9825ef9e158dfe8d739db409a4",
    "notes/uniform-chart-switch-word-target-affine-gate.md":
        "edb1083524d65036b374af26be47d29bd6493f7f086fe744d25865f4e1c046ab",
    "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py":
        "b03c096eb5bc4e6307cafa966f3d66d8c087e78bb8793c8448eec33f51e7e76a",
    "notes/h3-active-coloop-redistribution-second-hasse-face-classification.md":
        "985737011ea321c70096a89ea2a719db207c304d947ff4899133b39e14c46276",
    "computations/verify_h3_pf_dark_kernel_support_lowering_hasse_coloop_gate.py":
        "5feb07c35c4e5ce304a305f0146441de7af5a9dc2d5466a794d315d99b626e48",
    "notes/h3-pf-dark-kernel-support-lowering-hasse-coloop-gate.md":
        "bff81dd6a7d920db178418d9509dd1dd47f426a35d48a156be9941344683659c",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "notes/uniform-target-augmented-private-site-active-minor.md":
        "d7b16ecbb867524615ecf3034e0911e0add34825a7f9088f369f3a11e1c61f0d",
}
EXPECTED_LEDGER_SHA256 = "299f3d06b8dc986bc900d28072a95b320e900f69139f5b34b7d7301f44f1814d"

Exponent = tuple[int, int]
Polynomial = dict[Exponent, Q]


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


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    answer = dict(left)
    for exponent, coefficient in right.items():
        answer[exponent] = answer.get(exponent, Q(0)) + coefficient
        if answer[exponent] == 0:
            del answer[exponent]
    return answer


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for (ls, lt), lc in left.items():
        for (rs, rt), rc in right.items():
            exponent = (ls + rs, lt + rt)
            answer[exponent] = answer.get(exponent, Q(0)) + lc * rc
    return {exponent: coefficient for exponent, coefficient in answer.items()
            if coefficient}


def coordinate_polynomial(variable, point, xi, zeta, eta) -> Polynomial:
    answer: Polynomial = {}
    for exponent, values in (
            ((0, 0), point), ((1, 0), xi),
            ((0, 1), zeta), ((1, 1), eta)):
        value = Q(values.get(variable, 0))
        if value:
            answer[exponent] = value
    return answer


def expand_row(monomials, point, xi, zeta, eta) -> Polynomial:
    answer: Polynomial = {}
    for monomial in monomials:
        term: Polynomial = {(0, 0): Q(1)}
        for variable in monomial:
            term = multiply(
                term, coordinate_polynomial(variable, point, xi, zeta, eta))
        answer = add(answer, term)
    return answer


def jacobian_mixed_face(monomials, point, eta) -> Q:
    answer = Q(0)
    for monomial in monomials:
        for index, variable in enumerate(monomial):
            complement = monomial[:index] + monomial[index + 1:]
            value = Q(eta.get(variable, 0))
            for other in complement:
                value *= Q(point.get(other, 0))
            answer += value
    return answer


def pair_faces(monomials, point, xi, zeta):
    answer = []
    for monomial in monomials:
        for left_index, left in enumerate(monomial):
            for right_index, right in enumerate(monomial):
                if left_index == right_index:
                    continue
                coefficient = Q(xi.get(left, 0)) * Q(zeta.get(right, 0))
                for index, variable in enumerate(monomial):
                    if index not in (left_index, right_index):
                        coefficient *= Q(point.get(variable, 0))
                if coefficient:
                    answer.append({
                        "ordered_pair": [repr(left), repr(right)],
                        "matching": [repr(variable) for variable in monomial],
                        "value": coefficient,
                    })
    return answer


def complete_product_rule_inventory(classifier) -> dict[str, object]:
    target, response = classifier.source_monomials()
    target_index = classifier.pair_index(target)
    response_index = classifier.pair_index(response)
    examples = (
        ("QQ_target", target_index, classifier.q(0, 1), classifier.q(2, 3)),
        ("QQ_response", response_index, classifier.q(0, 1), classifier.q(2, 3)),
        ("DQ_response", response_index, classifier.D, classifier.q(0, 1)),
        ("PS_response", response_index, classifier.p(0), classifier.s(1)),
        ("PQ_response", response_index, classifier.p(0), classifier.q(1, 2)),
        ("SQ_response", response_index, classifier.s(0), classifier.q(1, 2)),
    )
    records = {}
    for name, index, left, right in examples:
        complements = tuple(index[frozenset((left, right))])
        expected = 1 if name == "QQ_target" else 3
        require(len(complements) == expected, (name, complements))
        records[name] = {
            "retained_pair": [repr(left), repr(right)],
            "literal_complement_count": len(complements),
            "literal_complements": [
                [repr(variable) for variable in complement]
                for complement in complements
            ],
        }
    return {
        "pair_shapes": records,
        "actual_bivariate_st_boundary": [
            "J_xF(eta): the mixed second-order correction face",
            "sum over every ordered xi/zeta pair occurring in one literal matching",
        ],
        "right_hand_side_st_coefficient": 0,
        "isolated_marked_pair_equation": False,
        "conditional_isolation": (
            "only after J_xF(eta) and every other same-grade pair face vanish"
        ),
    }


def literal_mixed_two_pair_guard(classifier) -> dict[str, object]:
    target, response = classifier.source_monomials()
    q = classifier.q
    d = classifier.D
    point = {q(4, 5): Q(1), d: Q(1)}
    xi = {q(0, 1): Q(1), q(0, 2): Q(1)}
    zeta = {q(2, 3): Q(1), q(1, 3): Q(-1)}
    eta = {}

    target_expansion = expand_row(target, point, xi, zeta, eta)
    response_expansion = expand_row(response, point, xi, zeta, eta)
    require(target_expansion == {} and response_expansion == {},
            (target_expansion, response_expansion))

    target_faces = pair_faces(target, point, xi, zeta)
    response_faces = pair_faces(response, point, xi, zeta)
    require([face["value"] for face in target_faces] == [Q(1), Q(-1)],
            target_faces)
    require([face["value"] for face in response_faces] == [Q(1), Q(-1)],
            response_faces)
    require(sum((face["value"] for face in target_faces), Q(0)) == 0
            and sum((face["value"] for face in response_faces), Q(0)) == 0,
            (target_faces, response_faces))
    require(jacobian_mixed_face(target, point, eta) == 0
            and jacobian_mixed_face(response, point, eta) == 0,
            "the zero mixed correction acquired a Jacobian face")

    supported_variables = set(point) | set(xi) | set(zeta)
    supported_target_matchings = tuple(
        monomial for monomial in target
        if set(monomial) <= supported_variables
    )
    require(supported_target_matchings == (
        tuple(sorted((q(0, 1), q(2, 3), q(4, 5)))),
        tuple(sorted((q(0, 2), q(1, 3), q(4, 5)))),
    ), supported_target_matchings)

    occupied_q = {variable for variable, value in point.items()
                  if value and variable[0] == "q"}
    varied_q = set(xi) | set(zeta)
    require(occupied_q == {q(4, 5)} and occupied_q.isdisjoint(varied_q),
            (occupied_q, varied_q))
    offdiagonal_varied = {q(0, 2), q(1, 3)}
    require(offdiagonal_varied <= varied_q
            and offdiagonal_varied.isdisjoint(occupied_q),
            (offdiagonal_varied, occupied_q))

    return {
        "physical_output_word": "001122",
        "base_values": {
            "q45[22]": "1",
            "D": "1 (only for the direct response row)",
            "all_four_varied_cells": "0",
        },
        "actual_polynomial_family": {
            "q01[00]": "s",
            "q02[01]": "s",
            "q23[11]": "t",
            "q13[01]": "-t",
            "q45[22]": "1",
        },
        "complete_target_polynomial": "q45*(q01*q23+q02*q13)=st-st=0",
        "complete_direct_response_polynomial": "D*q45*(st-st)=0",
        "supported_target_matchings": [
            [repr(variable) for variable in monomial]
            for monomial in supported_target_matchings
        ],
        "all_supported_target_matchings_have_word": "001122",
        "other_mixed_target_words": "identically zero on this row packet",
        "first_missing_full_GHZ_rows": (
            "the three normalized pure target coefficients (and their full response/augmented companions)"
        ),
        "target_pair_faces": [
            {**face, "value": str(face["value"])} for face in target_faces
        ],
        "response_pair_faces": [
            {**face, "value": str(face["value"])} for face in response_faces
        ],
        "marked_retained_pair_value": "1",
        "silent_mate_pair_value": "-1",
        "mixed_correction_J_eta": "0",
        "base_occupied_q_support": ["q45[22]"],
        "base_nonzero_offdiagonal_q_cells": 0,
        "generic_support_change": "+4 varied cells; no occupied cell is killed",
        "minimum_support_consequence": "none: the family leaves the base support stratum",
        "existing_active_minor_consequence": (
            "none at the base: the offdiagonal cells q02[01],q13[01] are zero"
        ),
        "scope": (
            "literal complete mixed target plus direct-response coefficient; "
            "not a completion of the normalized pure targets or the other "
            "unary/four response/anchor rows"
        ),
    }


def route_audit() -> dict[str, object]:
    return {
        "occupied_occurrence_incompatible_direction": (
            "if additionally anchor-safe and marked, the pinned affine-line theorem deletes support"
        ),
        "nonzero_offdiagonal_base_cell": (
            "the pinned target-augmented identity produces an active determinant/cofactor product"
        ),
        "what_extraction_alone_supplies": (
            "only J_xF(eta)+sum(pair faces)=0 in the retained repeated grade"
        ),
        "not_supplied": [
            "support of xi,zeta,eta inside occupied coordinates",
            "vanishing of the other compatible pair packets",
            "a nonzero offdiagonal base cell",
            "extension of a local cokernel covector through augmented terminal rows",
        ],
        "smallest_remaining_full_row_statement": (
            "complete unary/four-response/anchor/q/ridge rows forbid the silent "
            "same-tail mate pair, or force one of its varied cells to be already "
            "occupied/active; otherwise the marked H2 packet is not isolated"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    classifier = load(
        "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py",
        "retained_pair_face_classifier",
    )
    ledger = {
        "theorem": "h3 retained-pair actual divided-Hasse minimum-support gate",
        "pins": PINS,
        "complete_product_rule_inventory": complete_product_rule_inventory(classifier),
        "literal_mixed_two_pair_guard": literal_mixed_two_pair_guard(classifier),
        "proved_route_scope": route_audit(),
        "verdict": (
            "Actual divided-Hasse coefficient extraction does not force the "
            "selected retained-pair lower packet.  It forces the sum of its "
            "mixed Jacobian correction and every compatible pair face.  A "
            "literal mixed 001122 target/direct-response family has marked "
            "pair +1 and silent mate -1 while both complete rows vanish "
            "identically.  Every varied cell is zero at the base, so the "
            "family deletes no occupied coordinate and presents no nonzero "
            "offdiagonal base cell to the existing active-minor theorem.  "
            "Minimum support alone therefore does not remove this complete-"
            "row alternative; a theorem using the omitted full rows may."
        ),
        "scope": (
            "exact matching-multiaffine bivariate coefficient extraction and "
            "a literal complete mixed target/direct-response row guard; no "
            "claim that the guard completes all physical GHZ rows"
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
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("actual divided-Hasse extraction isolates marked pair: NO")
    print("full st boundary: J*eta + ALL COMPATIBLE PAIR FACES")
    print("literal mixed guard: marked +1, silent mate -1")
    print("occupied-coordinate deletion: NO")
    print("nonzero offdiagonal base cell / active-minor route: NO")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
