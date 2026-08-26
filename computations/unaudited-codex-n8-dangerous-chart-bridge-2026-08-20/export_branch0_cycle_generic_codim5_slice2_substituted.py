#!/usr/bin/env python3
"""Losslessly eliminate both deterministic generic-slice linears."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
PRIMES = (1073741827, 1073741789)
RESULT = HERE / "results_branch0_cycle_generic_codim5_slice2_substituted.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    outputs = []
    for prime in PRIMES:
        source = HERE / f"branch0_cycle_generic_codim5_slice2_p{prime}.msolve"
        lines = source.read_text().splitlines()
        require(lines[:2] == ["b0,b1,d1,d3,d4", str(prime)],
                "slice2 header changed")
        rows = "\n".join(lines[2:]).strip().split(",\n")
        require(len(rows) == 12, "slice2 row count changed")
        require(rows[9] == "b0+2*b1+3*d1+5*d3+7*d4-11"
                and rows[10] == "2*b0-3*b1+5*d1-7*d3+11*d4+13",
                "slice2 linear forms changed")
        retained = [*rows[:9], rows[11]]
        # Solving L1=L2=0 gives
        # b1=(35-d1-17*d3-3*d4)/7 and
        # b0=11-2*b1-3*d1-5*d3-7*d4.
        b1_value = "(35-d1-17*d3-3*d4)/7"
        b0_value = f"11-2*({b1_value})-3*d1-5*d3-7*d4"
        program = (
            f"ring R={prime},(b0,b1,d1,d3,d4),dp;\n"
            f"ideal I={','.join(retained)};poly L1={rows[9]};poly L2={rows[10]};\n"
            f"ring S={prime},(d1,d3,d4),dp;\n"
            f"map phi=R,{b0_value},{b1_value},d1,d3,d4;\n"
            "ideal J=phi(I);poly check1=phi(L1);poly check2=phi(L2);\n"
            'if(check1!=0||check2!=0){print("MAP_FAILURE");quit;};\n'
            'print("BEGIN_ROWS");\n'
            'for(int i=1;i<=size(J);i++){print(string(J[i]));print("ROW_END");};\n'
            'print("END_ROWS");quit;\n')
        completed = subprocess.run(["Singular", "-q", "-c", program],
                                   text=True, capture_output=True,
                                   timeout=300, check=False)
        require(completed.returncode == 0 and not completed.stderr
                and "MAP_FAILURE" not in completed.stdout,
                "Singular slice2 substitution failed")
        middle = completed.stdout.split("BEGIN_ROWS\n", 1)[1] \
            .split("END_ROWS", 1)[0]
        substituted = [value.strip() for value in middle.split("ROW_END\n")
                       if value.strip()]
        require(len(substituted) == 10, "substituted row count changed")
        require(all("b0" not in row and "b1" not in row and "(" not in row
                    and "**" not in row for row in substituted),
                "strict substituted syntax guard failed")
        target = HERE / f"branch0_cycle_generic_codim5_slice2_sub_p{prime}.msolve"
        target.write_text("d1,d3,d4\n" + str(prime) + "\n"
                          + ",\n".join(substituted) + "\n")
        require(substituted[-1] not in ("0", "1"),
                "mapped live product collapsed")
        outputs.append({
            "prime": prime, "source": source.name,
            "source_sha256": sha256(source.read_bytes()).hexdigest(),
            "path": target.name,
            "sha256": sha256(target.read_bytes()).hexdigest(),
            "row_count": len(substituted),
        })
    result = {
        "status": "UNAUDITED lossless modular slice2 substitution",
        "substitution": {
            "b1": "(35-d1-17*d3-3*d4)/7",
            "b0": "11-2*b1-3*d1-5*d3-7*d4",
        },
        "outputs": outputs,
        "scope": (
            "Exact finite-field quotient by the first two declared generic "
            "affine slices. Both linears are must-fire mapped to zero and the "
            "nine necessary rows plus final live product are retained. "
            "Modular geometry only."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("codim-five slice2 substitution: PASS")
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
