#!/usr/bin/env python3
"""Identify the order-six primitive face with one-sided overlap landing.

The source-shadow lift has a primitive factor 07:11 wedge 24:11.  The first
edge is an endpoint arm at S=7 through internal site 0; the second is a
disjoint internal cofactor edge.  If site 0 is target-full and the deficient
S quotient is normalized to miss colour 1, this arm is exactly quotient
visible.  The overlap cap (S,0) (or its oriented equivalent) then has rank
(3,3).  The theorem is conditional on a source-faithful physical
totalization retaining this literal face and a nonzero cofactor.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_order6_missing_face_probe.py":
        "5f0e6ad385547aed67f1d954da57c71929d336552bb98d07c68d271889b982ab",
    "computations/verify_h3_post_ks_full_nine_overlap_visibility_reduction.py":
        "3a18ddb3cf717d41dd3d8033d128382093d33561c98ab164bec9876b74fb8eb8",
    "notes/h3-post-ks-full-nine-overlap-visibility-reduction.md":
        "fd026f47e61d0bd25ea82ac2a3e83bd54cc8416bcd7cb56f746a0d449dc69a95",
}
EXPECTED_LEDGER_SHA256 = "ee0d5de58b1e74555af7617e5d72f894fff4dab304dc3ee04d3bac5b3cde2900"


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
        "overlap_order6",
    )
    overlap = load(
        "computations/verify_h3_post_ks_full_nine_overlap_visibility_reduction.py",
        "overlap_rank",
    )
    order6_audit = order6.audit()
    incidence = overlap.audit_h3_six_site_incidence()
    rank_reduction = overlap.audit_overlap_rank_reduction()

    endpoint_arm = (0, 7, 1, 1)
    cofactor_edge = (2, 4, 1, 1)
    require(order6_audit["missing_face"] == "07:11 wedge 24:11"
            and endpoint_arm in {
                tuple(cell) for cell in
                order6_audit["solution_common_derivative_cells"]
            }
            and cofactor_edge in {
                tuple(cell) for cell in
                order6_audit["solution_common_derivative_cells"]
            }, "the primitive order-six overlap face changed")
    require(set(endpoint_arm[:2]).isdisjoint(cofactor_edge[:2]),
            "the endpoint arm stopped having a disjoint cofactor tail")
    require(incidence["minimum_target_full_sites"] == 2,
            "the overlap opportunity count changed")

    # Normalize the deficient outer endpoint quotient to miss colour 1.
    e0 = (Q(1), Q(0), Q(0))
    e1 = (Q(0), Q(1), Q(0))
    e2 = (Q(0), Q(0), Q(1))
    deficient_outer = (e0, e2)
    target_full_inner = (e0, e1, e2)
    visible_arm = e1
    before = (overlap.rank(deficient_outer), overlap.rank(target_full_inner))
    after = (overlap.rank(deficient_outer + (visible_arm,)),
             overlap.rank(target_full_inner + (visible_arm,)))
    require(before == (2, 3) and after == (3, 3),
            "the primitive face stopped restoring the overlap rank")
    require(rank_reduction["visible_transport_profile"] == [3, 3],
            "the pinned one-sided rank profile changed")

    return {
        "primitive_face": [list(endpoint_arm), list(cofactor_edge)],
        "endpoint_arm": "S7--0 in colour 1",
        "disjoint_internal_cofactor": "24:11",
        "minimum_target_full_internal_sites": 2,
        "incidence_reason": (
            "on the six residual sites, q^[3]=X_0 makes colour zero full "
            "and the two bright four-covers intersect in at least two sites"
        ),
        "normalized_outer_deficient_span": ["e0", "e2"],
        "primitive_arm_outer_image": "e1",
        "overlap_rank_before": list(before),
        "overlap_rank_after": list(after),
        "conditional_landing": (
            "if the physical order-six totalization retains a nonzero "
            "07:11*24:11 carrier and site 0 is a chosen target-full internal "
            "site, then the overlapping cap has ranks (3,3)"
        ),
        "remaining_label_gate": (
            "choose/transport the order-six primitive face so that one of the "
            "at least two target-full sites occupies its internal endpoint "
            "and colour 1 is the deficient outer quotient direction"
        ),
        "physical_transport_proved": False,
        "global_consequence_if_typed": (
            "the same relative totalization that closes residual endpoint "
            "holonomy also supplies the one-sided active-rank overlap; no "
            "separate double-transverse arm theorem is needed"
        ),
    }


def main():
    ledger = {
        "theorem": "order-six primitive face one-sided overlap landing target",
        "audit": audit(),
        "scope": (
            "exact face topology and rank algebra, conditional on physical "
            "source typing, nonzero cofactor, and compatible site/colour "
            "normalization"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"order-six overlap ledger changed: {digest}")
    print("h3 residual-q order-six one-sided overlap target: PASS")
    print("primitive face: endpoint arm 07:11 with cofactor 24:11")
    print("conditional overlap ranks: (2,3) -> (3,3)")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
