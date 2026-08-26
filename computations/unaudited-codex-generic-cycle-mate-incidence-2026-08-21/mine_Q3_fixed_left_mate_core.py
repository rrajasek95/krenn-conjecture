#!/usr/bin/env python3
"""Greedily mine and two-prime replay a Q3 fixed-left mate unit core."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
EXPORT = HERE / "results_Q3_fixed_left_mate_export.json"
OUT = HERE / "results_Q3_fixed_left_mate_core.json"
PRIMES = (1073741827, 1073741789)


def parse_input(path):
    lines = path.read_text().splitlines()
    variables = lines[0]
    prime = int(lines[1])
    body = "\n".join(lines[2:]).strip()
    rows = [row.strip() for row in body.split(",\n")]
    return variables, prime, rows


def write_input(path, variables, prime, ordinary, hrow):
    h_terms = hrow.split("+")
    rabinowitsch = "-1+"+"+".join(
        "u" if term == "1" else "u*"+term for term in h_terms)
    path.write_text(variables+f",u\n{prime}\n"
                    +",\n".join((*ordinary, rabinowitsch))+"\n")


def is_unit(variables, prime, ordinary, hrow, directory, counter):
    source = directory / f"trial_{counter}.msolve"
    output = directory / f"trial_{counter}.gb.out"
    write_input(source, variables, prime, ordinary, hrow)
    completed = subprocess.run(
        ["msolve", "-f", str(source), "-o", str(output), "-t", "4",
         "-g", "2", "-l", "2"],
        capture_output=True, text=True, timeout=15, check=False)
    if completed.returncode != 0 or not output.exists():
        raise RuntimeError(
            f"msolve trial {counter} failed rc={completed.returncode}: "
            f"stdout={completed.stdout[-500:]!r} stderr={completed.stderr[-500:]!r}")
    text = output.read_text()
    return "#length of basis:      1 element" in text and text.rstrip().endswith("[1]:")


def main():
    export = json.loads(EXPORT.read_text())
    aliases = export["generator_aliases"]
    path = HERE / "Q3_fixed_left_mate_p1073741827.msolve"
    variables, prime, rows = parse_input(path)
    ordinary, hrow = rows[:-1], rows[-1]
    if len(ordinary) != len(aliases):
        raise RuntimeError("Q3 mate label/input count changed")
    active = list(range(len(ordinary)))
    trials = []
    with tempfile.TemporaryDirectory(prefix="q3-mate-core-") as tmp:
        directory = Path(tmp)
        counter = 0
        for index in tuple(active):
            candidate = [value for value in active if value != index]
            counter += 1
            unit = is_unit(variables, prime,
                           [ordinary[value] for value in candidate], hrow,
                           directory, counter)
            trials.append({"removed_index": index,
                           "removed_aliases": aliases[index], "unit": unit})
            if unit:
                active = candidate
        # Inclusion-minimality replay after the greedy pass.
        mutations = []
        for index in active:
            candidate = [value for value in active if value != index]
            counter += 1
            unit = is_unit(variables, prime,
                           [ordinary[value] for value in candidate], hrow,
                           directory, counter)
            mutations.append({"removed_index": index,
                              "removed_aliases": aliases[index], "unit": unit})
        if any(record["unit"] for record in mutations):
            raise RuntimeError("greedy core failed inclusion-minimality replay")
    core_outputs = []
    for replay_prime in (0, *PRIMES):
        tag = "exact" if replay_prime == 0 else f"p{replay_prime}"
        replay_path = HERE / f"Q3_fixed_left_mate_core_{tag}.msolve"
        write_input(replay_path, variables, replay_prime,
                    [ordinary[value] for value in active], hrow)
        unit = None
        if replay_prime:
            with tempfile.TemporaryDirectory(prefix="q3-mate-replay-") as tmp:
                unit = is_unit(variables, replay_prime,
                               [ordinary[value] for value in active], hrow,
                               Path(tmp), 0)
            if not unit:
                raise RuntimeError(f"Q3 core failed replay at p{replay_prime}")
        core_outputs.append({
            "characteristic": replay_prime,
            "path": replay_path.name,
            "sha256": sha256(replay_path.read_bytes()).hexdigest(),
            "unit": unit,
        })
    result = {
        "status": "UNAUDITED two-prime inclusion-minimal Q3 mate core UNIT PASS",
        "active_indices": active,
        "active_aliases": [aliases[index] for index in active],
        "ordinary_row_count": len(active),
        "trials": trials,
        "minimality_mutations": mutations,
        "outputs": core_outputs,
        "scope": (
            "Greedy inclusion-minimal modular core for the nested minimal "
            "Q3-exception fixed-left incidence signature. This is discovery "
            "only until the compact rows are lifted to an exact-Q identity."
        ),
        "source_sha256": sha256(EXPORT.read_bytes()).hexdigest(),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("Q3 mate core mining PASS")
    print("core", len(active), [aliases[index][0] for index in active])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
