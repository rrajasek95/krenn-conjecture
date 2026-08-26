#!/usr/bin/env python3
"""Exact h=3 countermodel: switch families plus charge do not imply fillers."""

from __future__ import annotations

import hashlib
import json
import os
from fractions import Fraction as Q
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TOTAL = ROOT / "computations/unaudited-codex-n8-pacomp-x23-total-carrier-et-construction-audit-2026-08-25"
CIRCULAR = ROOT / "computations/unaudited-codex-n8-pacomp-x23-et-dependency-circularity-audit-2026-08-25"
CHARGE = ROOT / "computations/unaudited-codex-orbit0-k19-direct-charge-correction-referee-2026-08-24"
LEDGER = CHARGE / "results_corrected_k19_through_k24_ledgers.json"
PINS = {
    TOTAL / "MANIFEST.sha256": "f4c40ad4801fcf2950af2871e46eb6971e3a5fee12f124a8f37367d6e343117b",
    TOTAL / "results_total_carrier_et_construction_audit.json": "6b0e778da9351c804e311735a5ba2cdfbcfbcd172e18f571773de1b99ea74218",
    CIRCULAR / "MANIFEST.sha256": "42573cc253b38b66eee8324e671124657728373fbcb707fbf9df71a360116009",
    CIRCULAR / "results_et_dependency_circularity_audit.json": "bce2efe321bb54e07f783cb3c2acffa279511f07629dbce067d81dce90ce0cf2",
    ROOT / "computations/verify_h3_first_collision_minimal_augp2_bimodule_candidate_gate.py": "48703772c5bba258e32a032d42d8389bf449a794bf45bde4739e01a7d15c877f",
    CHARGE / "MANIFEST.sha256": "3a6f2316f48c58687bebb1c724598b9085483d3ee6e741bdbe16adda24ad36d4",
    LEDGER: "b9521f13fef3a98a60a2597b5a43a57cee99e87ea467eeb6b20173370dd87a2e",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def rank(columns):
    columns = [list(map(Q, column)) for column in columns]
    if not columns:
        return 0
    rows = [[columns[j][i] for j in range(len(columns))] for i in range(len(columns[0]))]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, len(rows)) if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(len(rows)):
            if row != answer and rows[row][column]:
                value = rows[row][column]
                rows[row] = [a - value * b for a, b in zip(rows[row], rows[answer])]
        answer += 1
    return answer


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right)), Q(0))


def replay_manifest(directory: Path):
    for line in (directory / "MANIFEST.sha256").read_text().splitlines():
        expected, relative = line.split("  ", 1)
        assert sha256(directory / relative) == expected


def fraction(record):
    return Q(record["numerator"], record["denominator"])


