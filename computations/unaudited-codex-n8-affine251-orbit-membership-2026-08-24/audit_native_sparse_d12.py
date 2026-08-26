#!/usr/bin/env python3
"""Independent, fail-closed audit of the native sparse D12 CEGAR controls."""

import argparse
import hashlib
import json
import struct
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def checkpoint_header(path: Path) -> dict:
    with path.open("rb") as stream:
        header = stream.read(44)
    assert len(header) == 44 and header[:12] == b"AFF12CEG1\0\0\0"
    prime, round_number, columns, support = struct.unpack_from("<QQQQ", header, 12)
    expected = 44 + 15 * columns + 21 * support
    assert path.stat().st_size == expected
    return {"prime": prime, "round": round_number, "columns": columns, "support": support}


def vector_header(path: Path) -> dict:
    with path.open("rb") as stream:
        header = stream.read(44)
    assert len(header) == 44 and header[:12] == b"AFF12VEC1\0\0\0"
    prime, provider_fingerprint, vector_fingerprint, columns = struct.unpack_from("<QQQQ", header, 12)
    assert path.stat().st_size > 44
    return {
        "prime": prime,
        "provider_fingerprint": provider_fingerprint,
        "vector_fingerprint": vector_fingerprint,
        "columns": columns,
        "bytes": path.stat().st_size,
    }


