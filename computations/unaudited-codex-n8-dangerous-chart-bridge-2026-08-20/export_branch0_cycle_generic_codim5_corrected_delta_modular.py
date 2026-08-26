#!/usr/bin/env python3
"""Export the corrected-Delta modular codim-five full core.

The characteristic-zero source input uses a Rabinowitsch inverse.  This
exporter recovers its exact live product, proves that it contains the true
cleared Cramer Delta ``b0*A*b1*d3-B*d1*d4``, fires a hostile dropped-``b0``
mutation, and places the verified product in msolve's final F4SAT row.
"""

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
SOURCE = HERE / "branch0_cycle_generic_qrstu_codim5_exact.msolve"
SOURCE_EXPORTER = HERE / "export_branch0_cycle_generic_qrs_codim3_exact.py"
TREE_PATH = HERE / "audit_branch0_cycle_generic_b3_resultant_tree.py"
RESULT = HERE / "results_branch0_cycle_generic_codim5_corrected_delta_modular_export.json"
PRIMES = (1073741827, 1073741789)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


TREE = load("corrected_delta_tree", TREE_PATH)


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
    require(lines[1] == "0", "corrected source ceased to be exact-Q")
    all_variables = tuple(sp.symbols(lines[0]))
    require(tuple(map(str, all_variables)) ==
            ("b0", "b1", "d1", "d3", "d4", "z"),
            "corrected codim-five variable order changed")
    variables = all_variables[:-1]
    z = all_variables[-1]
    encoded_rows = "\n".join(lines[2:]).strip().split(",\n")
    require(len(encoded_rows) == 10, "corrected codim-five row count changed")
    local = {str(variable): variable for variable in all_variables}
    rows = [sp.sympify(row.replace("^", "**"), locals=local)
            for row in encoded_rows]
    require(all(not row.has(z) for row in rows[:-1]),
            "z leaked into a corrected core row")
    live = sp.cancel((rows[-1]+1)/z)
    require(not live.has(z) and sp.expand(z*live-1-rows[-1]) == 0,
            "corrected Rabinowitsch row did not recover its live product")

    core_rows, _, _ = TREE.SOURCE.derive()
    b0, b1, b3, d1, d3, d4 = TREE.SOURCE.SOURCE.PARAMETERS
    compact = [sp.cancel(poly/factor) for poly, factor in zip(
        core_rows, (b1*b3*d1*d3, d4, b3, b1*b3, 1, 1, 1),
        strict=True)]
    pivot = compact[1]
    leading = sp.diff(pivot, b3)
    constant = sp.expand(pivot.subs(b3, 0))
    a_divisor = sp.cancel(leading/(2*b0))
    b_constant = sp.cancel(constant/2)
    true_delta = sp.expand(b0*a_divisor*b1*d3-b_constant*d1*d4)
    dropped_b0 = sp.expand(a_divisor*b1*d3-b_constant*d1*d4)
    require(sp.cancel(
        true_delta
        - (b0*a_divisor*(b1*d3+b3*d1*d4)).subs(
            b3, -b_constant/(b0*a_divisor))) == 0,
        "literal Delta/pivot equivalence changed")
    profile = [(len(sp.Poly(factor, *variables).terms()),
                sp.Poly(factor, *variables).total_degree(), int(power))
               for factor, power in sp.factor_list(true_delta)[1]]
    require(profile == [(8, 4, 1), (10, 5, 1)],
            "true Delta numerator factor profile changed")
    live_poly = sp.Poly(live, *variables, domain="ZZ")
    true_poly = sp.Poly(true_delta, *variables, domain="ZZ")
    dropped_poly = sp.Poly(dropped_b0, *variables, domain="ZZ")
    require(live_poly.rem(true_poly).is_zero,
            "corrected live product lacks true Delta numerator")
    quotient = live_poly.exquo(true_poly)
    require(not live_poly.rem(dropped_poly).is_zero,
            "corrected live product still localizes the dropped-b0 mutation")
    mutated_live = quotient.as_expr()*dropped_b0
    require(sp.expand(live-mutated_live) != 0,
            "dropped-b0 hostile live-product mutation did not fire")

    outputs = []
    for prime in PRIMES:
        path = HERE / f"branch0_cycle_generic_qrstu_codim5_corrected_p{prime}.msolve"
        equations = [*rows[:-1], live]
        path.write_text(
            ",".join(map(str, variables)) + f"\n{prime}\n"
            + ",\n".join(encode(row, variables) for row in equations)
            + "\n")
        payload = path.read_text().split("\n", 2)[2]
        require("(" not in payload and "**" not in payload,
                "strict corrected modular syntax guard failed")
        outputs.append({
            "prime": prime,
            "path": path.name,
            "sha256": sha256(path.read_bytes()).hexdigest(),
            "row_count": len(equations),
        })
    result = {
        "status": "UNAUDITED corrected-Delta modular codim-five export",
        "source": SOURCE.name,
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "source_exporter": SOURCE_EXPORTER.name,
        "source_exporter_sha256": sha256(SOURCE_EXPORTER.read_bytes()).hexdigest(),
        "variables": list(map(str, variables)),
        "core_row_count": 9,
        "pivot_root": "b3=-B/(b0*A)",
        "literal_delta_identity": (
            "b0*A*Delta|pivot=b0*A*b1*d3-B*d1*d4"),
        "true_delta_profile": profile,
        "live_terms_degree": [len(live_poly.terms()), live_poly.total_degree()],
        "dropped_b0_mutation_fired": True,
        "outputs": outputs,
        "scope": (
            "Native F4SAT modular discovery for the nine source-complete "
            "A-open codim-five resultant rows, localized at the exact true "
            "cleared Cramer Delta and all previously declared chart factors. "
            "Modular UNIT remains discovery until exact replay."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("corrected-Delta codim-five modular export: PASS")
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
