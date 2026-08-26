#!/usr/bin/env python3
"""Finite-field deletion/core discovery for the hard (0,31,13) face.

This script is deliberately labelled discovery.  Only a later homogeneous
characteristic-zero replay can turn its row subset into a theorem.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import time


HERE = Path(__file__).resolve().parent
INPUT = HERE / "results_recursive_face_charts.json"
OUTPUT = HERE / "results_face_03113_modular_row_core.json"
KEY = "0:31:13"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def base_c_localizer(record):
    factors = []
    for label in ("selected_base_terms", "both_live_c_numerators"):
        value = record["localizers"][label]
        require(value.endswith("-1") and "*(" in value,
                "unexpected localizer encoding")
        factors.append(value[value.index("*(") + 1:-2])
    return "s*" + "*".join(factors) + "-1"


def solve(record, kept_indices, prime, timeout):
    rows = [row for row in record["rows"]
            if row["raw_index"] in kept_indices]
    generators = [row["polynomial"] for row in rows] + [base_c_localizer(record)]
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
    try:
        completed = subprocess.run(
            ["Singular", "-q", "-c", command], text=True,
            capture_output=True, timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT",
                "elapsed_seconds": round(time.monotonic() - started, 6)}
    elapsed = round(time.monotonic() - started, 6)
    lines = completed.stdout.splitlines()
    if completed.returncode or "BEGIN" not in lines or "END" not in lines:
        return {"status": "ERROR", "elapsed_seconds": elapsed,
                "stderr_tail": completed.stderr[-500:]}
    body = lines[lines.index("BEGIN") + 1:lines.index("END")]
    return {"status": "UNIT" if body[0] == "0" else "NONUNIT",
            "basis_size": int(body[1]), "dimension": int(body[2]),
            "elapsed_seconds": elapsed}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=1009)
    parser.add_argument("--timeout", type=float, default=90)
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    payload = json.loads(INPUT.read_text())
    record = next(row for row in payload["states"] if row["key"] == KEY)
    all_indices = [row["raw_index"] for row in record["rows"]]

    def single(omitted):
        outcome = solve(record, set(all_indices) - {omitted},
                        args.prime, args.timeout)
        outcome["omitted"] = omitted
        print(outcome, flush=True)
        return outcome

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        singles = list(pool.map(single, all_indices))

    # Greedily delete all single-deletion UNIT rows, rechecking cumulatively.
    candidates = [row["omitted"] for row in singles
                  if row["status"] == "UNIT"]
    kept = set(all_indices)
    greedy = []
    for candidate in candidates:
        outcome = solve(record, kept - {candidate}, args.prime, args.timeout)
        accepted = outcome["status"] == "UNIT"
        if accepted:
            kept.remove(candidate)
        greedy.append({"candidate": candidate, "accepted": accepted,
                       **outcome, "kept_after": sorted(kept)})
        print(greedy[-1], flush=True)

    result = {
        "status": "UNAUDITED finite-field row-core discovery",
        "key": KEY, "prime": args.prime,
        "timeout_seconds": args.timeout,
        "single_deletions": singles,
        "single_deletion_histogram": {
            status: sum(row["status"] == status for row in singles)
            for status in ("UNIT", "NONUNIT", "TIMEOUT", "ERROR")
        },
        "greedy_records": greedy,
        "greedy_kept_source_rows": sorted(kept),
        "greedy_dropped_source_rows": sorted(set(all_indices) - kept),
        "always_kept_localizer": "selected_base_terms times c_numerators",
        "scope_guard": (
            "Every UNIT is only a finite-field discovery statement.  The "
            "subset is not a characteristic-zero theorem until an exact "
            "homogeneous replay succeeds."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("final kept:", sorted(kept))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
