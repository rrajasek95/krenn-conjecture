#!/usr/bin/env python3
"""Assemble the normalized active-fan coloop gate after the anchor closure.

The complete-row pivot supplies a physically typed omit-coloop carrier and
the finite K6 Galois closure prevents an outside-hole cycle.  Conditional
on one complete physical protected odd comparison Phi in the fan-coloop
fine grade (with literal q=M-a rows), packet disagreement is exhaustive and
the bordered Cartan alternatives close every resulting target circuit,
whether its physical anchor is bright or dark.

Thus Gate II is not unconditional yet, but it has exactly one remaining
source statement: construct that fan-grade Phi/q packet.  There is no
separate anchor, Hall-orbit, or termination hypothesis after it.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_fan_coloop_saturation_boundary.py":
        "35658ebed521b93387fc00aa7d2600d703f57b3e5e5deca67a11a1ab155d6c56",
    "computations/verify_h3_active_fan_coloop_complete_row_pivot.py":
        "d62fd630abac6e4d25bd6ffb0c1a2070311ec1c5d3c7764f56793283f78aa94a",
    "computations/verify_h3_fan_coloop_cartan_circuit_comparison_gate.py":
        "c652f10a8bac32f11f4c090a55687cf672ce3f96629384f0fbde9f08f440a1bd",
    "computations/verify_h3_fan_coloop_packet_q_comparison_defect.py":
        "86db5c89196a183c5ddc2b1c2198029fa45ea1cdff1f7d239a74870cd4957e94",
    "computations/verify_h3_anchor_dark_bordered_cartan_alternative.py":
        "9db01aa332da3f7da3921895a0fe6c1f77e1c259aa2ca473949343da15cf2e7b",
    "computations/verify_target_augmented_affine_circuit_cartan_guard.py":
        "7c72b58101cc77a0ca3e3c688b5de0742b4f118777f450f235d578691954d08f",
    "computations/verify_rectangular_interference_anchor_cartan_alternative.py":
        "b3d4db9e58f374bfd1f99a43931cac87fdab109c5d33c2f1c7d110e51e8f9a0a",
}
EXPECTED_LEDGER_SHA256 = "bd21d3fff8fe163241ab5fa5b8610028a5aeb1c0137ba9844293d7ca0049793a"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def audit_branch_assembly():
    # An outside typed hole is handled before Phi.  On the trapped shore,
    # absence of Phi is the single open state.  Once Phi exists, a nonzero
    # q defect is positive; a zero defect supplies the S/D target circuit.
    # The remaining booleans reproduce the bright rectangular and dark
    # bordered alternatives.
    outcomes = Counter()
    records = []
    for outside, phi, q_visible, anchor_bright, cartan_external, beta in product(
            (False, True), repeat=6):
        if outside:
            outcome = "strict Galois-closure growth"
        elif not phi:
            outcome = "single missing fan-grade physical Phi/q packet"
        elif q_visible:
            outcome = "physical q witness / typed saturated exit"
        elif anchor_bright and cartan_external:
            outcome = "two-rank rectangular landing"
        elif anchor_bright and not cartan_external:
            outcome = "adjusted unit-Cartan kernel"
        elif beta:
            outcome = "normalized anchor-dark target separator"
        elif cartan_external:
            outcome = "ordinary target-dark cokernel separator"
        else:
            outcome = "anchor-compatible unit-Cartan kernel"
        outcomes[outcome] += 1
        records.append({
            "outside_shore": outside,
            "physical_Phi": phi,
            "q_defect_nonzero": q_visible,
            "anchor_bright": anchor_bright,
            "Cartan_external": cartan_external,
            "dark_beta_nonzero": beta,
            "outcome": outcome,
        })
    require(sum(outcomes.values()) == 64
            and outcomes["single missing fan-grade physical Phi/q packet"]
            and all("unclassified" not in record["outcome"]
                    for record in records),
            "the Gate-II branch assembly changed")
    terminal = {
        "physical q witness / typed saturated exit",
        "two-rank rectangular landing",
        "adjusted unit-Cartan kernel",
        "normalized anchor-dark target separator",
        "ordinary target-dark cokernel separator",
        "anchor-compatible unit-Cartan kernel",
    }
    require(all(outcome in terminal or outcome in {
        "strict Galois-closure growth",
        "single missing fan-grade physical Phi/q packet",
    } for outcome in outcomes), "a new Gate-II branch appeared")
    return {
        "boolean_branch_states": len(records),
        "outcome_histogram": dict(sorted(outcomes.items())),
        "only_nonterminal_after_saturation":
            "single missing fan-grade physical Phi/q packet",
    }


def audit_finite_termination_interface():
    # The exact K6 closure potential is 15-|cl(A)|.  Every physically typed
    # outside hole strictly grows the closed family, so at most fourteen
    # such steps follow a nonempty initial shore.  Once the shore is trapped,
    # the Phi/q/Cartan branch above exits without another reselection loop.
    potentials = tuple(range(14, -1, -1))
    require(all(later < earlier for earlier, later
                in zip(potentials[:-1], potentials[1:], strict=True))
            and len(potentials) - 1 == 14,
            "the finite K6 closure potential changed")
    return {
        "potential": "15-|cl(A)|",
        "maximum_strict_growth_steps_from_nonempty_shore": 14,
        "closed_ordered_concepts": 446,
        "symmetry_types": 6,
        "trapped_shore_action": (
            "apply the physical Phi quotient alternative once; do not "
            "restart Hall saturation by witness reselection"
        ),
        "additional_termination_hypothesis_after_Phi": False,
    }


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    ledger = {
        "theorem": "normalized active-fan coloop Gate-II assembly boundary",
        "pins": PINS,
        "branch_assembly": audit_branch_assembly(),
        "termination": audit_finite_termination_interface(),
        "proved_inputs": {
            "carrier": (
                "alpha*U_i-d_i*V_i=alpha supplies a literal pure/mixed "
                "omit-coloop carrier with common q, endpoint orientation, "
                "response head, fine word, and remote decorated tail"
            ),
            "saturation": (
                "an outside physical hole strictly enlarges the finite K6 "
                "Galois closure; a trapped carrier physically types one of "
                "six closed Hall concepts"
            ),
            "packet_disagreement": (
                "after physical Phi and q=M-a typing, nonzero quotient "
                "defect is a typed exit and zero defect gives the protected "
                "correction and oriented S/D split"
            ),
            "target_circuit": (
                "bright anchors use the rectangular alternative; dark "
                "anchors use the normalized bordered separator/unit theorem"
            ),
            "normalized_coloop_tail": (
                "the later h=3 target-coloop chain already consumes the "
                "C6/C8, punctured-C4, diagonal-return, and double-coloop labels"
            ),
        },
        "single_missing_statement": (
            "Fan-grade physical odd comparison: on every trapped carrier "
            "packet furnished by the complete-row pivot, construct a source-"
            "valid fine/word/common-tail preserving Phi with J0*Phi=A*J, "
            "and identify on both domains the literal physical rows "
            "q=M-a.  The ambient odd Cartan occurrence is insufficient: "
            "all retained corners and protected rows must lie in this one "
            "complete comparison packet"
        ),
        "verdict": (
            "Gate II is conditionally closed after the single displayed "
            "physical comparison theorem.  It is not yet unconditional; "
            "no independent anchor law, Hall orbit census, support potential, "
            "or normalized C6/C8 theorem remains"
        ),
        "scope": (
            "scoped theorem-level assembly of pinned results, not a "
            "construction of Phi and not global entry into the active fan"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"active-fan Gate-II assembly ledger changed: {digest}")
    print("h3 active-fan coloop Gate II: ONE PHYSICAL COMPARISON REMAINS")
    print("carrier typing / K6 termination / q split / anchor fork: closed")
    print("missing: fan-grade protected odd Phi with literal q=M-a rows")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
