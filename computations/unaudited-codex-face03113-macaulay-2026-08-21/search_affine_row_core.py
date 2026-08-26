#!/usr/bin/env python3
"""Discover a smaller modular source-row core for face (0,31,13).

This is finite-field discovery only.  It starts from the already audited
12-row p=1009 unit lead and greedily tests literal row deletions while always
retaining the combined selected-base/C-numerator Rabinowitsch generator.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import time


HERE = Path(__file__).resolve().parent
SOURCE = (HERE.parent / "unaudited-codex-branch0-offdiag-support-strata-2026-08-21" /
          "results_recursive_face_charts.json")
OUTPUT = HERE / "results_affine_row_core.json"
KEY = "0:31:13"
START = [7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def localizer(record):
    factors = []
    for label in ("selected_base_terms", "both_live_c_numerators"):
        encoded = record["localizers"][label]
        require(encoded.endswith("-1") and "*(" in encoded,
                f"unexpected localizer {label}")
        factors.append(encoded[encoded.index("*(") + 1:-2])
    return "s*" + "*".join(factors) + "-1"


def solve(record, kept, prime, timeout):
    expressions = [row["polynomial"] for row in record["rows"]
                   if row["raw_index"] in kept]
    expressions.append(localizer(record))
    names = record["variable_names"] + ["s"]
    names = [name for name in names if any(
        re.search(rf"\b{re.escape(name)}\b", expression)
        for expression in expressions)]
    program = (
        f"ring R={prime},({','.join(names)}),dp;"
        f"ideal I={','.join(expressions)};ideal G=slimgb(I);"
        'print("BEGIN");print(string(reduce(1,G)));print(size(G));'
        'print(dim(G));print("END");quit;'
    )
    started = time.monotonic()
    try:
        completed = subprocess.run(
            ["Singular", "-q", "-c", program], text=True,
            capture_output=True, timeout=timeout, check=False)
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
    parser.add_argument("--timeout", type=float, default=120.0)
    args = parser.parse_args()
    payload = json.loads(SOURCE.read_text())
    record = next(row for row in payload["states"] if row["key"] == KEY)
    kept = list(START)
    trials = []
    # Repeated sweeps matter: a deletion rejected early can become useful
    # after another source row is removed.
    changed = True
    sweep = 0
    while changed:
        changed = False
        sweep += 1
        for candidate in list(kept):
            proposed = [row for row in kept if row != candidate]
            outcome = solve(record, set(proposed), args.prime, args.timeout)
            accepted = outcome["status"] == "UNIT"
            if accepted:
                kept = proposed
                changed = True
            trial = {"sweep": sweep, "candidate": candidate,
                     "accepted": accepted, "kept_after": kept.copy(),
                     **outcome}
            trials.append(trial)
            print(json.dumps(trial, sort_keys=True), flush=True)
    result = {
        "status": "UNAUDITED finite-field row-core discovery",
        "face": KEY, "prime": args.prime,
        "timeout_seconds": args.timeout,
        "starting_rows": START, "final_rows": kept,
        "trials": trials,
        "source": str(SOURCE),
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "scope_guard": (
            "Finite-field affine UNIT is discovery only.  Only a later "
            "homogeneous characteristic-zero/source replay is a theorem."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(OUTPUT), "final_rows": kept,
                      "result_sha256": result["result_sha256"]},
                     sort_keys=True))


if __name__ == "__main__":
    main()
