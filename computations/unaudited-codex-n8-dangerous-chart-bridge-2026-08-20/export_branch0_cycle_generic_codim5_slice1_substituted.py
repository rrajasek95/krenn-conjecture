#!/usr/bin/env python3
"""Losslessly eliminate the first generic slice linear form with Singular."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
PRIMES = (1073741827, 1073741789)
RESULT = HERE / "results_branch0_cycle_generic_codim5_slice1_substituted.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    outputs = []
    for prime in PRIMES:
        source = HERE / f"branch0_cycle_generic_codim5_slice1_p{prime}.msolve"
        lines = source.read_text().splitlines()
        require(lines[:2] == ["b0,b1,d1,d3,d4", str(prime)],
                "slice1 header changed")
        rows = "\n".join(lines[2:]).strip().split(",\n")
        require(len(rows) == 11, "slice1 row count changed")
        require(rows[9] == "b0+2*b1+3*d1+5*d3+7*d4-11",
                "first slice linear form changed")
        retained = [*rows[:9], rows[10]]
        program = (
            f"ring R={prime},(b0,b1,d1,d3,d4),dp;\n"
            f"ideal I={','.join(retained)};\n"
            f"ring S={prime},(b1,d1,d3,d4),dp;\n"
            "map phi=R,11-2*b1-3*d1-5*d3-7*d4,b1,d1,d3,d4;\n"
            "ideal J=phi(I);\n"
            'print("BEGIN_ROWS");\n'
            'for(int i=1;i<=size(J);i++){print(string(J[i]));print("ROW_END");};\n'
            'print("END_ROWS");quit;\n')
        completed = subprocess.run(["Singular", "-q", "-c", program],
                                   text=True, capture_output=True,
                                   timeout=300, check=False)
        require(completed.returncode == 0 and not completed.stderr,
                "Singular slice substitution failed")
        middle = completed.stdout.split("BEGIN_ROWS\n", 1)[1] \
            .split("END_ROWS", 1)[0]
        substituted = [value.strip() for value in middle.split("ROW_END\n")
                       if value.strip()]
        require(len(substituted) == 10, "substituted row count changed")
        require(all("b0" not in row and "(" not in row and "**" not in row
                    for row in substituted),
                "strict substituted syntax guard failed")
        target = HERE / f"branch0_cycle_generic_codim5_slice1_sub_p{prime}.msolve"
        target.write_text("b1,d1,d3,d4\n" + str(prime) + "\n"
                          + ",\n".join(substituted) + "\n")
        # Native F4SAT consumes the mapped live product as the final row.
        require(substituted[-1] != "0" and substituted[-1] != "1",
                "mapped live product collapsed")
        outputs.append({
            "prime": prime,
            "source": source.name,
            "source_sha256": sha256(source.read_bytes()).hexdigest(),
            "path": target.name,
            "sha256": sha256(target.read_bytes()).hexdigest(),
            "row_count": len(substituted),
        })
    result = {
        "status": "UNAUDITED lossless modular slice1 substitution",
        "substitution": "b0=11-2*b1-3*d1-5*d3-7*d4",
        "outputs": outputs,
        "scope": (
            "Exact finite-field quotient by the declared generic affine "
            "slice. The nine necessary rows and final F4SAT live product are "
            "mapped by a literal Singular ring map; modular results remain "
            "discovery evidence only."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("codim-five slice1 substitution: PASS")
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
