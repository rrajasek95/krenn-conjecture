#!/usr/bin/env python3
"""Fail-closed structural and literal-referee validation for hidden-decorated shard 0."""

import hashlib
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/hidden_k16_decorated_pair_orbits_full.bin"
RESULT = HERE / "results_shard0.json"
SAMPLES = HERE / "results_shard0.json.samples.tsv"
REFEREE = HERE / "results_shard0_literal_referee.json"
U = 400_591_699_200
N = 101_545_723
HEADER = 80
RECORD = 53
START = 0
END = 33_848_574
SOURCE_SHA = "22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8"
PINS = {
    RESULT: "1e2cdfc9df0662a96f74b130910f35a0b74e18b2ad942a4de08c82086a2236a9",
    SAMPLES: "65609aecef0feba6d219580972c27c66f25ddcba031a6f2ada0b627372ea0219",
    REFEREE: "0f60e83463049cfbeafb8bb98526347b5cc9de34c6b6107acc4314bfec267069",
    HERE / "referee_k23_hidden_decorated_pair_literals.rs": "08b1c9494e85db6d23f973bd892c1635abd305f1cbf93acfd6692491ee6bbedc",
    HERE / "referee_k23_hidden_decorated_pair_literals": "20ef2854d3d40d6151b5c16af2911a2cc286465092914eb83182e0639b959148",
    HERE / "k23_hidden_decorated_pair_impl.rs": "ebb79e9dcd7ee76dcbee224355668ce62bc386c6eb68bb748e36d9871ae4afac",
    HERE / "run_k23_hidden_decorated_pair.rs": "b761c7c235a65f633c0ce884261934e422a2ed9fad129d6c949f0177d3d2a607",
}
IDS = ["D14:222|R:2-3-4", "D14:222|R:2-4-3"]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> None:
    assert SOURCE.stat().st_size == HEADER + RECORD * N == 5_381_923_399
    assert sha(SOURCE) == SOURCE_SHA
    with SOURCE.open("rb") as handle:
        header = handle.read(HEADER)
    assert header[:8] == b"H16ORM1\0"
    assert int.from_bytes(header[8:24], "little", signed=True) == U
    assert header[24:28] == b"\0" * 4
    assert int.from_bytes(header[28:30], "little") == RECORD
    assert header[30:32] == b"\0" * 2
    assert int.from_bytes(header[32:40], "little") == 246
    assert int.from_bytes(header[40:48], "little") == 305
    assert int.from_bytes(header[48:56], "little") == N
    assert header[56:64] == b"\0" * 8
    assert int.from_bytes(header[64:80], "little", signed=True) == 146_230_609_431_055_564_800
    for path, digest in PINS.items():
        assert sha(path) == digest, path

    result = load(RESULT)
    assert result["status"] == "PASS_BOUNDED_K23_HIDDEN_DECORATED_PAIR_TWO_SINK"
    assert result["covered_lineage_ids"] == IDS
    assert int(result["scale_U"]) == U
    assert result["input_sha256_expected"] == SOURCE_SHA
    assert result["input_records_declared"] == N
    assert result["input_interval"] == [START, END]
    assert result["input_records_consumed"] == END - START
    assert sum(result["stabilizer_histogram"].values()) == END - START
    assert all(384 % int(stabilizer) == 0 for stabilizer in result["stabilizer_histogram"])

    structural = {}
    for lineage, first_count, terminal_count in ((IDS[0], 32, 60), (IDS[1], 60, 32)):
        sink = result["sinks"][lineage]
        assert sink["first_tail_evaluations"] == first_count * (END - START)
        assert sink["terminal_K23_occurrences"] == terminal_count * sink["selected_p3"]
        assert sink["full_occurrences"] == sink["irreducible_occurrences"] == sink["terminal_K23_occurrences"]
        assert sink["cache"]["hits"] + sink["cache"]["misses"] == sink["selected_p3"]
        assert int(sink["normalized_p3_weight_scaled"]) == -int(sink["pivotable_weight_scaled"])
        assert int(sink["terminal_weight_scaled"]) == terminal_count * int(sink["normalized_p3_weight_scaled"])
        assert sink["full_charge_scaled"] == sink["irreducible_charge_scaled"]
        histogram = sink["m2_m3_histogram"]
        parsed = [(tuple(map(int, key.split("_"))), value) for key, value in histogram.items()]
        assert all(m2 > 0 and m3 > 0 and U % (m2 * m3) == 0 and value > 0 for (m2, m3), value in parsed)
        assert sum(value for _, value in parsed) == sink["pivotable_intermediate_children"]
        assert sum(m3 * value for (_, m3), value in parsed) == sink["selected_p3"]
        structural[lineage] = {
            "first_tail_ratio": first_count,
            "terminal_tail_ratio": terminal_count,
            "pivotable_intermediate_children": sink["pivotable_intermediate_children"],
            "selected_p3": sink["selected_p3"],
            "terminal_K23_occurrences": sink["terminal_K23_occurrences"],
            "divisor_bins": len(histogram),
            "divisor_histogram_sum": sum(histogram.values()),
            "divisor_histogram_m3_weighted_sum": sum(m3 * value for (_, m3), value in parsed),
            "full_charge_scaled_U": sink["full_charge_scaled"],
        }

    lines = SAMPLES.read_text().splitlines()
    assert len(lines) == 258
    rows = [line.split("\t") for line in lines[1:]]
    assert all(len(row) == 21 for row in rows)
    expected_indices = [START + ordinal * (END - START - 1) // 256 for ordinal in range(257)]
    assert [int(row[0]) for row in rows] == expected_indices
    assert len(set(expected_indices)) == 257
    nonzero34 = sum(int(row[19]) for row in rows)
    nonzero43 = sum(int(row[20]) for row in rows)
    terminal34 = sum(int(row[10]) for row in rows)
    terminal43 = sum(int(row[16]) for row in rows)
    assert (nonzero34, nonzero43, terminal34, terminal43) == (220, 128, 515_520, 245_760)
    assert all(int(row[7]) == 32 and int(row[10]) == 60 * int(row[9]) for row in rows)
    assert all(int(row[13]) == 60 and int(row[16]) == 32 * int(row[15]) for row in rows)

    referee = load(REFEREE)
    assert referee["status"] == "PASS_INDEPENDENT_K23_HIDDEN_DECORATED_PAIR_LITERAL_REPLAY"
    assert referee["input_interval"] == [START, END]
    assert (referee["samples"], referee["R234_nonzero"], referee["R243_nonzero"]) == (257, nonzero34, nonzero43)
    assert referee["source_sha256_expected"] == SOURCE_SHA
    for field in (
        "source_header_checked",
        "all_source_fields_exact",
        "all_occurrencewise_U_and_weight_divisions_exact",
        "all_literal_terminal_K23_children_nonpivotable",
        "all_abstract_literal_cycle_keys_and_charges_equal",
    ):
        assert referee[field] is True
    assert referee["sign_rule"] == "w3=-w2/m3"

    payload = {
        "status": "PASS_INDEPENDENT_K23_HIDDEN_DECORATED_PAIR_SHARD0_VALIDATION",
        "degree": 23,
        "strict_ids": IDS,
        "source": {
            "path": str(SOURCE.relative_to(ROOT)),
            "sha256": SOURCE_SHA,
            "bytes": SOURCE.stat().st_size,
            "records": N,
            "header_bytes": HEADER,
            "record_bytes": RECORD,
            "header_all_fields_checked": True,
        },
        "shard": {
            "interval": [START, END],
            "records": END - START,
            "result_sha256": sha(RESULT),
            "samples_sha256": sha(SAMPLES),
            "elapsed_seconds": result["elapsed_seconds"],
            "structural_counts_and_ratios": structural,
            "sign": "w3=-w2/m3",
            "all_histogram_m2_m3_divide_U": True,
            "histogram_exact_sum_and_m3_weighted_sum": True,
            "full_equals_irreducible": True,
        },
        "literal_referee": {
            "source_sha256": sha(HERE / "referee_k23_hidden_decorated_pair_literals.rs"),
            "binary_sha256": sha(HERE / "referee_k23_hidden_decorated_pair_literals"),
            "result_sha256": sha(REFEREE),
            "compile_cfg": ["feature=full_hidden_charge", "feature=hidden_child_prefix"],
            "samples": 257,
            "R234_nonzero": nonzero34,
            "R243_nonzero": nonzero43,
            "R234_terminal_children_literally_checked": terminal34,
            "R243_terminal_children_literally_checked": terminal43,
            "all_source_rows_and_fields_seek_replayed": True,
            "all_terminal_children_nonpivotable": True,
            "all_abstract_literal_keys_and_charges_equal": True,
        },
        "scope": "independent validation of hidden-decorated shard0 only; no scalar rerun, aggregate merge, other interval, K24, membership, or conjecture claim",
    }
    logical = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    payload["logical_sha256"] = logical
    output = HERE / "results_shard0_validation.json"
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(json.dumps({"status": payload["status"], "logical_sha256": logical, "literal_terminal_children": terminal34 + terminal43}, indent=2))


if __name__ == "__main__":
    main()