def main():
    for path, expected in PINS.items():
        assert sha256(path) == expected, path
    for directory in (TOTAL, CIRCULAR, CHARGE):
        replay_manifest(directory)

    total = json.loads((TOTAL / "results_total_carrier_et_construction_audit.json").read_text())["result"]
    circular = json.loads((CIRCULAR / "results_et_dependency_circularity_audit.json").read_text())["result"]
    assert total["status"] == "PASS_NO_EXISTING_CONSTRUCTION_ONE_DIMENSIONAL_FACE_OBSTRUCTION"
    assert total["minimal_extension"]["constructor_level_requirements"][0] == "both fixed-window DQ<->PS switch families"
    assert circular["status"] == "PASS_CIRCULAR_STOP_NO_EXISTING_ROUTE_IMPLIES_FILLERS"

    # Stronger-than-available top presentation: generously treat all four
    # formal K2,2 mates from both switch families as actual boundary columns.
    switch_columns = (
        (1, 0, 1, 0),
        (1, 0, 0, 1),
        (0, 1, 1, 0),
        (0, 1, 0, 1),
    )
    eta_top = (1, 1, -1, -1)
    L01 = (2, 0, 0, 0)  # normalized to the sealed detector value 2
    assert rank(switch_columns) == 3
    assert all(dot(eta_top, column) == 0 for column in switch_columns)
    assert dot(eta_top, L01) == 2
    assert rank(switch_columns + (L01,)) == 4

    # Strongest face-complete retained-r presentation from the sealed E_T audit.
    face_columns = (
        (1, 1, 1, 0, 0),
        (1, 0, 0, 1, 1),
        (1, 1, 0, 1, 0),
        (1, 0, 1, 0, 1),
    )
    eta_retained = (Q(1), Q(-1, 2), Q(-1, 2), Q(-1, 2), Q(-1, 2))
    R_ret = (1, 0, 0, 0, 0)
    assert rank(face_columns) == 3
    assert all(dot(eta_retained, column) == 0 for column in face_columns)
    assert dot(eta_retained, R_ret) == 1
    assert rank(face_columns + (R_ret,)) == 4

    # Replay the corrected scalar ledger exactly.  It conserves the actual
    # truncated packet, and explicitly supplies no membership/placement map.
    ledger = json.loads(LEDGER.read_text())
    pages = ledger["corrected_charges"]
    page_sum = sum((fraction(pages[f"K{k}"]) for k in range(14, 25)), Q(0))
    raw_packet = fraction(ledger["raw_27_packet_charge"])
    through_k24 = fraction(ledger["corrected_cumulative_ledgers"]["through_K24"])
    actual_delta = fraction(ledger["actual_minus_conditional_zero_target"]["charge"])
    assert page_sum == raw_packet == through_k24 == actual_delta == Q(4564224)
    assert ledger["conservation_against_actual_input"]["unexplained_residual"]["numerator"] == 0
    assert ledger["interface_classification"]["required_only_not_computed"] is True
    assert "does not compute the omitted K9+ lift, membership, or a conjecture verdict" in ledger["scope"]

    # Product countermodel.  On the local chain sort, declare charge zero on
    # every coordinate.  Thus every displayed boundary has charge zero, but
    # so do the two detected non-boundaries.  The page constants live in a
    # disjoint scalar sort and satisfy the K14..K24 identities above.
    # Passing to the two detected cokernel lines gives the minimal graded
    # countermodel Q*[L] direct-sum Q*[R] with zero incoming differential.
    result = {
        "schema": "PACOMP_H3_SWITCH_CHARGE_NONIMPLICATION_COUNTERMODEL_V1",
        "status": "PASS_NO_IMPLICATION_MINIMAL_EXACT_COUNTERMODEL",
        "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
        "generous_switch_presentation": {
            "target_dimension": 4,
            "source_columns": 4,
            "boundary_rank": 3,
            "both_switch_families_present": True,
            "annihilator": list(eta_top),
            "L01_detector_value": 2,
            "conclusion": "L01 is not in the boundary image even after all four formal mates are promoted to columns",
        },
        "retained_face_presentation": {
            "target_dimension": 5,
            "source_columns": 4,
            "boundary_rank": 3,
            "annihilator": [str(value) for value in eta_retained],
            "R_ret_detector_value": 1,
            "conclusion": "neither R_ret nor -R_ret is in the face-complete boundary image",
        },
        "smallest_countermodel": {
            "graded_target": "Q*[L01] direct_sum Q*[R_ret] in the two relevant filtration quotients",
            "incoming_source": "0",
            "differential": "0",
            "local_charge_functional": "0 on both quotient lines",
            "missing": ["dLambda_01=L01", "dPi_r,01=-R_ret"],
        },
        "charge_product_factor": {
            "corrected_K14_K24_sum": str(page_sum),
            "raw_truncated_packet_charge": str(raw_packet),
            "unexplained_residual": 0,
            "omitted_lift_correction_required_but_uncomputed": -4564224,
            "interface_to_local_PAComp_source_image": "NONE",
            "logical_role": "disjoint exact scalar factor; it does not alter either boundary image",
        },
        "first_missing_axiom": "an explicit source-labelled, same-grade physical placement whose differential has nonzero image in one of the two detected quotient lines",
        "scope": {"h": 3, "symbolic_only": True, "D12_reads": False, "solves": 0, "PAComp_promotion": False, "conjecture_promotion": False},
    }
    temporary = HERE / "results_countermodel.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_countermodel.json")
    print(json.dumps({"status": result["status"], "L_detector": 2, "R_detector": 1}, sort_keys=True))


if __name__ == "__main__":
    main()
