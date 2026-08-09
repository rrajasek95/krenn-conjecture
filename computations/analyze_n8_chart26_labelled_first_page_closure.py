#!/usr/bin/env python3
"""Bounded closure of the labelled chart26 diagonal-12 Macaulay page."""

from collections import Counter, deque
import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
STAR_PATH = HERE / "verify_n8_chart26_labelled_first_page.py"
SPEC = importlib.util.spec_from_file_location("n8_chart26_labelled_star", STAR_PATH)
STAR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(STAR)
SOURCE = STAR.SOURCE
EXPECTED_LEDGER_SHA256 = (
    "5727ce606e12e72ab151b33858a941e96cbd002e78559e65d121db72da8f6d03"
)


def close_component(state_cap):
    root = SOURCE.SUPPORT_PRODUCT
    states = {root}
    columns = {}
    queue = deque([root])
    truncated = False
    next_report = 1000
    processed = 0
    while queue:
        row = queue.popleft()
        processed += 1
        for column in SOURCE.incident_columns(row):
            if column in columns:
                continue
            outputs = SOURCE.column_rows(column)
            top = Counter(
                output for output in outputs
                if STAR.diagonal_count(output) == 12
            )
            STAR.require(row in top,
                         "incident diagonal-12 column lost its source row")
            columns[column] = top
            for other in top:
                if other in states:
                    continue
                if len(states) >= state_cap:
                    truncated = True
                    return (tuple(sorted(states)), tuple(columns.items()),
                            truncated, processed, len(queue))
                states.add(other)
                queue.append(other)
        if len(states) >= next_report:
            print("closure states/columns/queue", len(states), len(columns),
                  len(queue), flush=True)
            next_report = ((len(states) // 1000) + 1) * 1000
    return (tuple(sorted(states)), tuple(columns.items()), truncated,
            processed, len(queue))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-cap", type=int, default=200000)
    arguments = parser.parse_args()
    states, columns, truncated, processed, queued = close_component(
        arguments.state_cap
    )
    STAR.require(truncated and len(states) == arguments.state_cap,
                 "default labelled closure frontier unexpectedly closed")
    column_keys = tuple(sorted(column for column, _values in columns))
    ledger = {
        "state_cap": arguments.state_cap,
        "discovered_labelled_diagonal12_rows": len(states),
        "discovered_labelled_columns": len(columns),
        "processed_rows": processed,
        "queued_unprocessed_rows": queued,
        "truncated": truncated,
        "anchor_laurent_translations_included": False,
        "state_sha256": sha256(repr(states).encode()).hexdigest(),
        "column_sha256": sha256(repr(column_keys).encode()).hexdigest(),
        "column_top_support_histogram": dict(sorted(Counter(
            sum(values.values()) for _column, values in columns
        ).items())),
        "root_cokernel_verdict": "unresolved",
        "scope_guard": (
            "exact labelled balanced-multidegree breadth-first prefix inside "
            "chart26 with no orbit compression; truncation occurs before the "
            "first diagonal page closes, and permitted anchor-Laurent "
            "translations would only enlarge it, so no full rank or cokernel "
            "is claimed"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if (arguments.state_cap == 50000
            and EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN"):
        STAR.require(digest == EXPECTED_LEDGER_SHA256,
                     "chart26 labelled closure frontier changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
