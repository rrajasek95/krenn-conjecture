#!/usr/bin/env python3
r"""Full-Jacobian audit of the formal corrected clean-C5 aggregate F.

The formal scalar

    F = sum_v Omega_v + 5*t - sum_v u_v
      = 5*q_pq^22 - sum_v q_xv^(0,m_v)

kills the five p0/z0 stabilizer tangents found by the first endpoint-kernel
audit.  It is not invariant under the full physical endpoint/q Jacobian.
Two further colour-diagonal GHZ stabilizers, both preserving the clean C5
and all q_(v,N) ordinary-residue companions, read respectively

    dF = 5*q_pq^22,       dF = -sum_v q_xv^(0,m_v).

Thus a nonzero normalized F cannot descend to the physical cokernel.  The
checker also records the source-grade failure: F is a coefficient-ring
polynomial, not a repeated-degree source-resolution cell with defined
target/ores/ainc/W readouts.
"""

from __future__ import annotations

from hashlib import sha256
import json
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "0f6a4a7162615595b0b727c6f6105b65df241ec40ba19fcb45baa427d737777e"
PINS = {
    "computations/verify_h3_rootless_clean_c5_separator_endpoint_kernel_boundary.py":
        "a98c6e0e90127e81e869c68342f3999abbbd8898d2b2eeafbeccbad06575a324",
    "computations/verify_h3_rootless_non_euler_diagonal_stabilizer_jet.py":
        "0bbed406d393543b6badf222ff0665dc1b12445a2360a015e5398bd538bd5e5c",
    "computations/verify_h3_rootless_endpoint_word_change_attachment_or_dual.py":
        "a98a37e07b7847c4484de9505b1f833fc269b02126091d3ee92463bc65ad60d4",
    "computations/verify_h3_rootless_endpoint_to_collision_chain_map_boundary.py":
        "be39a61df8e3723983eea7a20d405fba7ff0f3822bc90e8d48b8039177f69cfc",
}

SITES = tuple(range(8))
COLORS = (0, 1, 2)
ODD = (1, 2, 3, 4, 5)
MIDDLE = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
X, P, QSITE = 0, 6, 7
CYCLE = ((1, 2), (2, 3), (3, 4), (4, 5), (1, 5))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def weights(*entries: tuple[int, int, int]) -> dict[tuple[int, int], int]:
    answer = {(site, colour): value
              for site, colour, value in entries if value}
    for colour in COLORS:
        require(sum(answer.get((site, colour), 0) for site in SITES) == 0,
                ("not a colour-diagonal GHZ stabilizer", entries, colour))
    return answer


def edge_weight(field: dict[tuple[int, int], int],
                left: int, right: int,
                left_colour: int, right_colour: int) -> int:
    return (field.get((left, left_colour), 0)
            + field.get((right, right_colour), 0))


def full_source_kernel_audit(field: dict[tuple[int, int], int]) -> None:
    """Replay the exact covariance proof on all 3^8 output words.

    J X_lambda at word w is Lambda(w) H_w.  On pure words Lambda is the
    corresponding colour sum, hence zero.  On mixed words the exact GHZ
    target coefficient H_w is zero.  This is the complete 6561-row source
    Jacobian, not a selected response quotient.
    """
    words = tuple(product(COLORS, repeat=8))
    require(len(words) == 6561, "complete output-word count changed")
    for word in words:
        scalar = sum(field.get((site, word[site]), 0) for site in SITES)
        pure = len(set(word)) == 1
        target_coefficient = 1 if pure else 0
        require(scalar * target_coefficient == 0,
                ("stabilizer left the full Jacobian kernel", field, word))


def clean_and_residue_audit(field: dict[tuple[int, int], int]) -> None:
    # Every selected cycle cell and every residual q_(v,N) edge uses only
    # odd sites in colours m_i.  The two test fields below live on external
    # sites, so they fix all of these cells coefficientwise.
    for left, right in ((a, b) for a in ODD for b in ODD if a < b):
        require(edge_weight(
            field, left, right, MIDDLE[left], MIDDLE[right]
        ) == 0, ("an internal selected-colour cell moved", field, left, right))
    require(all(edge_weight(
        field, left, right, MIDDLE[left], MIDDLE[right]
    ) == 0 for left, right in CYCLE),
        "the normalized C5 moved")


def formal_identity() -> dict[str, object]:
    # Coefficients in (z,t,w1,...,w5,u1,...,u5), where
    # z=q_pq^22, t=q_pq^00, w_v=q_xv^(0,m_v), u_v=q_xv^00.
    omega_sum = (5, -5) + (-1,) * 5 + (1,) * 5
    correction = (0, 5) + (0,) * 5 + (-1,) * 5
    total = tuple(a + b for a, b in zip(
        omega_sum, correction, strict=True
    ))
    expected = (5, 0) + (-1,) * 5 + (0,) * 5
    require(total == expected, "formal F identity changed")
    return {
        "coordinate_order": [
            "z=q_pq^22", "t=q_pq^00",
            *[f"w_{v}=q_x{v}^(0,{MIDDLE[v]})" for v in ODD],
            *[f"u_{v}=q_x{v}^00" for v in ODD],
        ],
        "sum_Omega": list(omega_sum),
        "formal_correction_5t-sum_u": list(correction),
        "F": list(total),
        "identity": "F=5*q_pq^22-sum_v q_xv^(0,m_v)",
    }


