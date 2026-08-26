#!/usr/bin/env python3
"""Independent fail-closed referee for the bounded factorized B20 gate/plan."""
import copy
import hashlib
import importlib.util
import json
import os
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROVIDER = HERE / "k24_factorized_B20_provider.py"
RESULT = HERE / "results_factorized_B20_one_column.json"
ASSEMBLY = HERE / "results_factorized_relative_gram_one_column.json"
SCHEMA = HERE / "factorized_B20_relative_interface.schema.json"
PLAN = HERE / "k24_factorized_35_shard_plan_held.json"
VECTOR = ROOT / "computations/unaudited-codex-orbit0-k24-relative-column-interface-gate-2026-08-24/prefix_control_full_vector.tsv"
CONTRACT = ROOT / "computations/unaudited-codex-orbit0-k24-availability-schedule-2026-08-24/k24_expected_scalar_groups.json"
AVAILABILITY = ROOT / "computations/unaudited-codex-orbit0-k24-availability-schedule-2026-08-24/results_k24_availability_schedule.json"
PINS = {
    VECTOR: "f66279b3eb83fbda64cf49a8b9ca6a614ba90a6325e862868f898d2b03509d96",
    CONTRACT: "9ee7c5b6c31b70a7e06f8a4909c8b9aa77a87444cb12992c9971b5259bb8a986",
    AVAILABILITY: "ec91fa81b164d1ecd83d234f5aa5d6c8ae5921f76f7b6d5c2145c4be3737f733",
    ROOT / "computations/unaudited-codex-orbit0-k24-relative-column-interface-gate-2026-08-24/k24_relative_column_provider.py": "bc69f705fea1aad120a622055d25687b22e12ac6141bd47166274d16f47fb3cd",
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_intervals(intervals, total):
    need(intervals and intervals[0][0] == 0 and intervals[-1][1] == total, "interval endpoints")
    need(all(start < end for start, end in intervals), "positive intervals")
    need(all(intervals[index][1] == intervals[index + 1][0] for index in range(len(intervals) - 1)), "interval no-gap/no-overlap")


def validate_plan(plan):
    need(plan["status"] == "HELD_NO_K24_FACTORIZED_RELATIVE_PRODUCTION_AUTHORIZED", "held status")
    need(plan["required_paths"] == 35 and plan["required_scalar_groups"] == 10, "35/10 contract")
    contract = json.loads(CONTRACT.read_text())
    expected_groups = contract["groups"]
    expected_ids = [identifier for ids in expected_groups.values() for identifier in ids]
    need(len(expected_ids) == len(set(expected_ids)) == 35, "expected ID set")
    families = plan["source_fold_families"]
    need(len(families) == 6 and sum(family["covered_ids"] for family in families) == 35, "family ID count")
    groups = [group for family in families for group in family["group_ids"]]
    need(len(groups) == len(set(groups)) == 10 and set(groups) == set(expected_groups), "exact group set")
    for family in families:
        need(sum(len(expected_groups[group]) for group in family["group_ids"]) == family["covered_ids"], "family covered-ID count")
        if "intervals" in family:
            exact_intervals(family["intervals"], family["source_units"])
            need(len(family["intervals"]) == family["shards"], "family shard count")
        else:
            need(family["family_id"] == "direct_D17_D18_formula" and family["interval_rule"] == "[8*j,min(8*(j+1),485)) for j=0..60", "direct interval rule")
            generated = [[8 * j, min(8 * (j + 1), 485)] for j in range(61)]
            exact_intervals(generated, 485)
            need(len(generated) == family["shards"] == 61, "direct shard count")
    need(sum(family["shards"] for family in families) == plan["source_fold_shards_total"] == 103, "total shard count")
    output = plan["source_fold_output"]
    need(output["binary_record_bytes"] == 39 and "orbit_total_mass_scaled_U:i128_le" in output["binary_record_format"], "compact source record")
    relative = plan["relative_closure_and_gram_shards"]
    need(relative["gram_edge_bytes"] == 48 and relative["dense_matrix_forbidden"] is True, "sparse Gram record")
    need("below K20" in relative["global_negative_guard"], "global negative correction")
    resources = plan["measured_and_formula_resources"]
    need(resources["one_column_exhaustive_seconds"] / resources["one_column_factorized_seconds"] > 250, "measured speedup")
    need(resources["prefix1_dense_gram_bytes_at_48_bytes_forbidden"] > 100_000_000_000_000, "dense rejection scale")
    need(resources["feasibility"].startswith("factorized source/residual ledgers are production-feasible"), "feasibility split")
    need(plan["launch_gates"]["no_launch_while_K15_active"] is True and plan["launch_gates"]["reject_if_dense_pair_enumeration_requested"] is True, "launch holds")


def validate_result(result):
    need(result["status"] == "PASS_BOUNDED_FACTORIZED_K24_B20_EQUIVALENCE", "result status")
    need(result["factorized_equals_exhaustive"] is True and result["row_orbit_canonicalization_performed"] is False, "equivalence/no rows")
    expected = {"20": "384", "22": "4608", "23": "12288", "24": "23040"}
    need(result["factorized_block_gram"] == result["exhaustive_orbit_mass_block_gram"] == expected, "block Gram values")
    need(result["lower_gram_K20_K22_K23"] == "17280" and result["top_gram_K24"] == "23040", "lower/top Gram")
    column = result["column"]
    need(column["output_degree_histogram"] == {"20": 1, "22": 12, "23": 32, "24": 60}, "shared term degree histogram")
    need(column["shared_word_term_count"] == 105 and column["column_orbit_size"] == 384, "term/orbit census")
    need("negative/global completeness" in result["scope_guard"], "bounded scope guard")


def replay_provider(result):
    spec = importlib.util.spec_from_file_location("B20_gate_replay", PROVIDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    column = module.P.parse_column_key(result["column"]["natural_column_key"])
    descriptor = module.column_descriptor(column)
    grams = module.orbit_block_gram(column, column)
    need(descriptor == result["column"], "descriptor replay")
    need({str(key): str(value) for key, value in sorted(grams.items())} == result["factorized_block_gram"], "Gram replay")


def validate_assembly(assembly):
    need(assembly["status"] == "PASS_INCONCLUSIVE_BOUNDED_FACTORIZED_RELATIVE_GRAM_CONTROL", "assembly status")
    need(assembly["component_status"] == "COLUMN_CAP_1_NOT_COMPLETE" and assembly["global_membership_verdict"] == "INCONCLUSIVE_INCOMPLETE_CLOSURE", "cap is inconclusive")
    need(assembly["lower_rank"] == 1 and assembly["lower_nullity"] == assembly["relative_columns"] == 0, "bounded lower kernel")
    need(assembly["target_top_norm"] == "377487360" and assembly["full_filtered_exact_norm_identity"] is False, "bounded norm rejection")
    need(assembly["kernel_route_and_full_gram_route_agree"] is True and assembly["bounded_component_membership"] is False, "route equivalence")


def validate_schema(schema):
    need(schema["$id"] == "orbit0-factorized-B20-relative-interface-v1" and schema["additionalProperties"] is False, "schema closed identity")
    theorem = schema["x-factorized-theorem"]
    need("|Orb(C)|" in theorem["orbit_gram"] and "ker(G20+G22+G23)=ker(L20)" in theorem["lower_kernel"], "factorized theorem")
    need("no materialized" in theorem["no_row_orbit_requirement"], "no-row theorem")
    correction = schema["x-scope-correction"]
    need("valid global positive" in correction["positive"] and "not global nonmembership" in correction["negative"] and "inconclusive" in correction["cap"], "scope correction")
    need(schema["properties"]["column_runs"]["items"]["allOf"][1]["properties"]["record_bytes"]["const"] == 39, "column record size")
    need(schema["properties"]["gram_blocks"]["items"]["allOf"][1]["properties"]["record_bytes"]["const"] == 48, "Gram record size")


def hostile_self_test(result, plan, schema):
    rejected = 0
    mutations = []
    bad = copy.deepcopy(result); bad["factorized_equals_exhaustive"] = False; mutations.append(("result", bad))
    bad = copy.deepcopy(result); bad["factorized_block_gram"]["24"] = "0"; mutations.append(("result", bad))
    bad = copy.deepcopy(plan); bad["source_fold_families"][0]["group_ids"] = ["source_D14_R2_4_4"]; mutations.append(("plan", bad))
    bad = copy.deepcopy(plan); bad["launch_gates"]["reject_if_dense_pair_enumeration_requested"] = False; mutations.append(("plan", bad))
    bad = copy.deepcopy(schema); bad["x-scope-correction"]["negative"] = "global negative allowed"; mutations.append(("schema", bad))
    for kind, bad in mutations:
        try:
            {"result": validate_result, "plan": validate_plan, "schema": validate_schema}[kind](bad)
        except ValueError:
            rejected += 1
        else:
            need(False, f"hostile {kind} mutation accepted")
    need(rejected == 5, "hostile count")
    return rejected


def main():
    for path, digest in PINS.items():
        need(path.is_file() and sha(path) == digest, f"pin {path}")
    result = json.loads(RESULT.read_text())
    assembly = json.loads(ASSEMBLY.read_text())
    plan = json.loads(PLAN.read_text())
    schema = json.loads(SCHEMA.read_text())
    validate_result(result)
    replay_provider(result)
    validate_assembly(assembly)
    validate_plan(plan)
    validate_schema(schema)
    rejected = hostile_self_test(result, plan, schema)
    audit = {
        "status": "PASS_INDEPENDENT_FACTORIZED_K24_B20_RELATIVE_GATE",
        "factorized_vs_exhaustive_block_grams_equal": True,
        "blocks": {"K20": "384", "K22": "4608", "K23": "12288", "K24": "23040"},
        "measured_factorized_seconds": result["factorized_elapsed_seconds"],
        "row_orbit_canonicalization": False,
        "kernel_and_full_gram_routes_agree": True,
        "bounded_cap_global_verdict": "INCONCLUSIVE",
        "strict_35_ID_10_group_103_source_shard_plan": True,
        "dense_gram_forbidden": True,
        "hostile_mutations_rejected": rejected,
        "schema_sha256": sha(SCHEMA),
        "provider_sha256": sha(PROVIDER),
        "result_sha256": sha(RESULT),
        "assembly_sha256": sha(ASSEMBLY),
        "plan_sha256": sha(PLAN),
        "production_launched": False,
        "scope": "bounded factorized B20 equivalence/referee and held all-35 plan only; no K24 charge, membership, or conjecture verdict",
    }
    output = HERE / "results_factorized_B20_relative_gate_audit.json"
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps(audit, sort_keys=True))


if __name__ == "__main__":
    main()
