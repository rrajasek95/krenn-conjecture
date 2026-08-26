#!/usr/bin/env python3
"""Exact restriction of the global cycle charge to the local 23-row dual.

This checker deliberately does not resume the capped coloured-content span.
It only reads the two frozen ledgers and proves that all eleven local cycle
types lie outside the 77-row support of the global cycle functional.
"""

from __future__ import annotations

import argparse
import csv
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TAIL_DIR = (ROOT / "computations"
            / "unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23")
TAIL_DUAL = TAIL_DIR / "k16_cycle_partition_dual.tsv"
TAIL_RESULT = TAIL_DIR / "results_k16_cycle_partition_quotient.json"
LOCAL_RESULT = (ROOT / "computations"
                / "unaudited-codex-orbit0-k16-dual-sparse-factor-2026-08-23"
                / "results_k16_dual_sparse_factor.json")
RESULT = HERE / "results_colored_cycle_capped.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha256(path):
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build(mutate=False):
    pinned = {
        TAIL_DUAL: "fea91d03250128fa6ea99252659ddd2b46329a9318916a19d6dae0ecfb69dd84",
        TAIL_RESULT: "d4cbc7350253bcec3cb34768386b7a83265251ef569b3f4654507da389a9b8bb",
        LOCAL_RESULT: "7f045197795272b7ed75d82704b03c29495b50d516826e97ee68e9f6e6d4a17c",
    }
    for path, expected in pinned.items():
        require(file_sha256(path) == expected, f"frozen input drift: {path}")
    tail = json.loads(TAIL_RESULT.read_text())
    local = json.loads(LOCAL_RESULT.read_text())
    require(tail["logical_sha256"]
            == "99693d522e3127a8aa5ac7074a6e55d522be7eeb8f8c050c0a5fea3007e8b559"
            and local["logical_sha256"]
            == "1080f3886801d39ec6a62e87daf5a75b086eb6701f536988fb232bb7cabaf6fd",
            "logical input theorem drift")

    with TAIL_DUAL.open() as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        charge = {
            tuple(sorted(int(value) for value
                         in record["cycle_partition"].split(","))):
            int(record["integer_coefficient"])
            for record in reader
        }
    require(len(charge) == tail["exact_dual_support"] == 77,
            "global cycle charge support changed")

    local_types = {
        tuple(sorted(record["cycle_partition"]))
        for record in local["port_graphs"]["rows"]
    }
    require(len(local_types) == 11, "local cycle-type count changed")
    if mutate:
        charge[min(local_types)] = 1
    restrictions = {partition: charge.get(partition, 0)
                    for partition in local_types}
    require(set(restrictions.values()) == {0},
            "hostile mutation/global charge no longer restricts to zero")
    polynomial_pairing = sum(
        record["coefficient"][0]
        * charge.get(tuple(sorted(record["cycle_partition"])), 0)
        for record in local["port_graphs"]["rows"])
    require(polynomial_pairing == 0, "global charge hits local polynomial")

    result = {
        "format": "n8-orbit0-k16-colored-cycle-capped-v1",
        "status": "CAPPED_UNRESOLVED_WITH_EXACT_ZERO_RESTRICTION",
        "pinned": {str(path.relative_to(ROOT)): digest
                   for path, digest in pinned.items()},
        "global_cycle_charge": {
            "coordinate_space": tail["cycle_partition_coordinates"],
            "support": len(charge),
            "abstract_columns_annihilated":
                tail["all_abstract_profile_pairings_zero"],
            "global_K16_residual_pairing": tail["exact_target_pairing"],
            "structured_a_times_T_pairing":
                tail["original_structured_aT_pairing"],
        },
        "local_23_restriction": {
            "cycle_types": len(local_types),
            "types": [
                {"partition": list(partition), "charge": coefficient}
                for partition, coefficient in sorted(restrictions.items())
            ],
            "nonzero_restrictions": 0,
            "signed_polynomial_pairing": polynomial_pairing,
            "proportionality_verdict":
                "NOT_A_NONZERO_MULTIPLE_OF_THE_LOCAL_23_ROW_DUAL",
            "interpretation": (
                "The global 77-support cycle functional is identically zero "
                "on the entire eleven-type coordinate support of the local "
                "23-row cochain. It therefore cannot explain that local "
                "descendant by restriction or nonzero proportionality."),
        },
        "colored_content_attempt": {
            "hard_cap_seconds": 240,
            "terminal_verdict": "UNRESOLVED_AT_CAP",
            "complete_profile_coordinate_count": 3097802,
            "structured_target_profile_support": 125,
            "structured_target_literal_terms": 1157625,
            "preliminary_pure_path_shell": {
                "columns": 2394,
                "coordinate_union": 5463,
                "rank_mod_1009": 2334,
                "target_in_shell_span_mod_1009": False,
                "target_remainder_support_mod_1009": 182,
                "scope": (
                    "Only the preliminary pure-path/pure-closed shell; "
                    "nonmembership here gives no full abstract-quotient "
                    "nonmembership inference."),
            },
            "two_colour_subproblem": {
                "complete_profile_coordinates_enumerated": 1430,
                "complete_mixed_columns_enumerated": 4180,
                "span_solve": "INTERRUPTED_NO_RESULT",
            },
            "strict_no_result": (
                "The full coloured-content column span was not completed, "
                "and no exact dual or membership certificate was obtained. "
                "The computation must not be cited as a coloured quotient "
                "separation or membership theorem."),
        },
        "scope_guard": (
            "The zero-restriction theorem is exact and replayable. All "
            "coloured-content counts/ranks are frozen capped checkpoints only; "
            "no literal frontier and no resumed span computation."),
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(payload.encode("ascii")).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = build(mutate=args.mutate)
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("global cycle charge/local dual restriction: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
