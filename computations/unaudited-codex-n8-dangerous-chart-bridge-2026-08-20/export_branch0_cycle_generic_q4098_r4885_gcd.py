#!/usr/bin/env python3
"""Export exact and two-prime gcd checks for Q4098 and Cof43 R4885."""

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
TREE = HERE / "audit_branch0_cycle_generic_b3_resultant_tree.py"
FULL = HERE / "export_branch0_cycle_generic_azero_bzero_full_source_exact.py"
RESULT = HERE / "results_branch0_cycle_generic_q4098_r4885_gcd_export.json"
PRIMES = (1073741827, 1073741789, 0)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load("q4098_r4885_tree", TREE)
FULL_SOURCE = load("q4098_r4885_full", FULL)


def encode(poly: sp.Expr) -> str:
    return str(sp.expand(poly)).replace("**", "^")


def polynomial_sha(poly: sp.Expr, variables) -> str:
    primitive = sp.Poly(poly, *variables, domain="QQ").primitive()[1].as_expr()
    return sha256(encode(primitive).encode("ascii")).hexdigest()


def derive():
    rows, labels, _ = SOURCE.SOURCE.derive()
    b0, b1, b3, d1, d3, d4 = SOURCE.SOURCE.SOURCE.PARAMETERS
    variables = (b0, b1, d1, d3, d4)
    compact = [sp.cancel(poly/factor) for poly, factor in zip(
        rows, (b1*b3*d1*d3, d4, b3, b1*b3, 1, 1, 1), strict=True)]
    pivot = compact[1]
    leading = sp.diff(pivot, b3)
    constant = sp.expand(pivot.subs(b3, 0))
    r33 = SOURCE.linear_resultant(compact[5], b3, leading, constant)
    primitive33 = sp.Poly(r33, *variables).primitive()[1].as_expr()
    factors33 = sp.factor_list(primitive33)[1]
    profile33 = [(len(sp.Poly(f, *variables).terms()),
                  sp.Poly(f, *variables).total_degree(), int(e))
                 for f, e in factors33]
    require(profile33 == [(2, 2, 1), (1, 1, 2), (8, 4, 1), (4098, 26, 1)],
            "Cof(3,3) factor profile changed")
    c8 = next(f for f, e in factors33 if len(sp.Poly(f, *variables).terms()) == 8)
    q4098 = next(f for f, e in factors33
                 if len(sp.Poly(f, *variables).terms()) == 4098)

    lower, lower_hashes, *_ = FULL_SOURCE.derive_lower_cofactors()
    r43 = SOURCE.linear_resultant(lower[4], b3, leading, constant)
    primitive43 = sp.Poly(r43, *variables).primitive()[1].as_expr()
    factors43 = sp.factor_list(primitive43)[1]
    profile43 = [(len(sp.Poly(f, *variables).terms()),
                  sp.Poly(f, *variables).total_degree(), int(e))
                 for f, e in factors43]
    require(profile43 == [(2, 2, 1), (1, 1, 2), (8, 4, 1), (4885, 26, 1)],
            "Cof(4,3) factor profile changed")
    c8_43 = next(f for f, e in factors43
                 if len(sp.Poly(f, *variables).terms()) == 8)
    r4885 = next(f for f, e in factors43
                 if len(sp.Poly(f, *variables).terms()) == 4885)
    require(sp.expand(c8-c8_43) == 0 or sp.expand(c8+c8_43) == 0,
            "Cof(3,3)/Cof(4,3) quartic factors differ")
    require(sp.expand(q4098-r4885) != 0 and sp.expand(q4098+r4885) != 0,
            "degree-26 factors unexpectedly associate")
    return variables, q4098, r4885, lower_hashes[4], profile33, profile43


def main() -> None:
    variables, q4098, r4885, source_hash, profile33, profile43 = derive()
    files = []
    for prime in PRIMES:
        suffix = "char0" if prime == 0 else f"p{prime}"
        path = HERE / f"branch0_cycle_generic_q4098_r4885_gcd_{suffix}.sing"
        program = (
            f"ring K={prime},({','.join(map(str, variables))}),dp;\n"
            f"poly q={encode(q4098)};\n"
            f"poly r={encode(r4885)};\n"
            "poly g=gcd(q,r);\n"
            'print("BEGIN");print(size(g));print(deg(g));print(string(g));'
            'print("END");quit;\n')
        path.write_text(program)
        files.append({"characteristic": prime, "path": path.name,
                      "sha256": sha256(path.read_bytes()).hexdigest()})
    result = {
        "status": "UNAUDITED exact/two-prime Q4098-R4885 gcd export",
        "cofactor33_factor_profile": profile33,
        "cofactor43_factor_profile": profile43,
        "cofactor43_literal_source_sha256": source_hash,
        "q4098_sha256": polynomial_sha(q4098, variables),
        "r4885_sha256": polynomial_sha(r4885, variables),
        "programs": files,
        "scope": (
            "On A!=0, b3 is eliminated fraction-free. The already-closed C8 "
            "factor is removed only by its exact branch theorem, and frozen "
            "live b0^2*D0 factors are removed. gcd=1 certifies no shared "
            "hypersurface component, not emptiness of the codimension-two "
            "intersection Q4098=R4885=0."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("Q4098/R4885 gcd export: PASS")
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
