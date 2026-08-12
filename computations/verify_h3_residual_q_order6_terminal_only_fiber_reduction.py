#!/usr/bin/env python3
"""Reduce the residual-q fiber target to a terminal-only relative lift.

The order-six source-shadow theorem constructs the residual projection
(-delta) with zero literal pair-generator boundary.  The earlier one-cell
fiber criterion asked one new cell to carry both that residual and the
eta/sigma terminal packet.  Subtracting the constructed order-six direction
leaves a terminal-only vector.  This checker pins that exact linear
reduction; physical typing of either direction remains an explicit guard.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_order6_missing_face_probe.py":
        "5f0e6ad385547aed67f1d954da57c71929d336552bb98d07c68d271889b982ab",
    "notes/h3-residual-q-order6-missing-face-source-shadow-lift.md":
        "e24324f495b7c9402b6d7fa43e6e30997c437987d35236335e1d88cd2142d9b1",
    "computations/verify_h3_residual_q_eta_one_cell_fiber_product_gate.py":
        "4e84ad031b97ee67e1336c9a9d785acd3c581c2d80aeeb005d4eee784f91eccb",
}
EXPECTED_LEDGER_SHA256 = "f804422d5924462820a3ac95c4813c19c3d0c90c51df4ee79be6d8e38b609ebc"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            f"cannot load dependency: {relative}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    order6 = load(
        "computations/verify_h3_residual_q_order6_missing_face_probe.py",
        "terminal_reduction_order6",
    )
    fiber = load(
        "computations/verify_h3_residual_q_eta_one_cell_fiber_product_gate.py",
        "terminal_reduction_fiber",
    )
    order6_audit = order6.audit()
    require(order6_audit["source_boundary_terms"] == 0
            and order6_audit["shadow_reconstruction_terms"] == 16
            and order6_audit["exact_minus_delta_solvable"],
            "the order-six source-shadow lift changed")
    require(order6_audit["block_coefficient_colour_zero_cells"] == 0
            and order6_audit["block_marked_colour_two_cells"] == 0,
            "the ordinary order-six block acquired a terminal character")

    residual = fiber.vector(R_q00=-1, R_q11=1)
    eta_entries = {
        **{f"eta{face}_constant": 1 for face in fiber.FACES},
        "eta1_U1": 1,
    }
    terminal_only = fiber.vector(**eta_entries, sigma_qpq22=-1)
    full_target = fiber.add(residual, terminal_only)
    require(fiber.add(full_target, fiber.scale(-1, residual)) == terminal_only,
            "subtracting the order-six residual did not isolate the terminal")

    protected = tuple(f"D_{corner}" for corner in fiber.CORNERS) + (
        "W", "target", "ainc",
    )
    require(all(terminal_only[fiber.ROWS.index(row)] == 0
                for row in protected),
            "the terminal-only complement acquired a protected row")
    require(all(terminal_only[fiber.ROWS.index(f"R_{corner}")] == 0
                for corner in fiber.CORNERS),
            "the terminal-only complement retained residual curvature")
    require(terminal_only[fiber.ROWS.index("sigma_qpq22")] == -1,
            "the terminal-only sigma sign changed")

    return {
        "order6_source_boundary": 0,
        "order6_residual_projection": [-1, 1, 1, -1],
        "order6_natural_eta_sigma": 0,
        "remaining_residual_projection": [0, 0, 0, 0],
        "remaining_protected_rows": {
            "D": 0, "W": 0, "target": 0, "ainc": 0,
        },
        "remaining_eta": "1+delta_(1,z)*u_z/t",
        "remaining_sigma": "-q_pq^22",
        "linear_reduction": (
            "full residual/terminal fiber target = typed order-six "
            "source-shadow direction + terminal-only relative direction"
        ),
        "conditional_equivalence": (
            "after the order-six chain is physically typed in the repeated "
            "grade, the former one-cell image-membership problem is "
            "equivalent to constructing a zero-boundary, zero-residue "
            "relative class carrying only eta/sigma"
        ),
        "physical_membership_proved": False,
        "why_not": (
            "the order-six theorem is still a bounded differential-operator "
            "source-shadow lift, and the terminal-only class still needs the "
            "shifted physical relative comparison"
        ),
    }


def main():
    ledger = {
        "theorem": "order-six residual to terminal-only fiber reduction",
        "audit": audit(),
        "scope": (
            "exact augmented-row reduction conditional on physical typing of "
            "the order-six source-shadow chain; no relative terminal cell is "
            "constructed"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"order-six terminal reduction ledger changed: {digest}")
    print("h3 residual-q order-six terminal-only reduction: PASS")
    print("source/residual side: constructed at order six")
    print("remaining relative direction: eta/sigma only")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
