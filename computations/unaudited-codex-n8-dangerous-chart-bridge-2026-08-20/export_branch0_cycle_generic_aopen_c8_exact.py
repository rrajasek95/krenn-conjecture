#!/usr/bin/env python3
"""Export the exact-Q A-open/C8 generic-cycle source core."""

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
OUT = HERE / "branch0_cycle_generic_aopen_c8_exact.sing"
OUT_MSOLVE = HERE / "branch0_cycle_generic_aopen_c8_exact.msolve"
RESULT = HERE / "results_branch0_cycle_generic_aopen_c8_export.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load(path: Path):
    spec = importlib.util.spec_from_file_location("generic_aopen_c8_source", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load(CORE)


def singular(poly: sp.Expr) -> str:
    return str(sp.expand(poly)).replace("**", "^")


def coefficient_first(poly: sp.Expr,
                      variables: tuple[sp.Symbol, ...]) -> str:
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
    source_rows = rows[:6]
    source_labels = labels[:6]
    b0, b1, b3, d1, d3, d4 = SOURCE.SOURCE.PARAMETERS
    # The exact t013 affine pivot divisor and its Cof(3,3) resultant quartic.
    normalized_t013 = sp.cancel(source_rows[1]/d4)
    leading = sp.diff(normalized_t013, b3)
    constant = sp.expand(normalized_t013.subs(b3, 0))
    require(sp.expand(normalized_t013-leading*b3-constant) == 0,
            "t013 affine pivot changed")
    a_divisor = sp.cancel(leading/(2*b0))
    require(len(sp.Poly(a_divisor, b0, b1, d1, d3, d4).terms()) == 19,
            "A divisor profile changed")
    c8 = (b0**2*d1*d3-b0**2*d3-b0*d1*d3*d4-b0*d1*d3
          -b0*d1*d4-b0*d3*d4-d1*d3*d4+d1*d4**2)
    require(len(sp.Poly(c8, b0, b1, d1, d3, d4).terms()) == 8,
            "C8 quartic profile changed")
    delta = b1*d3+b3*d1*d4
    d0 = d1*d4+d3
    bplus = b1+d1
    live = sp.expand(b0*b1*b3*d1*d3*d4*delta*d0*bplus*a_divisor)
    z = sp.Symbol("z")
    localizer = sp.expand(z*live-1)
    variables = (*SOURCE.SOURCE.PARAMETERS, z)
    generators = (*source_rows, c8, localizer)
    program = (
        f"ring R=0,({','.join(map(str, variables))}),dp;\n"
        f"ideal I={','.join(singular(poly) for poly in generators)};\n"
        "option(redSB);\n"
        "ideal G=slimgb(I);\n"
        'print("BEGIN");\n'
        'print("REDUCE_ONE");print(string(reduce(1,G)));\n'
        'print("SIZE");print(size(G));\n'
        'print("DIM");print(dim(G));\n'
        'print("FIRST");if(size(G)>0){print(string(G[1]));};\n'
        'print("END");quit;\n')
    OUT.write_text(program)
    OUT_MSOLVE.write_text(
        ",".join(map(str, variables)) + "\n0\n"
        + ",\n".join(coefficient_first(poly, variables)
                      for poly in generators) + "\n")
    require("(" not in OUT_MSOLVE.read_text()
            and "**" not in OUT_MSOLVE.read_text(),
            "canonical msolve export contains forbidden syntax")
    result = {
        "status": "UNAUDITED exact-Q A-open/C8 source-core export",
        "input": OUT.name,
        "input_sha256": sha256(OUT.read_bytes()).hexdigest(),
        "msolve_input": OUT_MSOLVE.name,
        "msolve_input_sha256": sha256(OUT_MSOLVE.read_bytes()).hexdigest(),
        "variables": [str(v) for v in variables],
        "source_row_labels": source_labels,
        "source_row_count": len(source_rows),
        "source_core_omitted_sha256": metadata["omitted_sha256"],
        "extra_equation": "C8",
        "c8": str(c8),
        "c8_sha256": sha256(singular(c8).encode("ascii")).hexdigest(),
        "localized_factors": ["b0", "b1", "b3", "d1", "d3", "d4",
                              "Delta", "D0", "Bplus", "A"],
        "a_terms_degree": [19, 6],
        "live_product_terms": len(sp.Poly(live, *SOURCE.SOURCE.PARAMETERS).terms()),
        "scope": (
            "Only the generic Delta,D0,Bplus-open cycle chart with A!=0 and "
            "C8=0. The six frozen source-derived rows are imposed directly; "
            "no b3 resultants replace them. Q4098 and A=0 remain out of scope."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("generic A-open/C8 exact export: PASS")
    print("input sha256:", result["input_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
