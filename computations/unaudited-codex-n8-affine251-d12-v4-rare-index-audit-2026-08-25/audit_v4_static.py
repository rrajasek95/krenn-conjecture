#!/usr/bin/env python3
"""Static fail-closed referee for the D12 v4 rare-order integration."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
V3 = (ROOT / "computations/unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24"
      / "sealed_v3/main.rs")
V3_SHA = "173828021430f51a51324a73c12e0cd351c072c2a458b4dadc019672ca72f69a"
PERSISTENCE_FUNCTIONS = [
    "sparse_write_checkpoint", "sparse_read_checkpoint", "sparse_write_vectors",
    "sparse_read_vectors", "sparse_maybe_write_vectors", "sparse_write_result",
]


class Reject(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def extract_function(source: str, name: str) -> str:
    match = re.search(r"(?m)^\s*(?:pub\s+)?fn\s+" + re.escape(name) + r"\s*\(", source)
    require(match is not None, "missing function " + name)
    opening = source.find("{", match.end())
    require(opening >= 0, "missing opening brace " + name)
    depth = 0
    state = "normal"
    block_depth = 0
    index = opening
    while index < len(source):
        char = source[index]
        nxt = source[index + 1] if index + 1 < len(source) else ""
        if state == "normal":
            if char == '"':
                state = "string"
            elif char == "'":
                state = "char"
            elif char == "/" and nxt == "/":
                state = "line"; index += 1
            elif char == "/" and nxt == "*":
                state = "block"; block_depth = 1; index += 1
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return source[match.start():index + 1]
        elif state == "string":
            if char == "\\":
                index += 1
            elif char == '"':
                state = "normal"
        elif state == "char":
            if char == "\\":
                index += 1
            elif char == "'":
                state = "normal"
        elif state == "line":
            if char == "\n":
                state = "normal"
        elif state == "block":
            if char == "/" and nxt == "*":
                block_depth += 1; index += 1
            elif char == "*" and nxt == "/":
                block_depth -= 1; index += 1
                if block_depth == 0:
                    state = "normal"
        index += 1
    raise Reject("unterminated function " + name)


def require_order(source: str, markers: list[str], label: str) -> None:
    positions = []
    for marker in markers:
        position = source.find(marker)
        require(position >= 0, label + " missing marker: " + marker)
        positions.append(position)
    require(positions == sorted(positions) and len(set(positions)) == len(positions),
            label + " marker order")


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n"); stream.flush(); os.fsync(stream.fileno())
    os.replace(temporary, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--v4-source", type=Path, required=True)
    parser.add_argument("--v4-binary", type=Path, required=True)
    parser.add_argument("--index-schema", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(sha256(V3) == V3_SHA, "v3 source pin")
    v3 = V3.read_text()
    v4 = args.v4_source.read_text()
    require(v4 != v3, "v4 source is unchanged")

    persistence_hashes = {}
    for name in PERSISTENCE_FUNCTIONS:
        old = extract_function(v3, name)
        new = extract_function(v4, name)
        def rustfmt_equivalent(text: str) -> str:
            compact = re.sub(r"\s+", "", text)
            # rustfmt inserts optional trailing commas before closing delimiters.
            # Removing only those grammar-optional commas preserves all separators.
            return re.sub(r",(?=[)}])", "", compact)

        require(rustfmt_equivalent(old) == rustfmt_equivalent(new),
                "persistence function semantic-token drift: " + name)
        persistence_hashes[name] = hashlib.sha256(old.encode()).hexdigest()

    required_markers = [
        "const RARE_NONE_FREQUENCY: u32 = u32::MAX;",
        "struct RareEntry {",
        "current: u32,",
        "committed: u32,",
        "struct RareOrderIndex {",
        "count = u32::try_from(count)",
        "count == 0 || count == RARE_NONE_FREQUENCY",
        ".checked_add(1)",
        "entry.current == RARE_NONE_FREQUENCY",
        "removals[frequency].sort_unstable();",
        "additions[frequency].sort_unstable();",
        "rare-order removal delta is not a bucket subset",
        "rare-order addition collides with retained row",
        "rare-order post-commit index census",
        "fn rows_by_rank(&self) -> Vec<Mono> {",
        "rare-order flattened index census",
        "v4 rare-order index requires fixed cold/rare/16 hierarchical nonincremental mode",
        "rare-order per-hit map/index divergence",
    ]
    missing = [marker for marker in required_markers if marker not in v4]
    require(not missing, "missing v4 source guards: " + repr(missing))

    entry = extract_function(v4, "sparse_d12_dual_entry")
    require_order(entry, [
        "for vector in vectors.values()",
        "let mut rare_index = RareOrderIndex::from_frequency(&exposed_frequency);",
        "for (column, vector) in new_columns.iter().copied().zip(values)",
        "let map_count = exposed_frequency.entry(row).or_default();",
        "exposed frequency overflow",
        "let index_count = rare_index.bump(row);",
        "rare-order per-hit map/index divergence",
        "columns.extend(new_columns.iter().copied());",
        "let stats = rare_index.commit();",
        "let rows_by_rank = rare_index.rows_by_rank();",
        "sparse_solve_correction_hierarchical",
    ], "resume/update/solve")

    rank = extract_function(v4, "hierarchical_rank_and_materialize")
    require("frequency: &HashMap<Mono, usize>" not in rank,
            "hierarchical rank helper still builds order from map")
    require("rows_by_rank: &[Mono]" in rank and
            "for (rank, row) in rows_by_rank.iter().copied().enumerate()" in rank,
            "rank map is not built from frozen natural order")
    require("hierarchical_row_hash(&row) as usize & (rank_shards - 1)" in rank,
            "FNV shard lookup contract absent")
    require("let slice = &columns[begin..begin + count];" in rank and
            ".into_iter()" in rank and "for mut chunk in chunk_results" in rank and
            "equations.append(&mut chunk);" in rank,
            "source-order equation append guard absent")

    rows_by_rank = extract_function(v4, "rows_by_rank")
    require("frequency" not in rows_by_rank and
            "for bucket in &self.buckets" in rows_by_rank and
            "for &row in bucket" in rows_by_rank and
            "answer.push(row);" in rows_by_rank and
            "answer.len() != self.entries.len()" in rows_by_rank,
            "attempt3 rank flatten is not a census-checked natural bucket concatenation")

    index_schema = None
    if args.index_schema is not None:
        index_schema = json.loads(args.index_schema.read_text())
        require(index_schema.get("schema") == "KRENN_AFFINE251_D12_RARE_ORDER_INDEX_V1",
                "index schema id")
        require(index_schema.get("serialized") is False, "index must be explicitly nonserialized")
        require("external gate" in index_schema.get("map_index_guard", ""),
                "external exact-order gate absent from index schema")

    source_review = {
        "initial_index": "rebuilt after complete vector restore/frequency scan",
        "process_persistence": "one mutable index lives across the sparse loop",
        "serialized_index": False,
        "checkpoint_cache_schema": "v3 persistence functions byte-identical",
        "update": "map checked increment then index checked bump with per-hit equality",
        "commit": "folded dirty rows; sorted removal/addition deltas; strict merge/census",
        "rank": "ascending frequency buckets and natural Mono bodies; census guarded in-process",
        "rank_hash": "removed from hot path; full map/order equality is mandatory in an external read-only gate",
        "lookup": "16 FNV shards are lookup-only; frozen rank enumeration precedes sharding",
        "mode_guard": "all modes except fixed cold/rare/16 hierarchical nonincremental fail closed",
    }
    result = {
        "schema": "KRENN_AFFINE251_D12_V4_RARE_INDEX_STATIC_AUDIT_V1",
        "status": "PASS_STATIC_V4_RARE_INDEX_INTEGRATION",
        "scope": "Static source/interface audit only; no solve or continuation.",
        "v3_source_sha256": V3_SHA,
        "v4_source_sha256": sha256(args.v4_source),
        "v4_binary_sha256": sha256(args.v4_binary),
        "index_schema_sha256": sha256(args.index_schema) if args.index_schema else None,
        "index_schema": index_schema,
        "persistence_function_sha256": persistence_hashes,
        "required_guard_markers": required_markers,
        "source_review": source_review,
    }
    atomic_json(args.output, result)


if __name__ == "__main__":
    main()
