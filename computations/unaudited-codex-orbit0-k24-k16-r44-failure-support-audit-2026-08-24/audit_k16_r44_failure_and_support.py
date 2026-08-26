#!/usr/bin/env python3
"""Fail-closed audit of the rejected K16 R4-4 full attempt and support repair."""

import csv
import hashlib
import json
import struct
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
FAST = ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24"
REF = ROOT / "computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24"
INPUT = ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k16.bin"
N = 24_097_095
U = 400_591_699_200

PINS = {
    "failure_evidence": (FAST / "results_k16_r44_full_failure.json", "4d78151f2326b93b629d5fd273016448008b4c659fc8779a6640e1e9faf79aea"),
    "failed_binary": (FAST / "run_k24_charge_k16_r44", "3a1b5e716ff4f781a5e523e990d8f209975b34231faf55cce8e8dd72e4f88ef9"),
    "candidate_aware_source": (FAST / "run_k24_charge_k16_r44.rs", "ca18746eb9368fe67d24e6cafc376b5e3f21530be0536313db9822efc2e58cd0"),
    "candidate_aware_binary": (REF / "run_k24_charge_k16_r44_support_v2", "2d41110bcb5e3b608d045555a7b2cf22f5a4c7e9cb26d3d53d83f4e64d75b405"),
    "checkpoint": (INPUT, "93c1b21eaa1723b98eb4d3b59ada6d6a867c434573a255d2a48fcdeead0656d3"),
    "support_candidates": (REF / "k24_k16_r44_support_candidates.tsv", "57b7f0cfa15b436b6b821922c426f19d15496eb7a1cd64e7e632acaa003d5fbf"),
    "support_census": (REF / "results_k24_k16_r44_support_census.json", "24ef69c2d8708f549f58cb5e39fd6abeaf2e1589cf854fdecdc5047f4449803e"),
    "candidate_literal_referee": (REF / "results_k24_k16_r44_support_candidates_literal_referee.json", "d0fd9bd271ba8842a1b74f27c226a7fc3b45e46eb68c265d40d1fa8045625319"),
    "independent_literal_rerun": (HERE / "results_support_candidates_literal_replay.json", "d0fd9bd271ba8842a1b74f27c226a7fc3b45e46eb68c265d40d1fa8045625319"),
    "literal_referee_source": (REF / "referee_k24_charge_literals.rs", "66f027edb3e1abbdfb16875069dec34db963c3345ef021f70991f05882b64e79"),
    "literal_referee_binary": (REF / "referee_k24_charge_literals", "3a36fcc61d7b8de805375fa58cb71f632f828788c08a24412efc4719ab656340"),
    "old_prefix": (FAST / "results_k16_r44_prefix262144.json", "237c4c132ab4f3dfef51ae4ddaad8469b9f28719b90cb13ecbe9c98326e52110"),
    "candidate_prefix": (REF / "control_k16_r44_distributed262144_support_v2.json", "f48edef8b17d3d3e7ce116cee952ff68af784cb8964a623f66186cdf9b970797"),
    "contract": (HERE / "k24_k16_r44_support_witness_contract.json", "641e162cc27e6d44d99cb5b762499624e6d33fdf2dc8fb96aecb395c8876cf32"),
}

TARGETS = [
    FAST / "results_k16_r44_complete.json",
    FAST / "results_k16_r44_complete.json.tmp",
    FAST / "results_k16_r44_complete.json.samples.tsv",
    FAST / "results_k16_r44_complete.json.samples.tsv.tmp",
    FAST / "results_k16_r44_complete_validation.json",
]

HEADER = [
    "candidate_slot", "support_bin", "record_index", "coefficient", "source_row",
    "intermediate_row", "p1", "t1", "p2", "m1", "m2", "terminal_q",
    "unit_scaled_U", "nonzero_contribution_scaled_U", "final_degree",
]

SCALAR_FIELDS = [
    "group_id", "degree", "scale_U", "ids", "covered_ids", "individual_id_charges",
    "record_interval", "records_declared", "distributed_prefix", "source_rows",
    "signed_source_coefficient", "l1_source_coefficient", "pivotable_K16_rows",
    "p1_uses", "first_children", "pivotable_intermediate_children", "p2_uses",
    "K24_terminal_occurrences", "full_occurrences", "irreducible_occurrences",
    "full_charge_scaled_U", "irreducible_charge_scaled_U", "m1_m2_hist",
]


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(8 << 20)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def input_record(stream, index):
    stream.seek(16 + 32 * index)
    data = stream.read(32)
    need(len(data) == 32, "short checkpoint record")
    return data[:24].hex(), struct.unpack_from("<q", data, 24)[0]