def derivative_of_F(field: dict[tuple[int, int], int]) -> dict[str, object]:
    z_weight = edge_weight(field, P, QSITE, 2, 2)
    w_weights = {
        v: edge_weight(field, X, v, 0, MIDDLE[v]) for v in ODD
    }
    return {
        "z_coefficient": 5 * z_weight,
        "w_coefficients": {str(v): -w_weights[v] for v in ODD},
        "formula": " + ".join(
            ([f"{5*z_weight}*q_pq^22"] if z_weight else [])
            + [f"{-w_weights[v]}*q_x{v}^(0,{MIDDLE[v]})"
               for v in ODD if w_weights[v]]
        ) or "0",
    }


def jacobian_columns() -> dict[str, object]:
    # The five old columns eta_z are included only to verify the advertised
    # repair.  The first new failing columns use external sites only, hence
    # preserve every internal clean/tail coefficient.
    old = []
    for auxiliary in ODD:
        field = weights((P, 0, 1), (auxiliary, 0, -1))
        full_source_kernel_audit(field)
        result = derivative_of_F(field)
        require(result["formula"] == "0",
                ("F stopped killing eta_z", auxiliary, result))
        old.append({"auxiliary": auxiliary, "dF": result["formula"]})

    z_field = weights((P, 2, 1), (X, 2, -1))
    full_source_kernel_audit(z_field)
    clean_and_residue_audit(z_field)
    z_result = derivative_of_F(z_field)
    require(z_result == {
        "z_coefficient": 5,
        "w_coefficients": {str(v): 0 for v in ODD},
        "formula": "5*q_pq^22",
    }, ("first z failure changed", z_result))

    w_field = weights((X, 0, 1), (P, 0, -1))
    full_source_kernel_audit(w_field)
    clean_and_residue_audit(w_field)
    w_result = derivative_of_F(w_field)
    expected_w = " + ".join(
        f"-1*q_x{v}^(0,{MIDDLE[v]})" for v in ODD
    )
    require(w_result["z_coefficient"] == 0
            and set(w_result["w_coefficients"].values()) == {-1}
            and w_result["formula"] == expected_w,
            ("first w failure changed", w_result))

    return {
        "five_repaired_eta_z_columns": old,
        "first_full_jacobian_failure_z": {
            "weights": "lambda_(p,2)=1, lambda_(x,2)=-1",
            "complete_source_J": 0,
            "clean_C5": "fixed coefficientwise",
            "each_q_(v,N)_ordinary_residue": 0,
            "target": 0,
            "dF": z_result["formula"],
        },
        "first_full_jacobian_failure_w": {
            "weights": "lambda_(x,0)=1, lambda_(p,0)=-1",
            "complete_source_J": 0,
            "clean_C5": "fixed coefficientwise",
            "each_q_(v,N)_ordinary_residue": 0,
            "target": 0,
            "dF": "-sum_v q_xv^(0,m_v)",
        },
        "invariance_consequence": (
            "the two displayed kernel columns force q_pq^22=0 and "
            "sum_v q_xv^(0,m_v)=0; hence F=0"
        ),
    }


def source_typing_gate() -> dict[str, object]:
    return {
        "coefficient_ring_status": (
            "F is a legitimate degree-one scalar polynomial in six "
            "decorated q coordinates"
        ),
        "source_chain_status": False,
        "first_degree_reason": (
            "the complete physical route for -Omega_v is "
            "(-Omega_v,+q_(v,N),ores=1), not (-Omega_v,0,0); the raw "
            "5t-sum_u polynomial is not a companion-cancelling source cell"
        ),
        "repeated_degree_reason": (
            "each face Omega_v reaches the rootless P3+K2 grade only after "
            "its own labelled multiplier t_v*N; the six monomials of F "
            "do not share that multiplier or terminal word grade"
        ),
        "readouts": {
            "target": "undefined for F as a declared chain (kernel tests are zero)",
            "ordinary_residue": "undefined; physical endpoint bars carry +1",
            "anchor_incidence": "undefined",
            "W": "undefined",
        },
        "desired_normalized_value": (
            "not fixed by the clean-C5 equations; if F were invariant under "
            "the two displayed full-Jacobian columns, it would be forced to "
            "zero and could not provide a unit-normalized terminal readout"
        ),
    }


def main() -> None:
    pin_dependencies()
    ledger = {
        "theorem": "formal corrected aggregate F: full endpoint/q Jacobian boundary",
        "formal_identity": formal_identity(),
        "full_jacobian": jacobian_columns(),
        "source_typing": source_typing_gate(),
        "verdict": (
            "F repairs the five eta_z pairings but is not a source-typed "
            "terminal correction and fails two earlier full physical "
            "stabilizer kernel columns"
        ),
        "minimal_missing_datum": (
            "a repeated-grade source cell whose complete companions give the "
            "Omega-to-rootless-r comparison with tgt=ores=ainc=W=0; a raw "
            "coefficient-ring primitive cannot replace it"
        ),
        "scope": (
            "exact universal colour-diagonal GHZ covariance and clean C5 "
            "typing; no full source point and no claim outside the displayed "
            "formal F candidate"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"formal F ledger changed: {digest}")
    print("h3 rootless clean-C5 formal F full-Jacobian boundary: PASS")
    print("F kills the five eta_z columns: YES")
    print("F kills full physical endpoint/q kernel: NO")
    print("first failures: 5*q_pq^22 and -sum_v q_xv^(0,m_v)")
    print("source-typed terminal correction: NO")
    print("ledger SHA-256:", digest)


if __name__ == "__main__":
    main()
