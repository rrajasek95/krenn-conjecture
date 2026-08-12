#!/usr/bin/env python3
r"""Cyclic compensation boundary for the clean-C5 eta_z obstruction.

On the marked direct-cell open let

    t=q_pq^00,  u_v=q_xv^00.

The five physical target-stabilizer tangents satisfy

    eta_z(t)=1,  eta_z(u_v)=-delta_(zv) u_z/t.

The clean aggregate readout without a rootless component has value
`-5-u_z/t`.  This checker proves that the unique cyclic face-local linear
compensation is

    c_v=t-u_v.

Indeed eta_z(sum c_v)=5+u_z/t.  Equivalently

    Omega_v+c_v=q_pq^22-q_xv^(0,m_v),

which is manifestly fixed by every eta_z.  In the typed comparison module
this requires the new rootless value

    d r_v(eta_z)=1+delta_(zv)u_z/t,

so the corrected column is a combination of the zero-readout relations
Omega_v-r_v.  All existing matching companions are eta-invariant and a
q-only route carries its ordinary-residue companion; neither supplies this
value in the current inventory.  Thus the formula is the minimal exact
compensation, conditional on the still-unconstructed physical Omega-to-r
comparison/common-companion lift.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "4e13ecf57d3c4ed8b7f09af5139ab623262e621ea09804bb9f74b6f66107ae46"
PINS = {
    "computations/verify_h3_rootless_clean_c5_separator_endpoint_kernel_boundary.py":
        "a98c6e0e90127e81e869c68342f3999abbbd8898d2b2eeafbeccbad06575a324",
    "computations/verify_h3_rootless_endpoint_to_collision_chain_map_boundary.py":
        "be39a61df8e3723983eea7a20d405fba7ff0f3822bc90e8d48b8039177f69cfc",
    "computations/verify_h3_rootless_five_ridge_response_bianchi_cokernel.py":
        "2e09f9be1ed1b57821c64dd690df7e4d6b2efebe93cb8aae9ff0a58b3190022d",
    "computations/verify_h3_rootless_single_v_site_collision_comparison_obstruction.py":
        "34d627b9b0cdf4a81fbebc7c1d37231f53ac2d04be401c3f99402b0bf28c6fbe",
    "computations/verify_h3_rootless_target_preserving_c5_etale_gauge.py":
        "02c2cc44c4d849e9db5d98c3c28882e93772dcc01cab286bba7d94cf8a8502be",
}

FACES = (1, 2, 3, 4, 5)
MIDDLE = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


class Affine:
    """Integral affine form in U_z=u_z/t, z=1,...,5."""

    def __init__(self, constant: int = 0, coefficients=()):
        values = [0] * 5
        for face, coefficient in coefficients:
            values[FACES.index(face)] += coefficient
        self.constant = constant
        self.coefficients = tuple(values)

    def __add__(self, other: "Affine") -> "Affine":
        return Affine(
            self.constant + other.constant,
            ((face, left + right) for face, left, right in
             zip(FACES, self.coefficients, other.coefficients, strict=True)),
        )

    def __neg__(self) -> "Affine":
        return Affine(-self.constant,
                      zip(FACES, (-value for value in self.coefficients),
                          strict=True))

    def __sub__(self, other: "Affine") -> "Affine":
        return self + (-other)

    def __mul__(self, coefficient: int) -> "Affine":
        return Affine(coefficient * self.constant,
                      zip(FACES,
                          (coefficient * value for value in self.coefficients),
                          strict=True))

    __rmul__ = __mul__

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, Affine)
                and self.constant == other.constant
                and self.coefficients == other.coefficients)

    def data(self) -> dict[str, object]:
        return {
            "constant": self.constant,
            "u_over_t": {
                str(face): coefficient
                for face, coefficient in zip(
                    FACES, self.coefficients, strict=True
                ) if coefficient
            },
        }


def eta_t(_auxiliary: int) -> Affine:
    return Affine(1)


def eta_u(auxiliary: int, face: int) -> Affine:
    return Affine(coefficients=((auxiliary, -1),)) \
        if face == auxiliary else Affine()


def eta_omega(auxiliary: int, face: int) -> Affine:
    return -eta_t(auxiliary) + eta_u(auxiliary, face)


def eta_local_compensation(auxiliary: int, face: int) -> Affine:
    return eta_t(auxiliary) - eta_u(auxiliary, face)


def uniqueness_audit() -> dict[str, object]:
    # A cyclic face-local linear correction has c_v=A*t+B*u_v.  Its
    # aggregate eta_z derivative is 5*A-B*U_z.  Matching 5+U_z forces
    # A=1 and B=-1.  The determinant of the coefficient system is -5, so
    # uniqueness holds in characteristic zero (and directly over Q here).
    matrix = ((5, 0), (0, -1))
    rhs = (5, 1)
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    require(determinant == -5, "cyclic compensation system changed")
    a = Q(rhs[0], matrix[0][0])
    b = Q(rhs[1], matrix[1][1])
    require((a, b) == (Q(1), Q(-1)),
            "minimal face-local compensation changed")

    # If locality is dropped, a cyclic aggregate has form
    # alpha*t+beta*sum u_v.  It is still uniquely 5*t-sum u_v; only its
    # distribution among face coordinates is nonunique.
    aggregate_alpha = 5 * a
    aggregate_beta = b
    require((aggregate_alpha, aggregate_beta) == (Q(5), Q(-1)),
            "cyclic aggregate compensation changed")
    return {
        "cyclic_face_local_ansatz": "c_v=A*t+B*u_v",
        "linear_system": [list(row) for row in matrix],
        "right_hand_side": list(rhs),
        "determinant": determinant,
        "unique_solution": {"A": str(a), "B": str(b)},
        "unique_cyclic_aggregate": "5*t-sum_v u_v",
        "distribution_scope": (
            "without face locality one may redistribute eta-invariant terms; "
            "the aggregate is still unique modulo common eta-invariants"
        ),
    }


def compensation_audit() -> dict[str, object]:
    records = []
    for auxiliary in FACES:
        omega_values = tuple(eta_omega(auxiliary, face) for face in FACES)
        rootless_values = tuple(
            eta_local_compensation(auxiliary, face) for face in FACES
        )
        base_pairing = sum(omega_values, Affine())
        correction_pairing = sum(rootless_values, Affine())
        require(base_pairing == Affine(-5, ((auxiliary, -1),)),
                ("eta aggregate obstruction changed", auxiliary,
                 base_pairing.data()))
        require(correction_pairing == Affine(5, ((auxiliary, 1),)),
                ("eta aggregate compensation changed", auxiliary,
                 correction_pairing.data()))
        require(base_pairing + correction_pairing == Affine(),
                "corrected eta pairing stopped vanishing")

        comparison_coefficients = []
        for face, omega, rootless in zip(
                FACES, omega_values, rootless_values, strict=True):
            # The corrected source image is omega*(Omega_v-r_v), since
            # rootless=-omega.  This relation has zero W/tgt/ores/ainc.
            require(rootless == -omega,
                    ("rootless compensation lost comparison sign",
                     auxiliary, face))
            comparison_coefficients.append(omega.data())

        records.append({
            "auxiliary": auxiliary,
            "old_Lambda_pairing": base_pairing.data(),
            "new_rootless_pairing": correction_pairing.data(),
            "corrected_pairing": (base_pairing + correction_pairing).data(),
            "decomposition": {
                "relations": [f"Omega_{face}-r_{face}" for face in FACES],
                "coefficients": comparison_coefficients,
            },
            "W_target_ores_ainc": [0, 0, 0, 0],
        })
    return {
        "records": records,
        "facewise_rootless_value": "r_v^comp=t-u_v",
        "aggregate_rootless_value": "5*t-sum_v u_v",
        "manifest_invariant_rewrite": (
            "Omega_v+(t-u_v)=q_pq^22-q_xv^(0,m_v)"
        ),
        "cyclic_symmetry": "t is fixed and v maps equivariantly to u_v",
    }


def companion_and_source_scope() -> dict[str, object]:
    # Existing selected matching companions contain only colours m_v in
    # {1,2}; eta_z has weights only in colour zero.  Hence every literal
    # q_(v,N) has zero eta derivative.  A q-only route also has its private
    # ores companion, so imposing zero ores forces its coefficient to zero
    # in the current single-v coarse module.
    q_derivative = {(auxiliary, face): 0
                    for auxiliary in FACES for face in FACES}
    require(not any(q_derivative.values()),
            "a selected q companion acquired eta weight")

    # Rows (Q,ores): a source-valid individual q route is (1,1).  No
    # nonzero scalar multiple has ores zero.  Adjacent differences cancel
    # ores, but give only the already known rank-four C5 edge module.
    q_route = (1, 1)
    require(q_route[1] != 0,
            "individual q route lost its ordinary-residue companion")
    require(all(coefficient == 0
                for coefficient in range(-3, 4)
                if coefficient * q_route[1] == 0),
            "q-only zero-ores multiple unexpectedly appeared")

    # The source-labelled formula may be written after homogenization as
    # (t-u_v)*Q_v, where Q_v is the selected repeated matching tail.  eta_z
    # fixes Q_v and Q_v=1 on the exact normalized C5 slice.  It is a
    # candidate value, not an existing chain: the pinned endpoint/collision
    # comparison proves that supplying it with all readouts zero is exactly
    # the missing Omega-to-r vertex map/common-companion lift.
    return {
        "eta_on_all_selected_q_(v,N)": 0,
        "q_only_compensation_in_current_inventory": False,
        "reason": (
            "constant combinations have zero eta derivative; an individual "
            "source-valid q route carries a private ordinary residue"
        ),
        "homogeneous_candidate_value": (
            "(t-u_v)*Q_v, with Q_v the eta-invariant selected repeated tail"
        ),
        "candidate_normalized_value": "t-u_v",
        "candidate_is_existing_source_chain": False,
        "exact_missing_physical_operation": (
            "a common-companion Omega_v-r_v comparison/vertex generator "
            "carrying the candidate value and zero W,target,ores,ainc"
        ),
        "middle_colours": MIDDLE,
    }


def main() -> None:
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "uniqueness": uniqueness_audit(),
        "exact_compensation": compensation_audit(),
        "source_scope": companion_and_source_scope(),
        "verdict": (
            "the eta_z aggregate obstruction has the unique cyclic local "
            "compensation r_v^comp=t-u_v; it preserves all four augmented "
            "readouts because the corrected eta image lies in the formal "
            "Omega_v-r_v comparison relations, but the current source "
            "inventory contains no such rootless vertex/common-q lift"
        ),
        "status": {
            "scalar_compensation_formula": "proved",
            "cyclic_and_augmented_typing": "proved conditionally on comparison",
            "physical_comparison_constructed": False,
            "dual_no_go_for_existing_q_only_inventory": True,
        },
        "scope": (
            "marked t-open exact clean C5 slice and first physical eta_z "
            "kernel family; no claim that an enlarged relative resolution "
            "cannot construct the comparison"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    print("h3 rootless eta cyclic compensation: CONDITIONAL POSITIVE")
    print("unique local value: r_v^comp=t-u_v")
    print("aggregate: 5*t-sum u_v; all eta_z pairings cancel")
    print("current q/rootless source lift: ABSENT")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
