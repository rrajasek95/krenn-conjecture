#!/usr/bin/env python3
"""Exact generic upper-label construction and lower/Rees obstruction.

For h=3 and the selected diagonal colour 0, the two literal cap rows have

    T(J1) = (beta, -alpha, -alpha),
    T(J2) = (-beta, -2 alpha, -2 alpha).

The combination

    J* = (beta-2 alpha) J1 + (beta+alpha) J2

has T(J*) = -3 alpha beta Delta.  Consequently the already physical
two-root Cartan source orbit, applied to J* and divided by 9 alpha beta,
has rho-even target -2(w-1)Delta.  Thus the upper root-decorated label map
is not a new generator on the generic alpha*beta != 0 branch.

The Cartan formula on a non-cycle P(J*) leaves the explicit lower remainder

    R+ = (1+rho) H_w d(P(J*)).

This remainder is rho-even.  It cannot cancel the Gate-I remainder
K_- d(u_012), because K_-=(1-rho)H_w is rho-odd and a rho-equivariant
differential preserves the parity splitting, including after invariant
divided-power/Rees base change.

The known fourth-Hasse filler is only formal: componentwise in the nonzero
root label D=(w-1)Delta its physical projection retains (H0-u)Eq.  This
checker freezes that tensor conormal and the independent literal Rees
membership guard; it does not claim that the actual R+ class is nonzero.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_signless_cartan_adjacent_power_shared_cell_gate.py":
        "9679c047e440f48899f1385682bcf64b725e049da01a42b8134b40c3fda73177",
    "computations/verify_h3_phi_diagonal_rees_extension_gate.py":
        "d719c507db7c2c1f2ecfb3b639cfae34fc06e930435891be789aa8243a844630",
    "computations/verify_oo_adjacent_power_relative_generator_inventory.py":
        "e25e7416273618acf39ee11d688fe3c980808a616c26eb49d3ef77509e3546b7",
    "computations/verify_h3_full_hasse_cone_d4_descent_obstruction.py":
        "ed2f2b3451074500b39a100da91ffefed27f748636de172d81aabd5cfe394240",
    "computations/verify_h3_source_valid_tower_first_obstruction.py":
        "ba37c966c2ef2cca2f8909a91e8ff8a8567282e68a847ac4eef75d3bb78a56ac",
    "computations/verify_h3_cut_swap_collision_word_orbit_obstruction.py":
        "d7281084a0fc084e6d951f527daf92c92faefebec183a83d6cfa33e055596c77",
}
EXPECTED_LEDGER_SHA256 = (
    "693b007a6dda020a6a075fe291e418c781a6ee1c00d6fb3a4ad669294c372239"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def add(left, right):
    return tuple(Q(a) + Q(b) for a, b in zip(left, right, strict=True))


def scale(value, vector):
    return tuple(Q(value) * Q(entry) for entry in vector)


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


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def audit_generic_upper_label():
    # The symbolic proof is the displayed two-line calculation.  Sweep
    # enough exact active values to guard every coefficient and sign.
    records = []
    for h in range(3, 13):
        for alpha, beta in ((Q(2), Q(3)), (Q(-3), Q(5, 2)),
                            (Q(7, 3), Q(-4))):
            j1 = (beta, -alpha, -alpha)
            j2 = (-beta, -(h - 1) * alpha, -(h - 1) * alpha)
            left = beta - (h - 1) * alpha
            right = beta + alpha
            jstar = add(scale(left, j1), scale(right, j2))
            expected = (-h * alpha * beta,) * 3
            require(jstar == expected,
                    ("the GHZ-valued cap combination changed", h,
                     alpha, beta, jstar))

            # Target coordinates are (pure0,mixed0,pure2,mixed2).  The
            # simultaneous local 0<->2 Weyl action fixes pure1 and sends
            # the two relevant pure summands to the two mixed words.
            d0 = (Q(-1), Q(1), Q(0), Q(0))
            d2 = (Q(0), Q(0), Q(-1), Q(1))
            defect = add(d0, d2)
            literal_target_scale = h * jstar[0]  # h*T(J*)
            even_cartan_target = scale(2 * literal_target_scale, defect)
            normalized = scale(Q(1, h * h * alpha * beta),
                               even_cartan_target)
            require(normalized == scale(-2, defect),
                    "the normalized even Cartan target is not -2(w-1)Delta")
            records.append({
                "h": h,
                "alpha": str(alpha),
                "beta": str(beta),
                "Jstar_coefficients": [str(left), str(right)],
                "T_Jstar": [str(value) for value in jstar],
                "normalized_even_target": [str(value)
                                             for value in normalized],
            })

    # At h=3 neither J1 nor J2 alone is uniformly proportional to Delta.
    # Their two branch coefficients become equal only on the exceptional
    # divisors beta=-alpha and beta=2alpha, respectively.
    alpha, beta = Q(2), Q(3)
    j1_branches = (beta, -alpha)
    j2_branches = (-beta, -2 * alpha)
    equal = (Q(1), Q(1))
    require(rank((j1_branches, equal)) == 2
            and rank((j2_branches, equal)) == 2,
            "one uncombined generic diagonal row unexpectedly gave Delta")
    return {
        "formula_all_h": (
            "J*=(beta-(h-1)alpha)J1+(beta+alpha)J2, "
            "T(J*)=-h alpha beta Delta"
        ),
        "h3_formula": "J*=(beta-2alpha)J1+(beta+alpha)J2",
        "literal_h3_target": "hT(J*)=-9 alpha beta Delta",
        "normalized_even_Cplus_target": "-2(w-1)Delta",
        "normalization": "1/(9 alpha beta)",
        "active_hypothesis": "alpha*beta != 0",
        "single_J1_exception": "beta=-alpha (trace zero)",
        "single_J2_exception": "beta=2alpha",
        "records": records,
    }


def audit_parity_and_remainder():
    # In the orbit basis (H,rho H), rho swaps the two coordinates.
    rho = ((Q(0), Q(1)), (Q(1), Q(0)))
    even = (Q(1), Q(1))
    odd = (Q(1), Q(-1))

    def mat_vec(matrix, vector):
        return tuple(dot(row, vector) for row in matrix)

    require(mat_vec(rho, even) == even and mat_vec(rho, odd) == scale(-1, odd),
            "the Cartan orbit parity split changed")
    require(rank((even, odd)) == 2, "even and odd Cartan lines met")

    # K_-=(1-rho)H maps every input to the odd line, while
    # K_+=(1+rho)H maps every input to the even line.  Applying a commuting
    # differential does not alter the output parity.  This finite matrix is
    # the exact parity statement for the two residuals.
    identity = ((Q(1), Q(0)), (Q(0), Q(1)))
    kminus = tuple(tuple(identity[i][j] - rho[i][j] for j in range(2))
                   for i in range(2))
    kplus = tuple(tuple(identity[i][j] + rho[i][j] for j in range(2))
                  for i in range(2))
    seed = (Q(1), Q(0))
    gate_i_remainder = mat_vec(kminus, seed)
    adjacent_remainder = mat_vec(kplus, seed)
    require(gate_i_remainder == odd and adjacent_remainder == even,
            "the two Cartan remainders lost their opposite parities")
    require(rank((gate_i_remainder, adjacent_remainder)) == 2,
            "the even adjacent remainder absorbed the odd Gate-I remainder")

    # Tensoring by an invariant divided-power/Rees algebra repeats the same
    # direct parity sum.  Check the h=3 jet lengths used by the diagonal
    # route; there is no cross-parity intersection at any level.
    jet_records = []
    for length in (1, 2, 3):
        evens = []
        odds = []
        for level in range(length):
            ev = [Q(0)] * (2 * length)
            od = [Q(0)] * (2 * length)
            ev[2 * level:2 * level + 2] = even
            od[2 * level:2 * level + 2] = odd
            evens.append(tuple(ev))
            odds.append(tuple(od))
        require(rank(evens) == rank(odds) == length
                and rank(evens + odds) == 2 * length,
                "Rees base change mixed the rho parity summands")
        jet_records.append({"length": length,
                            "even_rank": length,
                            "odd_rank": length,
                            "total_rank": 2 * length})
    return {
        "even_operator": "K_+=(1+rho)H_w",
        "odd_operator": "K_-=(1-rho)H_w",
        "Cartan_formula_on_adjacent_row": (
            "d K_+(P*)=(1+rho)(w-1)P* - K_+ d(P*)"
        ),
        "sole_lower_remainder": "R_+=K_+ d(P*) (rho-even)",
        "Gate_I_remainder": "R_-=K_- d(u_012) (rho-odd)",
        "can_one_absorb_the_other": False,
        "invariant_Rees_base_change": jet_records,
    }


def audit_formal_filler_and_rees_guard():
    # D=(w-1)Delta has four nonzero target labels.  In that root-label
    # basis the normalized even companion asks for -2D.
    defect = (Q(-1), Q(1), Q(-1), Q(1))
    require(sum(bool(value) for value in defect) == 4,
            "the root target label lost support")

    # The fourth-Hasse cone has projected boundary (B,Y) and desired (0,Y).
    # Tensor by -2D.  The polynomial covector (Y,-B) kills every projected
    # component but detects every nonzero desired component.  B,Y are kept
    # as formal independent monomials, so record only their coefficients.
    conormal_coefficients = []
    for value in defect:
        projected = (-2 * value, -2 * value)  # coefficients of (B,Y)
        desired = (Q(0), -2 * value)
        # Pairing coefficients after factoring B*Y:
        projected_pairing = projected[0] - projected[1]
        desired_pairing = -desired[1]
        require(projected_pairing == 0 and desired_pairing == 2 * value,
                "the root-decorated Hasse conormal changed")
        conormal_coefficients.append(desired_pairing)
    require(any(conormal_coefficients),
            "the root-decorated conormal tensor vanished")

    # Literal Rees membership is independent of evaluated divisibility.
    # M=<b,z,r>, N_lit=<b>, epsilon(b)=epsilon(z)=0, epsilon(r)=1.
    b = (Q(1), Q(0), Q(0))
    z = (Q(0), Q(1), Q(0))
    response = (Q(0), Q(0), Q(1))
    epsilon = lambda vector: vector[2]
    good = (b, b, response)
    bad = (z, b, response)
    require(tuple(map(epsilon, good)) == tuple(map(epsilon, bad))
            == (Q(0), Q(0), Q(1)),
            "the Rees representatives stopped agreeing after evaluation")
    good_obstruction = tuple(vector[1] for vector in good[:2])
    bad_obstruction = tuple(vector[1] for vector in bad[:2])
    require(good_obstruction == (Q(0), Q(0))
            and bad_obstruction == (Q(1), Q(0)),
            "the literal Rees obstruction changed")

    # Root decoration cannot make the bad low jet disappear: tensoring a
    # nonzero D with z remains nonzero over Q.
    decorated_bad = tuple(value * bad_obstruction[0] for value in defect)
    require(decorated_bad == defect and any(decorated_bad),
            "root decoration killed a nonzero literal low-jet class")
    return {
        "known_formal_filler": {
            "projected_boundary": ["-2D*(H0-u)*Eq", "-2D*Y*w"],
            "desired_boundary": ["0", "-2D*Y*w"],
            "missing_relative_correction": "+2D*(H0-u)*Eq",
            "componentwise_cokernel_pairing": [
                str(value) + "*(H0-u)*Y" for value in conormal_coefficients
            ],
            "source_valid_template": False,
            "reason": (
                "the selected fourth Hasse operator sends H_m to 1; a "
                "source-valid fourth tower puts its top coefficient back "
                "in the source ideal"
            ),
        },
        "literal_Rees_criterion": (
            "obs(P*)=[R_+-L_desired mod ell^r] in "
            "(ker epsilon/N_lit) tensor k[ell]/ell^r must vanish"
        ),
        "same_evaluated_jet_can_have_different_literal_obstruction": True,
        "actual_Rplus_obstruction_value": "not computed here",
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    ledger = {
        "theorem": "generic Cartan prolongation constructs the upper root label",
        "upper_label_construction": audit_generic_upper_label(),
        "parity_and_lower_remainder": audit_parity_and_remainder(),
        "formal_filler_and_Rees_guard": audit_formal_filler_and_rees_guard(),
        "sharp_status": (
            "on alpha*beta!=0 the literal J1/J2 combination J* and the "
            "physical Cartan source orbit construct the rho-even upper "
            "target -2(w-1)Delta.  The remaining construction is exactly "
            "the landing/nullhomotopy of R_+=(1+rho)H_w d(P(J*)) in the "
            "desired adjacent lower face.  It is parity-distinct from the "
            "rho-odd Gate-I remainder.  The old fourth-Hasse filler does "
            "not settle R+: it retains the root-decorated (H0-u) Eq "
            "conormal, after which literal Rees membership is still an "
            "independent finite criterion"
        ),
        "scope": (
            "generic beta!=0, alpha!=0 branch.  This constructs the upper "
            "label map, not the lower Cartan landing, its actual Rees "
            "membership, beta=0 collision, or Krenn's conjecture"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("generic Cartan adjacent-label ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 generic Cartan adjacent target-label prolongation: PASS")
    print("J* target: -3 alpha beta Delta; literal target: -9 alpha beta Delta")
    print("normalized rho-even Cartan upper target: -2(w-1)Delta")
    print("remaining lower face: R+=(1+rho)H_w d(P(J*))")
    print("Gate-I K_-d(u_012): rho-odd, hence parity-distinct")
    print("old formal filler: root-decorated (H0-u)Eq conormal remains")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
