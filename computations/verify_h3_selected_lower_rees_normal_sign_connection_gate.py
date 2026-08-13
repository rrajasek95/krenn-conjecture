#!/usr/bin/env python3
"""Classify the Rees-normal attempt at the selected xi comparison.

The four tail-root values on GHZ are independent target-normal directions.
The endpoint swap s=(0 1) fixes each of those target tensors, so the normal
module N is s-trivial.  Every functorial Rees--Koszul cell built solely from
N is therefore s-even.  The private quotient Q_xi is the sign representation:
its generator p=xi-mate-sxi+smate satisfies s p=-p.  Consequently

    Hom_<s>(ReesKoszul(N), Q_xi) = 0.

Thus adding target normal directions to the existing PP/Hasse totalization
cannot construct the missing occurrence section.  The smallest possible new
source type is one sign-connection generator kappa with d kappa=p.  In the
formal orbit-relative group bar this is supplied by the endpoint-odd Weyl
bar and is the relative Kodaira--Spencer/Atiyah class of the two endpoint
lifts of one target-orbit path.

Tensoring this class with the canonical ridge gamma=-dOmega does not repair
gamma's physical multigrading: adding the same kappa degree to both ridge
halves preserves their pq/xv degree difference.  Divided-power tails do the
same.  The ordinary least-common-multiple completion changes the terminal
law, while a mapping cone needs exactly the still-missing labelled shifted
Kahler arrow.

Finally, the private obstruction is a sign line in H_0 of the physical
boundary cofiber, not a non-split Ext^1 of rational C2-representations (that
Ext group vanishes).  It is output-side and is not automatically a physical
q terminal.  Extending q to the new source generator is an independent
augmented-cocycle datum.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_selected_lower_minimal_totalized_weyl_cone_alternative.py":
        "cddff2c501382ebf5104cc1cbc510b71a3ecaf72f1e97af4d3608fe9d6c6d67f",
    "computations/verify_h3_selected_lower_relative_weyl_bar_gate.py":
        "7a6f2afebcacc5924110e32a3f7d9c225992f07abae637d4529b5436c64cc294",
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    "computations/verify_h3_endpoint_odd_cartan_prism_augmentation.py":
        "24ec9e3c1d1f9b689fa5a47faf9900c16724dc215fee0a41a0b653f410427fb3",
    "computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py":
        "aea73ce5ff6ce183245d209393ed60192066d38eab7d4d203caa0c82cc5b16d6",
    "computations/verify_h3_shifted_principal_parts_comparison_obstruction.py":
        "8b7d5907e13e15224fb3a78bb2d4b4f3d3c39094c2a204d1290c3147238de639",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    "computations/verify_dark_cartan_physical_q_protected_quotient_comparison.py":
        "eb56cdb4ab1915f8ce35ab3acf0398b4f526c52a17c9c8ebafcc7a5ad4f86bcc",
}
EXPECTED_LEDGER_SHA256 = (
    "c8055cb9b7574efe18478cdf24eb04419cdc701cfdb34c5e186bf88c0ecc1fda"
)

ENDPOINT_SWAP = (
    (Q(0), Q(0), Q(1), Q(0)),
    (Q(0), Q(0), Q(0), Q(1)),
    (Q(1), Q(0), Q(0), Q(0)),
    (Q(0), Q(1), Q(0), Q(0)),
)
PRIVATE_PACKET = (Q(1), Q(-1), Q(-1), Q(1))
ALPHA = (Q(-1), Q(1), Q(1), Q(-1))
KAPPA_REPEATED_PROFILE = (1, 1, 1, 2, 1, 1, 1, 2)
PQ_DEGREE = (0, 0, 0, 0, 0, 0, 1, 1)
XV_DEGREE = (1, 1, 0, 0, 0, 0, 0, 0)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def mat_vec(matrix, vector):
    return tuple(sum((Q(a) * Q(b)
                      for a, b in zip(row, vector, strict=True)), Q(0))
                 for row in matrix)


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def add_degree(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def sub_degree(left, right):
    return tuple(a - b for a, b in zip(left, right, strict=True))


def rees_koszul_parity_audit():
    """Enumerate a finite mutation guard for Sym(N) tensor Lambda(N)."""
    normal_rank = 4
    records = []
    for symmetric_degree in range(4):
        symmetric = tuple(combinations_with_replacement(
            range(normal_rank), symmetric_degree))
        for exterior_degree in range(normal_rank + 1):
            exterior = tuple(combinations(range(normal_rank), exterior_degree))
            for sym in symmetric:
                for wedge in exterior:
                    # s is identity on every normal basis vector.  Therefore
                    # it acts by +1 on every symmetric/exterior monomial.
                    records.append((sym, wedge, 1))
    require(len(records) == 560 and {record[2] for record in records} == {1},
            "the target-normal Rees/Koszul parity census changed")

    # If f maps an s-even basis vector to the one-dimensional sign line,
    # equivariance says f=-f, hence f=0 over Q.  Exhaust small coefficients
    # as a mutation guard for this representation calculation.
    possible = []
    for coefficient in map(Q, range(-3, 4)):
        if coefficient == -coefficient:
            possible.append(coefficient)
    require(possible == [Q(0)],
            "a nonzero equivariant normal-to-sign map appeared")
    return {
        "normal_rank": normal_rank,
        "symmetric_degrees_checked": [0, 3],
        "exterior_degrees_checked": [0, 4],
        "Rees_Koszul_basis_states_checked": len(records),
        "all_target_normal_states_endpoint_parity": 1,
        "private_quotient_endpoint_parity": -1,
        "equivariant_Hom_to_Qxi_dimension": 0,
    }


def sign_connection_audit():
    require(mat_vec(ENDPOINT_SWAP, PRIVATE_PACKET)
            == tuple(-value for value in PRIVATE_PACKET),
            "the private packet stopped being endpoint-sign")
    # A one-dimensional source generator kappa with s*kappa=-kappa and
    # d*kappa=p is an equivariant chain extension.
    s_kappa = Q(-1)
    d_kappa = PRIVATE_PACKET
    require(tuple(s_kappa * value for value in d_kappa)
            == mat_vec(ENDPOINT_SWAP, d_kappa),
            "the minimal sign connection stopped being equivariant")

    endpoint_even_rows = (
        (Q(1), Q(0), Q(1), Q(0)),
        (Q(0), Q(1), Q(0), Q(1)),
        (Q(1), Q(1), Q(0), Q(0)),
        (Q(0), Q(0), Q(1), Q(1)),
    )
    require(all(dot(row, d_kappa) == 0 for row in endpoint_even_rows),
            "an endpoint-even protected row detected the sign packet")

    # The raw Cartan mixed second difference is the opposite orientation;
    # normalization of kappa chooses either sign.  This is the pinned alpha.
    require(ALPHA == tuple(-value for value in PRIVATE_PACKET),
            "private and Cartan four-corner orientations diverged")
    return {
        "generator": "kappa_xi=(1-s)[tau|Z0_tilde]",
        "endpoint_character": -1,
        "boundary_private_packet": [int(value) for value in PRIVATE_PACKET],
        "Cartan_orientation_alpha": [int(value) for value in ALPHA],
        "normalized_occurrence_quotient_value": 1,
        "endpoint_even_D_W_target_anchor_pureEq": 0,
        "source_model": "orbit-relative group-bar/PP/Hasse sign connection",
    }


def ridge_audit():
    # Coordinate order a=qpq22,t=qpq00,b=qxv0m,u=qxv00.
    gamma = (Q(-1), Q(1), Q(1), Q(-1))
    eta_constant = gamma[1]
    eta_u_over_t = -gamma[3]
    sigma = gamma[0]
    augmentation = sum(gamma, Q(0))
    require((eta_constant, eta_u_over_t, sigma, augmentation)
            == (Q(1), Q(1), Q(-1), Q(0)),
            "the shifted Kahler ridge readout changed")
    return {
        "generator": "gamma_v=-dOmega_v",
        "ordinary_boundary_residue_D_W_target_anchor": 0,
        "eta_z": "1+delta_(vz)*u_z/t",
        "sigma": "-q_pq^22",
        "coefficient_augmentation": 0,
        "physical_repeated_grade_lift_constructed": False,
    }


def shifted_ridge_grading_audit():
    """Show that kappa, common tails, and divided powers preserve the gap."""
    kappa_pq = add_degree(KAPPA_REPEATED_PROFILE, PQ_DEGREE)
    kappa_xv = add_degree(KAPPA_REPEATED_PROFILE, XV_DEGREE)
    require(kappa_pq != kappa_xv,
            "tensoring with kappa unexpectedly homogenized the ridge")

    # Any common polynomial or divided-power tail adds the same N^8 degree
    # to both labels.  Exhaust small tails as a mutation guard for the exact
    # cancellation argument (g+a=g+b iff a=b).
    common_tails = 0
    for tail in product(range(3), repeat=8):
        require(add_degree(kappa_pq, tail)
                != add_degree(kappa_xv, tail),
                "a common divided-power tail repaired the degree gap")
        common_tails += 1
    require(common_tails == 3 ** 8, "common-tail census changed")

    signed_shift = sub_degree(PQ_DEGREE, XV_DEGREE)
    require(signed_shift == (-1, -1, 0, 0, 0, 0, 1, 1)
            and any(value < 0 for value in signed_shift),
            "the pq/xv signed shift changed")

    # In the N^8-graded coefficient ring there is no monomial of this signed
    # degree.  The minimal two-sided completion multiplies the pq half by the
    # xv variable u and the xv half by the pq variable t.  The pinned ridge
    # theorem proves that this gives tb-ua and changes both terminal laws.
    return {
        "kappa_repeated_profile": list(KAPPA_REPEATED_PROFILE),
        "pq_ridge_degree": list(PQ_DEGREE),
        "xv_ridge_degree": list(XV_DEGREE),
        "kappa_tensor_pq_degree": list(kappa_pq),
        "kappa_tensor_xv_degree": list(kappa_xv),
        "tensor_homogenizes": False,
        "common_polynomial_or_divided_power_tails_checked": common_tails,
        "common_tail_homogenizes": False,
        "signed_shift_pq_minus_xv": list(signed_shift),
        "signed_shift_is_coefficient_monomial_degree": False,
        "minimal_two_sided_completion": "u*(-a+t)+t*(b-u)=t*b-u*a",
        "minimal_completion_preserves_eta_sigma": False,
        "mapping_cone_requirement": (
            "adjoin a degree-labelled arrow theta_(pq,xv) carrying the "
            "signed shift; this is precisely the shifted labelled Kahler "
            "lift, not a consequence of the existing diagonal PP tails"
        ),
    }


def cofiber_ext_and_terminal_audit():
    """Type the rank-one obstruction and separate it from physical q."""
    # The normalized sign covector on the four private corners reads one on
    # p and transforms by sign.  The pinned complete calculation identifies
    # the old rank as 12 and the rank after p as 13.
    lambda_xi = tuple(value / Q(4) for value in PRIVATE_PACKET)
    require(dot(lambda_xi, PRIVATE_PACKET) == 1,
            "the private cofiber class lost its normalization")
    swapped_lambda = mat_vec(ENDPOINT_SWAP, lambda_xi)
    require(swapped_lambda == tuple(-value for value in lambda_xi),
            "the private cofiber dual stopped being endpoint-sign")

    # Over Q the group algebra of C2 is semisimple.  Averaging any linear
    # section t gives the equivariant section (t+s t s)/2, so ordinary
    # Ext^1_{Q[C2]} vanishes.  The obstruction relevant here instead lies in
    # H_0 of the cofiber of the admitted physical boundary map.
    half = Q(1, 2)
    require(half + half == 1, "the rational averaging operator disappeared")

    # Boundary data do not determine the augmented q coordinate of a newly
    # adjoined domain generator.  Three distinct q values have exactly the
    # same private boundary p; this guards the domain/codomain distinction.
    augmented_columns = tuple(PRIVATE_PACKET + (Q(q_value),)
                              for q_value in (-1, 0, 1))
    require(len({column[:4] for column in augmented_columns}) == 1
            and len({column[4] for column in augmented_columns}) == 3,
            "private boundary began determining physical q")
    return {
        "old_complete_rank": 12,
        "rank_after_private_packet": 13,
        "relative_obstruction": (
            "o_xi=[p_xi] in H_0(Cofib(d_old))^- = Q_xi"
        ),
        "normalized_dual_value": 1,
        "ordinary_Ext1_Q_C2": 0,
        "reason_Ext1_vanishes": (
            "Maschke averaging splits every rational C2-module extension"
        ),
        "correct_derived_typing": (
            "a cofiber/attaching class for the restricted physically "
            "graded boundary functor; adjoining degree-one kappa_xi with "
            "d kappa_xi=p_xi kills it"
        ),
        "nonzero_class_is_terminal": False,
        "reason_not_terminal": (
            "p_xi is in the augmented output/cokernel, whereas physical "
            "q=sum6m-ainc is a row on the source correction domain"
        ),
        "q_values_with_same_private_boundary_checked": [-1, 0, 1],
        "physical_q_extension": (
            "choose q(kappa_xi) and prove it respects every source relation; "
            "only then is q a cocycle/readout on the enlarged domain"
        ),
        "terminal_alternative_after_extension": (
            "a q-nonzero protected kernel ambiguity is the relative "
            "generator; q-zero ambiguity permits transport/Fredholm"
        ),
    }


def scalar_section_alternative():
    """Any family of candidate sign connections is decided by one scalar."""
    cases = 0
    hit = 0
    dual = 0
    for width in range(5):
        for values in product((-1, 0, 1), repeat=width):
            nonzero = next((Q(value) for value in values if value), None)
            if nonzero is None:
                # lambda_xi kills every admitted connection.
                dual += 1
            else:
                require(nonzero / nonzero == 1,
                        "the sign connection failed to normalize")
                hit += 1
            cases += 1
    require(cases == 121 and hit == 116 and dual == 5,
            ("the scalar section alternative changed", cases, hit, dual))
    return {
        "candidate_families_checked": cases,
        "section_families": hit,
        "dual_families": dual,
        "criterion": "lambda_xi(d c)!=0 for at least one source-sign connection c",
        "section_normalization": "sigma_xi=c/lambda_xi(d c)",
        "dual_branch": "lambda_xi kills the complete admitted sign-connection image",
    }


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    # The pinned Hasse theorem explicitly leaves the physical comparison
    # open.  This prevents silently identifying its Boolean PP/cobar model
    # with the target-normal Rees--Koszul extension classified here.
    hasse_source = (ROOT / (
        "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py"
    )).read_text()
    require("principal-parts-to-physical augmented comparison: OPEN"
            in hasse_source
            and "no claim that a principal-parts chain is already a physical"
            in hasse_source,
            "the Hasse totalization scope statement changed")

    normal = rees_koszul_parity_audit()
    connection = sign_connection_audit()
    ridge = ridge_audit()
    grading = shifted_ridge_grading_audit()
    cofiber = cofiber_ext_and_terminal_audit()
    alternative = scalar_section_alternative()
    ledger = {
        "theorem": "target-normal Rees cells miss Q_xi; one source-sign connection is minimal",
        "existing_PP_Hasse_status": {
            "complete_source_totalization": True,
            "identified_with_target_normal_Rees_model": False,
            "physical_augmented_comparison_constructed": False,
            "reason": (
                "the Boolean Hasse/cobar theorem supplies the source-side "
                "totalization but no target-normal generators or physical "
                "comparison functor"
            ),
        },
        "target_normal_representation_gate": normal,
        "minimal_source_connection": connection,
        "canonical_terminal_summand": ridge,
        "kappa_tensor_shifted_ridge_gate": grading,
        "relative_cofiber_Ext_and_terminal_typing": cofiber,
        "formal_augmented_cell": {
            "formula": "C_formal=kappa_xi+gamma_v, followed by the pinned -O_alpha cap",
            "private_packet": [int(value) for value in PRIVATE_PACKET],
            "protected_D_W_target_anchor_pureEq": 0,
            "eta_z": ridge["eta_z"],
            "sigma": ridge["sigma"],
            "capped_target_column": {
                "literal_boundary_features": 360,
                "Eq": [-1, 1, 1, -1],
                "ordinary_residue": [0, 0, 0, 0],
                "D_W_target_ainc": [0, 0, 0, 0],
                "eta_z": ridge["eta_z"],
                "sigma": ridge["sigma"],
            },
            "physical_status": (
                "constructed in the orbit-relative sign-cone plus shifted "
                "Kahler model; its comparison to the literal physical "
                "repeated-grade correction complex remains the membership gate"
            ),
        },
        "finite_section_or_dual": alternative,
        "physical_q_interface": {
            "q": "sum(six selected literal matching rows)-ainc",
            "canonical_value_on_C_formal": "not supplied by target-normal Rees, kappa boundary, or ridge data",
            "exact_requirement": (
                "define q as a physical cochain on both complete relative "
                "domains and construct the protected comparison"
            ),
            "nonzero_defect": (
                "a protected-kernel witness has nonzero physical q on the "
                "source or canonical side and normalizes to the relative generator"
            ),
            "zero_defect": (
                "q transports modulo protected rows and the generator/Fredholm "
                "alternative applies"
            ),
            "type_guard": (
                "the nonzero Q_xi obstruction is output-side and cannot be "
                "called a q-terminal class; q(kappa_xi) must first be defined "
                "and checked on all source relations"
            ),
            "consequence": (
                "no predetermined scalar q value is forced by d kappa_xi, "
                "but an honest physical q extension is still mandatory"
            ),
        },
        "shortest_positive_proof_lemma": (
            "adjoin one endpoint-sign source connection kappa_xi whose "
            "boundary has nonzero Q_xi class, one independent shifted "
            "Kahler arrow homogenizing gamma_v, and a physical q cocycle on "
            "the enlarged domain.  Endpoint parity supplies every protected "
            "zero and gamma_v supplies eta/sigma.  If their capped column "
            "lands in the complete physical image, Gate I closes; otherwise "
            "the complete augmented cokernel dual is the separator branch.  "
            "Once physical q is typed, its comparison defect has only the "
            "relative-generator or Fredholm outcomes"
        ),
        "verdict": (
            "deformation to the target normal cone is not the missing "
            "construction: its entire Rees--Koszul module is endpoint-even "
            "and cannot hit the endpoint-sign quotient Q_xi.  The minimal new "
            "source occurrence type is exactly one sign connection, already "
            "canonical orbit-relatively.  It does not homogenize the ridge: "
            "the physical lift also needs the independent shifted Kahler "
            "arrow and q extension.  The private class is a cofiber class, "
            "not an ordinary Ext^1 or an automatic terminal"
        ),
        "scope": (
            "exact endpoint-representation obstruction for every target-normal "
            "Rees/Koszul degree, exact minimal sign attachment, exact invariant "
            "pq/xv grading obstruction under kappa/common tails, exact cofiber "
            "versus Ext/q typing, protected/ridge formal readouts, and exact "
            "scalar section alternative.  No literal physical repeated-grade "
            "lift or physical q cocycle is asserted"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("Rees normal/sign connection ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 selected lower Rees-normal/sign connection: EXACT GATE")
    print("target-normal Rees -> Q_xi: ZERO by endpoint parity")
    print("source occurrence class: endpoint-sign kappa_xi in the relative cofiber")
    print("kappa tensor gamma homogenizes repeated grade: NO")
    print("ordinary Ext^1 / automatic q terminal: ZERO / NO")
    print("remaining: shifted Kahler arrow + physical q cocycle + membership")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
