#!/usr/bin/env python3
"""Fail-closed audit for the round-538 D12 portfolio and continuation gate."""

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


def checkpoint(path: Path) -> dict:
    with path.open("rb") as stream:
        header = stream.read(44)
    assert header[:12] == b"AFF12CEG1\0\0\0" and len(header) == 44
    prime, rounds, columns, support = struct.unpack_from("<QQQQ", header, 12)
    assert path.stat().st_size == 44 + 15 * columns + 21 * support
    return {"prime": prime, "rounds": rounds, "columns": columns, "support": support}


def vectors(path: Path) -> dict:
    with path.open("rb") as stream:
        header = stream.read(44)
    assert header[:12] == b"AFF12VEC1\0\0\0" and len(header) == 44
    prime, provider, checksum, columns = struct.unpack_from("<QQQQ", header, 12)
    assert path.stat().st_size > 44
    return {
        "prime": prime,
        "provider_fingerprint": provider,
        "vector_fingerprint": checksum,
        "columns": columns,
        "bytes": path.stat().st_size,
    }


def state(result: dict) -> tuple[int, int, int]:
    return result["rounds_completed"], result["column_orbits_exposed"], result["dual_support"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-result", type=Path, required=True)
    parser.add_argument("--period1-result", type=Path, required=True)
    parser.add_argument("--continuation-result", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--vectors", type=Path, required=True)
    parser.add_argument("--fixed-result", type=Path, required=True)
    parser.add_argument("--fixed-checkpoint", type=Path, required=True)
    parser.add_argument("--fixed-vectors", type=Path, required=True)
    parser.add_argument(
        "--advanced-state",
        nargs=3,
        action="append",
        metavar=("RESULT", "CHECKPOINT", "VECTORS"),
        default=[],
        help="later exact continuation triple; may be repeated in chronological order",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    base = json.loads(args.base_result.read_text())
    period1 = json.loads(args.period1_result.read_text())
    continuation = json.loads(args.continuation_result.read_text())
    fixed = json.loads(args.fixed_result.read_text())
    schema = "KRENN_AFFINE251_D12_NATIVE_SPARSE_DUAL_V1"
    assert base["schema"] == period1["schema"] == continuation["schema"] == schema
    assert state(base) == (538, 147_230, 233)
    assert period1["status"] == "INCOMPLETE_SEARCH_CAP" and period1["incomplete_reason"] == "ROUND_CAP"
    assert state(period1) == (546, 152_244, 249)
    assert period1["portfolio_period"] == 1 and len(period1["rounds"]) == 8
    assert [row["round"] for row in period1["rounds"]] == list(range(539, 547))
    assert all(row["selected_strategy"] == "cold" and row["selected_pivot"] == "rare"
               for row in period1["rounds"])
    assert continuation["status"] == "INCOMPLETE_RESOURCE_GATE"
    assert continuation["incomplete_reason"] == "WALL_CAP"
    assert state(continuation) == (634, 221_914, 307)
    assert continuation["portfolio_period"] == 32
    assert continuation["cached_vectors_loaded"] == 152_244
    assert continuation["vectors_materialized_on_restore"] == 0
    assert continuation["global_annihilation"] is None and continuation["target_pairing"] is None
    assert fixed["schema"] == schema
    assert fixed["status"] == "INCOMPLETE_RESOURCE_GATE" and fixed["incomplete_reason"] == "WALL_CAP"
    assert state(fixed) == (659, 245_290, 384)
    assert fixed["pivot_mode"] == "rare" and fixed["strategy"] == "cold"
    assert fixed["cached_vectors_loaded"] == 222_676
    assert fixed["vectors_materialized_on_restore"] == 0
    assert fixed["global_annihilation"] is None and fixed["target_pairing"] is None

    checkpoint_state = checkpoint(args.checkpoint)
    vector_state = vectors(args.vectors)
    assert checkpoint_state == {
        "prime": continuation["prime"],
        "rounds": 634,
        "columns": 221_914,
        "support": 307,
    }
    assert vector_state["prime"] == continuation["prime"]
    assert vector_state["columns"] == 221_914
    assert vector_state["bytes"] == continuation["vector_cache_bytes"]
    fixed_checkpoint_state = checkpoint(args.fixed_checkpoint)
    fixed_vector_state = vectors(args.fixed_vectors)
    assert fixed_checkpoint_state == {
        "prime": fixed["prime"],
        "rounds": 659,
        "columns": 245_290,
        "support": 384,
    }
    assert fixed_vector_state["prime"] == fixed["prime"]
    assert fixed_vector_state["columns"] == 245_290
    assert fixed_vector_state["bytes"] == fixed["vector_cache_bytes"]

    advanced_states = []
    advanced_hashes = []
    previous = fixed
    for result_name, checkpoint_name, vectors_name in args.advanced_state:
        result_path = Path(result_name)
        checkpoint_path = Path(checkpoint_name)
        vectors_path = Path(vectors_name)
        result = json.loads(result_path.read_text())
        assert result["schema"] == schema
        assert result["status"] in {"INCOMPLETE_RESOURCE_GATE", "INCOMPLETE_SEARCH_CAP"}
        assert result["incomplete_reason"] in {"WALL_CAP", "RSS_CAP", "ROUND_CAP"}
        if result["pivot_mode"] == "rare" and result["strategy"] == "cold":
            pass
        else:
            assert result["pivot_mode"] == "auto" and result["strategy"] == "best"
            assert result["rounds"]
            assert all(
                row["selected_strategy"] == "cold" and row["selected_pivot"] == "rare"
                for row in result["rounds"]
            )
        assert result["cached_vectors_loaded"] == previous["column_orbits_exposed"]
        assert result["vectors_materialized_on_restore"] == 0
        assert result["rounds_completed"] > previous["rounds_completed"]
        assert result["column_orbits_exposed"] > previous["column_orbits_exposed"]
        assert result["global_annihilation"] is None and result["target_pairing"] is None
        cp = checkpoint(checkpoint_path)
        vec = vectors(vectors_path)
        assert cp == {
            "prime": result["prime"],
            "rounds": result["rounds_completed"],
            "columns": result["column_orbits_exposed"],
            "support": result["dual_support"],
        }
        assert vec["prime"] == result["prime"]
        assert vec["columns"] == result["column_orbits_exposed"]
        assert vec["bytes"] == result["vector_cache_bytes"]
        advanced_states.append({
            "rounds": result["rounds_completed"],
            "columns": result["column_orbits_exposed"],
            "support": result["dual_support"],
        })
        advanced_hashes.append({
            "result": sha256(result_path),
            "checkpoint": sha256(checkpoint_path),
            "vectors": sha256(vectors_path),
        })
        previous = result

    latest = advanced_states[-1] if advanced_states else {
        "rounds": 659,
        "columns": 245_290,
        "support": 384,
    }

    report = {
        "schema": "KRENN_AFFINE251_D12_PORTFOLIO_CONTINUATION_AUDIT_V1",
        "status": "PASS_INCOMPLETE_EXACT_CONTINUATION",
        "base_state": {"rounds": 538, "columns": 147_230, "support": 233},
        "period1_state": {"rounds": 546, "columns": 152_244, "support": 249},
        "wall_continuation_state": {"rounds": 634, "columns": 221_914, "support": 307},
        "advanced_states": advanced_states,
        "latest_state": latest,
        "period1_selected_only_cold_rare": True,
        "period1_promoted": False,
        "latest_global_annihilation": None,
        "latest_target_pairing": None,
        "mathematical_verdict": None,
        "sha256": {
            "base_result": sha256(args.base_result),
            "period1_result": sha256(args.period1_result),
            "continuation_result": sha256(args.continuation_result),
            "checkpoint": sha256(args.checkpoint),
            "vectors": sha256(args.vectors),
            "fixed_result": sha256(args.fixed_result),
            "fixed_checkpoint": sha256(args.fixed_checkpoint),
            "fixed_vectors": sha256(args.fixed_vectors),
            "advanced_states": advanced_hashes,
        },
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
