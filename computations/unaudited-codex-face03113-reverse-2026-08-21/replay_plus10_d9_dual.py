#!/usr/bin/env python3
"""Replay the p=1009 degree-9 dual for base12 plus raw Cof(0,0)."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
CORE = HERE / "face03113_plus10_d9_core.jsonl"
SOLVE = HERE / "results_face03113_plus10_d9_p1009.json"
RESULT_PREFIX = HERE / "results_plus10_d9_dual_replay"
PRIME = 1009
EXTRA = 10
CORE_SHA = "a44099a42dabb33bff215c0475baad5aa30c84b897c5331745b0e3960e643ea5"
SOLVE_SHA = "5131cd0a6efbb0048e7a3c30efa6d13efcd9872152127220f84691e1e5e4bf0c"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def mathematical_digest(path):
    hasher = sha256()
    with path.open() as source:
        header = json.loads(next(source))
        stable = {key: header[key] for key in
                  ("row_count", "column_count", "target", "variables",
                   "kept_raw_rows", "generators")}
        hasher.update(json.dumps(stable, sort_keys=True,
                                 separators=(",", ":")).encode())
        for line in source:
            if line.strip():
                record = json.loads(line)
                stable_column = {key: record[key] for key in
                                 ("index", "source_label", "source_degree",
                                  "multiplier", "entries")}
                hasher.update(json.dumps(stable_column, sort_keys=True,
                                         separators=(",", ":")).encode())
    return hasher.hexdigest()


def rebuild_source_interface():
    mac = REPO / "computations/unaudited-codex-face03113-macaulay-2026-08-21"
    with tempfile.TemporaryDirectory(prefix="face03113-plus10-replay-") as temp:
        temp = Path(temp)
        full = temp / "full.jsonl"
        filtered = temp / "filtered.jsonl"
        core = temp / "core.jsonl"
        commands = [
            [sys.executable, str(mac / "export_face03113_macaulay.py"),
             "--degree", "9", "--full-rows", "--output", str(full)],
            [sys.executable, str(HERE / "filter_d9_extra_rows.py"),
             str(full), str(filtered), "--extra", str(EXTRA)],
            [sys.executable, str(mac / "peel_target_component.py"),
             str(filtered), str(core)],
        ]
        for command in commands:
            completed = subprocess.run(command, cwd=REPO, text=True,
                                       capture_output=True, check=False)
            require(completed.returncode == 0,
                    f"source rebuild failed: {completed.stderr[-500:]}")
        rebuilt_math = mathematical_digest(core)
        frozen_math = mathematical_digest(CORE)
        require(rebuilt_math == frozen_math,
                "source-rebuilt peeled core mathematics changed")
        return {"file_sha256_full_filtered_core":
                    [sha(full), sha(filtered), sha(core)],
                "mathematical_core_sha256": rebuilt_math}


def replay(mode):
    require(sha(CORE) == CORE_SHA and sha(SOLVE) == SOLVE_SHA,
            "frozen input digest changed")
    solve = json.loads(SOLVE.read_text())
    dual = {int(index): int(coefficient) % PRIME
            for index, coefficient in solve["left_dual"]}
    with CORE.open() as source:
        header = json.loads(next(source))
        columns = [json.loads(line) for line in source if line.strip()]
    require(len(columns) == header["column_count"] == solve["column_count"]
            and header["row_count"] == solve["row_count"],
            "peeled core shape changed")
    if mode == "-O":
        columns = list(reversed(columns))
        for column in columns:
            column["entries"] = list(reversed(column["entries"]))
    nonzero = []
    hostile_delta = None
    for column in columns:
        pairing = sum(coefficient*dual.get(row, 0)
                      for row, coefficient in column["entries"]) % PRIME
        if pairing:
            nonzero.append([column["index"], pairing])
        if hostile_delta is None:
            for row, _ in column["entries"]:
                if dual.get(row, 0):
                    hostile_delta = dual[row]
                    break
    target_pairing = sum(numerator*dual.get(row, 0)
                         for row, numerator, denominator in header["target"]
                         if denominator == 1) % PRIME
    require(not nonzero and target_pairing ==
            solve["left_dual_target_pairing"] % PRIME,
            "dual annihilation/target pairing failed")
    require(hostile_delta not in (None, 0),
            "hostile coefficient mutation did not fire")
    rebuilt = rebuild_source_interface() if mode == "-I-S" else None
    result = {
        "status": "UNAUDITED modular d9 dual replay PASS",
        "mode": mode, "prime": PRIME,
        "row_count": header["row_count"],
        "column_count": header["column_count"],
        "rank_reported": solve["rank"],
        "target_in_image_reported": solve["target_in_image"],
        "dual_terms": len(dual),
        "nonzero_column_pairings": len(nonzero),
        "target_pairing": target_pairing,
        "hostile_mutation_pairing": hostile_delta,
        "source_rebuild_sha256_full_filtered_core": rebuilt,
        "core_sha256": CORE_SHA, "solve_sha256": SOLVE_SHA,
        "scope_guard": ("This proves target nonmembership only in the "
                        "p=1009 homogeneous degree-9 component. It is not "
                        "an affine or characteristic-zero nonunit theorem."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    suffix = {"standard": "standard", "-O": "O", "-I-S": "I-S"}[mode]
    output = Path(str(RESULT_PREFIX) + "_" + suffix + ".json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(mode, "PASS", result["result_sha256"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("standard", "-O", "-I-S"),
                        default="standard")
    args = parser.parse_args()
    replay(args.mode)


if __name__ == "__main__":
    main()
