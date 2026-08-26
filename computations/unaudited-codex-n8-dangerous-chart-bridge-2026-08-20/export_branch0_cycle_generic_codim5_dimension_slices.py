#!/usr/bin/env python3
"""Export deterministic large-prime generic slices of the codim-five core.

The nine necessary-core rows are copied byte-logically from the exact
coefficient-first input.  Its expanded Rabinowitsch row z*L-1 is divided
exactly to recover the declared live product L; native msolve F4SAT receives
L as the final row.  Slice results remain modular geometry discovery.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys

_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))
import sympy as sp


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "branch0_cycle_generic_qrstu_codim5_exact.msolve"
RESULT = HERE / "results_branch0_cycle_generic_codim5_dimension_slices.json"
PRIMES = (1073741827, 1073741789)
SLICES = (
    None,
    (1, 2, 3, 5, 7, -11),
    (2, -3, 5, -7, 11, 13),
    (3, 5, -7, 11, -13, 17),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def encode(poly: sp.Expr, variables: tuple[sp.Symbol, ...]) -> str:
    value = sp.Poly(sp.expand(poly), *variables, domain="ZZ")
    pieces = []
    for monomial, coefficient in value.terms():
        coefficient = int(coefficient)
        factors = [] if abs(coefficient) == 1 else [str(abs(coefficient))]
        for variable, power in zip(variables, monomial, strict=True):
            if power:
                factors.append(str(variable) if power == 1
                               else f"{variable}^{power}")
        body = "*".join(factors) or "1"
        pieces.append(("-" if coefficient < 0 else ("+" if pieces else ""))
                      + body)
    return "".join(pieces) or "0"


def main() -> None:
    lines = SOURCE.read_text().splitlines()
    require(lines[1] == "0", "source is no longer characteristic zero")
    source_variables = tuple(sp.symbols(lines[0]))
    require(tuple(map(str, source_variables)) ==
            ("b0", "b1", "d1", "d3", "d4", "z"),
            "source variable order changed")
    variables = source_variables[:-1]
    z = source_variables[-1]
    body = "\n".join(lines[2:]).strip()
    require(body.endswith(",") is False, "unexpected trailing comma")
    encoded_rows = [row.strip() for row in body.split(",\n")]
    require(len(encoded_rows) == 10, "codim-five row count changed")
    local = {str(variable): variable for variable in source_variables}
    rows = [sp.sympify(row.replace("^", "**"), locals=local)
            for row in encoded_rows]
    require(all(not row.has(z) for row in rows[:-1]),
            "z leaked into necessary-core rows")
    live = sp.cancel((rows[-1] + 1)/z)
    require(not live.has(z) and sp.expand(z*live-1-rows[-1]) == 0,
            "expanded Rabinowitsch row did not recover live product")
    outputs = []
    linear_rows = []
    for coefficients in SLICES[1:]:
        linear_rows.append(sp.expand(sum(coefficient*variable
                                         for coefficient, variable
                                         in zip(coefficients[:5], variables))
                                     + coefficients[5]))
    for prime in PRIMES:
        for slice_count in (0, 1, 2, 3):
            path = HERE / (f"branch0_cycle_generic_codim5_slice{slice_count}_"
                           f"p{prime}.msolve")
            equations = [*rows[:-1], *linear_rows[:slice_count], live]
            path.write_text(
                ",".join(map(str, variables)) + f"\n{prime}\n"
                + ",\n".join(encode(row, variables) for row in equations)
                + "\n")
            payload = path.read_text().split("\n", 2)[2]
            require("(" not in payload and "**" not in payload,
                    "strict msolve syntax guard failed")
            outputs.append({
                "prime": prime, "slice_count": slice_count,
                "path": path.name, "sha256": sha256(path.read_bytes()).hexdigest(),
                "row_count": len(equations),
            })
    result = {
        "status": "UNAUDITED modular codim-five dimension-slice interface",
        "source": SOURCE.name,
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "core_row_count": 9,
        "variables": list(map(str, variables)),
        "slice_coefficients": [list(value) for value in SLICES[1:]],
        "outputs": outputs,
        "scope": (
            "Native F4SAT treats the final row as the exact declared live "
            "product. Generic affine slices are deterministic modular "
            "geometry probes only; matching primes do not prove a char0 "
            "dimension or source theorem."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("codim-five dimension slices: PASS")
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
