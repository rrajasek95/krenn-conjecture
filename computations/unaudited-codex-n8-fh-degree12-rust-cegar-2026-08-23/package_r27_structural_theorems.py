#!/usr/bin/env python3
"""Fast replay ledger for the frozen r27 structural/homology artifacts."""

import argparse
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "results_r27_structural_theorems_package.json"
EXPECTED_PACKAGE_SHA256 = "1614b22dd85c350026874f7bc111fcfb3136868cc06bb4845cfc19de46cfeb6c"
ARTIFACTS = {
    "incremental_base": (
        "results_fh_degree12_incremental_bounded.json",
        "d469ae0d58c7ddea174bc18abeb07cda1e37d0e7dc724fc5e647911890225341",
        False,
    ),
    "incremental_round": (
        "results_fh_degree12_incremental_round_bounded.json",
        "a85d61d1183be2d94d6279f9456d46cc2527a626ebbfb0c58ef7597c7881f01d",
        False,
    ),
    "packet_private": (
        "results_r27_pending_structure.json",
        "ff43d5930325a6bd1f2afe39f4ef14b6fc0fdd2023ae801178579058ab355f81",
        False,
    ),
    "global_private_referee": (
        "results_r27_global_private_core.json",
        "2b31f4252eb46d51bd81c31b9c4e585fec2a27e596f32bdf5f580039246705b7",
        False,
    ),
    "owner_shell": (
        "results_r27_owner_shell_topology.json",
        "e92e1fd60a4ee4f61ec0cb89b85bdce354b59ff010d66f21605983270459c9af",
        False,
    ),
    "extended_dual": (
        "results_r27_extended_dual_homology.json",
        "701d9d866b1ab8cfdf13d52bd3a6b2e8ea340220403249f5ea07a8760ede35f9",
        False,
    ),
    "one_attachment": (
        "results_r27_two_row_one_attachment.json",
        "cb5d5fb70a8b70b32bd0928e504ceaf4f8d86720d81d3fec193c6ba817167da0",
        True,
    ),
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def replay_logical(payload, drops_elapsed):
    work = dict(payload)
    claimed = work.pop("logical_sha256")
    if drops_elapsed:
        work.pop("elapsed_seconds_nonlogical")
    encoded = json.dumps(work, sort_keys=True, separators=(",", ":"))
    require(sha256(encoded.encode("ascii")).hexdigest() == claimed,
            "artifact logical digest does not replay")
    return claimed


def audit(mutate=False):
    loaded = {}
    file_hashes = {}
    for label, (name, expected, drops_elapsed) in ARTIFACTS.items():
        path = HERE / name
        payload = json.loads(path.read_text())
        require(replay_logical(payload, drops_elapsed) == expected,
                f"{label} logical digest changed")
        loaded[label] = payload
        file_hashes[label] = sha256(path.read_bytes()).hexdigest()

    packet = loaded["packet_private"]
    require(packet["counts"]["pending_columns"] == 7_316
            and packet["counts"]["new_rows"] == 524_268
            and packet["counts"]["initial_private_rows"] == 447_520
            and packet["counts"]["initial_private_columns"] == 7_316
            and packet["counts"]["residual_columns"] == 0,
            "packet-private theorem changed")
    global_referee = loaded["global_private_referee"]
    require(global_referee["global_referee"]["globally_private_rows"] == 0
            and global_referee["selected_top_residual_owner_shell"]["rows"] == 7_316
            and global_referee["selected_top_residual_owner_shell"]
                ["extra_column_orbits_beyond_r27"] == 51_181,
            "global-private referee changed")
    shell = loaded["owner_shell"]
    exact = shell["two_core"]["exact_rank_decomposition"]
    require((shell["two_core"]["rows"], shell["two_core"]["columns"],
             shell["two_core"]["edges"])
            == (3_942, 7_180, 15_400)
            and exact["exact_rank_over_Q"] == 3_178
            and exact["exact_left_nullity"] == 764
            and shell["external_escape"]
                ["columns_with_rows_beyond_r27_interface"] == 51_181,
            "owner-shell theorem changed")
    homology = loaded["extended_dual"]
    require(homology["extended_dual"]["target_pairing_mod_prime"] == 600_319_282
            and homology["sparsest_target_coupled_class"]["support"] == 2
            and homology["sparsest_target_coupled_class"]
                ["pairing_with_extended_correction_mod_prime"] == 97_612_875,
            "extended-dual homology seed changed")
    attachment = loaded["one_attachment"]
    if mutate:
        attachment["status"] = "MIGRATES_SPARSE_EXACT_Z"
    require(attachment["status"] == "DIES_ON_FIRST_ATTACHMENT"
            and attachment["input"]["escaping_owner_columns"] == 20
            and attachment["input"]["collected_escape_rows"] == 1_665
            and attachment["input"]["relevant_frozen_shell_columns"] == 88
            and attachment["solve"] == {
                "label": "1:04088385b0c5e5f9", "residual": [-1, 1]},
            "one-attachment terminal changed")

    payload = {
        "format": "n8-fh-d12-r27-structural-theorems-package-v1",
        "status": "PASS_BOUNDED_D12_LANE_RETIRED",
        "logical_artifacts": {label: expected for label, (_name, expected, _drop)
                              in ARTIFACTS.items()},
        "artifact_file_sha256": file_hashes,
        "terminal_ledger": {
            "r27_packet_exact_Z_independent_relative_to_r26": True,
            "global_private_shortcut": "fails on all 447520 packet leaves",
            "owner_shell_exact_Q_rank": 3_178,
            "owner_shell_left_nullity": 764,
            "sparsest_modular_target_coupled_core_class_support": 2,
            "first_attachment": "dies exactly on residual -1",
        },
        "scope": (
            "bounded homogeneous degree12 normalized Fh lane only; the final "
            "attachment is terminal and no second shell, degree13, saturation, "
            "exact-Q target lift, or global conjecture inference is made"
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_PACKAGE_SHA256 is not None:
        require(payload["logical_sha256"] == EXPECTED_PACKAGE_SHA256,
                "r27 theorem package changed")
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("r27 structural theorem package: PASS")
    print("logical", payload["logical_sha256"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    audit(parser.parse_args().mutate)
