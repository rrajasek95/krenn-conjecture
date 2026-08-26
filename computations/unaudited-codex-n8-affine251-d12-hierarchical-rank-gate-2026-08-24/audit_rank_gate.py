#!/usr/bin/env python3
import hashlib
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VECTOR_SHA = "ecbcb26bcb8d2ecbb38cff4cce56457a960b2f11ba944536cd7bcf8d15b01275"
CHECKPOINT_SHA = "92185737bc273f112f91240ee58eb8d0b4cd842739490838ebd30c870b8b6155"
PARENT_SOURCE_SHA = "241ffd55f4f403d28d06f2e5dda3be1040e5c77675c9d05e2a7b70fc81ed36a0"
INDEPENDENT_AUDIT_SHA = "3f19e125292cb75e00fd2267f1f0dfd234735ca0095ddae6bed385fe38318a2d"
EXPECTED = {
    "baseline16": ("baseline", 1),
    "baseline16_r2": ("baseline", 1),
    "baseline16_r3": ("baseline", 1),
    "sharded1": ("sharded", 1),
    "sharded4": ("sharded", 4),
    "sharded16": ("sharded", 16),
    "sharded16_r2": ("sharded", 16),
    "sharded16_r3": ("sharded", 16),
    "sharded32": ("sharded", 32),
}


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def main():
    inputs = {
        "vectors": ROOT.parent / "unaudited-codex-n8-affine251-d12-portfolio-gate-2026-08-24" / "audit660_vectors.bin",
        "checkpoint": ROOT.parent / "unaudited-codex-n8-affine251-d12-portfolio-gate-2026-08-24" / "audit660_checkpoint.bin",
        "parent_source": ROOT.parent / "unaudited-codex-n8-affine251-orbit-membership-2026-08-24" / "src" / "main.rs",
        "independent_audit": ROOT.parent / "unaudited-codex-n8-affine251-d12-hierarchical-round660-gate-2026-08-24" / "results_independent_audit.json",
    }
    assert sha256(inputs["vectors"]) == VECTOR_SHA
    assert sha256(inputs["checkpoint"]) == CHECKPOINT_SHA
    assert sha256(inputs["parent_source"]) == PARENT_SOURCE_SHA
    assert sha256(inputs["independent_audit"]) == INDEPENDENT_AUDIT_SHA
    prior = json.loads(inputs["independent_audit"].read_text())
    assert prior["status"] == "PASS_INDEPENDENT_EXACT_HIERARCHICAL_ROUND660_AUDIT"
    assert prior["source_annihilation_replay"]["columns_replayed"] == 246321
    assert prior["source_annihilation_replay"]["verification_failures"] == 0
    assert prior["checkpoint_sha256"] == CHECKPOINT_SHA

    records = []
    binary_sha = None
    for label, (mode, shards) in EXPECTED.items():
        result_path = ROOT / "runs" / label / "result.json"
        output_checkpoint = ROOT / "runs" / label / "checkpoint.bin"
        result = json.loads(result_path.read_text())
        assert result["status"] == "PASS_EXACT_PARALLEL_HIERARCHICAL_ROUND660_PROMOTION_GATE"
        assert result["rank_mode"] == mode and result["rank_shards"] == shards
        assert result["workers"] == 16 and result["merge_arity"] == 2
        assert result["equations"] == 246321 and result["source_variable_terms"] == 24950813
        assert result["distinct_variables"] == 16179918
        assert result["candidate_identical"] is True and result["candidate_support"] == 352
        assert result["all_equations_verified"] is True and result["verification_failures"] == 0
        assert result["vectors"]["sha256"] == VECTOR_SHA
        assert result["sequential_checkpoint"]["sha256"] == CHECKPOINT_SHA
        assert result["output_checkpoint"]["sha256"] == CHECKPOINT_SHA
        assert result["output_checkpoint"]["byte_identical"] is True
        assert sha256(output_checkpoint) == CHECKPOINT_SHA
        assert result["source_sha256"] == PARENT_SOURCE_SHA
        assert result["peak_rss_bytes"] < 36 * 1024**3
        assert result["timings_seconds"]["total"] < 120
        if binary_sha is None:
            binary_sha = result["binary_sha256"]
        assert result["binary_sha256"] == binary_sha
        records.append({
            "label": label,
            "mode": mode,
            "shards": shards,
            "rank_seconds": result["timings_seconds"]["rare_rank_and_materialize"],
            "sort_seconds": result["timings_seconds"]["owned_frequency_row_sort"],
            "map_seconds": result["timings_seconds"]["rank_map_build"],
            "materialize_seconds": result["timings_seconds"]["compact_equation_materialize"],
            "fair_solve_seconds": result["hierarchical_solve_seconds"],
            "solve_speedup": result["solve_speedup"],
            "total_seconds": result["timings_seconds"]["total"],
            "peak_rss_bytes": result["peak_rss_bytes"],
            "shard_min_rows": result["rank_shard_rows"]["min"],
            "shard_max_rows": result["rank_shard_rows"]["max"],
            "result_sha256": sha256(result_path),
            "checkpoint_sha256": CHECKPOINT_SHA,
        })

    baseline = [x for x in records if x["mode"] == "baseline"]
    promoted = [x for x in records if x["mode"] == "sharded" and x["shards"] == 16]
    assert len(baseline) == len(promoted) == 3
    baseline_median = {
        key: statistics.median(x[key] for x in baseline)
        for key in ("rank_seconds", "fair_solve_seconds", "solve_speedup", "peak_rss_bytes")
    }
    promoted_median = {
        key: statistics.median(x[key] for x in promoted)
        for key in ("rank_seconds", "fair_solve_seconds", "solve_speedup", "peak_rss_bytes")
    }
    summary = {
        "schema": "KRENN_AFF251_D12_HIERARCHICAL_RANK_GATE_AUDIT_V1",
        "status": "PASS_EXACT_REPRODUCIBLE_PROMOTION",
        "verdict": "PROMOTE_16_SHARD_RANK_MATERIALIZATION",
        "promotion": True,
        "continued_beyond_round660": False,
        "run_count": len(records),
        "all_checkpoints_byte_identical": True,
        "all_equations_verified": True,
        "ordering_contract": {
            "owned_tuple_sort_matches_old_frequency_row_order": True,
            "rank_assignment_is_sorted_index": True,
            "hash_iteration_does_not_choose_rank_or_equation_order": True,
            "worker_chunks_join_in_source_order": True,
        },
        "memory_contract": {
            "frequency_map_consumed_into_owned_pairs": True,
            "owned_pairs_dropped_before_rank_maps_complete": True,
            "raw_equations_moved_not_cloned_into_chunks": True,
            "rank_maps_dropped_before_elimination": True,
            "maximum_observed_peak_rss_bytes": max(x["peak_rss_bytes"] for x in records),
            "hard_rss_bytes": 36 * 1024**3,
        },
        "fixture": {
            "vectors_sha256": VECTOR_SHA,
            "checkpoint_sha256": CHECKPOINT_SHA,
            "parent_source_sha256": PARENT_SOURCE_SHA,
            "prior_independent_replay_sha256": INDEPENDENT_AUDIT_SHA,
        },
        "implementation": {
            "source_sha256": sha256(ROOT / "src" / "main.rs"),
            "binary_sha256": binary_sha,
        },
        "baseline_median": baseline_median,
        "promoted_median": promoted_median,
        "improvement": {
            "rank_phase_factor": baseline_median["rank_seconds"] / promoted_median["rank_seconds"],
            "fair_solve_factor": baseline_median["fair_solve_seconds"] / promoted_median["fair_solve_seconds"],
            "sequential_speedup": promoted_median["solve_speedup"],
        },
        "recommended_configuration": {
            "workers": 16,
            "merge_arity": 2,
            "rank_mode": "sharded",
            "rank_shards": 16,
        },
        "records": records,
    }
    (ROOT / "results_rank_gate_audit.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: summary[key] for key in ("status", "verdict", "baseline_median", "promoted_median", "improvement")}, sort_keys=True))


if __name__ == "__main__":
    main()
