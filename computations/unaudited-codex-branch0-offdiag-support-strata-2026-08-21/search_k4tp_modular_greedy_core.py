#!/usr/bin/env python3
"""Deterministic greedy modular row-core discovery for k4 triangle-pendant."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import time


HERE = Path(__file__).resolve().parent
INPUT = Path("/tmp/k4tp_input.json")
OUT = HERE / "results_k4tp_mod1009_greedy_core.json"
ORDER = (13, 20, 11, 19, 14, 21, 12, 8, 7, 17, 9, 10, 15, 16, 18)
TIMEOUT = 40


def status(payload, dropped):
    kept = [(generator, label)
            for generator, label in zip(payload["generators"],
                                         payload["labels"])
            if label not in {"H", "AD"} | {str(value) for value in dropped}]
    generators = [generator for generator, _ in kept]
    names = [name for name in payload["variables"]
             if any(re.search(rf"\b{re.escape(name)}\b", generator)
                    for generator in generators)]
    command = (
        f"ring R=1009,({','.join(names)}),dp;"
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
        return "TIMEOUT", round(time.monotonic() - started, 6)
    elapsed = round(time.monotonic() - started, 6)
    lines = completed.stdout.splitlines()
    if completed.returncode or "BEGIN" not in lines or "END" not in lines:
        return "ERROR", elapsed
    body = lines[lines.index("BEGIN") + 1:lines.index("END")]
    return ("UNIT" if body[0] == "0" else "NONUNIT"), elapsed


def main():
    payload = json.loads(INPUT.read_text())
    dropped = set()
    records = []
    for candidate in ORDER:
        outcome, elapsed = status(payload, dropped | {candidate})
        if outcome == "UNIT":
            dropped.add(candidate)
        records.append({"candidate": candidate, "status": outcome,
                        "accepted": outcome == "UNIT",
                        "elapsed_seconds": elapsed,
                        "dropped_after": sorted(dropped)})
        print(records[-1], flush=True)
    kept = [value for value in range(6, 22) if value not in dropped]
    result = {
        "status": "UNAUDITED modular discovery greedy core",
        "prime": 1009,
        "timeout_seconds": TIMEOUT,
        "order": list(ORDER),
        "records": records,
        "kept_source_rows": kept,
        "dropped_source_rows": sorted(dropped),
        "always_kept_localizer": "B",
        "scope_guard": (
            "This is finite-field discovery only.  The final kept set is a "
            "characteristic-zero theorem only after an exact-Q replay."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("kept", kept)
    print("result sha256", result["result_sha256"])


if __name__ == "__main__":
    main()
