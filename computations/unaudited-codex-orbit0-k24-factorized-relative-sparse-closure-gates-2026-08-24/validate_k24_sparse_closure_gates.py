#!/usr/bin/env python3
"""Fail-closed referee for bounded K24 sparse and arbitrary-word closure gates."""
import copy
import hashlib
import json
import math
import os
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
INITIAL_DIR = HERE / "gate_run"
INITIAL = INITIAL_DIR / "results_k24_sparse_257_and_source1_gate.json"
COLUMNS = INITIAL_DIR / "sample257_columns.tsv"
EDGES = INITIAL_DIR / "sample257_sparse_gram_edges.tsv"
ASSEMBLY = HERE / "results_sample257_relative_gram_equivalence.json"
LAYER_DIR = HERE / "layered_gate_run_attempt6"
LAYERED = LAYER_DIR / "results_k24_arbitrary_word_layered_closure_gate.json"
ONE_PROBE = HERE / "results_one_K20_row_ambient_incidence.json"
WITNESS = ROOT / "computations/unaudited-codex-orbit0-k24-factorized-direct-d17-d18-producer-2026-08-24/prefix1_fast/literal_witnesses.tsv"
D17 = ROOT / "computations/unaudited-codex-orbit0-k24-factorized-direct-d17-d18-producer-2026-08-24/prefix1_fast/compact/source_D17_R3_4/final.bin"
D18 = ROOT / "computations/unaudited-codex-orbit0-k24-factorized-direct-d17-d18-producer-2026-08-24/prefix1_fast/compact/source_D18_R2_4/final.bin"
PINS = {
    WITNESS: "477b9ae9249b72d2e1c9ba4c71fd5b63605866ce533c6c79eb199b8103dd001c",
    D17: "cf4843d1ffc826c361e16540b33c3bd4bdf52be51c2a24f54a6d9182a7cc6a69",
    D18: "85fbfab465a7c007e6a3222e251c076c05457f86da421a0cb70251fe270f5fd1",
    ROOT / "computations/unaudited-codex-orbit0-k24-factorized-relative-production-gate-2026-08-24/k24_factorized_B20_provider.py": "689499ecf501eb37879b41f05e3f3caecfad454eaf57f5586b28edd7c616a018",
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    lines = path.read_text().splitlines()
    need(lines[0] == "K_degree\tnatural_row_hex", f"row header {path.name}")
    records = [(int(line.split("\t")[0]), line.split("\t")[1]) for line in lines[1:]]
    need(len(records) == len(set(records)), f"row dedup {path.name}")
    need([value for _degree, value in records] == sorted(value for _degree, value in records), f"row natural order {path.name}")
    return records


def columns(path):
    lines = path.read_text().splitlines()
    need(lines[0] == "natural_column_key\torbit_size\tfrozen_78_source_word", f"column header {path.name}")
    records = [line.split("\t") for line in lines[1:]]
    keys = [item[0] for item in records]
    need(keys == sorted(keys) and len(keys) == len(set(keys)), f"column natural dedup {path.name}")
    need(all(int(item[1]) > 0 and 384 % int(item[1]) == 0 and item[2] in ("0", "1") for item in records), f"column guards {path.name}")
    return records


def validate_initial(initial, assembly):
    need(initial["status"] == "PASS_BOUNDED_K24_SPARSE_CLOSURE_GATES_NO_LAUNCH", "initial status")
    sample = initial["sample257"]
    need(sample["input_records"] == sample["natural_unique_columns"] == 257, "sample census")
    need(sample["events_by_degree"] == {"20": 98688, "22": 1184256, "23": 3158016, "24": 5921280}, "sample events")
    need(sample["unique_labelled_rows_by_degree"] == sample["events_by_degree"], "sample row collision census")
    need(sample["nonzero_upper_edges_any"] == sample["nonzero_upper_edges_lower"] == sample["nonzero_upper_edges_top"] == 257, "sample sparse E")
    need(sample["dense_upper_pairs"] == 33153 and sample["natural_order_dedup_exact"], "sample dense comparison")
    source = initial["one_source_unit"]
    need(source["premerge_records"] == 2165760 and source["natural_union_columns"] == source["retained_nonzero_columns_N"] == 2042880, "source N")
    need(source["cross_group_duplicate_keys"] == 122880 and source["exact_zero_sums"] == 0, "source merge")
    need(source["closure_status"] == "COLUMN_CAP_BEFORE_INCIDENCE" and source["column_cap"] == 1000000, "source cap")
    need(source["queued_columns"] == source["known_nonzero_self_edges_lower_bound_E"] == 2042880, "source E lower bound")
    need(source["lower_transfer_below_K20_complete"] is False, "source incomplete lower")
    need(assembly["status"] == "PASS_EXACT_K24_SAMPLE257_KERNEL_RELATIVE_FULL_GRAM_EQUIVALENCE", "assembly status")
    need(assembly["lower_rank"] == 257 and assembly["lower_nullity"] == assembly["relative_gram_dimension"] == 0, "assembly kernel")
    need(assembly["kernel_and_full_gram_routes_agree"] and assembly["exact_positive_norm_gap"] == "8508187607040/343", "assembly equivalence")
    need(assembly["global_verdict"] == "INCONCLUSIVE_INCOMPLETE_CLOSURE", "assembly global guard")


def validate_layered(layered):
    need(layered["status"] == "PASS_BOUNDED_K24_ARBITRARY_WORD_LAYERED_CLOSURE_NO_LAUNCH", "layered status")
    need(layered["caps"] == {"column_layer": 257, "global_columns": 1000000, "global_rows": 1000000, "row_layer": 257}, "frozen caps")
    one = layered["one_K20_row_gate"]
    need(one["layer1_row_to_column"]["unique_columns"] == one["layer1_row_to_column"]["unique_incidence_edges_E"] == 56, "one row layer1")
    need(one["layer2_column_to_row"]["unique_columns"] == 56 and one["layer2_column_to_row"]["unique_rows"] == 5077 and one["layer2_column_to_row"]["unique_incidence_edges_E"] == 5880, "one row layer2")
    need(one["layer3_row_to_column_prefix"]["unique_rows"] == 257 and one["layer3_row_to_column_prefix"]["unique_columns"] == 14852 and one["layer3_row_to_column_prefix"]["unique_incidence_edges_E"] == 16391, "one row layer3 prefix")
    need(one["closure_status"] == "ROW_LAYER_CAP_257_NOT_COMPLETE", "one row cap")
    distributed = layered["distributed257_gate"]
    need(distributed["lower_seed_rows"] == distributed["target_seed_rows"] == 257, "distributed seeds")
    need(distributed["lower_row_to_column"]["unique_columns"] == 18898 and distributed["target_row_to_column"]["unique_columns"] == 21720, "distributed row expansion")
    need(distributed["combined_unique_columns"] == 40361 and distributed["processed_columns"] == 257 and distributed["queued_columns"] == 40104, "distributed queue")
    forward = distributed["column_to_row_prefix"]
    need(forward["unique_rows"] == 26752 and forward["unique_incidence_edges_E"] == 26985 and forward["layer_cap_reached"], "distributed forward prefix")
    need(distributed["closure_status"] == "COLUMN_LAYER_CAP_257_NOT_COMPLETE", "distributed cap")
    words = layered["word_tables"]
    need(words["on_demand_tables_materialized"] == 83 and words["arbitrary_non_frozen_word_tables_realized"] == 75, "word tables")
    need(words["frozen_78_source_dictionary_is_closure_complete"] is False and words["hostile_restricted_word_domain_rejected"], "word-domain correction")
    need(layered["lower_transfer_below_K20_complete"] is False and layered["global_verdict"] == "INCONCLUSIVE_INCOMPLETE_LAYERED_CLOSURE", "layered global guard")
    for name, descriptor in layered["artifacts_before_result"].items():
        path = LAYER_DIR / name
        need(path.is_file() and path.stat().st_size == descriptor["bytes"] and sha(path) == descriptor["sha256"], f"layer artifact {name}")
    one_hist = Counter(degree for degree, _row in rows(LAYER_DIR / "one_lower_layer2_rows.tsv"))
    distributed_hist = Counter(degree for degree, _row in rows(LAYER_DIR / "distributed257_layer2_rows_prefix.tsv"))
    need(one_hist == {16: 2, 17: 5, 18: 69, 19: 495, 20: 2530, 21: 1354, 22: 530, 23: 32, 24: 60}, "one-row degree histogram")
    need(distributed_hist == {17: 67, 18: 445, 19: 2295, 20: 6020, 21: 4060, 22: 2840, 23: 3382, 24: 7643}, "distributed degree histogram")
    need(set(range(16, 25)) <= set(one_hist | distributed_hist), "ambient blocks K16 through K24")
    lower_columns = columns(LAYER_DIR / "distributed257_lower_layer1_columns.tsv")
    need(Counter(item[2] for item in lower_columns) == {"0": 16954, "1": 1944}, "restricted-word hostile census")
    return one_hist, distributed_hist


def hostile_self_test(layered):
    rejected = 0
    mutations = []
    bad = copy.deepcopy(layered); bad["lower_transfer_below_K20_complete"] = True; mutations.append(bad)
    bad = copy.deepcopy(layered); bad["distributed257_gate"]["closure_status"] = "COMPLETE"; mutations.append(bad)
    bad = copy.deepcopy(layered); bad["word_tables"]["frozen_78_source_dictionary_is_closure_complete"] = True; mutations.append(bad)
    bad = copy.deepcopy(layered); bad["caps"]["global_columns"] = 2000000; mutations.append(bad)
    bad = copy.deepcopy(layered); bad["global_verdict"] = "NONMEMBER"; mutations.append(bad)
    bad = copy.deepcopy(layered); bad["distributed257_gate"]["queued_columns"] = 0; mutations.append(bad)
    for bad in mutations:
        try:
            validate_layered(bad)
        except ValueError:
            rejected += 1
        else:
            need(False, "hostile mutation accepted")
    need(rejected == 6, "hostile mutation count")
    return rejected


def main():
    for path, digest in PINS.items():
        need(path.is_file() and sha(path) == digest, f"pin {path}")
    initial = json.loads(INITIAL.read_text())
    assembly = json.loads(ASSEMBLY.read_text())
    layered = json.loads(LAYERED.read_text())
    probe = json.loads(ONE_PROBE.read_text())
    validate_initial(initial, assembly)
    one_hist, distributed_hist = validate_layered(layered)
    need(probe["natural_incident_column_orbits_N"] == 56 and probe["incident_orbits_outside_frozen_78_source_word_dictionary"] == 48, "independent one-row probe")
    rejected = hostile_self_test(layered)
    forward = layered["distributed257_gate"]["column_to_row_prefix"]
    total_columns = layered["distributed257_gate"]["combined_unique_columns"]
    shard_columns = 2048
    projections = {
        "full_40361_columns_wall_seconds_linear": forward["elapsed_seconds"] * total_columns / 257,
        "full_40361_columns_rows_linear": math.ceil(forward["unique_rows"] * total_columns / 257),
        "full_40361_columns_edges_linear": math.ceil(forward["unique_incidence_edges_E"] * total_columns / 257),
        "next_bounded_shard_columns": shard_columns,
        "next_bounded_shard_wall_seconds_linear": forward["elapsed_seconds"] * shard_columns / 257,
        "next_bounded_shard_peak_rss_bytes_conservative_linear": math.ceil(layered["resources"]["peak_rss_bytes"] * shard_columns / 257),
        "next_bounded_shard_rows_linear": math.ceil(forward["unique_rows"] * shard_columns / 257),
        "next_bounded_shard_edges_linear": math.ceil(forward["unique_incidence_edges_E"] * shard_columns / 257),
        "one_source_unit_minimum_2048_column_seed_tiles": math.ceil(initial["one_source_unit"]["retained_nonzero_columns_N"] / shard_columns),
    }
    need(projections["full_40361_columns_wall_seconds_linear"] > 4 * 540 and projections["full_40361_columns_rows_linear"] > 4 * 1000000, "no-launch projection")
    need(projections["next_bounded_shard_wall_seconds_linear"] < 450 and projections["next_bounded_shard_peak_rss_bytes_conservative_linear"] < 8 * 1024**3 and projections["next_bounded_shard_rows_linear"] < 1000000, "next bounded shard")
    audit = {
        "status": "PASS_INDEPENDENT_K24_SPARSE_CLOSURE_GATES_NO_LAUNCH",
        "sample257_N": 257,
        "sample257_nonzero_gram_edges_E": 257,
        "sample257_lower_rank": 257,
        "sample257_lower_nullity": 0,
        "kernel_and_full_gram_routes_agree": True,
        "one_source_unit_N": 2042880,
        "one_source_unit_E_lower_bound": 2042880,
        "one_source_unit_status": "COLUMN_CAP_BEFORE_INCIDENCE",
        "one_row_layer_known_N_columns": layered["one_K20_row_gate"]["known_unique_columns"],
        "one_row_layer_known_N_rows": layered["one_K20_row_gate"]["known_unique_rows"],
        "one_row_layer_known_E": layered["one_K20_row_gate"]["known_unique_bipartite_edges_E"],
        "distributed_combined_columns": total_columns,
        "distributed_queued_columns": layered["distributed257_gate"]["queued_columns"],
        "ambient_output_degree_histogram_one_row": {str(k): v for k, v in sorted(one_hist.items())},
        "ambient_output_degree_histogram_distributed_prefix": {str(k): v for k, v in sorted(distributed_hist.items())},
        "global_lower_operator": "P_<24 B on every realized lower K block; the special K20/K22/K23-only lower Gram is not ambiently complete",
        "arbitrary_word_tables_required": True,
        "hostile_mutations_rejected": rejected,
        "peak_rss_bytes": layered["resources"]["peak_rss_bytes"],
        "retained_layer_bytes": layered["resources"]["retained_bytes"],
        "projections": projections,
        "launch_decision": "NO_LAUNCH_103_SHARDS_OR_FULL_RELATIVE_CLOSURE",
        "next_authorized_action": "at most one 2048-column arbitrary-word bounded closure tile after resource clearance; merge is not a completeness claim",
        "production_launched": False,
        "global_verdict": "INCONCLUSIVE_INCOMPLETE_LOWER_TRANSFER",
    }
    output = HERE / "results_k24_sparse_closure_gates_audit.json"
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps(audit, sort_keys=True))


if __name__ == "__main__":
    main()
