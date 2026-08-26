#!/usr/bin/env python3
"""Independent exact validation for K23 D14 source-three shard [0,243)."""

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULT = HERE / "results_shard0.json"
SAMPLES = HERE / "results_shard0.json.samples.tsv"
REFEREE = HERE / "results_shard0_literal_referee.json"
U = 400_591_699_200
START, END = 0, 243
IDS = ["D14:222|R:3-2-4", "D14:222|R:3-3-3", "D14:222|R:4-2-3"]
DEGREES = [(3, 2, 4, 60), (3, 3, 3, 32), (4, 2, 3, 32)]
PINS = {
    RESULT: "def0a170451b52294e3df852d0911eda824c22dfbf1903534e0f316960fbdf4b",
    SAMPLES: "1c3c2d59f3ccec85c27bb9dfc5edea362f2f7286fc6589c93de0ddb3a5166076",
    REFEREE: "7fad67c93686d7167a736887d726a1b93f5d222cabc888f6f0ccf44149da06a3",
    HERE / "run_k23_d14_source_three.rs": "32a23e26bced387be2ce348b1bb41de126f5f17e2f5ee2adeccc9320d69f116b",
    HERE / "run_k23_d14_source_three": "5ecb715d1861280495d92a9d970b4c50db6cc32ba78577ecbc97a5837b66373f",
    HERE / "referee_k23_d14_source_three_literals.rs": "64bc0cd19c859f57a9fb01c6a8a66a54a4d798de6dc524e1459b5015395bd6d4",
    HERE / "referee_k23_d14_source_three_literals": "8ea90ad3caa491833ad214a2df2d5a17367addc6b78353be25b200e84eb199b6",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def weighted(histogram: dict, power: int = 1) -> int:
    return sum((int(key) ** power) * value for key, value in histogram.items())


def main() -> None:
    for path, digest in PINS.items():
        assert sha(path) == digest, path
    input_pins = load(HERE / "input_pins.json")
    for entry in input_pins.values():
        assert sha(ROOT / entry["path"]) == entry["sha256"], entry["path"]

    physical = ROOT / input_pins["physical_source"]["path"]
    raw = physical.read_bytes()
    assert raw[:11] == b"K16DIRECT1\0"
    nt = int.from_bytes(raw[11:15], "little")
    nr = int.from_bytes(raw[15:19], "little")
    np = int.from_bytes(raw[19:23], "little")
    na = int.from_bytes(raw[23:27], "little")
    assert (nt, nr, np, na) == (384, 485, 78, 12)
    offset = 27 + 12 + nt * (252 + 12)
    masses = []
    for index in range(nr):
        record = raw[offset + 24 * index: offset + 24 * (index + 1)]
        size = int.from_bytes(record[12:16], "little")
        coefficient = int.from_bytes(record[16:24], "little", signed=True)
        masses.append(size * coefficient)

    result = load(RESULT)
    assert result["status"] == "PASS_BOUNDED_D14_222_K23_SOURCE_THREE_EVALUATOR"
    assert result["covered_lineage_ids"] == IDS and int(result["scale_U"]) == U
    assert result["R8_record_interval"] == [START, END] and not result["distributed_record_mode"]
    assert result["R8_records_consumed"] == END - START and result["R8_records_declared"] == 485
    assert result["source_heads"] == (END - START) * 1728 == 419_904
    assert int(result["source_mass_sum"]) == sum(masses[START:END]) * 1728
    assert int(result["source_mass_l1"]) == sum(abs(value) for value in masses[START:END]) * 1728
    assert result["all_realized_cached_K23_responses_terminal"] is True
    assert result["terminal_cache_resource_guard"]["hard_cap_keys_per_worker"] == 3_000_000
    assert result["terminal_cache_resource_guard"]["peak_keys_per_worker"] <= 3_000_000
    assert result["workers"] == 8 and result["elapsed_seconds"] < 600
    assert result["sign_rule"] == "direct D14 coefficient=-M; three normalized response flips give terminal +M/(m1*m2*m3), implemented as source_mass*U/(m1*m2*m3)"

    structural = {}
    for lineage, (d1, d2, d3, terminal_tails) in zip(IDS, DEGREES, strict=True):
        sink = result["sinks"][lineage]
        assert (sink["first_response_degree"], sink["second_response_degree"], sink["terminal_response_degree"]) == (d1, d2, d3)
        assert sink["first_children"] == {2:12, 3:32, 4:60}[d1] * sink["selected_p1_uses"]
        assert sink["second_children"] == {2:12, 3:32, 4:60}[d2] * sink["selected_p2_uses"]
        assert sink["K23_terminal_occurrences"] == terminal_tails * sink["selected_p3_uses"]
        assert sink["full_occurrences"] == sink["irreducible_occurrences"] == sink["K23_terminal_occurrences"]
        assert sink["full_charge_scaled_U"] == sink["irreducible_charge_scaled_U"]
        h1, h2, h3, hp = (sink[field] for field in (
            "first_denominator_hist", "second_denominator_hist",
            "third_denominator_hist", "product_denominator_hist",
        ))
        assert sum(h1.values()) == result["source_heads"]
        assert weighted(h1) == sink["selected_p1_uses"]
        assert sum(h2.values()) == sink["pivotable_first_children"]
        assert weighted(h2) == sink["selected_p2_uses"]
        assert sum(h3.values()) == sink["pivotable_second_children"]
        assert weighted(h3) == sink["selected_p3_uses"]
        assert sum(hp.values()) == sink["pivotable_second_children"]
        assert all(int(key) > 0 and U % int(key) == 0 and value > 0 for key, value in hp.items())
        assert sink["plan_cache"]["first_hits"] + sink["plan_cache"]["first_misses"] == sink["selected_p1_uses"]
        assert sink["plan_cache"]["second_hits"] + sink["plan_cache"]["second_misses"] == sink["selected_p2_uses"]
        assert sink["literal_preterminal_cache"]["hits"] + sink["literal_preterminal_cache"]["misses"] == sink["pivotable_second_children"]
        assert sink["terminal_profile_cache"]["hard_cap_keys_per_worker"] == 3_000_000
        assert sink["terminal_profile_cache"]["misses"] <= 3_000_000 * (sink["terminal_profile_cache"]["clears_at_hard_cap"] + 8)
        assert sink["literal_samples"] == 129
        structural[lineage] = {
            "selected_p1_uses": sink["selected_p1_uses"],
            "selected_p2_uses": sink["selected_p2_uses"],
            "selected_p3_uses": sink["selected_p3_uses"],
            "terminal_K23_occurrences": sink["K23_terminal_occurrences"],
            "full_charge_scaled_U": sink["full_charge_scaled_U"],
            "denominator_product_bins": len(hp),
            "all_products_divide_U": True,
        }

    sample_lines = SAMPLES.read_text().splitlines()
    assert len(sample_lines) == 388
    counts = {lineage: 0 for lineage in IDS}
    bins = {lineage: [] for lineage in IDS}
    for line in sample_lines[1:]:
        cols = line.split("\t")
        assert len(cols) == 28 and cols[0] in counts
        counts[cols[0]] += 1
        bins[cols[0]].append(int(cols[1]))
        head = int(cols[2])
        assert int(cols[1]) == head * 257 // (485 * 1728)
        assert int(cols[3]) == head // 1728 and START <= int(cols[3]) < END
        assert U % (int(cols[20]) * int(cols[21]) * int(cols[22])) == 0
    assert list(counts.values()) == [129, 129, 129]
    assert all(values == list(range(129)) for values in bins.values())
    assert result["literal_sample_guard"]["records"] == 387
    assert result["literal_sample_guard"]["records_per_sink"] == [129, 129, 129]

    referee = load(REFEREE)
    assert referee["status"] == "PASS_INDEPENDENT_K23_D14_SOURCE_THREE_LITERAL_REFEREE"
    assert referee["samples"] == 387 and referee["samples_per_sink"] == [129, 129, 129]
    assert referee["literal_terminal_children_checked"] == 92_864_640
    assert referee["witness_terminal_children_checked"] == 15_996
    for field in (
        "source_heads_reconstructed_from_frozen_R8", "all_literal_path_counts_and_charges_equal",
        "all_U_divisions_exact", "all_terminal_K23_children_nonpivotable",
        "all_abstract_literal_cycle_keys_equal",
    ):
        assert referee[field] is True

    payload = {
        "status": "PASS_INDEPENDENT_K23_D14_SOURCE_THREE_SHARD0_VALIDATION",
        "degree": 23,
        "strict_ids": IDS,
        "interval": [START, END],
        "records": END - START,
        "source_heads": result["source_heads"],
        "input_pins": {key: {"path": value["path"], "sha256": value["sha256"]} for key, value in input_pins.items()},
        "producer": {"source_sha256": sha(HERE / "run_k23_d14_source_three.rs"), "binary_sha256": sha(HERE / "run_k23_d14_source_three")},
        "result": {"sha256": sha(RESULT), "samples_sha256": sha(SAMPLES), "elapsed_seconds": result["elapsed_seconds"], "structural": structural},
        "guards": {
            "source_mass_independently_reparsed": True,
            "count_and_tail_ratios_exact": True,
            "denominator_histogram_sums_and_weighted_sums_exact": True,
            "all_product_denominators_divide_U": True,
            "three_flip_sign_rule_exact": True,
            "terminal_cache_caps_respected": True,
            "full_equals_irreducible": True,
        },
        "literal_referee": {
            "source_sha256": sha(HERE / "referee_k23_d14_source_three_literals.rs"),
            "binary_sha256": sha(HERE / "referee_k23_d14_source_three_literals"),
            "result_sha256": sha(REFEREE),
            "source_head_replays": 387,
            "full_literal_terminal_children_checked": referee["literal_terminal_children_checked"],
            "witness_terminal_children_checked": referee["witness_terminal_children_checked"],
            "bins_per_sink": [129, 129, 129],
        },
        "scope": "independent shard0 validation only; no scalar rerun, shard1 launch, aggregate merge, K24, membership, or conjecture claim",
    }
    logical = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    payload["logical_sha256"] = logical
    output = HERE / "results_shard0_validation.json"
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(json.dumps({"status": payload["status"], "logical_sha256": logical}, indent=2))


if __name__ == "__main__":
    main()
