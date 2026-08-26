#!/usr/bin/env python3
import hashlib
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHECKPOINT_SHA = "92185737bc273f112f91240ee58eb8d0b4cd842739490838ebd30c870b8b6155"
VECTOR_SHA = "ecbcb26bcb8d2ecbb38cff4cce56457a960b2f11ba944536cd7bcf8d15b01275"
SOURCE_SHA = "241ffd55f4f403d28d06f2e5dda3be1040e5c77675c9d05e2a7b70fc81ed36a0"
BASELINE_SECONDS = 8.726527
SEALED_RANK_SECONDS = 3.075534
SEALED_ELIMINATION_SECONDS = 0.267003
EXPECTED = {
    "w8_a2": (8, 2), "w8_a4": (8, 4),
    "w16_a2": (16, 2), "w16_a2_r2": (16, 2), "w16_a2_r3": (16, 2),
    "w16_a4": (16, 4),
    "w16_a8": (16, 8), "w16_a8_r2": (16, 8), "w16_a8_r3": (16, 8),
    "w16_a16": (16, 16),
    "w32_a4": (32, 4), "w32_a8": (32, 8), "w32_a16": (32, 16),
    "w48_a8": (48, 8), "w64_a8": (64, 8),
}


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    inputs = {
        "vectors": ROOT.parent / "unaudited-codex-n8-affine251-d12-portfolio-gate-2026-08-24" / "audit660_vectors.bin",
        "checkpoint": ROOT.parent / "unaudited-codex-n8-affine251-d12-portfolio-gate-2026-08-24" / "audit660_checkpoint.bin",
        "source": ROOT.parent / "unaudited-codex-n8-affine251-orbit-membership-2026-08-24" / "src" / "main.rs",
    }
    assert sha256(inputs["vectors"]) == VECTOR_SHA
    assert sha256(inputs["checkpoint"]) == CHECKPOINT_SHA
    assert sha256(inputs["source"]) == SOURCE_SHA

    records = []
    binary_sha = None
    source_sha = sha256(ROOT / "src" / "main.rs")
    for label, (workers, arity) in EXPECTED.items():
        result_path = ROOT / "runs" / label / "result.json"
        checkpoint_path = ROOT / "runs" / label / "checkpoint.bin"
        result = json.loads(result_path.read_text())
        assert result["status"] == "PASS_EXACT_PARALLEL_HIERARCHICAL_ROUND660_PROMOTION_GATE"
        assert result["workers"] == workers and result["merge_arity"] == arity
        assert result["equations"] == 246321 and result["candidate_support"] == 352
        assert result["candidate_identical"] is True
        assert result["all_equations_verified"] is True and result["verification_failures"] == 0
        assert result["vectors"]["sha256"] == VECTOR_SHA
        assert result["sequential_checkpoint"]["sha256"] == CHECKPOINT_SHA
        assert result["output_checkpoint"]["sha256"] == CHECKPOINT_SHA
        assert result["output_checkpoint"]["byte_identical"] is True
        assert sha256(checkpoint_path) == CHECKPOINT_SHA
        assert result["source_sha256"] == SOURCE_SHA
        assert result["peak_rss_bytes"] < 36 * 1024**3
        assert result["timings_seconds"]["total"] < 120
        if binary_sha is None:
            binary_sha = result["binary_sha256"]
        assert result["binary_sha256"] == binary_sha
        records.append({
            "label": label,
            "workers": workers,
            "merge_arity": arity,
            "rank_seconds": result["timings_seconds"]["rare_rank_and_materialize"],
            "elimination_seconds": result["hierarchical_elimination_backsolve_verify_seconds"],
            "fair_solve_seconds": result["hierarchical_solve_seconds"],
            "speedup": result["solve_speedup"],
            "total_seconds": result["timings_seconds"]["total"],
            "peak_rss_bytes": result["peak_rss_bytes"],
            "result_sha256": sha256(result_path),
            "checkpoint_sha256": CHECKPOINT_SHA,
        })

    best = min(records, key=lambda item: item["fair_solve_seconds"])
    controls = [item for item in records if item["workers"] == 16 and item["merge_arity"] == 2]
    candidates = [item for item in records if item["workers"] == 16 and item["merge_arity"] == 8]
    assert len(controls) == len(candidates) == 3
    control_median = {
        "fair_solve_seconds": statistics.median(x["fair_solve_seconds"] for x in controls),
        "elimination_seconds": statistics.median(x["elimination_seconds"] for x in controls),
    }
    candidate_median = {
        "fair_solve_seconds": statistics.median(x["fair_solve_seconds"] for x in candidates),
        "elimination_seconds": statistics.median(x["elimination_seconds"] for x in candidates),
    }
    normalized_candidate_solve = SEALED_RANK_SECONDS + candidate_median["elimination_seconds"]
    summary = {
        "schema": "KRENN_AFF251_D12_HIERARCHICAL_GEOMETRY_AUDIT_V1",
        "status": "PASS_EXACT_NONPROMOTION",
        "verdict": "NO_PROMOTION_TIMING_NOT_STABLE",
        "promotion": False,
        "continued_beyond_round660": False,
        "fixture": {
            "vectors_sha256": VECTOR_SHA,
            "checkpoint_sha256": CHECKPOINT_SHA,
            "source_sha256": SOURCE_SHA,
            "equations": 246321,
            "candidate_support": 352,
        },
        "implementation": {"source_sha256": source_sha, "binary_sha256": binary_sha},
        "run_count": len(records),
        "all_checkpoints_byte_identical": True,
        "all_equations_verified": True,
        "best_observed": best,
        "repeated_16x2_median": control_median,
        "repeated_16x8_median": candidate_median,
        "sealed_reference": {
            "rank_seconds": SEALED_RANK_SECONDS,
            "elimination_seconds": SEALED_ELIMINATION_SECONDS,
            "fair_solve_seconds": SEALED_RANK_SECONDS + SEALED_ELIMINATION_SECONDS,
            "speedup": BASELINE_SECONDS / (SEALED_RANK_SECONDS + SEALED_ELIMINATION_SECONDS),
        },
        "normalized_16x8": {
            "sealed_rank_plus_candidate_median_elimination_seconds": normalized_candidate_solve,
            "speedup": BASELINE_SECONDS / normalized_candidate_solve,
        },
        "records": records,
    }
    (ROOT / "results_geometry_audit.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: summary[key] for key in ("status", "verdict", "best_observed", "repeated_16x8_median", "normalized_16x8")}, sort_keys=True))


if __name__ == "__main__":
    main()
