#!/usr/bin/env python3
"""Drop only the final F4SAT row from the corrected modular core."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRIMES = (1073741827, 1073741789)
SOURCE_RESULT = HERE / "results_branch0_cycle_generic_codim5_corrected_delta_modular_export.json"
RESULT = HERE / "results_branch0_cycle_generic_codim5_corrected_ordinary_core_export.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    source_result = json.loads(SOURCE_RESULT.read_text())
    expected = {row["prime"]: row for row in source_result["outputs"]}
    outputs = []
    for prime in PRIMES:
        source = HERE / f"branch0_cycle_generic_qrstu_codim5_corrected_p{prime}.msolve"
        require(sha256(source.read_bytes()).hexdigest() == expected[prime]["sha256"],
                "corrected modular source hash changed")
        lines = source.read_text().splitlines()
        require(lines[:2] == ["b0,b1,d1,d3,d4", str(prime)],
                "corrected modular header changed")
        rows = "\n".join(lines[2:]).strip().split(",\n")
        require(len(rows) == 10, "corrected modular row count changed")
        target = HERE / f"branch0_cycle_generic_qrstu_codim5_corrected_ordinary_p{prime}.msolve"
        target.write_text(lines[0]+"\n"+lines[1]+"\n"
                          +",\n".join(rows[:-1])+"\n")
        require("(" not in target.read_text() and "**" not in target.read_text(),
                "ordinary core strict syntax guard failed")
        outputs.append({
            "prime": prime,
            "source": source.name,
            "source_sha256": expected[prime]["sha256"],
            "path": target.name,
            "sha256": sha256(target.read_bytes()).hexdigest(),
            "row_count": len(rows)-1,
            "removed_final_row_sha256": sha256(rows[-1].encode("ascii")).hexdigest(),
        })
    result = {
        "status": "UNAUDITED corrected codim-five ordinary-core export",
        "source_result": SOURCE_RESULT.name,
        "source_result_sha256": sha256(SOURCE_RESULT.read_bytes()).hexdigest(),
        "outputs": outputs,
        "scope": (
            "The first nine corrected source-resultant rows are preserved "
            "byte-logically; only the verified final F4SAT live-product row "
            "is removed. Intended for modular radical-membership discovery."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("corrected codim-five ordinary-core export: PASS")
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
