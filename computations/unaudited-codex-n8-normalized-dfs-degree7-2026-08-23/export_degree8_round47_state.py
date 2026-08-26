#!/usr/bin/env python3
"""Export the deterministic round-47/48 handoff for the degree-eight CEGAR.

This is a replay/export, not a new membership gate.  It reruns the frozen
exact lazy ledger through completed round 47, checks rounds 0..10 and 47
against the terminal JSON, and writes a deterministic compressed state with
the 1,977 solved columns, 114,087 exposed rows, exact 416-row extension, six
new violations, and the resulting 1,983-column round-48 selection.
"""

from collections import Counter
from fractions import Fraction
import gzip
from hashlib import sha256
import json
from pathlib import Path
from time import monotonic

import audit_degree8_lazy_dual_cegar as lazy


HERE = Path(__file__).resolve().parent
LEDGER_PATH = HERE / "results_degree8_lazy_dual_cegar.json"
STATE_PATH = HERE / "degree8_round47_state.json.gz"
MANIFEST_PATH = HERE / "results_degree8_round47_state.json"
QQ = Fraction
CHECK_ROUNDS = frozenset(range(11)) | {47}
FINAL_ROUND = 47


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def column_record(column):
    return [column[0], column[1].hex()]


def fraction_record(value):
    return [value.numerator, value.denominator]


def checked_record(round_index, selected, system, candidates, violations,
                   new_columns):
    return {
        "round": round_index,
        "selected_columns": len(selected),
        "exposed_degree8_rows": len(system["rows"]),
        "relative_nnz": system["nnz"],
        "exact_top_rank": system["rank"],
        "extension_support": len(system["extension"]),
        "exact_remainder_terms": len(system["remainder"]),
        "incident_degree8_columns": len(candidates),
        "nonzero_pairing_columns": len(violations),
        "new_violating_columns": len(new_columns),
        "violation_pairing_histogram": [
            [fraction_record(value), count]
            for value, count in sorted(Counter(violations.values()).items())
        ],
    }


def ledger_projection(record):
    return {key: value for key, value in record.items()
            if key != "elapsed_seconds"}


def run():
    started = monotonic()
    ledger_bytes = LEDGER_PATH.read_bytes()
    ledger = json.loads(ledger_bytes)
    require(ledger["status"] == "WALL_CAP" and len(ledger["rounds"]) == 48,
            "terminal lazy ledger changed")

    audit = lazy.load_audit()
    # This replay is known to finish just over the original discovery cap.
    # Raising the imported internal sentinel does not change the equations.
    audit.WALL_CAP_SECONDS = 420
    source = audit.load_d7()
    core = lazy.load_core()
    lambda7 = {
        bytes.fromhex(encoded): QQ(numerator, denominator)
        for encoded, numerator, denominator in core["degree7_dual"]
    }
    selected = {
        (item["word_code"], bytes.fromhex(item["multiplier_hex"]))
        for item in core["violating_columns"]
    }
    validations = []
    final = None

    for round_index in range(FINAL_ROUND + 1):
        system = lazy.exposed_system(audit, source, lambda7, selected, started)
        require(not system["remainder"],
                f"round {round_index} acquired an exact remainder")
        functional = dict(lambda7)
        functional.update(system["extension"])
        candidates = {
            column for column in source.bounded_incident_columns(
                functional, maximum_output_degree=8
            )
            if len(column[1]) == 4
        }
        violations = {}
        for column in candidates:
            value = audit.pairing(
                audit.invariant_entries(source, column), functional
            )
            if value:
                violations[column] = value
        require(not (set(violations) & selected),
                f"round {round_index} extension fails a selected column")
        new_columns = set(violations) - selected
        record = checked_record(
            round_index, selected, system, candidates, violations, new_columns
        )
        if round_index in CHECK_ROUNDS:
            expected = ledger_projection(ledger["rounds"][round_index])
            require(record == expected,
                    f"round {round_index} differs from the frozen ledger")
            validations.append(record)

        if round_index == FINAL_ROUND:
            require(len(selected) == 1977 and len(new_columns) == 6,
                    "round-47 handoff cardinality changed")
            next_selected = selected | new_columns
            require(len(next_selected) == 1983,
                    "round-48 selected cardinality changed")
            final = {
                "format": "n8-chart26-degree8-round47-state-v1",
                "source_checker_sha256": audit.EXPECTED_D7_SHA256,
                "degree7_dual_sha256": core["degree7_dual_sha256"],
                "initial_core_logical_sha256":
                    lazy.EXPECTED_CORE_LOGICAL_SHA256,
                "lazy_ledger_sha256": sha256(ledger_bytes).hexdigest(),
                "round": FINAL_ROUND,
                "solved_selected_column_count": len(selected),
                "next_selected_column_count": len(next_selected),
                "pending_new_column_count": len(new_columns),
                "exposed_degree8_row_count": len(system["rows"]),
                "relative_nnz": system["nnz"],
                "exact_top_rank": system["rank"],
                "exact_remainder_terms": len(system["remainder"]),
                "extension_support": len(system["extension"]),
                "solved_selected_columns": [
                    column_record(column) for column in system["columns"]
                ],
                "next_selected_columns": [
                    column_record(column) for column in sorted(next_selected)
                ],
                "pending_new_columns": [
                    column_record(column) for column in sorted(new_columns)
                ],
                "exposed_degree8_rows": [row.hex() for row in system["rows"]],
                "exact_extension": [
                    [row.hex(), value.numerator, value.denominator]
                    for row, value in sorted(system["extension"].items())
                ],
                "validation_rounds": validations,
                "scope_guard": (
                    "resumable deterministic state only; it proves neither "
                    "degree-eight membership nor nonmembership"
                ),
            }
            break
        selected.update(new_columns)

    require(final is not None, "round-47 state was not reached")
    logical_bytes = json.dumps(
        final, sort_keys=True, separators=(",", ":")
    ).encode()
    logical_sha = sha256(logical_bytes).hexdigest()
    compressed = gzip.compress(logical_bytes + b"\n", compresslevel=9, mtime=0)
    STATE_PATH.write_bytes(compressed)
    manifest = {
        "format": "n8-chart26-degree8-round47-state-manifest-v1",
        "status": "PASS exact round-47 replay/export",
        "state_path": STATE_PATH.name,
        "state_logical_sha256": logical_sha,
        "state_file_sha256": sha256(compressed).hexdigest(),
        "state_uncompressed_bytes": len(logical_bytes) + 1,
        "state_compressed_bytes": len(compressed),
        "solved_selected_columns": final["solved_selected_column_count"],
        "next_selected_columns": final["next_selected_column_count"],
        "pending_new_columns": final["pending_new_column_count"],
        "exposed_degree8_rows": final["exposed_degree8_row_count"],
        "relative_nnz": final["relative_nnz"],
        "exact_top_rank": final["exact_top_rank"],
        "extension_support": final["extension_support"],
        "validated_rounds": sorted(CHECK_ROUNDS),
        "elapsed_seconds": monotonic() - started,
        "scope_guard": final["scope_guard"],
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


if __name__ == "__main__":
    result = run()
    print(result["status"])
    print(
        "round47 solved/next/rows/rank/extension="
        f"{result['solved_selected_columns']}/"
        f"{result['next_selected_columns']}/"
        f"{result['exposed_degree8_rows']}/"
        f"{result['exact_top_rank']}/"
        f"{result['extension_support']}"
    )
    print(f"elapsed_seconds={result['elapsed_seconds']:.3f}")
