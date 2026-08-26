#!/usr/bin/env python3
"""Bounded exact target-rooted CEGAR for normalized F^h at degree 12.

The calculation is performed in the exact chart stabilizer invariant block.
Each round solves the literal finite source-column span over Q, extracts a
target-pairing dual, exhaustively enumerates every degree-12 source-column
orbit incident to its support, and adds every violating orbit.  A stall is a
full ideal separator because every nonincident column pairs zero tautologically.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import resource
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ROOT_STAR_PATH = (
    ROOT / "computations/unaudited-codex-n8-chart26-fh-root-star-2026-08-23"
    / "audit_fh_root_star.py"
)
ROOT_STAR_RESULT = ROOT_STAR_PATH.with_name("results_fh_root_star.json")
RESULTS = HERE / "results_fh_degree12_full_cegar.json"
TIME_CAP_SECONDS = 300.0
RSS_CAP_BYTES = 12 * 1024 ** 3
EXPECTED_ROOT_STAR_LOGICAL = (
    "57a5bb5aa092a6edb79644be16f8b07908f8533b6c59e33e1ef4727771b6aad1"
)
EXPECTED_LOGICAL_SHA256 = None


class BoundedStop(Exception):
    pass


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


ROOT_STAR = load(ROOT_STAR_PATH, "n8_fh_degree12_cegar_root")


def peak_rss_bytes():
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # Darwin reports bytes; Linux reports KiB.
    return int(value if value > 10_000_000 else value * 1024)


def check_cap(started, label):
    elapsed = time.monotonic() - started
    rss = peak_rss_bytes()
    if elapsed > TIME_CAP_SECONDS or rss > RSS_CAP_BYTES:
        raise BoundedStop({
            "label": label,
            "elapsed_seconds": elapsed,
            "peak_rss_bytes": rss,
        })


def audit():
    started = time.monotonic()
    root_frozen = json.loads(ROOT_STAR_RESULT.read_text())
    require(root_frozen["logical_sha256"] == EXPECTED_ROOT_STAR_LOGICAL,
            "root-star authority changed")
    source_api, source = ROOT_STAR.load_source()

    pure_terms = tuple(tuple(sorted(
        source.normalized_generator(source.D5.word_code((colour,) * 8)).items(),
        key=lambda item: (len(item[0]), item[0]),
    )) for colour in range(3))

    @lru_cache(None)
    def coefficient_fh(row, colours=(0, 1, 2)):
        if not colours:
            return int(not row)
        total = 0
        for term, coefficient in pure_terms[colours[0]]:
            if len(term) > len(row):
                break
            quotient = ROOT_STAR.quotient_if_divides(row, term)
            if quotient is not None:
                total += coefficient * coefficient_fh(
                    quotient, colours[1:]
                )
        return total

    root = b""
    columns = set(source.bounded_incident_columns(
        {root: Fraction(1)}, maximum_output_degree=12
    ))
    require(len(columns) == 1, "root column orbit changed")
    rows = {root}
    for column in columns:
        rows.update(source_api.invariant_entries(source, column))

    ledger = []
    last_dual = {}
    terminal = None
    while True:
        check_cap(started, f"round_{len(ledger)}_start")
        target = {
            row: Fraction(value)
            for row in rows if (value := coefficient_fh(row))
        }
        rank, remainder, maximum_basis, dual, target_pairing = (
            source.exact_rank_and_target(
                tuple(rows), tuple(sorted(columns)), target
            )
        )
        check_cap(started, f"round_{len(ledger)}_exact_solve")
        if not dual:
            terminal = {
                "status": "FINITE_TARGET_PROJECTION_MEMBER_UNRESOLVED_FULL",
                "reason": (
                    "the current target restriction entered the admitted "
                    "column span; a full literal coefficient replay would be "
                    "needed before claiming membership"
                ),
                "rank": rank,
                "remainder_support": len(remainder),
            }
            break
        require(target_pairing != 0,
                "finite dual lost its Fh target pairing")

        candidates = source.bounded_incident_columns(
            dual, maximum_output_degree=12
        )
        violating = {}
        for index, column in enumerate(sorted(candidates), 1):
            value = source_api.pairing(
                source_api.invariant_entries(source, column), dual
            )
            if value and column not in columns:
                violating[column] = value
            if index % 2048 == 0:
                check_cap(started, f"round_{len(ledger)}_scan_{index}")
        record = {
            "round": len(ledger),
            "rows": len(rows),
            "columns": len(columns),
            "rank": rank,
            "target_rows_in_interface": len(target),
            "target_remainder_support": len(remainder),
            "dual_support": len(dual),
            "target_pairing": [
                target_pairing.numerator, target_pairing.denominator
            ],
            "maximum_basis_support": maximum_basis,
            "incident_column_orbits": len(candidates),
            "new_violating_column_orbits": len(violating),
            "violating_pairing_histogram": [
                [[value.numerator, value.denominator], count]
                for value, count in sorted(Counter(violating.values()).items())
            ],
        }
        ledger.append(record)
        print("round", record["round"], "rows/cols/rank/dual/candidates/new=",
              record["rows"], record["columns"], record["rank"],
              record["dual_support"], record["incident_column_orbits"],
              record["new_violating_column_orbits"], flush=True)
        last_dual = dual
        if not violating:
            actual_columns = source.audit_expanded_dual(dual, candidates)
            expanded_target_pairing = sum(
                value * Fraction(coefficient_fh(row))
                for row, value in dual.items()
            )
            require(expanded_target_pairing == target_pairing
                    and expanded_target_pairing != 0,
                    "expanded target pairing changed")
            terminal = {
                "status": "EXACT_FULL_FH_DEGREE12_NONMEMBERSHIP",
                "invariant_incident_column_orbits": len(candidates),
                "expanded_actual_incident_columns": actual_columns,
                "expanded_nonzero_column_pairings": 0,
                "target_pairing": [
                    target_pairing.numerator, target_pairing.denominator
                ],
            }
            break

        columns.update(violating)
        for column in violating:
            rows.update(source_api.invariant_entries(source, column))

    check_cap(started, "terminal_replay")
    dual_record = [
        [row.hex(), value.numerator, value.denominator]
        for row, value in sorted(last_dual.items())
    ]
    payload = {
        "format": "n8-normalized-fh-degree12-full-cegar-v1",
        **terminal,
        "homogeneous_degree": 12,
        "target": "full normalized F^h=H0^h H1^h H2^h",
        "target_total_terms": 1_157_625,
        "cegar_ledger": ledger,
        "admitted_invariant_column_orbits": len(columns),
        "interface_rows": len(rows),
        "terminal_dual_support": len(last_dual),
        "terminal_dual": dual_record,
        "terminal_dual_sha256": sha256(json.dumps(
            dual_record, separators=(",", ":")
        ).encode("ascii")).hexdigest(),
        "scope": (
            "exact full homogeneous degree-12 normalized mixed ideal in the "
            "localized chart, expanded from the chart-stabilizer invariant "
            "block to literal actual columns; no degree13, saturation, or "
            "global unlocalized inference"
        ),
        "root_star_logical_sha256": root_frozen["logical_sha256"],
        "source_sha256": {
            str(ROOT_STAR_PATH.relative_to(ROOT)):
                sha256(ROOT_STAR_PATH.read_bytes()).hexdigest(),
        },
        "time_cap_seconds": TIME_CAP_SECONDS,
        "rss_cap_bytes": RSS_CAP_BYTES,
        "elapsed_seconds_nonlogical": time.monotonic() - started,
        "peak_rss_bytes_nonlogical": peak_rss_bytes(),
    }
    logical = {
        key: value for key, value in payload.items()
        if not key.endswith("_nonlogical")
    }
    encoded = json.dumps(logical, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LOGICAL_SHA256 is not None:
        require(payload["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
                "degree12 full-Fh CEGAR ledger changed")
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    try:
        result = audit()
    except BoundedStop as stopped:
        result = {
            "format": "n8-normalized-fh-degree12-full-cegar-v1",
            "status": "BOUNDED_UNRESOLVED",
            "detail": stopped.args[0],
            "scope": "no degree12 membership/nonmembership inference",
        }
    if args.write_results:
        RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.check_results:
        require(RESULTS.exists()
                and json.loads(RESULTS.read_text()) == result,
                "stored result changed")
    print(result["status"])
    print("logical", result.get("logical_sha256", "none"))


if __name__ == "__main__":
    main()
