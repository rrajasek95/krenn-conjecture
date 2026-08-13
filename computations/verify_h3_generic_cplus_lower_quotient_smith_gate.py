#!/usr/bin/env python3
"""Compute the generic C_plus lower quotient and its beta-Smith guard.

On alpha*beta != 0 the full diagonal cap identity is

    J* = -3*alpha*beta*I,

so the normalized first lower Cartan face is the parameter-free trace class

    R+ = -(1/3)(1+rho) H_w d(P(I)).

The physical thirteen-label part of the trace comparison has complete
landing (3,2,3,3,2,3), versus the uniform trace landing (3,...,3).  The
remaining rho-pair has normalized direct image

    v=(B1+B4)/2.

Its pinned actual-grade order-two loop-resolution coefficient is the complementary even
average l=(B0+B2+B3+B5)/4.  Hence, in the actual six-output lower quotient,
the first unresolved coefficient is exactly

    delta_plus = v-l = (-1,2,-1,-1,2,-1)/4.

This equality does not construct the missing source cell.  The complete
same-grade M_v realization ties lower delta_plus to Eq delta_plus, while the
desired lower bridge has Eq zero.  Independently, the root-decorated Cartan
product rule needs the Spencer face +2D(H0-u)Eq tensor v.  The canonical
derived K_Eq cone supplies that algebraic coefficient but its physical
word/fine/repeated descent is the same open C_plus orbit.

Finally, adjoining a beta-independent lower B-4 column does not force an
integral extension through beta=0.  The cap/unary packet retains Smith form
diag(1,1,beta); after adjoining an independent lower unit it is
diag(1,1,1,beta).  Its torsion class is [rho0]=[D0].  Only an integral
Bockstein face V with the unary primitive defect and zero root output gives
a unit minor and U-V=rho0.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_trace_cartan_lower_rees_typing_gate.py":
        "0190a8fa16dddf9cecf2de676d4f3ff87d184f031e523d87e1f80937ff55be94",
    "computations/verify_h3_trace_cartan_tau_plus_site_collapse_gate.py":
        "f0801bfcd5362f2fc8d9a81bf85a84b2d380fd37cbbe7db2252b352b785d5474",
    "computations/verify_h3_tau_plus_delta_literal_same_grade_gate.py":
        "f5d34986e086055dcba26e347c5a7f7470d9ec62a1346c9c872a8e828ec7b266",
    "computations/verify_h3_tau_plus_full_interface_product_bianchi_extension_gate.py":
        "32be7ef48ad9d35b8863a62889508ccdff0010d8ebff18b366e932aab8b2bf14",
    "computations/verify_h3_beta_rees_cap_smith_saturation_gate.py":
        "fb031132ddd0510197560be0644324c436216192a9f15140ae3ef52b2a1fb4e5",
    "computations/verify_h3_reduced_eq_integral_rho_comparison_master_gate.py":
        "813419c756e7f21c09d63d3ec10f44c787e9580ca08c87809b7c4c550b908b4f",
    "computations/verify_h2_b4_cplus_shared_interface_gate.py":
        "ee48f2d1446d938fc97cda4e0977472081ee9823d31dc91f3f4c46829f3d8400",
    "computations/verify_h2_lower_0112_bminus4_target_normal_gate.py":
        "8fffe45182c4bb304dabfbe9df568061a8049bec21949539bcae88f60f5d22e0",
}
EXPECTED_LEDGER_SHA256 = "73e79b2477cec9a9bfd077b18d07e2866ad6ef5ec70ed2311c3dd7b01c4b013a"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(columns):
    if not columns:
        return 0
    height = len(columns[0])
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


# Polynomials a+b*beta suffice for every determinant below.  Multiplication
# can temporarily raise the degree, so store arbitrary exact coefficient
# tuples.
def ptrim(poly):
    values = list(map(Q, poly))
    while len(values) > 1 and not values[-1]:
        values.pop()
    return tuple(values)


def padd(left, right):
    size = max(len(left), len(right))
    return ptrim(tuple((left[index] if index < len(left) else Q(0))
                       + (right[index] if index < len(right) else Q(0))
                       for index in range(size)))


def pscale(coefficient, poly):
    return ptrim(tuple(Q(coefficient) * value for value in poly))


def pmul(left, right):
    answer = [Q(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            answer[i + j] += a * b
    return ptrim(tuple(answer))


def pdet(columns):
    require(columns and len(columns) == len(columns[0]), "square determinant")
    size = len(columns)
    answer = (Q(0),)
    for order in permutations(range(size)):
        inversions = sum(order[i] > order[j] for i in range(size)
                         for j in range(i + 1, size))
        term = (Q(1),)
        for row, column in enumerate(order):
            term = pmul(term, columns[column][row])
        answer = padd(answer, pscale(-1 if inversions % 2 else 1, term))
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def generic_trace_reduction_audit():
    records = []
    identity = tuple(tuple(Q(row == column) for column in range(3))
                     for row in range(3))
    for alpha, beta in ((Q(2), Q(3)), (Q(-3, 2), Q(5)),
                        (Q(7), Q(-4, 3))):
        require(alpha and beta, "generic sample left the active open")
        k0 = tuple(tuple(Q(row == column == 0) for column in range(3))
                   for row in range(3))
        k1 = tuple(tuple((alpha + beta) * k0[row][column]
                         - alpha * identity[row][column]
                         for column in range(3)) for row in range(3))
        k2 = tuple(tuple(alpha * k0[row][column]
                         - alpha * identity[row][column]
                         for column in range(3)) for row in range(3))
        j2 = tuple(tuple(-beta * k0[row][column] + 2 * k2[row][column]
                         for column in range(3)) for row in range(3))
        jstar = tuple(tuple((beta - 2 * alpha) * k1[row][column]
                            + (beta + alpha) * j2[row][column]
                            for column in range(3)) for row in range(3))
        expected = tuple(tuple(-3 * alpha * beta * identity[row][column]
                               for column in range(3)) for row in range(3))
        require(jstar == expected, "J* stopped being -3 alpha beta I")
        coefficient = Q(1, 9) / (alpha * beta) * (-3 * alpha * beta)
        require(coefficient == Q(-1, 3),
                "the normalized trace remainder retained a parameter")
        records.append({
            "alpha": str(alpha),
            "beta": str(beta),
            "Jstar": "-3*alpha*beta*I",
            "Rplus_trace_coefficient": str(coefficient),
        })
    return {
        "active_hypothesis": "alpha*beta != 0",
        "full_matrix_identity": "J*=-3*alpha*beta*I",
        "normalized_first_lower_face": (
            "R+=-(1/3)(1+rho)H_w d(P(I))"
        ),
        "parameter_independent_after_normalization": True,
        "records": records,
    }


def actual_lower_quotient_audit():
    partial = tuple(map(Q, (3, 2, 3, 3, 2, 3)))
    uniform = (Q(3),) * 6
    missing = add(uniform, scale(-1, partial))
    v = tuple(map(Q, (0, Q(1, 2), 0, 0, Q(1, 2), 0)))
    local = tuple(map(Q, (Q(1, 4), 0, Q(1, 4),
                          Q(1, 4), 0, Q(1, 4))))
    delta = add(v, scale(-1, local))
    integral = tuple(map(Q, (-1, 2, -1, -1, 2, -1)))
    rho = (5, 1, 3, 2, 4, 0)
    require(missing == scale(2, v),
            "the thirteen-label quotient stopped being one rho-pair")
    require(delta == scale(Q(1, 4), integral)
            and sum(delta, Q(0)) == 0
            and tuple(delta[index] for index in rho) == delta,
            "the first lower relative class changed")

    # Endpoint adjacency on K4 holes, in the B ordering pinned by 22c950c.
    holes = ((0, 2), (0, 1), (0, 3), (1, 3), (2, 3), (1, 2))
    adjacency = tuple(tuple(Q(i != j and len(set(left) & set(right)) == 1)
                            for j, right in enumerate(holes))
                      for i, left in enumerate(holes))
    bdelta = tuple(dot(row, delta) for row in adjacency)
    require(bdelta == scale(-2, delta),
            "delta+ left the endpoint -2 eigenspace")
    bminus4_preimage = scale(Q(-1, 6), delta)
    require(tuple(dot(row, bminus4_preimage) - 4 * bminus4_preimage[i]
                  for i, row in enumerate(adjacency)) == delta,
            "the short B-4 preimage changed")
    return {
        "literal_thirteen_label_landing": [int(value) for value in partial],
        "uniform_trace_landing": [int(value) for value in uniform],
        "omitted_rho_pair_total_deficit": [int(value) for value in missing],
        "normalized_direct_pair_image_v": [str(value) for value in v],
        "order2_loop_resolution_even_face": [str(value) for value in local],
        "first_relative_lower_class": "delta_plus=v-local",
        "delta_plus": [str(value) for value in delta],
        "endpoint_adjacency_eigenvalue": -2,
        "B_minus_4_preimage": "-delta_plus/6",
        "scope": (
            "the thirteen-label map is literal and the lower quotient "
            "coefficient is exact; identifying the omitted source orbit with this "
            "coefficient class still requires the physical C_plus cell"
        ),
    }


def eq_product_rule_audit():
    delta4 = tuple(map(Q, (-1, 2, -1, -1, 2, -1)))
    zero = (Q(0),) * 6
    diagonal_columns = []
    for index in range(6):
        unit = tuple(Q(index == position) for position in range(6))
        diagonal_columns.append(unit + unit)
    desired = delta4 + zero
    chi = delta4 + scale(-1, delta4)
    require(rank(diagonal_columns) == 6
            and rank(diagonal_columns + [desired]) == 7
            and all(dot(chi, column) == 0 for column in diagonal_columns)
            and dot(chi, desired) == 12,
            "the lower/Eq tied-packet obstruction changed")
    correction = zero + scale(-1, delta4)
    require(add(delta4 + delta4, correction) == desired,
            "the minimal lower Eq correction changed")

    droot = tuple(map(Q, (-1, 1, -1, 1)))
    v = tuple(map(Q, (0, Q(1, 2), 0, 0, Q(1, 2), 0)))
    root_target = scale(-2, tuple(a * b for a in droot for b in v))
    root_eq = scale(2, tuple(a * b for a in droot for b in v))
    require(add(root_target, root_eq) == (Q(0),) * 24
            and sum(value != 0 for value in root_eq) == 8,
            "the root-decorated Spencer coefficient changed")

    # In the reduced (Eq,w) shadow the old fourth-Hasse face is (1,1),
    # whereas the desired final boundary is (0,1).  Their difference is a
    # pure Eq correction.  This algebraic correction is the K_Eq cone; its
    # physical placement remains part of C_plus.
    old = (Q(1), Q(1))
    final = (Q(0), Q(1))
    pure_eq_correction = add(final, scale(-1, old))
    separator = (Q(1), Q(-1))
    require(pure_eq_correction == (Q(-1), Q(0))
            and dot(separator, old) == 0
            and dot(separator, final) == -1,
            "the first reduced-Eq product-rule face changed")
    return {
        "complete_lower_Eq_tie": "known M_v packets give (delta_plus,delta_plus)",
        "desired_complete_lower_packet": "(delta_plus,0)",
        "minimal_complete_Eq_correction": "(0,-delta_plus)",
        "primitive_complete_dual": "chi_D=sum D_i(private_i-Eq_i)",
        "primitive_complete_dual_value_on_integral_bridge": 12,
        "root_decorated_target": "-2*Droot tensor v",
        "root_decorated_Spencer_face": "+2*Droot*(H0-u)*Eq tensor v",
        "root_decorated_nonzero_coefficients": 8,
        "old_fourth_Hasse_Eq_w": [1, 1],
        "desired_final_Eq_w": [0, 1],
        "needed_pure_Eq_difference": [-1, 0],
        "algebraic_K_Eq_core": "canonical in the derived source",
        "physical_same_grade_descent": False,
    }


def beta_smith_audit():
    one = (Q(1),)
    zero = (Q(0),)
    beta = (Q(0), Q(1))
    minus_beta = (Q(0), Q(-1))

    # Rows: primitive defect, rho0, rho2, independent lower B-4 coordinate.
    # Columns: U,Z1,Z2,W.  W is the strongest conclusion supplied merely by
    # a beta-independent lower realization: it is a unit in a disjoint row.
    unary = (one, one, zero, zero)
    z1 = (zero, beta, one, zero)
    z2 = (zero, minus_beta, (Q(2),), zero)
    lower_b4 = (zero, zero, zero, one)
    determinant = pdet((unary, z1, z2, lower_b4))
    require(determinant == (Q(0), Q(3)),
            ("lower B-4 unexpectedly removed beta torsion", determinant))

    # The displayed unit 3-minor (defect,rho2,lower) on U,Z1,W makes all
    # earlier Smith factors units.  The determinant leaves one beta factor.
    unit_minor = pdet(((unary[0], unary[2], unary[3]),
                       (z1[0], z1[2], z1[3]),
                       (lower_b4[0], lower_b4[2], lower_b4[3])))
    require(unit_minor in ((Q(1),), (Q(-1),)),
            ("the augmented packet lost its unit three-minor", unit_minor))

    # Add V with the same primitive defect as U and zero root output.  Its
    # lower coordinate is immaterial modulo W; take zero.  U-V is rho0 and
    # U,V,Z1,W have a beta-independent unit determinant.
    correction_v = (one, zero, zero, zero)
    positive = pdet((unary, correction_v, z1, lower_b4))
    require(positive in ((Q(1),), (Q(-1),)),
            ("the Bockstein correction did not create a unit minor", positive))
    u_minus_v = tuple(padd(left, pscale(-1, right))
                      for left, right in zip(unary, correction_v, strict=True))
    require(u_minus_v == (zero, one, zero, zero),
            "U-V stopped being the protected rho0/D0 direction")
    return {
        "base_ring": "Q[beta] localized at alpha and 3",
        "known_cap_unary_plus_independent_lower_B4_Smith": [
            "1", "1", "1", "beta"
        ],
        "determinant": "3*beta",
        "surviving_torsion": "[rho0]=[D0]",
        "beta_independent_lower_B4_forces_integral_extension": False,
        "reason": (
            "a lower unit is a direct Smith summand and carries no primitive "
            "descent/root information"
        ),
        "required_integral_Bockstein_face": (
            "V=(same primitive defect as U, rho0=rho2=0)"
        ),
        "positive_identity": "U-V=rho0=D0",
        "unit_minor_after_V": True,
    }


def scope_audit():
    trace_note = (ROOT / "notes/h3-trace-cartan-tau-plus-site-collapse-gate.md").read_text()
    delta_note = (ROOT / "notes/h3-tau-plus-delta-literal-same-grade-gate.md").read_text()
    lower_note = (ROOT / "notes/h2-lower-0112-bminus4-target-normal-gate.md").read_text()
    smith_note = (ROOT / "notes/h3-beta-rees-cap-smith-saturation-gate.md").read_text()
    require("unique equivariant linear repair" in trace_note
            and "B_1+B_4" in trace_note,
            "the thirteen-label repair scope changed")
    require("`Eq=delta_+`" in delta_note
            and "not the required Eq-zero translation" in delta_note,
            "the complete lower/Eq scope changed")
    require("not target-safe" in lower_note
            and "one-endpoint Hasse" in lower_note,
            "the literal lower target-normal scope changed")
    require("Smith form is `diag(1,beta)`" in smith_note
            and "Bockstein" in smith_note,
            "the beta-Smith scope changed")
    return {
            "literal_or_exact_now": [
            "J* diagonal cap input",
            "thirteen of fifteen trace labels",
            "lower endpoint B-4 coefficient preimage",
            "audited lower endpoint Cartan target normal",
            "canonical derived reduced-Eq Spencer core",
        ],
        "one_remaining_integral_cell": (
            "a rho-even Q[beta]-linear C_plus product-rule/Bianchi orbit "
            "whose order-two restriction is the lower B-4 family, whose "
            "generic complete quotient is delta_plus with Eq zero and the "
            "root Spencer face, and whose beta-Bockstein is V"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "generic C-plus first lower quotient and beta-Smith gate",
        "pins": PINS,
        "generic_trace_reduction": generic_trace_reduction_audit(),
        "actual_lower_order2_quotient": actual_lower_quotient_audit(),
        "Eq_and_product_rule_face": eq_product_rule_audit(),
        "beta_integrality_and_Smith": beta_smith_audit(),
        "physical_scope": scope_audit(),
        "verdict": (
            "For beta nonzero the normalized J* Cartan remainder is the "
            "parameter-free trace class.  Modulo the literal thirteen-label "
            "landing and the pinned local loop-resolution coefficient, its first "
            "six-output lower coefficient is exactly delta_plus=v-local. "
            "This does not close the source orbit: the same-grade complete "
            "packet still needs Eq=-delta_plus and the root product rule "
            "needs its physically descended Spencer face.  A beta-independent "
            "lower B-4 realization alone leaves the cap Smith class D0; only "
            "one integral full C_plus orbit with Bockstein V closes both "
            "the generic and collision faces."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("generic C-plus lower quotient ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("generic C_plus normalized R+: PARAMETER-FREE TRACE CLASS")
    print("first actual six-output lower quotient: delta_plus=v-local")
    print("complete lower Eq correction: -delta_plus")
    print("root product-rule Eq face: CANONICAL FORM / PHYSICAL DESCENT OPEN")
    print("beta-independent B-4 alone: SMITH TORSION D0 SURVIVES")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