def validate_candidates(rows):
    need(len(rows) == 257, "candidate count")
    slots = [int(row["candidate_slot"]) for row in rows]
    need(slots == list(range(257)), "candidate slots/order")
    indices = [int(row["record_index"]) for row in rows]
    need(len(set(indices)) == 257, "candidate source indices not distinct")
    bins = [int(row["support_bin"]) for row in rows]
    expected_counts = {index: (7 if index < 35 else 6) for index in range(37)}
    need(dict(sorted(Counter(bins).items())) == expected_counts, "support-bin quota")
    need(all(bin_index == index * 257 // N for bin_index, index in zip(bins, indices)), "global support-bin formula")
    need(rows == sorted(rows, key=lambda row: (int(row["support_bin"]), int(row["record_index"]), int(row["p1"]), int(row["t1"]), int(row["p2"]))), "candidate natural order")
    with INPUT.open("rb") as stream:
        header = stream.read(16)
        need(header[:8] == b"K16DIR1\0" and struct.unpack_from("<Q", header, 8)[0] == N, "checkpoint header")
        for row in rows:
            index = int(row["record_index"])
            source_row, coefficient = input_record(stream, index)
            need(row["source_row"] == source_row, "candidate source row")
            need(int(row["coefficient"]) == coefficient, "candidate coefficient")
            m1, m2 = int(row["m1"]), int(row["m2"])
            denominator = m1 * m2
            need(denominator > 0 and U % denominator == 0, "candidate exact U division")
            unit = U // denominator
            q = int(row["terminal_q"])
            contribution = int(row["nonzero_contribution_scaled_U"])
            need(q != 0, "zero candidate")
            need(int(row["unit_scaled_U"]) == unit, "candidate unit")
            need(contribution == coefficient * unit * q, "candidate contribution")
            need(int(row["final_degree"]) == 4, "candidate final degree")
    return expected_counts


def main():
    hashes = {}
    for name, (path, expected) in PINS.items():
        got = sha(path)
        need(got == expected, f"pin mismatch {name}: {got}")
        hashes[name] = got

    failure = json.loads(PINS["failure_evidence"][0].read_text())
    need(failure["status"] == "REJECT_NO_RESULT_K24_GROUPED_D16_R44_FULL_SAMPLE_GUARD", "failure status")
    need(failure["launch"]["exit_code"] == 101, "failed exit code")
    need(failure["failure"]["observed_left"] == 37 and failure["failure"]["required_right"] == 257, "failure assertion")
    need(failure["failure"]["phase"].endswith("before any result/sample write"), "failure phase")
    need(failure["atomic_output_audit"] == {
        "complete_json_present": False,
        "complete_sample_ledger_present": False,
        "matching_tmp_present": False,
        "scalar_claim_accepted": False,
    }, "failure atomic audit")
    absent = [str(path.relative_to(ROOT)) for path in TARGETS if not path.exists()]
    need(len(absent) == len(TARGETS), "failed attempt left an output/temp/validation artifact")

    candidate_marker = b"k24_k16_r44_support_candidates.tsv"
    failed_binary_has_marker = candidate_marker in PINS["failed_binary"][0].read_bytes()
    candidate_binary_has_marker = candidate_marker in PINS["candidate_aware_binary"][0].read_bytes()
    source_has_marker = b"k24_k16_r44_support_candidates.tsv" in PINS["candidate_aware_source"][0].read_bytes()
    need(not failed_binary_has_marker and source_has_marker and candidate_binary_has_marker, "failed/repaired executable provenance distinction")

    with PINS["support_candidates"][0].open(newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        need(reader.fieldnames == HEADER, "candidate header")
        candidates = list(reader)
    quotas = validate_candidates(candidates)

    census = json.loads(PINS["support_census"][0].read_text())
    need(census["status"] == "PASS_K24_K16_R44_READ_ONLY_SUPPORT_CENSUS", "census status")
    need(census["candidate_count"] == 257 and census["realized_support_bins"] == list(range(37)), "census coverage")
    need({int(k): v for k, v in census["quota_by_bin"].items()} == quotas, "census quotas")
    replay = json.loads(PINS["independent_literal_rerun"][0].read_text())
    need(replay["status"] == "PASS_INDEPENDENT_K24_LITERAL_REPLAY", "literal replay status")
    need(replay["family"] == "k16r44candidates" and replay["witnesses_replayed"] == replay["distinct_group_bins"] == 257, "literal replay coverage")
    need(replay["scalar_shard_rerun"] is False, "literal replay traversed scalar shard")

    old = json.loads(PINS["old_prefix"][0].read_text())
    repaired = json.loads(PINS["candidate_prefix"][0].read_text())
    mismatches = [field for field in SCALAR_FIELDS if old[field] != repaired[field]]
    need(not mismatches, "sample repair changed scalar prefix fields: " + repr(mismatches))

    contract = json.loads(PINS["contract"][0].read_text())
    need(contract["deterministic_selection"]["candidate_count"] == 257, "contract candidate count")
    need(contract["deterministic_selection"]["quota_by_bin"] == {str(k): v for k, v in quotas.items()}, "contract quotas")
    need(contract["full_traversal_certificate"]["required"] is True, "contract lacks full support certificate")
    need(contract["production_relaunch_authorized"] is False, "contract authorizes production")

    output = {
        "status": "PASS_INDEPENDENT_K16_R44_FAILURE_AUDIT_AND_SUPPORT_CONTRACT",
        "failed_attempt": {
            "exit_code": 101,
            "observed_support_bins": 37,
            "accepted_scalar": False,
            "all_target_result_sample_temp_validation_paths_absent": True,
            "absent_paths": absent,
        },
        "provenance_separation": "failed source/binary pins are 1ed9ef.../3a1b5e...; repaired candidate-aware source/binary pins are ca1874.../2d4111...; the failed binary lacks and the repaired pair contains the candidate-manifest marker",
        "support_contract": {
            "candidates": 257,
            "certified_bins": list(range(37)),
            "quota": "7 in bins 0..34; 6 in bins 35..36",
            "candidate_ledger_arithmetic_and_checkpoint_rows": "PASS",
            "independent_literal_terminal_replays": 257,
            "old_vs_candidate_aware_262144_distributed_scalar_fields_equal": True,
            "full_support_histogram_required_before_relaunch": True,
            "current_candidate_aware_engine_emits_full_support_histogram": False,
            "production_relaunch_authorized": False,
        },
        "pins": hashes,
        "heavy_or_full_run_launched_by_audit": False,
    }
    text = json.dumps(output, indent=2, sort_keys=True) + "\n"
    (HERE / "results_k16_r44_failure_support_audit.json").write_text(text)
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
