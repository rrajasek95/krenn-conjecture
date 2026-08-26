#!/usr/bin/env python3
"""Export the exact finite boundary seed for the unresolved degree-eight lift.

This reconstructs the pinned 49-row degree-seven dual and records only the
new multiplier-degree-four columns having nonzero lower-boundary pairing,
together with their degree-eight top outputs.  It does not close incidence or
perform a rank computation.
"""

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
from time import monotonic


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_degree8_dual_extension.py"
RESULTS = HERE / "results_degree8_initial_core.json"


def main():
    spec = importlib.util.spec_from_file_location("degree8_audit", AUDIT_PATH)
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    started = monotonic()
    module = audit.load_d7()
    dual, records = audit.reconstruct_degree7_dual(module, started)
    candidates = sorted(
        column for column in module.bounded_incident_columns(
            dual, maximum_output_degree=8
        )
        if len(column[1]) == 4
    )
    violating = []
    top_rows = set()
    boundary_histogram = Counter()
    top_support_histogram = Counter()
    for column in candidates:
        entries = audit.invariant_entries(module, column)
        value = audit.pairing(entries, dual)
        if not value:
            continue
        top = sorted(
            (row, coefficient) for row, coefficient in entries.items()
            if len(row) == 8
        )
        top_rows.update(row for row, _coefficient in top)
        boundary_histogram[value] += 1
        top_support_histogram[len(top)] += 1
        violating.append({
            "word_code": column[0],
            "word": "".join(map(str, module.D5.decode_word(column[0]))),
            "multiplier_hex": column[1].hex(),
            "boundary_pairing": [value.numerator, value.denominator],
            "degree8_top_outputs": [
                [row.hex(), coefficient] for row, coefficient in top
            ],
        })
    dual_record = [
        [row.hex(), value.numerator, value.denominator]
        for row, value in sorted(dual.items())
    ]
    result = {
        "format": "n8-chart26-degree8-relative-initial-core-v1",
        "degree7_dual_sha256": audit.EXPECTED_D7_DUAL_SHA256,
        "degree7_dual": dual_record,
        "degree7_reconstruction_records": [list(item) for item in records],
        "degree8_new_incident_columns": len(candidates),
        "degree8_boundary_violating_columns": len(violating),
        "degree8_initial_top_rows": len(top_rows),
        "boundary_pairing_histogram": [
            [[value.numerator, value.denominator], count]
            for value, count in sorted(boundary_histogram.items())
        ],
        "top_support_histogram": dict(sorted(top_support_histogram.items())),
        "violating_columns": violating,
        "elapsed_seconds": monotonic() - started,
        "scope": (
            "Exact initial relative boundary core only. The subsequent "
            "degree-eight top-incidence closure exceeded its 2M-row/200k-column "
            "combined guard before a rank test."
        ),
    }
    logical = dict(result)
    logical.pop("elapsed_seconds")
    result["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        "degree8 initial core: PASS; "
        f"candidates={len(candidates)}, violations={len(violating)}, "
        f"top_rows={len(top_rows)}"
    )
    print(f"logical sha256: {result['logical_sha256']}")


if __name__ == "__main__":
    main()
