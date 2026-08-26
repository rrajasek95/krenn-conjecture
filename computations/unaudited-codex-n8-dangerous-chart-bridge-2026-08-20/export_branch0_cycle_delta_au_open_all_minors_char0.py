#!/usr/bin/env python3
"""Export the all-minor exceptional scheme over Q with honest saturation.

The frozen prime-field seed uses msolve F4SAT: its last row is a saturating
factor rather than an equation.  In characteristic zero we replace that
contract by a literal Rabinowitsch equation ``z*live-1``.  The product is
expanded before export because msolve 0.10.1 silently misparses parentheses.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
import sys

_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))
import sympy as sp


HERE = Path(__file__).resolve().parent
TOOLKIT = HERE.parent / "toolkit" / "groebner"
SOURCE = HERE / "branch0_cycle_delta_au_open_all_minors_p1073741827.msolve"
OUTPUT = HERE / "branch0_cycle_delta_au_open_all_minors_char0.msolve"
RESULT = HERE / "results_branch0_cycle_delta_au_open_all_minors_char0_export.json"

if str(TOOLKIT) not in sys.path:
    sys.path.append(str(TOOLKIT))
from msolve_io import read_msolve_input, polynomial_sha256  # noqa: E402


def multiply_by_z(poly: str) -> str:
    """Parse exactly, distribute, and print coefficients before variables."""
    b0, b1, d1, x, z = sp.symbols("b0 b1 d1 x z")
    expression = sp.sympify(poly.replace("^", "**"), locals={
        "b0": b0, "b1": b1, "d1": d1, "x": x})
    result = str(sp.expand(z*expression-1)).replace("**", "^")
    # SymPy's canonical printer places every integer coefficient before its
    # monomial, avoiding a second msolve parser ambiguity such as z*2*x.
    if re.search(r"(?:^|[+\- ])z\*\d", result):
        raise RuntimeError("a coefficient remained after z")
    return result


def main() -> None:
    source = read_msolve_input(SOURCE, strict=True)
    if (source.characteristic != 1073741827 or
            source.variables != ("b0", "b1", "d1", "x") or
            len(source.polynomials) != 17):
        raise RuntimeError("the frozen prime-field all-minor seed changed")
    rabinowitsch = multiply_by_z(source.polynomials[-1])
    if any(token in rabinowitsch for token in ("(", ")", "**")):
        raise RuntimeError("the characteristic-zero row is not strict")
    lines = ["b0,b1,d1,x,z", "0"]
    rows = (*source.polynomials[:-1], rabinowitsch)
    lines.extend((row + ("," if index + 1 < len(rows) else ""))
                 for index, row in enumerate(rows))
    OUTPUT.write_text("\n".join(lines) + "\n")
    # Independent symbolic inverse: d/dz is exactly the frozen live factor,
    # and z=0 is exactly -1.
    b0, b1, d1, x, z = sp.symbols("b0 b1 d1 x z")
    rab_expr = sp.sympify(rabinowitsch.replace("^", "**"), locals={
        "b0": b0, "b1": b1, "d1": d1, "x": x, "z": z})
    live_expr = sp.sympify(source.polynomials[-1].replace("^", "**"),
                           locals={"b0": b0, "b1": b1, "d1": d1, "x": x})
    if sp.expand(sp.diff(rab_expr, z)-live_expr) != 0 \
            or sp.expand(rab_expr.subs(z, 0)+1) != 0:
        raise RuntimeError("Rabinowitsch expansion failed symbolic replay")
    result = {
        "status": "UNAUDITED exact characteristic-zero saturation export",
        "source_file": SOURCE.name,
        "source_file_sha256": source.file_sha256,
        "variables": ["b0", "b1", "d1", "x", "z"],
        "characteristic": 0,
        "row_count": len(rows),
        "source_equation_sha256": list(source.polynomial_sha256[:-1]),
        "saturating_factor_sha256": source.polynomial_sha256[-1],
        "rabinowitsch_sha256": polynomial_sha256(rabinowitsch),
        "output_file": OUTPUT.name,
        "output_file_sha256": sha256(OUTPUT.read_bytes()).hexdigest(),
        "scope": (
            "The first sixteen exact integer rows are unchanged. The final "
            "row is exactly z times the frozen live factor minus one. This "
            "is the characteristic-zero analogue of the prime-field F4SAT "
            "input; engine output still requires exact source replay."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("all-minor characteristic-zero export: PASS")
    print("output sha256:", result["output_file_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
