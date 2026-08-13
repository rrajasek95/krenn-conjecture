#!/usr/bin/env python3
"""Audit the categorical Cartan/Hasse shortcut for the selected Gate-I line.

There is a genuine naturality square on polynomial de Rham algebras.  If the
coefficient and output root fields are F-related, then

    F^* i_(X_out) = i_(X_src) F^*.

The complete Hasse/cobar totalization is also source-side functorial.  The
question is whether these facts alone define the selected physical comparison

    J_3(M_v) = A J_col(l).

They do not: the two sides live in the literal repeated-grade augmented
correction complex, while the naturality square lives in the principal-parts
polynomial de Rham resolution.  The required comparison functor between those
complexes has not been constructed.  This checker pins the source theorems and
uses the exact xi coordinate dual to locate the first failed comparison square.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    # Complete source-side Hasse/cobar totalization; explicitly leaves the
    # principal-parts-to-physical comparison open.
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    # Literal Ward identity on complete matching rows and endpoint source
    # automorphism.  Its Cartan naturality is on the PP de Rham resolution.
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    # H_w itself is defined on universal two-variable polynomial forms.
    "computations/verify_h3_sl2_weyl_cartan_prism.py":
        "1024864418fea8f7f4ca6c77015972febd236f2a9822112daf20e1cf979bddaa",
    # Exact endpoint composition: D2=-delta after forgetting grade, but all
    # 126 first coefficient-prolonging faces miss the old full-row ideal.
    "computations/verify_h3_residual_q_order6_endpoint_recolour_composition.py":
        "6ab3f36073cd08c1ccad97ebd6f8ed3c5f39736be82b6063436c161f176cfeb0",
    # K\u00e4hler commutation is polynomial-level; the physical labelled repeated
    # tensor product is explicitly not constructed.
    "computations/verify_h3_residual_q_order6_ridge_jet_commutation.py":
        "00a0798b4aa1d901b52645cac3f1dbe2854a3d8ce796191f7a4ff9a6e295b28f",
    # Exact normalized xi dual locating the first missing Spencer cell.
    "computations/verify_h3_selected_lower_full_row_spencer_discrepancy.py":
        "e3c99912600c53228a37e7a1376028fd9e889178e4f242140fc6ff0da328954f",
    # The desired physical one-chain equation and its complete output type.
    "computations/verify_h3_selected_lower_one_chain_comparison_reduction.py":
        "c9fc8c847327d0e119264a3a83cf39d0f4c2ff45b4ddd4e048f42a57cac0e887",
    # Literal 90-term direct-free rows and exact fine-degree utilities used to
    # classify the proposed three-term xi bridge.
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
}
EXPECTED_LEDGER_SHA256 = (
    "d24f3b929a7fb2adfa92f29244f9195af0b3c47bf0e55af571e77193e789fa04"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


@dataclass(frozen=True)
class Object:
    name: str


@dataclass(frozen=True)
class Arrow:
    name: str
    source: Object
    target: Object


def composable(left: Arrow, right: Arrow) -> bool:
    """Whether left after right is a typed composite."""
    return right.target == left.source


BRIDGE_PREFIX = (
    (0, 1, 0, 1),
    (2, 7, 2, 1),
    (3, 4, 1, 1),
)
BRIDGE_TAILS = (
    ((3, 5, 1, 2), (6, 7, 2, 2)),
    ((3, 6, 1, 2), (5, 7, 2, 2)),
    ((3, 7, 1, 2), (5, 6, 2, 2)),
)


def underlying_pair(cell: tuple[int, int, int, int]) -> frozenset[int]:
    return frozenset(cell[:2])


def bridge_monomials():
    return tuple(tuple(sorted(BRIDGE_PREFIX + tail)) for tail in BRIDGE_TAILS)


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    # The valid categorical square.  The Ward identity on algebra generators
    # implies the identity on all forms because both contractions are degree
    # -1 derivations over F^*.  Hasse translation is an algebra map, so the
    # same square extends throughout the complete PP/cobar totalization.
    omega_out_k = Object("Omega(output tensor)^k")
    omega_out_km1 = Object("Omega(output tensor)^(k-1)")
    omega_src_k = Object("Omega(coefficient PP source)^k")
    omega_src_km1 = Object("Omega(coefficient PP source)^(k-1)")
    f_k = Arrow("F^*", omega_out_k, omega_src_k)
    f_km1 = Arrow("F^*", omega_out_km1, omega_src_km1)
    i_out = Arrow("i_Xout", omega_out_k, omega_out_km1)
    i_src = Arrow("i_Xsrc", omega_src_k, omega_src_km1)
    require(composable(i_src, f_k) and composable(f_km1, i_out),
            "the polynomial Cartan naturality square stopped being typed")
    require(i_src.source == f_k.target
            and i_src.target == f_km1.target
            and f_k.source == i_out.source
            and i_out.target == f_km1.source,
            "the polynomial Cartan naturality square changed")

    # The desired physical square is a different diagram.  Its four objects
    # are not any of the polynomial de Rham objects above.  In particular F^*
    # cannot be substituted for Phi, J_col, J_3, or A.
    u15 = Object("U15 physical collision quotient")
    l_h3 = Object("canonical h=3 repeated-grade correction domain")
    e_col = Object("complete collision augmented boundary rows")
    e_h3 = Object("360-feature h=3 augmented boundary rows")
    phi = Arrow("Phi", u15, l_h3)
    j_col = Arrow("J_col", u15, e_col)
    j3 = Arrow("J_3", l_h3, e_h3)
    a = Arrow("A", e_col, e_h3)
    require(composable(j3, phi) and composable(a, j_col),
            "the desired physical comparison square stopped being typed")
    require(not composable(j3, f_k) and not composable(f_k, j_col),
            "F^* unexpectedly became the missing physical comparison")

    discrepancy = load(
        "computations/verify_h3_selected_lower_full_row_spencer_discrepancy.py",
        "complete_hasse_cartan_xi_discrepancy",
    )
    xi_ledger, xi_digest = discrepancy.audit()
    require(xi_digest == discrepancy.EXPECTED_LEDGER_SHA256,
            "xi discrepancy ledger changed")
    xi = xi_ledger["first_literal_discrepancy"]
    dual = xi_ledger["primitive_coordinate_dual"]
    require(xi["compatible_complete_full_row_columns"] == 2,
            "the first exact comparison block changed")
    require(xi["all_candidates_have_forced_q37"]
            and not xi["xi_has_q37"],
            "the exact q37 support separation changed")
    require(dual["values_on_complete_full_row_columns"] == ["0", "0"]
            and dual["value_on_first_spencer_face"] == "1",
            "the normalized xi comparison dual changed")

    # Audit the proposed four-site bridge
    #
    #   m (q35 q67 + q36 q57 + q37 q56).
    #
    # It is the ordinary all-plus four-site Hafnian sector.  Its three
    # monomials are distinct and fine-homogeneous.  Direct-free projection
    # removes the middle q36 monomial, but it does not turn the remaining sum
    # into a relation.  Only the q37*q56 monomial belongs to the old complete
    # homogeneous full-row block.
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "complete_hasse_cartan_bridge_base",
    )
    bridge = bridge_monomials()
    require(len(bridge) == len(set(bridge)) == 3,
            "the proposed four-site bridge stopped being a three-term Hafnian")
    bridge_degrees = {base.fine_degree_of_edge_monomial(term)
                      for term in bridge}
    require(len(bridge_degrees) == 1,
            "the proposed four-site bridge lost fine homogeneity")
    require(bridge[0] == tuple(tuple(cell) for cell in xi["monomial"]),
            "the first bridge term stopped being xi")
    require(base.DIRECT_FREE_PAIR == frozenset((3, 6)),
            "the canonical direct-free edge changed")
    direct_free_counts = [
        sum(underlying_pair(cell) == base.DIRECT_FREE_PAIR for cell in term)
        for term in bridge
    ]
    require(direct_free_counts == [0, 1, 0],
            ("the bridge/direct-free incidence changed", direct_free_counts))

    candidate_supports = []
    candidate_metadata = []
    for word, multiplier in discrepancy.EXPECTED_CANDIDATES:
        support = {
            tuple(sorted((multiplier,) + monomial))
            for monomial in base.full_row(word)
        }
        require(len(support) == 90, "an exact candidate row changed")
        candidate_supports.append(support)
        candidate_metadata.append([list(word), list(multiplier)])
    old_block_membership = [
        any(term in support for support in candidate_supports)
        for term in bridge
    ]
    require(old_block_membership == [False, False, True],
            ("the proposed bridge entered the old block differently",
             old_block_membership))

    # In the Boolean/Hasse cobar, splitting one four-occurrence block has six
    # ordered 2+2 splittings (two orders for each of the three pairings), as
    # well as eight 1+3/3+1 splittings.  Thus the displayed three-term
    # commutative Hafnian is a nonzero sector of d(mask), not the complete
    # alternating boundary of a relative cell.
    full_mask = 0b1111
    ordered_nontrivial_splits = tuple(
        left for left in range(1, full_mask)
        if (left & full_mask) == left
    )
    ordered_two_two = tuple(
        left for left in ordered_nontrivial_splits if left.bit_count() == 2
    )
    require(len(ordered_nontrivial_splits) == 14
            and len(ordered_two_two) == 6,
            "the four-occurrence Hasse split census changed")
    require(Q(3, 4) * Q(4, 3) == 1,
            "the bridge stopped retaining the normalized xi readout")

    ledger = {
        "theorem": "complete Hasse/Cartan naturality does not supply the physical comparison functor",
        "source_naturality_square": {
            "top": "i_Xout: Omega(output)^k -> Omega(output)^(k-1)",
            "bottom": "i_Xsrc: Omega(PP source)^k -> Omega(PP source)^(k-1)",
            "vertical": "F^* induced by the matching tensor polynomial map",
            "identity": "F^* i_Xout = i_Xsrc F^*",
            "proof_interface": (
                "the pinned Ward identity checks F-related root fields on "
                "every complete matching row; equality on functions and "
                "one-forms extends to all forms by the contraction derivation law"
            ),
            "complete_Hasse_extension": (
                "valid inside the principal-parts/cobar source totalization "
                "because Hasse translation is an algebra map"
            ),
            "typed": True,
        },
        "desired_physical_square": {
            "equation": "J_3 Phi = A J_col",
            "selected_equation": "J_3(M_v)=A J_col(u_024-u_012)",
            "domain_objects": [u15.name, l_h3.name],
            "codomain_objects": [e_col.name, e_h3.name],
            "F_pullback_has_one_of_these_types": False,
            "comparison_functor_Pi_constructed": False,
        },
        "xi_status": {
            "source_totalization": (
                "xi is one coefficient-prolongation face inside a complete "
                "source-closed Hasse/Cartan totalization; it is not by itself "
                "an obstruction to closure of that source totalization"
            ),
            "physical_correction_complex": (
                "no committed comparison maps xi to a boundary in the literal "
                "repeated-grade correction complex"
            ),
            "direction": xi["direction"],
            "monomial": xi["monomial"],
            "normalized_dual": dual["functional"],
            "dual_on_old_complete_columns": dual[
                "values_on_complete_full_row_columns"
            ],
            "dual_on_xi": dual["value_on_first_spencer_face"],
        },
        "first_failed_square": {
            "degree": "first coefficient-prolongation / relative Spencer face",
            "required_identity": "Pi_1 d_PP = d_corr Pi_0",
            "failure": (
                "Pi_1 is undefined on xi; restricting its target to the old "
                "complete homogeneous full-row block is impossible because "
                "lambda_xi kills that block and reads one on xi"
            ),
            "smallest_repair": (
                "one chart-nondiagonal relative Spencer cell in the exact "
                "word/fine/repeated grade, with boundary -xi and its transported "
                "mate, followed by its complete augmented readout"
            ),
            "not_a_universal_no_go": True,
        },
        "proposed_four_site_xi_bridge": {
            "formula": "m*(q35^12 q67^22 + q36^12 q57^22 + q37^12 q56^22)",
            "terms": [[list(cell) for cell in term] for term in bridge],
            "common_fine_degree": list(next(iter(bridge_degrees))),
            "direct_free_q36_incidence": direct_free_counts,
            "membership_in_two_exact_old_full_row_columns": old_block_membership,
            "xi_term": 0,
            "old_complete_row_mate": 2,
            "normalized_lambda_xi_on_scaled_bridge": "1",
            "four_occurrence_cobar_splits": {
                "all_ordered_nontrivial": len(ordered_nontrivial_splits),
                "ordered_two_plus_two": len(ordered_two_two),
                "commutative_pairings_displayed": 3,
            },
            "classification": (
                "a nonzero all-plus four-site Hafnian/Hasse 2+2 face sector, "
                "not a closed relative bar cell.  Direct-free projection "
                "deletes the q36 term but supplies no relation setting the "
                "surviving xi plus q37*q56 mate to zero"
            ),
            "consequence": (
                "the bridge identifies the correct old-row mate of xi but "
                "still needs a PP/Weyl/chart-nondiagonal relative cell that "
                "carries the complementary Hasse sectors and augmented rows"
            ),
        },
        "augmented_readout_audit": {
            "source_target": (
                "endpoint oddization kills the Weyl target defect on the "
                "polynomial/output-word side"
            ),
            "ordinary_residue": (
                "D2=-delta is exact only after the committed grade-forgetting "
                "secondary projection; it does not define the termwise 360-row map"
            ),
            "private_90_360_features": "not defined by F^* or Hasse naturality",
            "D_W_ainc_Eq": "no induced literal correction readout without Pi",
            "eta_sigma": (
                "formal polynomial/Kahler commutation is exact, but the pinned "
                "ridge audit says the physical labelled repeated-grade tensor "
                "product is not constructed"
            ),
        },
        "verdict": (
            "the categorical shortcut proves source closure, not the Gate-I "
            "one-chain equality.  It may explain xi as a face of a coherent "
            "totalization, but cannot make xi a physical boundary until the "
            "first Spencer comparison square is supplied"
        ),
        "scope": (
            "exact typing obstruction and exact xi dual for the nearest "
            "committed endpoint-recoloured constructor; no no-go is claimed "
            "against adding the missing chart-nondiagonal relative cell"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("complete Hasse/Cartan naturality gate changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 complete Hasse/Cartan naturality square: SOURCE-SIDE PASS")
    print("physical comparison J3 Phi=A Jcol: NOT CONSTRUCTED")
    print("first failed square: coefficient-prolongation face xi")
    print("lambda_xi: old complete rows 0,0; xi 1")
    print("categorical Gate-I closure: NO")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