def state(result: dict) -> tuple[int, int, int]:
    return result["rounds_completed"], result["column_orbits_exposed"], result["dual_support"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--python-baseline", type=Path, required=True)
    parser.add_argument("--native-equivalence", type=Path, required=True)
    parser.add_argument("--frontier-result", type=Path, required=True)
    parser.add_argument("--frontier-checkpoint", type=Path, required=True)
    parser.add_argument("--cache-build", type=Path, required=True)
    parser.add_argument("--warm-result", type=Path, required=True)
    parser.add_argument("--frontier-vectors", type=Path, required=True)
    parser.add_argument("--resume-result", type=Path, required=True)
    parser.add_argument("--resume-checkpoint", type=Path, required=True)
    parser.add_argument("--resume-vectors", type=Path, required=True)
    parser.add_argument("--repair-result", type=Path, required=True)
    parser.add_argument("--repair-vectors", type=Path, required=True)
    parser.add_argument("--portfolio-serial", type=Path, required=True)
    parser.add_argument("--portfolio-parallel", type=Path, required=True)
    parser.add_argument("--portfolio-serial-checkpoint", type=Path, required=True)
    parser.add_argument("--portfolio-parallel-checkpoint", type=Path, required=True)
    parser.add_argument("--portfolio-serial-vectors", type=Path, required=True)
    parser.add_argument("--portfolio-parallel-vectors", type=Path, required=True)
    parser.add_argument("--tree-result", type=Path, required=True)
    parser.add_argument("--vec-result", type=Path, required=True)
    parser.add_argument("--tree-checkpoint", type=Path, required=True)
    parser.add_argument("--vec-checkpoint", type=Path, required=True)
    parser.add_argument("--tree-vectors", type=Path, required=True)
    parser.add_argument("--vec-vectors", type=Path, required=True)
    parser.add_argument("--fastmod-result", type=Path, required=True)
    parser.add_argument("--fastmod-checkpoint", type=Path, required=True)
    parser.add_argument("--optimized-result", type=Path, required=True)
    parser.add_argument("--optimized-checkpoint", type=Path, required=True)
    parser.add_argument("--optimized-vectors", type=Path, required=True)
    parser.add_argument("--optimized-warm", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    python = json.loads(args.python_baseline.read_text())
    native = json.loads(args.native_equivalence.read_text())
    assert python["schema"] == "KRENN_AFFINE251_D12_SPARSE_DUAL_CEGAR_V1"
    assert python["status"] == "INCOMPLETE_OR_TARGET_FORCED"
    assert native["schema"] == "KRENN_AFFINE251_D12_NATIVE_SPARSE_DUAL_V1"
    assert native["status"] == "INCOMPLETE_SEARCH_CAP" and native["incomplete_reason"] == "ROUND_CAP"
    python_rounds = python["searches"][0]["rounds"]
    native_rounds = native["rounds"]
    assert len(python_rounds) == len(native_rounds) == 5
    comparable = ("round", "columns", "new_columns", "dual_support")
    for old, new in zip(python_rounds, native_rounds, strict=True):
        assert {key: old[key] for key in comparable} == {key: new[key] for key in comparable}
    assert state(native) == (5, 308, 168)
    assert native["global_annihilation"] is None and native["target_pairing"] is None

    frontier = json.loads(args.frontier_result.read_text())
    assert frontier["status"] == "INCOMPLETE_RESOURCE_GATE" and frontier["incomplete_reason"] == "WALL_CAP"
    assert state(frontier) == (449, 93_754, 220)
    assert frontier["global_annihilation"] is None and frontier["target_pairing"] is None
    frontier_checkpoint = checkpoint_header(args.frontier_checkpoint)
    assert (frontier_checkpoint["round"], frontier_checkpoint["columns"], frontier_checkpoint["support"]) == state(frontier)

    build = json.loads(args.cache_build.read_text())
    warm = json.loads(args.warm_result.read_text())
    assert state(build) == state(warm) == state(frontier)
    assert build["cached_vectors_loaded"] == 0
    assert build["vectors_materialized_on_restore"] == 93_754
    assert warm["cached_vectors_loaded"] == 93_754
    assert warm["vectors_materialized_on_restore"] == 0
    assert build["restore_seconds"] > 30 and warm["restore_seconds"] < 5
    speedup = build["restore_seconds"] / warm["restore_seconds"]
    assert speedup > 20
    vectors449 = vector_header(args.frontier_vectors)
    assert vectors449["prime"] == frontier["prime"] and vectors449["columns"] == 93_754
    assert vectors449["bytes"] == build["vector_cache_bytes"] == warm["vector_cache_bytes"]

    resume = json.loads(args.resume_result.read_text())
    repair = json.loads(args.repair_result.read_text())
    assert state(resume) == state(repair) == (452, 95_485, 210)
    assert resume["cached_vectors_loaded"] == repair["cached_vectors_loaded"] == 93_754
    assert resume["vectors_materialized_on_restore"] == 0
    assert repair["vectors_materialized_on_restore"] == 1_731
    resume_checkpoint = checkpoint_header(args.resume_checkpoint)
    assert (resume_checkpoint["round"], resume_checkpoint["columns"], resume_checkpoint["support"]) == state(resume)
    resume_vectors = vector_header(args.resume_vectors)
    repair_vectors = vector_header(args.repair_vectors)
    assert resume_vectors == repair_vectors
    assert sha256(args.resume_vectors) == sha256(args.repair_vectors)
    assert resume_vectors["columns"] == 95_485

    serial = json.loads(args.portfolio_serial.read_text())
    parallel = json.loads(args.portfolio_parallel.read_text())
    assert state(serial) == state(parallel) == (453, 96_082, 213)
    assert serial["portfolio_parallel"] is False and parallel["portfolio_parallel"] is True
    serial_solve = serial["rounds"][0]["solve_seconds"]
    parallel_solve = parallel["rounds"][0]["solve_seconds"]
    portfolio_speedup = serial_solve / parallel_solve
    assert portfolio_speedup > 2
    assert sha256(args.portfolio_serial_checkpoint) == sha256(args.portfolio_parallel_checkpoint)
    assert sha256(args.portfolio_serial_vectors) == sha256(args.portfolio_parallel_vectors)

    tree = json.loads(args.tree_result.read_text())
    vec = json.loads(args.vec_result.read_text())
    fastmod = json.loads(args.fastmod_result.read_text())
    assert state(tree) == state(vec) == state(fastmod) == (452, 95_485, 210)
    assert vec["elimination_kernel"] == "vec"
    assert sha256(args.tree_checkpoint) == sha256(args.vec_checkpoint) == sha256(args.fastmod_checkpoint)
    assert sha256(args.tree_vectors) == sha256(args.vec_vectors)
    tree_solve = sum(row["solve_seconds"] for row in tree["rounds"])
    vec_solve = sum(row["solve_seconds"] for row in vec["rounds"])
    fastmod_solve = sum(row["solve_seconds"] for row in fastmod["rounds"])
    assert vec_solve >= tree_solve * 0.95
    assert fastmod_solve > tree_solve

    optimized = json.loads(args.optimized_result.read_text())
    optimized_warm = json.loads(args.optimized_warm.read_text())
    assert optimized["status"] == "INCOMPLETE_RESOURCE_GATE"
    assert optimized["incomplete_reason"] == "WALL_CAP"
    assert state(optimized) == state(optimized_warm) == (538, 147_230, 233)
    assert optimized["global_annihilation"] is None and optimized["target_pairing"] is None
    assert optimized["portfolio_parallel"] is True and optimized["incremental_basis"] is False
    assert optimized_warm["cached_vectors_loaded"] == 147_230
    assert optimized_warm["vectors_materialized_on_restore"] == 0
    assert optimized_warm["restore_seconds"] < 5
    optimized_checkpoint = checkpoint_header(args.optimized_checkpoint)
    assert (optimized_checkpoint["round"], optimized_checkpoint["columns"], optimized_checkpoint["support"]) == state(optimized)
    optimized_vectors = vector_header(args.optimized_vectors)
    assert optimized_vectors["columns"] == 147_230
    assert optimized_vectors["bytes"] == optimized["vector_cache_bytes"] == optimized_warm["vector_cache_bytes"]

    audit = {
        "schema": "KRENN_AFFINE251_D12_NATIVE_SPARSE_AUDIT_V1",
        "status": "PASS_INCOMPLETE_NATIVE_SPARSE_CONTROLS",
        "python_native_first_five_rounds_exact": True,
        "python_gate_elapsed_seconds": python["elapsed_seconds"],
        "native_equivalence_elapsed_seconds": native["elapsed_seconds"],
        "warm_restore_speedup": speedup,
        "cold_restore_seconds": build["restore_seconds"],
        "warm_restore_seconds": warm["restore_seconds"],
        "frontier_state": {"rounds": 449, "columns": 93_754, "support": 220},
        "cache_repair_control_state": {"rounds": 452, "columns": 95_485, "support": 210},
        "latest_control_state": {"rounds": 538, "columns": 147_230, "support": 233},
        "interrupted_cache_repair_byte_identical": True,
        "parallel_portfolio_speedup": portfolio_speedup,
        "parallel_portfolio_byte_identical": True,
        "sorted_vec_kernel_promoted": False,
        "constant_prime_kernel_promoted": False,
        "rejected_vec_to_tree_solve_ratio": vec_solve / tree_solve,
        "rejected_fastmod_to_tree_solve_ratio": fastmod_solve / tree_solve,
        "repair_vector_cache_bytes": resume_vectors["bytes"],
        "optimized_vector_cache_bytes": optimized_vectors["bytes"],
        "global_annihilation": None,
        "target_pairing": None,
        "mathematical_verdict": None,
        "sha256": {
            name: sha256(path) for name, path in {
                "python_baseline": args.python_baseline,
                "native_equivalence": args.native_equivalence,
                "frontier_result": args.frontier_result,
                "frontier_checkpoint": args.frontier_checkpoint,
                "cache_build": args.cache_build,
                "warm_result": args.warm_result,
                "frontier_vectors": args.frontier_vectors,
                "resume_result": args.resume_result,
                "resume_checkpoint": args.resume_checkpoint,
                "resume_vectors": args.resume_vectors,
                "repair_result": args.repair_result,
                "repair_vectors": args.repair_vectors,
                "portfolio_serial": args.portfolio_serial,
                "portfolio_parallel": args.portfolio_parallel,
                "portfolio_serial_checkpoint": args.portfolio_serial_checkpoint,
                "portfolio_parallel_checkpoint": args.portfolio_parallel_checkpoint,
                "portfolio_serial_vectors": args.portfolio_serial_vectors,
                "portfolio_parallel_vectors": args.portfolio_parallel_vectors,
                "tree_result": args.tree_result,
                "vec_result": args.vec_result,
                "tree_checkpoint": args.tree_checkpoint,
                "vec_checkpoint": args.vec_checkpoint,
                "tree_vectors": args.tree_vectors,
                "vec_vectors": args.vec_vectors,
                "fastmod_result": args.fastmod_result,
                "fastmod_checkpoint": args.fastmod_checkpoint,
                "optimized_result": args.optimized_result,
                "optimized_checkpoint": args.optimized_checkpoint,
                "optimized_vectors": args.optimized_vectors,
                "optimized_warm": args.optimized_warm,
            }.items()
        },
    }
    args.output.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
