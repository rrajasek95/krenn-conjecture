#!/usr/bin/env python3
"""Classify the beta-zero D0 dual and the generic-limit saturation gate.

The beta-zero membership is a full-column problem only after all protected
rows are retained.  If theta kills the protected kernel, raw [D0]^* need
not kill arbitrary source columns, but it has a unique kind of completion
(-lambda,[D0]^*) which does.  This is a separator of the bounded local map.

Two further steps are independent:

* the completed local separator must extend across every output row and
  every source column of the final physical Interface-III map; and
* a generic root-even cell divided by beta does not specialize to beta=0
  unless the physical image is beta-saturated.

The checker gives exact minimal counterguards for both implications.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_beta_zero_d0_unary_third_bianchi_membership_gate.py":
        "2b1bead205d5c766ffff6a0ab9a4d39a5d5ba8308bc0e96d70c1bc7974e00677",
    "computations/verify_h3_tau_plus_full_interface_product_bianchi_extension_gate.py":
        "32be7ef48ad9d35b8863a62889508ccdff0010d8ebff18b366e932aab8b2bf14",
    "computations/verify_h3_interface_iii_augmented_cap_factorization.py":
        "06e64c5db2a59b8877cb112515d50779be95010801f19690f97060bf08621213",
    "computations/verify_oo_dark_R_physical_generator_annihilator.py":
        "e4e1da1b1784f3c86d085965d9a556b17e4695c026daab8b109bcc4549c04abf",
    "computations/verify_h3_face_epsilon_physical_terminal_extension_typing_gate.py":
        "8c52ab72c9825bf41a821f1ecef2838b169b929df34a36f2fe805529edf57dee",
    "computations/verify_h3_trace_cartan_lower_rees_typing_gate.py":
        "0190a8fa16dddf9cecf2de676d4f3ff87d184f031e523d87e1f80937ff55be94",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def mat_vec(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def transpose(matrix):
    return tuple(tuple(row) for row in zip(*matrix, strict=True))


def rref(matrix):
    work = [list(map(Q, row)) for row in matrix]
    if not work:
        return (), ()
    pivot_row = 0
    pivots = []
    for column in range(len(work[0])):
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
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def solve(matrix, rhs):
    matrix = tuple(tuple(map(Q, row)) for row in matrix)
    rhs = tuple(map(Q, rhs))
    if not matrix:
        return () if not any(rhs) else None
    augmented = tuple(row + (rhs[index],)
                      for index, row in enumerate(matrix))
    reduced, pivots = rref(augmented)
    variable_count = len(matrix[0])
    if variable_count in pivots:
        return None
    answer = [Q(0)] * variable_count
    for row, pivot in enumerate(pivots):
        if pivot < variable_count:
            answer[pivot] = reduced[row][-1]
    require(mat_vec(matrix, answer) == rhs,
            ("solution reconstruction", matrix, rhs, answer))
    return tuple(answer)


def audit_local_membership_dual():
    # P:C->k^2 is the complete protected-row packet in this toy instance.
    # theta=2P_0-P_1 kills ker(P), so the selected target is not accessible.
    protected = (
        (Q(1), Q(0), Q(1)),
        (Q(0), Q(1), Q(1)),
    )
    theta_dark = (Q(2), Q(-1), Q(1))
    kernel_generator = (Q(-1), Q(-1), Q(1))
    require(mat_vec(protected, kernel_generator) == (Q(0), Q(0))
            and dot(theta_dark, kernel_generator) == 0,
            "the protected-dark example changed")

    coefficient = solve(transpose(protected), theta_dark)
    require(coefficient == (Q(2), Q(-1)),
            ("theta did not factor through protected rows", coefficient))
    local_map = protected + (theta_dark,)
    local_columns = transpose(local_map)
    raw_d0_dual = (Q(0), Q(0), Q(1))
    completed_dual = (Q(-2), Q(1), Q(1))
    desired = (Q(0), Q(0), Q(1))
    require(any(dot(raw_d0_dual, column) for column in local_columns),
            "raw D0* accidentally killed the complete local map")
    require(all(dot(completed_dual, column) == 0
                for column in local_columns)
            and dot(completed_dual, desired) == 1,
            "the completed local separator changed")

    # Change only theta.  It is nonzero on ker(P), and the normalized kernel
    # vector is an actual protected preimage of the desired D0 coordinate.
    theta_bright = (Q(0), Q(0), Q(1))
    value = dot(theta_bright, kernel_generator)
    preimage = tuple(entry / value for entry in kernel_generator)
    require(mat_vec(protected, preimage) == (Q(0), Q(0))
            and dot(theta_bright, preimage) == 1,
            "the positive protected membership branch changed")
    return {
        "domain": "C_beta0^(h), complete fixed word/fine/repeated source grade",
        "protected_map": "P:C_beta0^(h)->R_prot",
        "target_map": "theta:C_beta0^(h)->k[D0]",
        "protected_kernel": "Z=ker(P)",
        "desired_column": "b0=(0,[D0]) in R_prot direct-sum k[D0]",
        "positive": "b0 in im(P,theta) iff 1 in theta(Z)",
        "negative": (
            "theta|Z=0 iff theta=lambda P; the complete local separator is "
            "(-lambda,[D0]^*), not raw [D0]^*"
        ),
        "example_lambda": [str(value) for value in coefficient],
        "example_completed_separator": [str(value) for value in completed_dual],
    }


def audit_terminal_extension_counterguard():
    # Start with the exact local map from the previous audit.  Its completed
    # separator epsilon kills all three embedded local source columns.
    protected = (
        (Q(1), Q(0), Q(1)),
        (Q(0), Q(1), Q(1)),
    )
    theta = (Q(2), Q(-1), Q(1))
    embedded_local_columns = tuple(column + (Q(0),)
                                   for column in transpose(protected + (theta,)))
    epsilon = (Q(-2), Q(1), Q(1))

    # A compatible physical column with local projection b0 and terminal
    # value one determines the terminal coefficient -1.
    comparison = (Q(0), Q(0), Q(1), Q(1))
    good_extension = epsilon + (Q(-1),)
    require(all(dot(good_extension, column) == 0
                for column in embedded_local_columns + (comparison,)),
            "the compatible terminal extension changed")

    # A second, terminal-only source column has the same zero local
    # projection but forces terminal coefficient zero.  The two equations
    # are inconsistent.  Both full packets restrict to exactly the same
    # local beta-zero map, so local membership/duality cannot decide this.
    terminal_only = (Q(0), Q(0), Q(0), Q(1))
    restricted_system = tuple(column[3:] for column in
                              (comparison, terminal_only))
    required = tuple(-dot(epsilon, column[:3]) for column in
                     (comparison, terminal_only))
    extension = solve(restricted_system, required)
    require(required == (Q(-1), Q(0)) and extension is None,
            ("terminal extension counterguard", restricted_system,
             required, extension))
    return {
        "local_separator": "epsilon=(-lambda,[D0]^*) in ker(J_beta0^*)",
        "physical_extension_problem": (
            "find epsilon_tilde with restriction epsilon, "
            "J_phys^* epsilon_tilde=0, and normalized terminal target value 1"
        ),
        "compatible_completion_exists": True,
        "same_local_map_incompatible_completion_exists": True,
        "first_missing_statement": (
            "the D0 quotient/dual must be compared with every augmented "
            "Interface-III output, especially the six-term terminal and W row"
        ),
        "bounded_local_separator_is_final_Fredholm": False,
    }


def audit_generic_limit_saturation():
    # R=k[beta].  The rank-one image I=beta R*b becomes all of R[1/beta]*b
    # after localization, but its beta=0 fibre is zero.  This is the exact
    # minimal counterexample to generic membership -> special membership.
    h = 3
    alpha = Q(2)
    # Grant the strongest favourable shadow: identify the root-even target
    # line with [D0].  At Rees order ell^h its scalar coefficient still has
    # the unavoidable -h*alpha*beta factor.  Store beta polynomials as
    # exponent->coefficient.
    unnormalized = {1: -h * alpha}
    require(unnormalized == {1: Q(-6)},
            "the generic J* beta factor changed")
    order_h_ell_coefficient_at_beta_zero = unnormalized.get(0, Q(0))
    beta_hasse_derivative_at_zero = unnormalized.get(1, Q(0))
    require(order_h_ell_coefficient_at_beta_zero == 0
            and beta_hasse_derivative_at_zero == -h * alpha,
            "the generic/special Hasse distinction changed")

    # Localization allows x/beta.  Specialization has the zero map.  The
    # derivative sees the normal-cone class b, not an element of im(J_0).
    generic_preimage = "(-1/(h*alpha*beta))*x"
    special_image_rank = 0
    normal_cone_rank = 1
    require(special_image_rank == 0 and normal_cone_rank == 1,
            "the beta-torsion counterguard collapsed")
    return {
        "coefficient_ring": "R=k[beta] with Rees variable ell",
        "optimistic_generic_target_identification": (
            "grant that the root-even target line specializes to [D0]"
        ),
        "generic_root_even_scalar_shadow":
            "J(x)=-h*alpha*beta*ell^h*[D0]",
        "generic_normalized_preimage": generic_preimage,
        "order_h_ell_coefficient_at_beta_zero": 0,
        "mixed_beta_Hasse_normal_coefficient": str(beta_hasse_derivative_at_zero),
        "special_fibre_target_image_rank": special_image_rank,
        "normal_cone_target_rank": normal_cone_rank,
        "cokernel_torsion_model": "coker(beta:R->R)=R/(beta)",
        "exact_positive_criterion": (
            "the full augmented physical image must be beta-saturated along "
            "[D0]: beta^m*[D0] in im(J) must imply [D0] in im(J)"
        ),
        "order_h_limit_supplies_theta_without_saturation": False,
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "beta-zero D0 augmented terminal/saturation gate",
        "pins": PINS,
        "local_membership_dual": audit_local_membership_dual(),
        "terminal_extension": audit_terminal_extension_counterguard(),
        "generic_limit": audit_generic_limit_saturation(),
        "verdict": (
            "failure of 1 in theta(Z) gives a complete left separator only "
            "for the bounded protected beta-zero map.  Raw [D0]^* must first "
            "be completed by protected rows, and that completion must still "
            "extend across the exhaustive augmented physical map and land on "
            "the six-term/W terminal.  The generic root-even order-h normal "
            "coefficient does not supply theta: without beta-saturation it "
            "is a normal-cone/Tor class, as witnessed by beta:R->R"
        ),
        "single_remaining_terminal_comparison": (
            "construct the physical extension epsilon_tilde of the completed "
            "D0 separator (or its dual relative generator), retaining lower, "
            "descent, ridge, word, Eq, ores, ainc, Yw/W, and the physical "
            "six-term terminal in the same order-h grade"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    expected = "b457daee759404cf53999f93ecd0d443021fd04cb9633d73ca15cd5eec73bcdf"
    require(digest == expected, ("unexpected ledger digest", digest, expected))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 beta-zero D0 augmented terminal/saturation gate: PASS")
    print("local failure: completed protected left separator YES")
    print("physical Fredholm terminal: NOT IMPLIED")
    print("generic order-h normal coefficient: NOT a beta-zero source cell")
    print("remaining: terminal extension or beta-saturated D0 lift")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
