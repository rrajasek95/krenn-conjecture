#!/usr/bin/env python3
"""Audit direct active-fan coloop normalization and the axis-pure shortcut.

The complete-row coloop pivot already supplies literal common-tail,
endpoint-port, orientation and fine-word provenance.  What it supplies is
the signless U/V packet.  The normalized target-coloop closure additionally
needs its complete protected endpoint-odd packet.

A six-row guard keeps the exact signless packet and a target-safe odd packet
with one private protected residue.  The desired odd packet is independent;
a primitive covector detects it.  This residue is independent of the
nonzero offdiagonal source coordinate which produced the active fan.

Moreover, the active-fan argument works after localizing a named nonzero
offdiagonal cell e (or determinant/cofactor product).  The axis-pure ideal
contains e, so in the localized ring it is the unit ideal:

    1 = e*s - (e*s-1).

Thus darkness/failure of the protected comparison cannot internally deform
the active chart to the axis-pure locus.  Such a boundary degeneration would
be a new anchor-safe source theorem, not a consequence of the comparison
cokernel.  The global emptiness of the axis-pure fibre cannot be used to
force the missing Phi without that theorem.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_fan_coloop_complete_row_pivot.py":
        "d62fd630abac6e4d25bd6ffb0c1a2070311ec1c5d3c7764f56793283f78aa94a",
    "computations/verify_h3_fan_coloop_packet_q_comparison_defect.py":
        "86db5c89196a183c5ddc2b1c2198029fa45ea1cdff1f7d239a74870cd4957e94",
    "computations/verify_h3_fan_coloop_cartan_circuit_comparison_gate.py":
        "c652f10a8bac32f11f4c090a55687cf672ce3f96629384f0fbde9f08f440a1bd",
    "computations/verify_h3_axis_pure_global_min_support_census.py":
        "4b88379419c94aa21f8a457b89821fb107d4b841c17ffa38ec10516e48426156",
    "computations/verify_h3_axis_pure_closure_active_crossword_frontier.py":
        "b3225f17209d8c920301575c563c9d07954e779339361ae4014d100895bbac67",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
}
EXPECTED_LEDGER_SHA256 = (
    "a8c648aa3747adb9f940306b4f0f1e30c61c75fe6b2980220acad3a5486057f8"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def complete_row_provenance_audit():
    pivot = load(
        "computations/verify_h3_active_fan_coloop_complete_row_pivot.py",
        "direct_coloop_pivot",
    )
    algebra = pivot.audit_complete_row_pivot()
    transport = pivot.audit_termwise_common_q_transport()
    concepts = pivot.audit_six_closed_concepts()
    require(algebra["elimination"] == "alpha*U_i-d_i*V_i=alpha"
            and transport["omit_edge_with_two_endpoint_ports"] == 78
            and transport["unordered_holes_realized"] == 15
            and transport["ordered_holes_realized"] == 30
            and concepts["closed_symmetry_types"] == 6,
            (algebra, transport, concepts))
    return {
        "coloop_unit": "alpha*C_c=1",
        "complete_row_pivot": algebra["elimination"],
        "forced_nonzero_alternative": algebra["typed_alternative"],
        "literal_matching_audit": {
            "omit_coloop_matchings": transport["omit_coloop_edge"],
            "two_endpoint_port_matchings": transport[
                "omit_edge_with_two_endpoint_ports"],
            "unordered_holes": transport["unordered_holes_realized"],
            "ordered_orientations": transport["ordered_holes_realized"],
        },
        "transported_data": [
            "one physical matching skeleton",
            "common residual q tail away from the two changed sites",
            "same P/S partners and orientation",
            "same endpoint output heads",
            "exact pure or two-site-mixed fine output word",
            "remote decorated cells and selected mutual anchors",
        ],
        "all_six_closed_Hall_types_use_same_pivot": True,
        "positive_verdict": (
            "choosing one nonzero literal summand from U_i or V_i really "
            "does supply the common-tail/head/orientation/fine-grade input; "
            "that part of arbitrary-coloop normalization is closed"
        ),
    }


def protected_odd_packet_guard():
    # Coordinates are (U+,U-,V+,V-,target,private protected residue).
    alpha, diagonal = Q(2), Q(3)
    signless = (alpha, alpha, -diagonal, -diagonal, -alpha, Q(0))
    desired_odd = (alpha, -alpha, -diagonal, diagonal, Q(0), Q(0))
    actual_odd = (alpha, -alpha, -diagonal, diagonal, Q(0), Q(1))
    separator = (Q(1, 2), Q(0), Q(0), Q(0), Q(1, 2), Q(-1))
    require(rank((signless, actual_odd)) == 2
            and rank((signless, actual_odd, desired_odd)) == 3,
            "the complete protected odd-packet guard changed")
    require(dot(separator, signless) == 0
            and dot(separator, actual_odd) == 0
            and dot(separator, desired_odd) == 1,
            "the primitive packet separator changed")

    plus = tuple((left + right) / 2
                 for left, right in zip(signless, desired_odd, strict=True))
    minus = tuple((left - right) / 2
                  for left, right in zip(signless, desired_odd, strict=True))
    require(plus == (alpha, 0, -diagonal, 0, -alpha/2, 0)
            and minus == (0, alpha, 0, -diagonal, -alpha/2, 0),
            "the normalized oriented split changed")
    return {
        "row_order": [
            "U+", "U-", "V+", "V-", "target",
            "private protected residue",
        ],
        "physical_signless_complete_row": [str(value) for value in signless],
        "target_safe_odd_near_hit": [str(value) for value in actual_odd],
        "required_complete_odd_packet": [str(value) for value in desired_odd],
        "rank_before_then_after_required_odd": [2, 3],
        "primitive_complete_row_dual": [str(value) for value in separator],
        "oriented_rows_after_exact_odd": {
            "plus": [str(value) for value in plus],
            "minus": [str(value) for value in minus],
        },
        "first_exact_obstruction": (
            "one protected private residue of the target-safe odd prism; "
            "the scalar pivot/common tail does not determine this row"
        ),
        "relation_to_q_defect_theorem": (
            "after a physical Phi exists, this residue is exactly tested by "
            "[q-q0*Phi]; before Phi, the quotient class is not defined"
        ),
    }


def active_localization_axis_pure_audit():
    # Let e be the selected nonzero offdiagonal reference cell.  Localizing
    # D(e) adjoins s=e^-1, represented by e*s-1=0.  Axis-purity adds e=0.
    # The displayed linear combination is an exact unit-ideal certificate.
    # Monomials are represented in the tiny basis (1,e,e*s).
    localization_relation = (Q(-1), Q(0), Q(1))
    axis_generator_times_s = (Q(0), Q(0), Q(1))
    unit = tuple(left - right for left, right in
                 zip(axis_generator_times_s, localization_relation,
                     strict=True))
    require(unit == (Q(1), Q(0), Q(0)),
            "the D(e) cap V(e) unit certificate changed")

    # The target-augmented private-site identity at a normalized local point.
    # q_e + Delta_ef*C_f = 0 with q_e=1, Delta=-1, C_f=1.
    q_e, determinant, cofactor = Q(1), Q(-1), Q(1)
    require(q_e + determinant * cofactor == 0,
            "the normalized active-fan identity changed")

    return {
        "active_reference_cell": "e=q_u=A_vu[b,a] != 0",
        "private_site_identity": "sum_s Delta_us*C_s=-e",
        "normalized_literal_fan_point": {
            "e": 1, "one_Delta": -1, "its_cofactor": 1,
        },
        "active_chart": "D(e), with e*s-1=0",
        "axis_pure_ideal_contains": "e",
        "unit_certificate": "1=e*s-(e*s-1)",
        "axis_pure_locus_inside_active_chart": "EMPTY",
        "consequence": (
            "a comparison obstruction inside D(e) cannot itself reach the "
            "axis-pure locus; a specialization e->0 leaves the active chart "
            "and needs a separately proved source-flat, anchor-safe boundary "
            "deformation"
        ),
    }


def comparison_darkness_independence_guard():
    # Extend the protected packet by one source coordinate e.  The comparison
    # separator has zero e coefficient, while the active point has e=1.
    # Hence its nonzero value gives no equation/deformation on e.
    # Row order: (e,U+,U-,V+,V-,target,private).
    alpha, diagonal = Q(2), Q(3)
    signless = (Q(0), alpha, alpha, -diagonal, -diagonal, -alpha, Q(0))
    actual_odd = (Q(0), alpha, -alpha, -diagonal, diagonal, Q(0), Q(1))
    desired_odd = (Q(0), alpha, -alpha, -diagonal, diagonal, Q(0), Q(0))
    separator = (Q(0), Q(1, 2), Q(0), Q(0), Q(0), Q(1, 2), Q(-1))
    active_point = (Q(1), Q(0), Q(0), Q(0), Q(0), Q(0), Q(0))
    axis_functional = (Q(1), Q(0), Q(0), Q(0), Q(0), Q(0), Q(0))
    require(dot(separator, signless) == dot(separator, actual_odd) == 0
            and dot(separator, desired_odd) == 1
            and dot(separator, active_point) == 0
            and dot(axis_functional, active_point) == 1,
            "the comparison/source-coordinate independence guard changed")
    return {
        "complete_coordinate_order": [
            "offdiagonal active cell e", "U+", "U-", "V+", "V-",
            "target", "private protected residue",
        ],
        "comparison_dual": [str(value) for value in separator],
        "comparison_dual_on_active_source_coordinate": 0,
        "axis_purity_functional_on_active_source_coordinate": 1,
        "logical_no_go": (
            "packet darkness/nonmembership is independent of setting e=0; "
            "it neither deletes the selected offdiagonal cell nor supplies "
            "a tangent or finite source deformation"
        ),
        "scope": (
            "an exact complete protected-row direct-sum counterguard, not an "
            "asserted new full GHZ source point"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": (
            "h3 arbitrary active-fan coloop direct normalization and "
            "axis-pure-shortcut boundary"
        ),
        "pins": PINS,
        "complete_row_provenance": complete_row_provenance_audit(),
        "protected_odd_packet": protected_odd_packet_guard(),
        "active_localization_vs_axis_pure": active_localization_axis_pure_audit(),
        "darkness_independence": comparison_darkness_independence_guard(),
        "verdict": (
            "The coloop unit plus complete pure/mixed rows really does supply "
            "a nonzero omit-coloop carrier with the common residual q tail, "
            "endpoint heads/orientation and fine grade required by normalized "
            "coloop routing.  It does not supply the complete protected odd "
            "U/V packet: one private row can survive while every literal "
            "matching label remains correct.  Failure/darkness of that packet "
            "cannot be converted to axis-purity.  The active proof is localized "
            "at a nonzero offdiagonal e, while the axis-pure ideal contains e "
            "and becomes the unit ideal after localization.  A boundary "
            "specialization deleting e would be a new anchor-safe source "
            "deformation theorem."
        ),
        "shortest_remaining_theorem": (
            "construct the fan-grade protected odd Phi/q comparison, or "
            "construct an independent source-flat anchor-safe degeneration "
            "from its first private defect to the axis-pure boundary.  Global "
            "axis-pure emptiness alone proves neither arrow"
        ),
        "scope": (
            "canonical h=3 active-fan localization, exact complete-row "
            "common-tail matching audit, and protected-row counterguard; not "
            "an all-h theorem or a full-source counterexample"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("coloop pivot common-q/head/orientation/fine typing: CONSTRUCTED")
    print("complete protected endpoint-odd packet: ONE PRIVATE ROW OPEN")
    print("active D(e) intersect axis-pure V(e): EMPTY")
    print("dark Phi -> axis-pure deformation: NO IMPLICATION")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
