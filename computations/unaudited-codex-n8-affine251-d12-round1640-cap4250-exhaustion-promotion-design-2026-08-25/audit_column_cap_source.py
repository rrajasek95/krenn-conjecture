#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
from pathlib import Path


EXPECTED_LINES = [
    "column_cap: usize,",
    "let column_cap = values",
    "|| column_cap < 17",
    "column_cap,",
    'writeln!(out, "  \\\"column_cap\\\": {},", config.column_cap).unwrap();',
    "if columns.len() + new_columns.len() > config.column_cap {",
]


def audit_text(text: str, expected_sha256: str, enforce_hash: bool = True) -> dict:
    digest = hashlib.sha256(text.encode()).hexdigest()
    if enforce_hash and digest != expected_sha256:
        raise ValueError(f"source hash mismatch: {digest}")

    occurrences = []
    for number, line in enumerate(text.splitlines(), 1):
        if re.search(r"\bcolumn_cap\b", line):
            occurrences.append({"line": number, "text": line.strip()})
    normalized = [item["text"] for item in occurrences]
    if normalized != EXPECTED_LINES:
        raise ValueError(f"unexpected column_cap occurrence census: {normalized!r}")
    if text.count("config.column_cap") != 2:
        raise ValueError("config.column_cap must occur exactly in serialization and guard")

    census = "let mut new_columns: Vec<_> = incident.difference(&columns).copied().collect();"
    sort = "new_columns.sort_unstable();"
    empty = "if new_columns.is_empty() {"
    guard = "if columns.len() + new_columns.len() > config.column_cap {"
    arithmetic = "let values =\n            parallel_invariant_columns"
    positions = {name: text.index(token) for name, token in [
        ("census", census),
        ("sort", sort),
        ("empty_terminal", empty),
        ("capacity_guard", guard),
        ("column_arithmetic", arithmetic),
    ]}
    if not (positions["census"] < positions["sort"] < positions["empty_terminal"]
            < positions["capacity_guard"] < positions["column_arithmetic"]):
        raise ValueError(f"unexpected cap/census/arithmetic order: {positions}")

    branch = text[positions["capacity_guard"]:positions["column_arithmetic"]]
    for required in [
        "sparse_write_checkpoint(",
        "sparse_maybe_write_vectors(",
        "sparse_write_result(",
        'Some("COLUMN_CAP")',
        "return;",
    ]:
        if required not in branch:
            raise ValueError(f"capacity branch missing {required}")
    for forbidden in [
        "parallel_invariant_columns(",
        "columns.insert(",
        "vectors.insert(",
        "rank_equations_sharded(",
    ]:
        if forbidden in branch:
            raise ValueError(f"capacity branch contains arithmetic mutation {forbidden}")

    return {
        "schema": "KRENN_AFFINE251_D12_COLUMN_CAP_STATIC_SOURCE_AUDIT_V1",
        "status": "PASS_COLUMN_CAP_ONLY_PRE_ARITHMETIC_CAPACITY_GUARD",
        "source_sha256": digest,
        "identifier_occurrence_count": len(occurrences),
        "config_field_read_count": text.count("config.column_cap"),
        "occurrences": occurrences,
        "ordered_landmarks_byte_offsets": positions,
        "proof": {
            "enumeration_before_guard": True,
            "new_column_sort_before_guard": True,
            "empty_terminal_before_guard": True,
            "capacity_guard_before_column_arithmetic": True,
            "capacity_failure_returns_before_column_arithmetic": True,
            "capacity_failure_checkpoint_uses_unchanged_columns_candidate": True,
            "other_config_field_read_is_result_serialization_only": True,
            "enumeration_scoring_and_elimination_do_not_read_column_cap": True,
        },
    }


def run_selftests(text: str, expected_sha256: str) -> list:
    tests = []
    audit_text(text, expected_sha256)
    tests.append("baseline_pass")
    hostile_cases = {
        "extra_runtime_read": text + "\nfn hostile(config: &Config) { let _ = config.column_cap; }\n",
        "missing_capacity_reason": text.replace('Some("COLUMN_CAP")', 'Some("HOSTILE")', 1),
        "missing_guard": text.replace(
            "if columns.len() + new_columns.len() > config.column_cap {",
            "if false {",
            1,
        ),
        "arithmetic_in_capacity_branch": text.replace(
            "if columns.len() + new_columns.len() > config.column_cap {",
            "if columns.len() + new_columns.len() > config.column_cap {\n            parallel_invariant_columns(&provider, &new_columns, config.prime, config.workers);",
            1,
        ),
    }
    for name, hostile in hostile_cases.items():
        try:
            audit_text(hostile, expected_sha256, enforce_hash=False)
        except (ValueError, KeyError):
            tests.append(f"{name}_rejected")
        else:
            raise RuntimeError(f"hostile selftest unexpectedly passed: {name}")
    return tests


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    text = Path(args.source).read_text()
    result = audit_text(text, args.expected_sha256)
    result["selftests"] = run_selftests(text, args.expected_sha256) if args.selftest else []
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
