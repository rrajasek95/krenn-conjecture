#!/usr/bin/env python3
"""Exact definability gate for the proposed h=3 Component-IV d2.

This checker deliberately does not differentiate the selected-row rational
calibration.  It combines three already literal audits:

* the calibration's complete 9*3^6 EqSystem census;
* the target-augmented scalar d2 square; and
* the source-labelled fourth-Hasse lift and its underived physical cokernel.

The result is a boundary theorem, not a nonexistence theorem for every
possible relative source resolution.  None of the currently typed physical
columns supplies the primitive invisible chain needed to define the desired
ordinary-residue readout.
"""

from fractions import Fraction as Q
from hashlib import sha256
import json

import verify_h3_five_exposed_two_chart_selected_cap_landing_counterguard as BASE
import verify_h3_primitive_attaching_universal_module as ATTACH
import verify_h3_target_augmented_filtered_d2_first_obstruction as D2


EXPECTED_DIGEST = "db7a21f63a68a9d73fed439af7a6096d5ed1eeb852c8c63c723da3693a82b5e2"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def normalize(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(key): normalize(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [normalize(item) for item in value]
    return value


def full_eqsystem_gate():
    packets = {}
    for name in ("direct_free", "tilted"):
        packet = BASE.build_packet(name)
        failures = BASE.full_pq_eqsystem_failures(packet)
        require(failures, f"{name} calibration became a full EqSystem point")
        packets[name] = failures

    expected_direct_free = [
        ((0, 0, 0, 0, 0, 0), 0, 0, Q(0), Q(1)),
        ((0, 1, 2, 1, 1, 2), 2, 2, Q(1), Q(0)),
        ((0, 1, 2, 2, 1, 2), 2, 1, Q(1), Q(0)),
        ((0, 1, 2, 2, 1, 2), 2, 2, Q(1), Q(0)),
        ((1, 1, 1, 1, 1, 1), 1, 1, Q(0), Q(1)),
        ((2, 2, 2, 2, 2, 2), 2, 2, Q(0), Q(1)),
    ]
    require(packets["direct_free"] == expected_direct_free,
            "direct-free full EqSystem failure locus changed")
    require(len(packets["tilted"]) == 7,
            "tilted full EqSystem failure count changed")
    return {
        "tested_coefficients_per_packet": 9 * 3**6,
        "direct_free_failures": packets["direct_free"],
        "tilted_failure_count": len(packets["tilted"]),
        "physical_basepoint": False,
    }


def selected_d2_gate():
    # This is the exact direct-free scalar packet used only to type the
    # filtered square.  It is intentionally not promoted to a source point.
    packet = D2.packet(Q(3), Q(0), Q(2), Q(5), Q(-4, 9))
    require(packet["kappa"] == "15", "direct-free curvature changed")
    require(packet["d2_pair"] == ["-15", "20/3"],
            "selected-row d2 graph changed")
    require(packet["desired_d2_defect"] == ["0", "20/3"],
            "target-zero cap defect changed")
    require(packet["e2_dimension"] == 1,
            "selected-row E2 dimension changed")
    return packet


def source_relative_gate():
    upstairs = ATTACH.source_four_cube()
    downstairs = ATTACH.physical_separator()
    bridge = ATTACH.primitive_bridge()

    require(upstairs["declared_n_A_column"] is False,
            "formal Hasse combination became a declared physical source row")
    require(upstairs["target"] == 0 and upstairs["ordinary_residue"] == 0,
            "formal Hasse lift lost its diagnostic readouts")
    require(downstairs["coordinates"]
            == ["u*Eq at edges=0", "Y*w", "target", "Y*ores"],
            "physical obstruction coordinates changed")
    require(downstairs["cokernel_generator"] == [1, 1, 1, -1],
            "primitive physical separator changed")
    require(downstairs["desired_K"] == [0, 1, 0, 0],
            "normalized invisible boundary changed")
    require(downstairs["separator_on_K"] == "1",
            "desired invisible chain entered the physical span")
    require(downstairs["candidate_rank"] == 3
            and downstairs["rank_after_K"] == 4
            and abs(int(downstairs["determinant_after_K"])) == 1,
            "primitive saturated cokernel certificate changed")
    require(downstairs["labelled_denominator_faces"] == 60,
            "labelled physical lower-face census changed")
    require(bridge["cap_normalized_boundary"] == "K=kappa*Y*w",
            "primitive bridge normalization changed")

    return {
        "upstairs": {
            "source_terms": upstairs["cycle_source_terms"],
            "boundary": upstairs["boundary"],
            "target": upstairs["target"],
            "ordinary_residue": upstairs["ordinary_residue"],
            "declared_physical_column": upstairs["declared_n_A_column"],
        },
        "downstairs": {
            "coordinates": downstairs["coordinates"],
            "physical_rank": downstairs["candidate_rank"],
            "maximal_minor_gcd": downstairs["maximal_minor_gcd"],
            "labelled_lower_faces": downstairs["labelled_denominator_faces"],
            "active_lower_faces": downstairs["active_denominator_faces"],
            "separator": downstairs["cokernel_generator"],
            "desired_chain": downstairs["desired_K"],
            "separator_value": downstairs["separator_on_K"],
            "rank_after_chain": downstairs["rank_after_K"],
            "determinant_after_chain": downstairs["determinant_after_K"],
        },
        "minimal_missing_chain": {
            "name": "n_c",
            "boundary": "kappa*Y*w",
            "target": 0,
            "ordinary_residue": 0,
            "required_new_coordinate": [0, 1, 0, 0],
            "source_condition": (
                "a literal full-EqSystem relative generator outside "
                "ker(E+W+target-ores)"
            ),
        },
    }


def main():
    ledger = {
        "scope": "h=3 Component-IV earliest physical definability gate",
        "full_eqsystem": full_eqsystem_gate(),
        "selected_d2": selected_d2_gate(),
        "source_relative": source_relative_gate(),
        "verdict": (
            "no committed physical basepoint/readout pair defines the proposed d2; "
            "the first missing datum is the literal relative chain n_c"
        ),
    }
    payload = json.dumps(normalize(ledger), sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, ("ledger changed", digest))

    print("h=3 Component-IV physical definability gate: PASS")
    print("direct-free/tilted full EqSystem failures: 6/7")
    print("selected d2: cap graph; target-zero replacement has nonzero boundary")
    print("physical relative module: rank 3 saturated; n_c is primitive rank-4 column")
    print("physical Component-IV d2: NOT YET DEFINED")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
