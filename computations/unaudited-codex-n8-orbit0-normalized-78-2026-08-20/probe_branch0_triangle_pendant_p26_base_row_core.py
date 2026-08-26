#!/usr/bin/env python3
"""Greedy modular source-row core for the minimal TP P26 base chart.

Every trial uses native F4SAT with the exact base Laurent factor as the final
row.  A deletion is accepted only when saturation is UNIT at the discovery
prime.  The final core is replayed at a second prime.  This is a complexity
reduction for exact lifting, not a characteristic-zero certificate.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
EXPORTER = HERE / "export_branch0_triangle_pendant_p26_boundary_msolve.py"
OUT = HERE / "results_branch0_triangle_pendant_p26_base_row_core.json"
PRIME = 1_073_741_827
PRIME2 = 1_073_741_789
DELETE_ORDER = (21, 13, 11, 17, 19, 15, 8, 7, 9, 10, 12, 101)


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


E = load(EXPORTER, "n8_tp_p26_exporter_row_core")
D = E.D


def file_sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def is_unit(path: Path) -> bool:
    text = path.read_text().replace(" ", "").replace("\n", "")
    return text.endswith("[1]:") or text.endswith("[1]")


def run(labels: tuple[int, ...], prime: int, tag: str) -> dict:
    data = D.cramer_branch_system(7, 12)
    row_map = {label: E.encode(poly) for label, poly in data["closed_rows"]}
    base = E.encode(data["closed_live_factors"][0])
    input_path = HERE / f"branch0_triangle_pendant_p26_base_core_{tag}_p{prime}.msolve"
    output_path = HERE / f"results_branch0_triangle_pendant_p26_base_core_{tag}_p{prime}.txt"
    input_path.write_text(E.msolve_text(E.VARIABLES,
                                        [*(row_map[label] for label in labels),
                                         base], prime))
    # Strict common parser, including the parenthesis/** regression.
    io = load(HERE.parent / "toolkit" / "groebner" / "msolve_io.py",
              f"n8_groebner_io_{tag}_{prime}")
    parsed = io.read_msolve_input(input_path, strict=True)
    command = ["msolve", "-f", str(input_path), "-S", "-g", "1",
               "-t", "2", "-v", "1", "-o", str(output_path)]
    started = time.monotonic()
    try:
        completed = subprocess.run(command, cwd=HERE, capture_output=True,
                                   text=True, check=False, timeout=90)
        status = "completed" if completed.returncode == 0 else "process_error"
        returncode = completed.returncode
    except subprocess.TimeoutExpired:
        status, returncode = "timeout", None
    elapsed = time.monotonic() - started
    return {
        "labels": list(labels), "prime": prime, "tag": tag,
        "status": status,
        "unit": status == "completed" and output_path.exists() and is_unit(output_path),
        "returncode": returncode, "elapsed_seconds": elapsed,
        "input_path": input_path.name, "input_sha256": file_sha(input_path),
        "input_logical_sha256": parsed.logical_sha256,
        "output_path": output_path.name if output_path.exists() else None,
        "output_sha256": file_sha(output_path) if output_path.exists() else None,
    }


def main() -> None:
    data = D.cramer_branch_system(7, 12)
    current = tuple(label for label, _ in data["closed_rows"])
    if set(current) != set(DELETE_ORDER):
        raise RuntimeError((current, DELETE_ORDER))
    records = []
    for label in DELETE_ORDER:
        candidate = tuple(value for value in current if value != label)
        record = run(candidate, PRIME, f"omit_{label}")
        records.append(record)
        if record["unit"]:
            current = candidate
        print("omit", label, record["status"], record["unit"],
              round(record["elapsed_seconds"], 2), "keep", current,
              flush=True)
    replay = run(current, PRIME2, "final")
    records.append(replay)
    print("second prime", replay["status"], replay["unit"],
          round(replay["elapsed_seconds"], 2), flush=True)
    result = {
        "status": "UNAUDITED modular discovery only",
        "scope": "exact TP P26=0 rows saturated by base F0",
        "delete_order": list(DELETE_ORDER),
        "final_labels": list(current),
        "final_second_prime_unit": replay["unit"],
        "records": records,
        "source_sha256": file_sha(Path(__file__)),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("result sha256", result["result_sha256"])


if __name__ == "__main__":
    main()
