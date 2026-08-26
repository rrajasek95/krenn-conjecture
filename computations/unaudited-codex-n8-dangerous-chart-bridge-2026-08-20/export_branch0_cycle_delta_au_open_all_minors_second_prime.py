#!/usr/bin/env python3
"""Rebase the strict exact-row all-minor seed at a second 30-bit prime."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
TOOLKIT = HERE.parent / "toolkit" / "groebner"
SOURCE = HERE / "branch0_cycle_delta_au_open_all_minors_p1073741827.msolve"
OUTPUT = HERE / "branch0_cycle_delta_au_open_all_minors_p1073741789.msolve"
RESULT = HERE / "results_branch0_cycle_delta_au_open_all_minors_second_prime.json"
PRIME = 1073741789

if str(TOOLKIT) not in sys.path:
    sys.path.append(str(TOOLKIT))
from msolve_io import read_msolve_input  # noqa: E402


def main():
    source = read_msolve_input(SOURCE, strict=True)
    if source.characteristic != 1073741827 or len(source.polynomials) != 17:
        raise RuntimeError("the frozen exact-row source seed changed")
    lines = SOURCE.read_text().splitlines()
    lines[1] = str(PRIME)
    OUTPUT.write_text("\n".join(lines) + "\n")
    output = read_msolve_input(OUTPUT, strict=True)
    if (output.characteristic != PRIME or
            output.variables != source.variables or
            output.polynomial_sha256 != source.polynomial_sha256):
        raise RuntimeError("second-prime rebasing changed a literal row")
    result = {
        "status": "UNAUDITED strict second-prime exact-row rebase",
        "source_file": SOURCE.name,
        "source_file_sha256": source.file_sha256,
        "prime": PRIME,
        "output_file": OUTPUT.name,
        "output_file_sha256": output.file_sha256,
        "output_logical_sha256": output.logical_sha256,
        "row_sha256": list(output.polynomial_sha256),
        "scope": (
            "The exact integer all-minor rows are byte-identical except for "
            "the characteristic line. Modular discovery only."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("all-minor second-prime rebase: PASS")
    print("output sha256:", result["output_file_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
