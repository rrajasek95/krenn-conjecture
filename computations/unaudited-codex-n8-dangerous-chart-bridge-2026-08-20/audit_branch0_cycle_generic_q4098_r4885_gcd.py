#!/usr/bin/env python3
"""Replay exact and two-prime unit gcd outputs for Q4098/R4885."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
EXPORT = HERE / "results_branch0_cycle_generic_q4098_r4885_gcd_export.json"
RESULT = HERE / "results_branch0_cycle_generic_q4098_r4885_gcd_audit.json"
EXPECTED = "BEGIN\n1\n0\n1\nEND\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    export = json.loads(EXPORT.read_text())
    require(export["cofactor33_factor_profile"][-1] == [4098, 26, 1]
            and export["cofactor43_factor_profile"][-1] == [4885, 26, 1],
            "degree-26 factor profiles changed")
    outputs = []
    for record in export["programs"]:
        path = HERE / record["path"]
        require(sha256(path.read_bytes()).hexdigest() == record["sha256"],
                "frozen gcd program hash changed")
        completed = subprocess.run(["Singular", "-q", str(path)], text=True,
                                   capture_output=True, timeout=30, check=False)
        require(completed.returncode == 0 and completed.stdout == EXPECTED
                and completed.stderr == "", "gcd replay was not literal unit")
        outputs.append({"characteristic": record["characteristic"],
                        "literal_output": completed.stdout,
                        "output_sha256": sha256(completed.stdout.encode("ascii")).hexdigest()})
    result = {
        "status": "UNAUDITED exact/two-prime gcd unit replay",
        "q4098_sha256": export["q4098_sha256"],
        "r4885_sha256": export["r4885_sha256"],
        "outputs": outputs,
        "statement": (
            "gcd_Q(Q4098,R4885)=1, independently mirrored at two 30-bit "
            "primes. This proves no common hypersurface component, not "
            "emptiness of their multivariate intersection."),
        "scope_guard": export["scope"],
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("Q4098/R4885 gcd audit: PASS")
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
