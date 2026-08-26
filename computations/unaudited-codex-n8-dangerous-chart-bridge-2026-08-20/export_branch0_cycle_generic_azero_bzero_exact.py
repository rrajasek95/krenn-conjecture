#!/usr/bin/env python3
"""Canonical exact-Q input for the generic cycle A=B=0 pivot branch."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
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
CORE = HERE / "export_branch0_cycle_generic_cofactor33_core.py"
OUT = HERE / "branch0_cycle_generic_azero_bzero_exact.msolve"
RESULT = HERE / "results_branch0_cycle_generic_azero_bzero_export.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load(path: Path):
    spec = importlib.util.spec_from_file_location("generic_azero_bzero_source", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load(CORE)


def encode(poly: sp.Expr, variables: tuple[sp.Symbol, ...]) -> str:
    value = sp.Poly(sp.expand(poly), *variables, domain="ZZ")
    pieces: list[str] = []
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
    rows, labels, metadata = SOURCE.derive()
    source_rows = tuple(rows[:6])
    b0, b1, b3, d1, d3, d4 = SOURCE.SOURCE.PARAMETERS
    normalized_t013 = sp.cancel(source_rows[1]/d4)
    leading = sp.diff(normalized_t013, b3)
    constant = sp.expand(normalized_t013.subs(b3, 0))
    require(sp.expand(normalized_t013-leading*b3-constant) == 0,
            "t013 affine identity changed")
    a_divisor = sp.cancel(leading/(2*b0))
    b_polynomial = sp.cancel(constant/2)
    require(len(sp.Poly(a_divisor, b0, b1, d1, d3, d4).terms()) == 19
            and len(sp.Poly(b_polynomial, b0, b1, d1, d3, d4).terms()) == 44,
            "A/B profiles changed")
    delta = b1*d3+b3*d1*d4
    d0 = d1*d4+d3
    bplus = b1+d1
    live = sp.expand(b0*b1*b3*d1*d3*d4*delta*d0*bplus)
    z = sp.Symbol("z")
    variables = (*SOURCE.SOURCE.PARAMETERS, z)
    generators = (*source_rows, a_divisor, b_polynomial, sp.expand(z*live-1))
    OUT.write_text(
        ",".join(map(str, variables)) + "\n0\n"
        + ",\n".join(encode(poly, variables) for poly in generators) + "\n")
    body = OUT.read_text().split("\n", 2)[2]
    require("(" not in body and "**" not in body,
            "canonical msolve syntax guard failed")
    result = {
        "status": "UNAUDITED exact-Q generic cycle A=B=0 export",
        "input": OUT.name,
        "input_sha256": sha256(OUT.read_bytes()).hexdigest(),
        "variables": [str(v) for v in variables],
        "source_row_labels": labels[:6],
        "source_omitted_sha256": metadata["omitted_sha256"],
        "extra_rows": ["A", "B"],
        "a_terms_degree": [19, 6],
        "b_terms_degree": [44, 7],
        "localized_factors": ["b0", "b1", "b3", "d1", "d3", "d4",
                              "Delta", "D0", "Bplus"],
        "scope": (
            "Direct generic cycle source core on A=B=0, localized only at "
            "b0*b1*b3*d1*d3*d4*Delta*D0*Bplus. A is not localized. The "
            "A-open Q4098 branch is out of scope."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("generic A=B=0 exact export: PASS")
    print("input sha256:", result["input_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
