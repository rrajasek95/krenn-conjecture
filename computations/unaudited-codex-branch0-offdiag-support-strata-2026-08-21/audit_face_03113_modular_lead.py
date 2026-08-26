#!/usr/bin/env python3
"""Two-prime literal-row lead for the sole unresolved recursive cycle face.

This deliberately proves no characteristic-zero statement.  It freezes the
stronger finite-field observation and the exactness blocker without converting
a failed Q computation into an algebraic conclusion.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import time


HERE = Path(__file__).resolve().parent
INPUT = HERE / "results_recursive_face_charts.json"
OUTPUT = HERE / "results_face_03113_modular_lead.json"
KEY = "0:31:13"
PRIMES = (1009, 1013)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def factor(record, label):
    value = record["localizers"][label]
    require(value.endswith("-1") and "*(" in value,
            f"unexpected {label} encoding")
    return value[value.index("*(") + 1:-2]


def run_prime(record, prime):
    source = [row["polynomial"] for row in record["rows"]]
    sat = ("s*(" + factor(record, "selected_base_terms") + ")*(" +
           factor(record, "both_live_c_numerators") + ")-1")
    generators = source + [sat]
    names = record["variable_names"] + ["s"]
    names = [name for name in names if any(
        re.search(rf"\b{re.escape(name)}\b", generator)
        for generator in generators)]
    command = (
        f"ring R={prime},({','.join(names)}),dp;"
        f"ideal I={','.join(generators)};ideal G=slimgb(I);"
        'print("BEGIN");print(string(reduce(1,G)));print(size(G));'
        'print(dim(G));print("END");quit;'
    )
    started = time.monotonic()
    completed = subprocess.run(
        ["Singular", "-q", "-c", command], text=True,
        capture_output=True, timeout=120, check=False,
    )
    elapsed = round(time.monotonic() - started, 6)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            f"prime {prime} Singular failure: {completed.stderr[-1000:]}")
    lines = completed.stdout.splitlines()
    begin, end = lines.index("BEGIN"), lines.index("END")
    body = lines[begin + 1:end]
    require(body == ["0", "1", "-1"],
            f"prime {prime} unit result changed: {body}")
    return {"prime": prime, "unit_basis": True, "basis_size": 1,
            "dimension": -1, "elapsed_seconds": elapsed}


def main():
    payload = json.loads(INPUT.read_text())
    record = next(row for row in payload["states"] if row["key"] == KEY)
    require([row["raw_index"] for row in record["rows"]]
            == list(range(6, 22)), "literal source-row ledger changed")
    expected_c = (
        "(1+a3*d3+a2*d2+a2*a3*d2*d3+a0+a0*a3*d3+a0*a2*d2+"
        "a0*a2*a3*d2*d3)"
    )
    require(factor(record, "both_live_c_numerators") == expected_c,
            "C-factor expansion changed")
    prime_records = [run_prime(record, prime) for prime in PRIMES]
    stable_prime_records = [
        {key: value for key, value in row.items()
         if key != "elapsed_seconds"} for row in prime_records
    ]
    result = {
        "status": "UNAUDITED two-prime lead; characteristic zero unresolved",
        "key": KEY,
        "literal_source_raw_indices": list(range(6, 22)),
        "gauges": {"b_edges": record["gauge_b_edges"],
                   "d_edge": record["gauge_d_edge"]},
        "strong_localization": {
            "selected_base_factor": factor(record, "selected_base_terms"),
            "remaining_c_factor": expected_c,
            "remaining_c_factorization": (
                "(1+a0)*(1+a2*d2)*(1+a3*d3)"
            ),
            "H_localized": False,
            "both_live_ad_localized": False,
        },
        "prime_records": stable_prime_records,
        "timings_seconds_nonlogical": {
            str(row["prime"]): row["elapsed_seconds"]
            for row in prime_records
        },
        "exactness_attempts": [
            {"method": "homogeneous Q slimgb", "timeout_seconds": 300,
             "result": "TIMEOUT"},
            {"method": "homogeneous modGB exactness=1", "timeout_seconds": 300,
             "result": "TIMEOUT"},
            {"method": "raw affine Q ideal before saturation",
             "timeout_seconds": 300, "result": "TIMEOUT"},
            {"method": "mod1009 homogeneous slimgb",
             "timeout_seconds": 180, "result": "TIMEOUT"},
            {"method": "mod1009 liftstd provenance",
             "timeout_seconds": 300, "result": "TIMEOUT"},
            {"method": "mod1009 post-GB lift(I,1)",
             "timeout_seconds": 240, "result": "TIMEOUT"},
        ],
        "discovery_subset": {
            "dropped_raw_rows": [6, 9, 10, 11],
            "kept_raw_rows": [7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
            "mod1009_status": "UNIT",
            "scope": "discovery only; no exact lift",
        },
        "scope_guard": (
            "Two finite-field unit bases do not certify a Q-unit.  Every "
            "timeout is nonterminal.  This face remains the sole exact "
            "boundary-recursion blocker."
        ),
    }
    logical_copy = dict(result)
    logical_copy.pop("timings_seconds_nonlogical")
    logical = json.dumps(logical_copy, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("(0,31,13) two-prime stronger unit lead: PASS")
    print("prime records:", stable_prime_records)
    print("timings:", result["timings_seconds_nonlogical"])
    print("logical result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
