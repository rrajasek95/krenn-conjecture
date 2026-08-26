#!/usr/bin/env python3
"""Modular factor profile for the exact TP P26=0 boundary.

This is discovery only.  Each run saturates the same twelve exact closed
source rows by the base Laurent factor

    b0*b1*b3*d4*d5*(b1*d4+b0*d5)

and a selected subset of the four remaining live factors A3,A2,A4,A5.
The script emits strict, parenthesis-free msolve inputs and a deterministic
ledger.  UNIT at two primes does not imply characteristic-zero closure.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
EXPORTER = HERE / "export_branch0_triangle_pendant_p26_boundary_msolve.py"
OUT = HERE / "results_branch0_triangle_pendant_p26_factor_profile.json"
PRIMES = (1_073_741_827, 1_073_741_789)
NAMES = ("A3", "A2", "A4", "A5")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


E = load(EXPORTER, "n8_tp_p26_exporter")
D = E.D
C = E.C


def file_sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def is_unit_output(path: Path) -> bool:
    text = path.read_text().replace(" ", "").replace("\n", "")
    return text.endswith("[1]:") or text.endswith("[1]")


def run_one(indices: tuple[int, ...], prime: int, timeout: int = 90) -> dict:
    data = D.cramer_branch_system(7, 12)
    rows = [E.encode(poly) for _, poly in data["closed_rows"]]
    factors = data["closed_live_factors"]
    saturator = factors[0]
    for index in indices:
        saturator = C.multiply(saturator, factors[index + 1])
    suffix = "base" + "".join(f"_{NAMES[index]}" for index in indices)
    input_path = HERE / f"branch0_triangle_pendant_p26_{suffix}_p{prime}.msolve"
    output_path = HERE / f"results_branch0_triangle_pendant_p26_{suffix}_p{prime}.txt"
    input_path.write_text(E.msolve_text(E.VARIABLES,
                                        [*rows, E.encode(saturator)], prime))
    # Reuse the common strict parser before handing the file to msolve.
    toolkit = HERE.parent / "toolkit" / "groebner" / "msolve_io.py"
    io = load(toolkit, "n8_groebner_msolve_io")
    parsed = io.read_msolve_input(input_path, strict=True)
    command = ["msolve", "-f", str(input_path), "-S", "-g", "1",
               "-t", "2", "-v", "1", "-o", str(output_path)]
    started = time.monotonic()
    try:
        completed = subprocess.run(command, cwd=HERE, capture_output=True,
                                   text=True, timeout=timeout, check=False)
        status = "completed" if completed.returncode == 0 else "process_error"
        stdout = completed.stdout
        stderr = completed.stderr
        returncode = completed.returncode
    except subprocess.TimeoutExpired as error:
        status = "timeout"
        stdout = error.stdout.decode() if isinstance(error.stdout, bytes) else (error.stdout or "")
        stderr = error.stderr.decode() if isinstance(error.stderr, bytes) else (error.stderr or "")
        returncode = None
    elapsed = time.monotonic() - started
    unit = status == "completed" and output_path.exists() and is_unit_output(output_path)
    return {
        "subset": [NAMES[index] for index in indices],
        "prime": prime,
        "status": status,
        "unit": unit,
        "elapsed_seconds": elapsed,
        "returncode": returncode,
        "input": {"path": input_path.name, "sha256": file_sha(input_path),
                  "logical_sha256": parsed.logical_sha256},
        "output": ({"path": output_path.name, "sha256": file_sha(output_path)}
                   if output_path.exists() else None),
        "stdout_sha256": sha256(stdout.encode()).hexdigest(),
        "stderr_sha256": sha256(stderr.encode()).hexdigest(),
    }


def main() -> None:
    records = []
    # Small subsets first; once a subset is UNIT every strict superset is
    # mathematically redundant for minimal-factor discovery.
    unit_subsets: list[frozenset[int]] = []
    for size in range(5):
        for indices in itertools.combinations(range(4), size):
            chosen = frozenset(indices)
            if any(unit <= chosen for unit in unit_subsets):
                continue
            pair = [run_one(indices, prime) for prime in PRIMES]
            records.extend(pair)
            if all(record["unit"] for record in pair):
                unit_subsets.append(chosen)
            print(indices, [(record["status"], record["unit"],
                             round(record["elapsed_seconds"], 2))
                            for record in pair], flush=True)
    result = {
        "status": "UNAUDITED modular discovery only",
        "scope": "exact TP P26=0 closed rows, base live factor plus subsets",
        "primes": list(PRIMES),
        "remaining_factor_names": list(NAMES),
        "minimal_two_prime_unit_subsets": [
            [NAMES[index] for index in sorted(value)] for value in unit_subsets
        ],
        "records": records,
        "source_sha256": file_sha(Path(__file__)),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("result sha256", result["result_sha256"])


if __name__ == "__main__":
    main()
