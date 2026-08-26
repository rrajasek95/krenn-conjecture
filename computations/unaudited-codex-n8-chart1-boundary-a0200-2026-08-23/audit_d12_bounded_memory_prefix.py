#!/usr/bin/env python3
"""Memory-only audit for a bounded-cache D12 resume; performs no solve."""

from collections import defaultdict
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import resource
import time


HERE = Path(__file__).resolve().parent
SOURCE_PATH = HERE / "run_d12_lazy_cegar.py"
CHECKPOINT = HERE / "checkpoint_d12_incremental_cegar.json"
RESULT = HERE / "results_d12_bounded_memory_prefix.json"
PREFIX = 2613
WALL = 300
RSS = 12 * 1024 ** 3


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None: raise RuntimeError(path)
    spec.loader.exec_module(module)
    return module


S = load(SOURCE_PATH, "chart1_boundary_memory_source")


def live_rss():
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value if value > 10_000_000 else value * 1024)


def require(condition, detail):
    if not condition: raise RuntimeError(detail)


def main():
    started = time.monotonic()
    provider = S.Provider()

    # These two routines deliberately bypass the source provider's unbounded
    # row-orbit and invariant-column memo tables.
    def row_orbit(row):
        return tuple(sorted(set(
            bytes(sorted(transform[value] for value in row))
            for transform in provider.transforms
        )))

    def invariant_entries(column):
        answer = defaultdict(int)
        for code, multiplier in provider.column_orbit(column):
            for term, coefficient in provider.generator(code).items():
                row = bytes(sorted(multiplier + term))
                orbit = row_orbit(row)
                if row == orbit[0]: answer[row] += coefficient
        return {row: value for row, value in answer.items() if value}

    # Build only the invariant target.  The old driver retained the full
    # 992,250-term literal target and all of its cached 32-element row orbits.
    target = {}
    for left, cl in provider.pure[0].items():
        for middle, cm in provider.pure[1].items():
            prefix = bytes(sorted(left + middle))
            for right, cr in provider.pure[2].items():
                row = bytes(sorted(prefix + right))
                representative = row_orbit(row)[0]
                coefficient = cl * cm * cr
                previous = target.setdefault(representative, coefficient)
                require(previous == coefficient, "invariant target coefficient changed")
        require(time.monotonic() - started < WALL and live_rss() < RSS,
                "bounded target-only audit exceeded gate")
    require(len(target) == 32965, "invariant target support changed")

    checkpoint = json.loads(CHECKPOINT.read_text())
    sequence = [(int(code), bytes.fromhex(multiplier))
                for code, multiplier in checkpoint["column_insertion_sequence"]]
    sequence = sequence[:PREFIX]
    rows = set(target)
    output_terms = 0
    milestones = []
    for position, column in enumerate(sequence, 1):
        entries = invariant_entries(column)
        rows.update(entries)
        output_terms += len(entries)
        if position % 256 == 0 or position == len(sequence):
            milestone = {
                "columns": position,
                "rows": len(rows),
                "cumulative_column_terms": output_terms,
                "live_rss_bytes": live_rss(),
                "elapsed_seconds": time.monotonic() - started,
            }
            milestones.append(milestone)
            print(milestone, flush=True)
            require(milestone["live_rss_bytes"] < RSS
                    and milestone["elapsed_seconds"] < WALL,
                    "bounded prefix audit exceeded gate")

    payload = {
        "format": "n8-chart1-boundary-d12-bounded-memory-prefix-v1",
        "status": "BOUNDED_MEMORY_PREFIX_PASS",
        "prefix_column_orbits": len(sequence),
        "invariant_target_support": len(target),
        "final_row_coordinates": len(rows),
        "cumulative_column_terms": output_terms,
        "milestones": milestones,
        "old_unbounded_retained_objects": [
            "992250-term literal target Counter",
            "unbounded row_orbit LRU containing 32 transformed rows per key",
            "unbounded invariant_entries LRU plus the driver output_cache",
        ],
        "bounded_design": [
            "construct invariant target directly and defer literal target to terminal replay",
            "compute row orbits without memoization during provider streaming",
            "spool selected column entries to disk and retain only row identifiers",
            "retain only the current incident batch in Python; Rust retains the pivot basis",
            "poll combined RSS every 64 incident columns and every 1 second in the child guard",
        ],
        "scope": "Memory/provider audit only; no modular or exact linear solve.",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    logical = {key: value for key, value in payload.items()
               if not key.endswith("seconds") and "rss" not in key}
    payload["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(payload["status"], payload["logical_sha256"])


if __name__ == "__main__": main()
