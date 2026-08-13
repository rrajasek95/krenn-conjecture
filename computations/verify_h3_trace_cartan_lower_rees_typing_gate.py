#!/usr/bin/env python3
"""Reduce the generic Cartan lower face to the trace jet and audit typing.

The generic combination from c6e08c6 is an equality of full cap matrices,
not only of target diagonals:

    J* = (beta-(h-1)alpha)J1 + (beta+alpha)J2
       = -h alpha beta I.

Hence its normalized rho-even Cartan remainder is universally

    R+ = -(1/h)(1+rho)H_w d(P(I)),

independent of alpha,beta on their active open.  At h=3 the coefficient is
-1/3.  This is the smallest input whose literal truncated-Rees class must
be computed.

The current committed maps do not put this trace-Cartan remainder and the
diagonal N_lit module in one labelled codomain.  Two Hasse/Rees-linear maps
with identical evaluated target and order-zero data can send the trace
remainder to a literal boundary b or to a nonboundary evaluation-zero jet z.
Thus its class is presently ill-typed/underdetermined, not proved nonzero.

At beta=0 the J1/J2 combination vanishes and their Weyl defects span only
the colour-2 root branch.  The missing colour-0 branch is exactly the
order-h unary/complementary target already isolated in the collision route.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_generic_cartan_adjacent_target_label_prolongation.py":
        "fc241034b4e2ce457f65ed059fa9266422108f1d098328938cdb82a9f6f182b0",
    "computations/verify_h3_phi_diagonal_rees_extension_gate.py":
        "d719c507db7c2c1f2ecfb3b639cfae34fc06e930435891be789aa8243a844630",
    "computations/verify_diagonal_rees_saturation_cap_jet_bockstein.py":
        "12c4cc4a947d99eee22cbd87e900ac6c7a56df2c533c4c44c52f0ab0fcedee2a",
    "computations/verify_oo_adjacent_power_relative_generator_inventory.py":
        "e25e7416273618acf39ee11d688fe3c980808a616c26eb49d3ef77509e3546b7",
    "computations/verify_h3_cut_swap_odd_prism_kdu_typing_gate.py":
        "a1c7868bee94baf12f0f4915305bb1e21cdc3f6732ccec9adf3d68768d3d90b0",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
}
EXPECTED_LEDGER_SHA256 = (
    "3b6a9b46c2511b69c06be5810e603cdc42856290b233d86dca7d5f8a57d50da2"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def identity(size=3):
    return tuple(tuple(Q(int(row == column)) for column in range(size))
                 for row in range(size))


def matrix_add(*terms):
    return tuple(tuple(sum(Q(coefficient) * Q(matrix[row][column])
                           for coefficient, matrix in terms)
                       for column in range(3)) for row in range(3))


def matrix_scale(coefficient, matrix):
    return matrix_add((coefficient, matrix))


def rank(rows):
    work = [list(map(Q, row)) for row in rows]
    pivot_row = 0
    columns = len(work[0]) if work else 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def audit_trace_reduction():
    records = []
    for h in range(3, 21):
        for alpha, beta in ((Q(2), Q(3)), (Q(-5, 2), Q(7)),
                            (Q(4, 3), Q(-2))):
            k0 = tuple(tuple(Q(int(row == column == 0))
                             for column in range(3)) for row in range(3))
            one = identity()
            tau = alpha + beta
            k1 = matrix_add((tau, k0), (-alpha, one))
            k2 = matrix_add((alpha, k0), (-alpha, one))
            j1 = k1
            j2 = matrix_add((-beta, k0), (h - 1, k2))
            left = beta - (h - 1) * alpha
            right = beta + alpha
            jstar = matrix_add((left, j1), (right, j2))
            expected = matrix_scale(-h * alpha * beta, one)
            require(jstar == expected,
                    ("J* stopped being the full trace matrix", h,
                     alpha, beta, jstar))

            # P is linear in its cap matrix and the Cartan roots do not act
            # on the scalar alpha,beta.  The normalized coefficient is
            # (h^2 alpha beta)^-1 * (-h alpha beta) = -1/h.
            remainder_coefficient = (Q(1, 1) / (h * h * alpha * beta)
                                     * (-h * alpha * beta))
            require(remainder_coefficient == Q(-1, h),
                    "the trace-Cartan remainder retained alpha or beta")
            records.append({
                "h": h,
                "alpha": str(alpha),
                "beta": str(beta),
                "Jstar": "-h*alpha*beta*I",
                "Rplus_coefficient": str(remainder_coefficient),
            })
    return {
        "full_matrix_identity": (
            "J*=(beta-(h-1)alpha)J1+(beta+alpha)J2="
            "-h alpha beta I"
        ),
        "universal_lower_remainder": (
            "R+=-(1/h)(1+rho)H_w d(P(I))"
        ),
        "h3_remainder": "R+=-(1/3)(1+rho)H_w d(P(I))",
        "parameter_dependence": "none after normalization",
        "records": records,
    }


def audit_rees_typing_counterguard():
    # The trace-Cartan lower module currently has one displayed generator r.
    # The diagonal Rees model has M=<b,z,response>, N_lit=<b>, and
    # epsilon(b)=epsilon(z)=0.  Both maps below preserve all currently fixed
    # order-zero/evaluated data; only phi_bad has nonzero literal obstruction.
    b = (Q(1), Q(0), Q(0))
    z = (Q(0), Q(1), Q(0))
    response = (Q(0), Q(0), Q(1))
    epsilon = lambda vector: vector[2]
    good = (b, b, response)
    bad = (z, b, response)
    require(tuple(map(epsilon, good)) == tuple(map(epsilon, bad))
            == (Q(0), Q(0), Q(1)),
            "the two comparison maps stopped agreeing after evaluation")
    good_obs = tuple(vector[1] for vector in good[:2])
    bad_obs = tuple(vector[1] for vector in bad[:2])
    require(good_obs == (Q(0), Q(0)) and bad_obs == (Q(1), Q(0)),
            "the trace Rees typing counterguard changed")

    # Rees-linear extension repeats either choice coefficientwise.  It does
    # not turn the bad order-zero choice into a boundary at higher length.
    jet_records = []
    for length in (1, 2, 3):
        good_jet = good_obs + (Q(0),) * max(0, length - 2)
        bad_jet = bad_obs + (Q(0),) * max(0, length - 2)
        good_jet = good_jet[:length]
        bad_jet = bad_jet[:length]
        require(not any(good_jet) and bad_jet[0] == 1,
                "Rees linearity removed the comparison-map ambiguity")
        jet_records.append({
            "length": length,
            "good_obstruction": [str(value) for value in good_jet],
            "bad_obstruction": [str(value) for value in bad_jet],
        })
    return {
        "Cartan_lower_domain": "complete trace principal-parts source orbit",
        "diagonal_codomain": (
            "M_rees/N_lit on the physical 15-label collision quotient"
        ),
        "committed_map_between_them": False,
        "two_maps_with_same_fixed_data": {
            "phi_good": "trace remainder -> b in N_lit",
            "phi_bad": "trace remainder -> z in ker(epsilon)\\N_lit",
            "same_evaluated_target_and_order_zero_data": True,
        },
        "jet_records": jet_records,
        "consequence": (
            "the actual truncated-Rees class cannot be computed from upper "
            "target, seed coherence, and Rees linearity alone; the shifted "
            "physical label map tau_plus is a prior typing datum"
        ),
    }


def audit_existing_fillers():
    # The known formal fourth-Hasse projection and desired boundary in
    # (Eq,w), with formal independent B=H0-u and Y suppressed to their
    # coefficients.  (Y,-B) kills projected and sees desired.
    projected = (Q(1), Q(1))
    desired = (Q(0), Q(1))
    require(projected[0] - projected[1] == 0
            and desired[0] - desired[1] == -1,
            "the fourth-Hasse reduced-Eq separator changed")

    # Odd M_v/collision rows cannot cancel an even trace remainder.  The
    # parity basis makes the separation primitive over Q.
    odd = (Q(1), Q(-1))
    even = (Q(1), Q(1))
    require(rank((odd, even)) == 2,
            "the odd collision family entered the even trace line")
    return {
        "fourth_Hasse_reduced_Eq_family": {
            "formal_projected_boundary": ["(H0-u)*Eq", "Y*w"],
            "desired_boundary": ["0", "Y*w"],
            "cokernel": "-(H0-u)*Y",
            "kills_trace_remainder": False,
        },
        "literal_Mv_collision_family": {
            "rho_parity": "odd",
            "trace_remainder_parity": "even",
            "kills_trace_remainder": False,
        },
        "smallest_new_interface": (
            "tau_plus from the complete trace-Cartan PP orbit to the "
            "diagonal 15-label Rees module, followed by a relative cell "
            "for any nonzero class of tau_plus(R+)-L_adj"
        ),
    }


def audit_beta_zero():
    h = 3
    alpha = Q(2)
    beta = Q(0)
    j1 = (beta, -alpha, -alpha)
    j2 = (-beta, -(h - 1) * alpha, -(h - 1) * alpha)
    require(j2 == tuple((h - 1) * value for value in j1),
            "the beta-zero diagonal rows stopped collapsing")
    jstar = tuple((beta - (h - 1) * alpha) * left
                  + (beta + alpha) * right
                  for left, right in zip(j1, j2, strict=True))
    require(jstar == (Q(0), Q(0), Q(0)),
            "J* survived the beta-zero collision")

    # Branch basis D0,D2 records the two pure-to-mixed root defects.  The
    # beta-zero J rows see only pure colour 2 for the chosen 0<->2 Weyl.
    d0 = (Q(1), Q(0))
    d2 = (Q(0), Q(1))
    j1_defect = (Q(0), -alpha)
    required = (Q(1), Q(1))
    require(rank((j1_defect, required)) == 2
            and rank((j1_defect, d0)) == 2,
            "the beta-zero cap row acquired the missing root branch")
    return {
        "J2_relation": "J2=(h-1)J1",
        "Jstar": 0,
        "surviving_root_branch": "D2 only",
        "missing_root_branch": "D0",
        "physical_source_for_missing_branch": (
            "the selected-colour order-h unary target jet, or a forced "
            "complementary surviving label"
        ),
        "trace_Cplus_status": (
            "-1/h times the identity-cap Cartan orbit still constructs the "
            "abstract signless upper correction, but it does not identify "
            "the collapsed selected diagonal jet with that correction"
        ),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    ledger = {
        "theorem": "trace-Cartan lower Rees typing gate",
        "trace_reduction": audit_trace_reduction(),
        "Rees_typing_counterguard": audit_rees_typing_counterguard(),
        "existing_filler_audit": audit_existing_fillers(),
        "beta_zero_collision": audit_beta_zero(),
        "sharp_status": (
            "the generic lower remainder is the parameter-free trace class "
            "-(1/3)(1+rho)H_w d(P(I)).  Its numerical truncated-Rees value "
            "is not yet a well-typed invariant because the committed "
            "Cartan and diagonal modules lack tau_plus; Rees linearity does "
            "not choose that map.  The old fourth-Hasse family leaves the "
            "reduced-Eq conormal and the literal M_v family has opposite "
            "parity.  At beta=0 the J rows lose exactly the D0 branch"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("trace-Cartan Rees ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 trace-Cartan lower/Rees typing gate: PASS")
    print("J*=-3 alpha beta I; R+=-(1/3)(1+rho)H_w d(P(I))")
    print("actual Rees class: ill-typed until shifted map tau_plus exists")
    print("old fourth-Hasse filler: reduced-Eq conormal survives")
    print("odd M_v family: parity-distinct")
    print("beta=0: missing root branch D0 requires order-3 unary/complement")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
