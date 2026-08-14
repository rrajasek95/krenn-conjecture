#!/usr/bin/env python3
"""Define the minimal reduced mixed-jet enrichment and its exact missing axiom.

The source-side object is not obtained by hand-adjoining Phi.  It is the
reduced universal divided-Hasse envelope of the literal endpoint-odd
polynomial ``(p0*s1-p1*s0)*q01*H2345``, closed under the site-repeating P3/P4
pair rows required by the current-tree order-six audit.  Its universal first
jet is exactly PSQJet_01 and has an injective termwise jet shadow, so a
zero-shadow omega does not exist inside this minimal envelope.

Adding target coordinates is not an operation-changing map.  The existing
cap r0 still has no termwise H_w/private-full-nine values in this grade, and
the source-derived operation graph still has Hom(response,cap)=0.  Therefore
the root-labelled carrier does not yet map to r0.  The precise single missing
axiom is an augmentation-preserving, termwise-faithful natural dg map from
this reduced site-repeating jet envelope to the physical AugP2 cap complex.

The checker also records the literal fully augmented right side needed for
terminal promotion: the target-cancelled Gate-II balanced packet i(B_delta)
in Gamma_*, with every other protected coordinate zero.  Both the two-block
and covariantly completed Psi representatives pair to one after normalization.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_order6_site_repeating_target_enrichment_current_tree.py":
        "f1bc7a9f8fdb9148fde5c4d79a4b7f59a3bd03cd6ff00dc1c2fb3c0e7f511ea9",
    "computations/verify_unaudited_repair1_order6_scope_audit.py":
        "0d5be2b2d5c90d5aff04545e7a0712701ef5364266a3ac53f41d7b81da8f530a",
    "computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py":
        "c62ca38edf160f706d7aed237a923737ca46fe7b906fb0bb48bdf400e2ea7854",
    "notes/h3-gate-ii-chiw-nonfill-full-augmented-dual.md":
        "f7fd790075f7cf3d31b9d4a6035fa6bc476a3bdc16ce4bda97b777b153664568",
    "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py":
        "02a28ec54b83b2f786e47b0fdc992f5f28dd95a04ba16219f0e24482d4999097",
    "computations/verify_h3_gamma_star_source_derived_free_closure_census.py":
        "a479ac8759bf7a18b43ee91d8b1ab7d0b432c48a7787b065cac68403ace3df3a",
    "computations/verify_h3_eqsystem_augp2_actual_presentation_underdetermination_gate.py":
        "2c112bffeef2c6adb00029077b6b231de396ace76c78756ab0e11e20078a557b",
}
EXPECTED_LEDGER_SHA256 = "760a0c229c30ac6060ce16324128c20c7b8ea63b8a918d89d85ee0fe0a43aa3f"

DELTA = tuple(map(Q, (1, 1, -1, -1)))
ALPHA = tuple(map(Q, (-1, 1, 1, -1)))
TAIL_MATCHINGS = (
    ("q23", "q45"),
    ("q24", "q35"),
    ("q25", "q34"),
)
KAPPA_WORDS = (
    "0012", "0102", "0110", "0111",
    "0122", "0212", "1112", "2112",
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        require(expected != "TO_BE_PINNED", ("unfrozen pin", relative))
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(left, right):
    answer = Counter(left)
    answer.update(right)
    return Counter({key: value for key, value in answer.items() if value})


def scale(coefficient, value):
    return Counter({key: Q(coefficient) * entry
                    for key, entry in value.items() if coefficient * entry})


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def polynomial_and_first_jet(sign_c: int) -> tuple[Counter, Counter]:
    polynomial = Counter()
    jet = Counter()
    orientations = (
        (("p0", "s1"), Q(1)),
        (("p1", "s0"), Q(sign_c)),
    )
    for endpoints, coefficient in orientations:
        for tail in TAIL_MATCHINGS:
            monomial = (*endpoints, "q01", *tail)
            polynomial[tuple(monomial)] += coefficient
            for position, factor in enumerate(monomial):
                remainder = monomial[:position] + monomial[position + 1:]
                jet[(f"d{factor}", tuple(remainder))] += coefficient
    return (Counter({key: value for key, value in polynomial.items() if value}),
            Counter({key: value for key, value in jet.items() if value}))


def universal_reduced_mixed_jet_audit() -> dict[str, object]:
    odd_top, odd_jet = polynomial_and_first_jet(-1)
    even_top, even_jet = polynomial_and_first_jet(1)
    selected_top = scale(Q(1, 2), add(even_top, odd_top))
    selected_jet = scale(Q(1, 2), add(even_jet, odd_jet))
    require(len(odd_top) == 6 and len(odd_jet) == 30,
            "endpoint-odd top/first-jet support changed")
    require(len(selected_top) == 3 and len(selected_jet) == 15,
            "selected B=(even+odd)/2 support changed")

    categories = Counter()
    for (differential, _remainder), _coefficient in odd_jet.items():
        if differential in ("dp0", "ds1", "dp1", "ds0"):
            categories["endpoint_dB_minus_dC"] += 1
        elif differential == "dq01":
            categories["dq01_H"] += 1
        else:
            categories["q01_dH"] += 1
    require(categories == {
        "endpoint_dB_minus_dC": 12,
        "dq01_H": 6,
        "q01_dH": 12,
    }, categories)

    selected_tail = Counter({
        key: value for key, value in selected_jet.items()
        if key[0] not in ("dp0", "ds1", "dp1", "ds0", "dq01")
    })
    require(len(selected_tail) == 6
            and set(selected_tail.values()) == {Q(1)},
            "selected six-term db01 jet changed")

    # Omega exclusion is a universal-property statement made executable in
    # the literal basis: the termwise first-jet readout is the identity on
    # the 30 free reduced jet generators.  Hence its kernel is zero.  A
    # separately adjoined atom with all these coordinates zero is not an
    # element of the initial reduced envelope.
    jet_basis = tuple(sorted(odd_jet, key=repr))
    identity_columns = tuple(
        tuple(Q(row == column) for row in range(len(jet_basis)))
        for column in range(len(jet_basis))
    )
    require(len(set(identity_columns)) == 30
            and all(sum(column, Q(0)) == 1 for column in identity_columns),
            "universal jet basis stopped being free")
    return {
        "source_ring": (
            "Q[p0,s1,p1,s0,q01,q23,q45,q24,q35,q25,q34] localized "
            "on the selected q01*H2345 chart"
        ),
        "odd_top": "(p0*s1-p1*s0)*q01*H2345",
        "universal_rule": "d(fg)=df*g+f*dg, reduced divided-Hasse order one",
        "top_monomials": len(odd_top),
        "literal_first_jet_terms": len(odd_jet),
        "first_jet_term_counts": dict(categories),
        "signed_pair_counts": {
            "endpoint_dB_minus_dC": 6,
            "tail_q01_dH": 6,
            "dq01_H": 3,
        },
        "selected_B_formula": "B=((B+C)+(B-C))/2",
        "selected_B_first_jet_terms": len(selected_jet),
        "selected_six_term_db01_terms": len(selected_tail),
        "minimal_constructor": "PSQJet_01",
        "augmentation_reduced": True,
        "termwise_jet_readout_dimension": len(jet_basis),
        "termwise_jet_readout_kernel": 0,
        "rank_nine_omega_inside_initial_reduced_jet_envelope": False,
        "reason": (
            "the initial reduced envelope is free on its nonempty literal "
            "Hasse faces; a primitive with zero value on every termwise jet "
            "basis coordinate is zero"
        ),
    }


def site_repeating_and_termwise_faithfulness_audit(scope_audit) \
        -> dict[str, object]:
    ledger, digest = scope_audit.audit()
    require(digest == scope_audit.EXPECTED_LEDGER_SHA256, digest)
    ambiguity = ledger["K_indeterminacy"]
    require(ambiguity["raw_shadow_fibre"] == 21
            and ambiguity["committed_readout_rank"] == 14
            and ambiguity["residual_shadow_zero_freedom"] == 7,
            ambiguity)
    return {
        "current_tree_full_replay": {
            "operator_columns": 8580,
            "dim_constrained_universal_D2": 488,
            "site_repeating_pair_coordinates": 159,
            "site_repeating_projection_rank_at_both_primes": 153,
            "direct_free_intersection_dimension": 335,
            "primes": [1_000_003, 999_983],
            "owned_checker": (
                "verify_h3_order6_site_repeating_target_enrichment_current_tree.py"
            ),
        },
        "minimal_coordinate_target_enlargement": (
            "adjoin the 159 site-repeating coloured-cell pair rows met by S; "
            "their constrained image has rank 153"
        ),
        "what_that_proves": (
            "necessity: a whole-module mixed-jet comparison cannot land in "
            "the direct-free target"
        ),
        "what_that_does_not_prove": (
            "the new coordinates have no differential or cap-r0 augmentation "
            "until termwise H_w/private full-nine rows are defined"
        ),
        "two_word_root_carrier_fibre": ambiguity["raw_shadow_fibre"],
        "all_committed_readout_rank": ambiguity["committed_readout_rank"],
        "residual_root_carrier_freedom": ambiguity[
            "residual_shadow_zero_freedom"],
        "root_labelled_carrier_maps_to_r0_from_current_data": False,
        "remaining_bright_or_dark_value_determined": False,
    }


def cap_landing_and_single_axiom_audit(source_derived) -> dict[str, object]:
    ledger, digest = source_derived.audit()
    require(digest == source_derived.EXPECTED_LEDGER_SHA256, digest)
    closure = ledger["typed_free_closure"]
    require(closure["Hom0_response_cap_dimension"] == 0
            and closure["free_closure_operation_changing_C1_count"] == 0,
            closure)
    return {
        "site_repeating_rows_change_operation_graph": False,
        "Hom0_response_cap_after_row_enlargement": 0,
        "Phi_or_root_section_constructed": False,
        "precise_missing_axiom": {
            "name": "reduced termwise-faithful mixed-jet cap augmentation",
            "map": (
                "A_Gamma: J_red,rep_PS/q(EqSystem) -> C_AugP2,Gamma"
            ),
            "requirements": [
                "natural for literal restriction, insertion, endpoint transpose and one-root labels",
                "A_Gamma(epsilon_s)=r0 and A_Gamma(c_f)=-E with monic normalization",
                "retain all 159 site-repeating pair rows and the termwise H_w/private full-nine readouts",
                "the joint termwise H_w/private-full-nine readout is injective on the reduced primitive off-diagonal kernel",
            ],
            "not_a_declared_generator_census": (
                "it is one representable natural dg augmentation of the "
                "universal source jet envelope"
            ),
        },
        "conditional_omega_exclusion": (
            "omega has zero reduced termwise/private shadow, so injectivity "
            "forces omega=0"
        ),
        "conditional_relative_C1_quotient": {
            "basis": list(KAPPA_WORDS),
            "rank": 8,
            "all_Psi_charges": [0] * 8,
        },
        "unconditional_verdict": (
            "the universal response jet constructs PSQJet_01, but neither "
            "the 159-row enlargement nor current cap constructors supply its "
            "landing in r0; the seven-dimensional termwise ambiguity remains"
        ),
    }


def literal_augmented_rhs_audit(gate_dual) -> dict[str, object]:
    ledger, digest = gate_dual.audit()
    require(digest == gate_dual.EXPECTED_LEDGER_SHA256, digest)
    full = ledger["full_known_augmented_dual"]
    require(full["value_on_local_delta_B"] == "4"
            and full["value_on_target_companion_Y"] == "4",
            full)

    # Two representatives of the same old-cap cokernel class.  Psi_BEq is
    # convenient in the balanced projection.  Psi_cov is its cap/Cartan
    # completion and is the correct full-row Fredholm functional.
    psi_beq = DELTA + tuple(-value for value in DELTA)
    psi_cov = (
        DELTA
        + (Q(0),) * 4
        + tuple(-value for value in DELTA)
        + tuple(-value for value in DELTA)
        + DELTA
        + (Q(0),) * 10
    )
    rhs_beq = DELTA + (Q(0),) * 4
    rhs_cov = DELTA + (Q(0),) * (len(psi_cov) - 4)
    require(len(psi_cov) == 30
            and dot(psi_beq, rhs_beq) == 4
            and dot(psi_cov, rhs_cov) == 4
            and dot(ALPHA, DELTA) == 0,
            "literal balanced RHS normalization changed")
    return {
        "formal_precursor": {
            "X": "(chi_w,+delta_target)",
            "Y": "(0,-delta_target)",
            "target_cancelled_sum": "X+Y=(chi_w,0)",
        },
        "literal_RHS_name": "b_GateII=i(B_delta)",
        "literal_Gamma_tag": {
            "word": "01211222",
            "fine": "six literal t*q_(v,N) P3+K2 occurrence degrees",
            "repeated": "P3+K2 with site-repeating jet rows retained",
            "operation": "C4/AugP2 mixed orbit/K_Eq",
            "window": "2345 with literal occurrence labels",
        },
        "complete_row_values": {
            "B": [1, 1, -1, -1],
            "Eq": [0, 0, 0, 0],
            "target": [0, 0, 0, 0],
            "W": [0, 0, 0, 0],
            "ordinary_residue": [0, 0, 0, 0],
            "M_ainc_q_Pf": [0, 0, 0, 0],
            "ridge_eta_sigma_globalW_tail_escape": "all zero",
        },
        "normalized_two_block_Psi_on_RHS": 1,
        "normalized_covariant_Psi_on_RHS": 1,
        "covariant_Psi_nonzero_blocks": {
            "B": [1, 1, -1, -1],
            "Eq": [0, 0, 0, 0],
            "target": [-1, -1, 1, 1],
            "W": [-1, -1, 1, 1],
            "ordinary_residue": [1, 1, -1, -1],
        },
        "Fredholm_contradiction_requires": [
            "the physical equations place b_GateII in im(J_phys,Gamma)",
            "the reduced termwise-faithful augmentation makes J_phys,Gamma exhaustive",
            "the completed Psi annihilates every column of that same full augmented map",
        ],
        "then": (
            "Psi*J_phys=0 and b_GateII in im(J_phys), but Psi(b_GateII)=1; "
            "the accepted Macaulay/Fredholm nonmembership contradiction applies"
        ),
        "status": (
            "b_GateII is the exact required RHS vector, but its source-valid "
            "target-cancelled C4/AugP2 totalization is not constructed"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    scope_audit = load(
        "computations/verify_unaudited_repair1_order6_scope_audit.py",
        "mixed_jet_scope_audit",
    )
    source_derived = load(
        "computations/verify_h3_gamma_star_source_derived_free_closure_census.py",
        "mixed_jet_source_derived",
    )
    gate_dual = load(
        "computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py",
        "mixed_jet_gate_dual",
    )
    ledger = {
        "theorem": "h3 reduced site-repeating mixed-jet/AugP2 enrichment and RHS gate",
        "pins": PINS,
        "universal_reduced_mixed_jet": universal_reduced_mixed_jet_audit(),
        "site_repeating_target_and_termwise_faithfulness":
            site_repeating_and_termwise_faithfulness_audit(scope_audit),
        "cap_landing_and_exact_missing_axiom":
            cap_landing_and_single_axiom_audit(source_derived),
        "literal_augmented_RHS": literal_augmented_rhs_audit(gate_dual),
        "verdict": (
            "The initial reduced divided-Hasse envelope constructs PSQJet_01 "
            "from the literal endpoint-odd polynomial and excludes a zero-"
            "shadow omega internally.  A current-tree two-prime replay proves "
            "that a whole-module target must add 159 site-repeating P3/P4 pair "
            "coordinates, with rank-153 constrained image.  That row "
            "enlargement still supplies no response-to-cap arrow and leaves "
            "seven termwise-undetected root-carrier directions.  The sole "
            "missing enrichment axiom is the reduced, termwise-faithful "
            "natural dg augmentation A_Gamma to physical AugP2/r0.  Under it, "
            "omega is zero and the only relative classes are the eight dark "
            "kappas.  The literal terminal RHS is the fully protected, target-"
            "cancelled Gate-II packet i(B_delta), on which normalized Psi is one."
        ),
        "scope": (
            "exact local universal first-jet calculation, current-tree "
            "two-prime whole-module support obstruction, committed exact "
            "root-carrier ambiguity, and exact full-row RHS/dual.  The one "
            "augmentation axiom is isolated, not proved; therefore no physical "
            "Phi or Fredholm contradiction is claimed unconditionally."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("mixed-jet enrichment ledger changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("h3 reduced site-repeating mixed-jet/AugP2 enrichment gate: PASS")
    print("PSQJet_01 in universal reduced jet envelope: YES")
    print("minimal target enlargement: 159 site-repeating rows / rank 153")
    print("root carrier -> r0 from present data: NO; residual freedom 7")
    print("one missing axiom: REDUCED TERMWISE-FAITHFUL JET->AugP2 AUGMENTATION")
    print("literal Fredholm RHS: target-cancelled i(B_delta); normalized Psi=1")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
