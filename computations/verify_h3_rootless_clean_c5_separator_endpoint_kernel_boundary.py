#!/usr/bin/env python3
r"""First full-source kernel column seen by the clean-C5 separator.

The clean aggregate separator assigns value one to every Omega_v,
q_(v,N), and rootless r_v, and zero to Eq/W/target/ores/ainc.  The endpoint
bar and denominator-Tor inventories are killed by it.  This checker audits
the first omitted *physical source-kernel* columns: the colour-diagonal GHZ
stabilizer tangents already constructed by the non-Euler marked-jet theorem.

On the marked direct-cell open t=q_pq^00 != 0, the tangent with colour-zero
weights +1 at p and -1 at an odd auxiliary site z preserves the complete
output tensor, the normalized C5, and every q_(v,N) residue companion.  It
nevertheless has

    d Omega_v = -1                 (v != z),
    d Omega_z = -1-u_z/t,

where u_z=q_xz^00.  Thus the aggregate separator reads -5-u_z/t.  This is
the first exact zero-indeterminacy condition missing from the coarse
attachment module.  It is not a full-source counterexample or a proof that
the displayed scalar is nonzero at every physical source.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "52f9a814e400edec24a7f82b4a19984655631243ea25d18545679c6458d23618"
PINS = {
    "computations/verify_h3_rootless_c5_clean_aggregate_tor_separator.py":
        "3b5cb07412f08eaea2492d4b4f981ecc5618053c211942bead0512b30393ce67",
    "computations/verify_h3_rootless_endpoint_word_change_attachment_or_dual.py":
        "a98a37e07b7847c4484de9505b1f833fc269b02126091d3ee92463bc65ad60d4",
    "computations/verify_h3_rootless_non_euler_diagonal_stabilizer_jet.py":
        "0bbed406d393543b6badf222ff0665dc1b12445a2360a015e5398bd538bd5e5c",
    "notes/h3-rootless-non-euler-diagonal-stabilizer-jet.md":
        "0a2321191cdd29dc21aed0c988e76d710e09a993303780527ca1502f4d833dc4",
}

SITES = tuple(range(8))
ODD = (1, 2, 3, 4, 5)
MIDDLE = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
X, P, QSITE = 0, 6, 7


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def edge_weight(weights: dict[tuple[int, int], int],
                left: tuple[int, int], right: tuple[int, int]) -> int:
    return weights.get(left, 0) + weights.get(right, 0)


def stabilizer_weights(auxiliary: int) -> dict[tuple[int, int], int]:
    """Colour-diagonal weights marking t=q_pq^00.

    The colour-zero sum is 1-1=0 and the other two colour sums are zero, so
    this is a literal infinitesimal stabilizer of all three GHZ targets.
    """
    require(auxiliary in ODD, "auxiliary site must be odd")
    weights = {(P, 0): 1, (auxiliary, 0): -1}
    for colour in (0, 1, 2):
        require(sum(weights.get((site, colour), 0) for site in SITES) == 0,
                ("not a GHZ stabilizer", auxiliary, colour))
    return weights


def logarithmic_derivative(weights: dict[tuple[int, int], int],
                           left_site: int, right_site: int,
                           left_colour: int, right_colour: int) -> int:
    """Coefficient w_e in eta(q_e)=w_e*q_e/t."""
    return edge_weight(weights,
                       (left_site, left_colour),
                       (right_site, right_colour))


def face_audit(auxiliary: int, face: int) -> dict[str, object]:
    weights = stabilizer_weights(auxiliary)

    # Omega_v=(q_pq^22-q_pq^00)-(q_xv^(0,m_v)-q_xv^00).
    coefficients = {
        "q_pq_22_over_t": logarithmic_derivative(
            weights, P, QSITE, 2, 2),
        "q_pq_00_over_t": -logarithmic_derivative(
            weights, P, QSITE, 0, 0),
        "q_xv_0m_over_t": -logarithmic_derivative(
            weights, X, face, 0, MIDDLE[face]),
        "q_xv_00_over_t": logarithmic_derivative(
            weights, X, face, 0, 0),
    }
    require(coefficients["q_pq_22_over_t"] == 0,
            "the stabilizer moved q_pq^22")
    require(coefficients["q_pq_00_over_t"] == -1,
            "the marked t contribution changed")
    require(coefficients["q_xv_0m_over_t"] == 0,
            "a selected-colour endpoint cell moved")
    expected_u = -1 if face == auxiliary else 0
    require(coefficients["q_xv_00_over_t"] == expected_u,
            "the auxiliary u-face contribution changed")

    # All three four-site companion matchings use only odd sites in their
    # selected nonzero colours.  The weights are colour-zero, so each
    # q_(v,N) logarithmic derivative is exactly zero, not just aggregate zero.
    companion_edge_weights = {
        (left, right): logarithmic_derivative(
            weights, left, right, MIDDLE[left], MIDDLE[right])
        for left in ODD for right in ODD if left < right
    }
    require(all(value == 0 for value in companion_edge_weights.values()),
            "a selected q_(v,N) residue companion moved")

    return {
        "auxiliary": auxiliary,
        "face": face,
        "d_Omega": "-1-u_%d/t" % auxiliary
        if face == auxiliary else "-1",
        "coefficient_ledger": coefficients,
        "all_selected_internal_edge_weights": sorted(set(
            companion_edge_weights.values()
        )),
        "d_each_q_(v,N)": 0,
        "d_rootless_r_v_in_existing_source_inventory": 0,
        "target": 0,
        "ordinary_residue": 0,
        "normalized_C5_selected_cells": 0,
    }


def aggregate_pairing_audit() -> dict[str, object]:
    records = []
    for auxiliary in ODD:
        faces = [face_audit(auxiliary, face) for face in ODD]
        constant = sum(
            record["coefficient_ledger"]["q_pq_22_over_t"]
            + record["coefficient_ledger"]["q_pq_00_over_t"]
            + record["coefficient_ledger"]["q_xv_0m_over_t"]
            for record in faces
        )
        u_coefficients = {
            face: record["coefficient_ledger"]["q_xv_00_over_t"]
            for face, record in zip(ODD, faces, strict=True)
            if record["coefficient_ledger"]["q_xv_00_over_t"]
        }
        require(constant == -5 and u_coefficients == {auxiliary: -1},
                ("aggregate pairing changed", auxiliary, constant,
                 u_coefficients))
        records.append({
            "auxiliary": auxiliary,
            "five_face_pairing": f"-5-u_{auxiliary}/t",
            "facewise": faces,
            "condition_for_this_kernel_column_to_be_killed":
                f"u_{auxiliary}+5*t=0",
        })

    # Killing all five automatic kernel columns imposes five independent
    # displayed equations before any further source relation is used.
    required_relations = tuple(f"u_{site}+5*t=0" for site in ODD)
    require(len(set(required_relations)) == 5,
            "the five zero-indeterminacy conditions collided")
    return {
        "records": records,
        "simultaneous_zero_indeterminacy_guard": list(required_relations),
        "equivalent_ratio_guard_on_t_open": [
            f"u_{site}/t=-5" for site in ODD
        ],
    }


def first_order_scope() -> dict[str, object]:
    # The tangent changes t with normalized component one and changes no
    # selected C5 internal cell.  Hence it stays in R=0 and precedes every
    # endpoint-tail mixed Hessian/Fitting correction.
    for auxiliary in ODD:
        weights = stabilizer_weights(auxiliary)
        require(logarithmic_derivative(
            weights, P, QSITE, 0, 0) == 1,
            "eta_t stopped being one")
        for left, right in ((1, 2), (2, 3), (3, 4), (4, 5), (1, 5)):
            require(logarithmic_derivative(
                weights, left, right,
                MIDDLE[left], MIDDLE[right]) == 0,
                "a normalized C5 edge moved")
    return {
        "order": 1,
        "source_column": (
            "eta_z=X_mu/t with mu_(p,0)=1, mu_(z,0)=-1"
        ),
        "complete_source_equations": (
            "J eta_z=0 by colourwise GHZ-stabilizer covariance"
        ),
        "clean_C5": "preserved coefficientwise",
        "target": 0,
        "ordinary_residue": 0,
        "why_earlier_than_tail_Fitting": (
            "no endpoint-tail normal or second Hasse factor is used"
        ),
    }


def main() -> None:
    pin_dependencies()
    pairing = aggregate_pairing_audit()
    ledger = {
        "theorem": (
            "clean C5 aggregate separator: first physical endpoint-kernel "
            "zero-indeterminacy boundary"
        ),
        "separator": {
            "value_one": ["Omega_v", "q_(v,N)", "rootless_r_v"],
            "value_zero": ["Eq", "W", "target", "ores", "ainc"],
        },
        "first_source_kernel_column": first_order_scope(),
        "pairing": pairing,
        "verdict": {
            "automatically_kills_full_source_kernel": False,
            "first_failed_columns": (
                "five colour-diagonal target-stabilizer tangents eta_z"
            ),
            "missing_exhaustivity_datum": (
                "a source-provenant terminal correction/comparison assigning "
                "the compensating rootless/q value, or a proof from the full "
                "source equations of u_z=-5*t for every z"
            ),
            "nonclaim": (
                "the five scalar guards are not proved inconsistent and no "
                "full physical rootless source point is constructed"
            ),
        },
        "scope": (
            "exact on the marked t-open clean normalized C5 packet; this is "
            "a first-order physical kernel/readout obstruction, not the "
            "secondary universal endpoint-tail Fitting stratification"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"endpoint-kernel separator ledger changed: {digest}")
    print("h3 rootless clean-C5 separator endpoint-kernel boundary: PASS")
    print("first omitted physical columns: eta_z=X_mu/t, z=1,...,5")
    print("aggregate separator pairings: -5-u_z/t")
    print("automatic full-source zero-indeterminacy: NO")
    print("ledger SHA-256:", digest)


if __name__ == "__main__":
    main()
