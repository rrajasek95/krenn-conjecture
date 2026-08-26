#!/usr/bin/env python3
"""Deterministic deletion census for the k4 triangle-pendant modular lead.

Discovery only: modular UNIT subsets guide a later exact-Q certificate.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import time


HERE = Path(__file__).resolve().parent
INPUT = Path("/tmp/k4tp_input.json")
OUT = HERE / "results_k4tp_mod1009_single_deletions.json"
PRIME = 1009
TIMEOUT = 45


def run_one(payload, omitted):
    kept = [(generator, label)
            for generator, label in zip(payload["generators"],
                                         payload["labels"])
            if label not in {"H", "AD", omitted}]
    generators = [generator for generator, _ in kept]
    names = [name for name in payload["variables"]
             if any(re.search(rf"\b{re.escape(name)}\b", generator)
                    for generator in generators)]
    command = (
        f"ring R={PRIME},({','.join(names)}),dp;"
        f"ideal I={','.join(generators)};ideal G=slimgb(I);"
        'print("BEGIN");print(string(reduce(1,G)));print(size(G));'
        'print(dim(G));print("END");quit;'
    )
    started = time.monotonic()
    try:
        completed = subprocess.run(
            ["Singular", "-q", "-c", command], text=True,
            capture_output=True, timeout=TIMEOUT, check=False,
        )
    except subprocess.TimeoutExpired:
        return {"omitted": omitted, "status": "TIMEOUT",
                "elapsed_seconds": round(time.monotonic() - started, 6)}
    elapsed = round(time.monotonic() - started, 6)
    lines = completed.stdout.splitlines()
    if completed.returncode or "BEGIN" not in lines or "END" not in lines:
        return {"omitted": omitted, "status": "ERROR",
                "elapsed_seconds": elapsed,
                "stderr_tail": completed.stderr[-500:]}
    body = lines[lines.index("BEGIN") + 1:lines.index("END")]
    return {"omitted": omitted,
            "status": "UNIT" if body[0] == "0" else "NONUNIT",
            "basis_size": int(body[1]), "dimension": int(body[2]),
            "elapsed_seconds": elapsed}


def main():
    payload = json.loads(INPUT.read_text())
    labels = [label for label in payload["labels"]
              if label not in {"H", "AD", "B"}]
    with ThreadPoolExecutor(max_workers=2) as pool:
        records = list(pool.map(lambda label: run_one(payload, label), labels))
    result = {
        "status": "UNAUDITED modular discovery deletion census",
        "prime": PRIME,
        "timeout_seconds": TIMEOUT,
        "base_generators": labels + ["B"],
        "records": records,
        "histogram": {
            status: sum(record["status"] == status for record in records)
            for status in ("UNIT", "NONUNIT", "TIMEOUT", "ERROR")
        },
        "scope_guard": (
            "UNIT is an exact finite-field subset statement.  Every other "
            "status is nonterminal, and no characteristic-zero conclusion "
            "is inferred from this discovery census."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("k4 triangle-pendant modular deletion census:",
          result["histogram"])
    for record in records:
        print(record)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
