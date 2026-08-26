#!/usr/bin/env python3
"""Canonical exact-Q full literal-row reduction on generic-cycle A=B=0."""

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
BASE = HERE / "export_branch0_cycle_generic_azero_bzero_exact.py"
OUT = HERE / "branch0_cycle_generic_azero_bzero_full_source_exact.msolve"
RESULT = HERE / "results_branch0_cycle_generic_azero_bzero_full_source_export.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load(path: Path):
    spec = importlib.util.spec_from_file_location("generic_ab_full_source", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load(BASE)


def derive_lower_cofactors():
    generic = SOURCE.SOURCE.SOURCE
    raw_rows, _ = generic.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    rows = {label: generic.expression(poly) for label, poly, _ in raw_rows}
    upper = [rows[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    p_solution = sp.solve(upper, generic.P, dict=True, simplify=False)[0]
    c50 = generic.numerator(rows["cofactor_5_0"], p_solution)
    a0_solution = sp.solve(c50, generic.A0, dict=True, simplify=False)[0]
    t023 = generic.numerator(
        generic.numerator(rows["t_023"], p_solution), a0_solution)
    a5_solution = sp.solve(t023, generic.A5, dict=True, simplify=False)[0]
    b0, b1, b3, d1, d3, d4 = generic.PARAMETERS
    delta = b1*d3+b3*d1*d4
    divisors = {
        1: (delta, b3), 2: (delta, b3), 3: (delta, b1),
        4: (delta, b1), 5: (b1, b3),
    }
    expected = {1: (487, 15), 2: (487, 17), 3: (472, 15),
                4: (472, 16), 5: (504, 16)}
    answer = {}
    source_hashes = {}
    for edge in range(1, 6):
        label = f"cofactor_{edge}_3"
        value = generic.numerator(rows[label], p_solution)
        value = generic.numerator(value, a0_solution)
        value = generic.numerator(value, a5_solution)
        poly = sp.Poly(value, *generic.PARAMETERS)
        for divisor in divisors[edge]:
            divisor_poly = sp.Poly(divisor, *generic.PARAMETERS)
            require(poly.rem(divisor_poly).is_zero,
                    f"{label} live divisor {divisor} changed")
            poly = poly.exquo(divisor_poly)
        reduced = poly.primitive()[1].as_expr()
        profile = sp.Poly(reduced, *generic.PARAMETERS)
        require((len(profile.terms()), profile.total_degree()) == expected[edge],
                f"{label} reduced profile changed")
        answer[edge] = reduced
        source_hashes[edge] = sha256(str(raw[label]).encode("ascii")).hexdigest()
    # Cof(3,3) must be byte-polynomial identical to the already frozen core row.
    core_rows, _, _ = SOURCE.SOURCE.derive()
    require(sp.expand(answer[3]-core_rows[5]) == 0,
            "full-source Cof(3,3) differs from frozen core")
    return answer, source_hashes, rows, p_solution, a0_solution, a5_solution


def main() -> None:
    rows, labels, metadata = SOURCE.SOURCE.derive()
    source_rows = tuple(rows[:6])
    b0, b1, b3, d1, d3, d4 = SOURCE.SOURCE.SOURCE.PARAMETERS
    normalized_t013 = sp.cancel(source_rows[1]/d4)
    a_divisor = sp.cancel(sp.diff(normalized_t013, b3)/(2*b0))
    b_polynomial = sp.cancel(normalized_t013.subs(b3, 0)/2)
    lower, lower_hashes, literal_rows, p_solution, a0_solution, a5_solution = \
        derive_lower_cofactors()
    delta = b1*d3+b3*d1*d4
    d0 = d1*d4+d3
    bplus = b1+d1
    live = sp.expand(b0*b1*b3*d1*d3*d4*delta*d0*bplus)
    z = sp.Symbol("z")
    variables = (*SOURCE.SOURCE.SOURCE.PARAMETERS, z)
    # Cof(3,3) is source_rows[5]; append precisely the other four lower rows.
    generators = (*source_rows, a_divisor, b_polynomial,
                  lower[1], lower[2], lower[4], lower[5], sp.expand(z*live-1))
    OUT.write_text(
        ",".join(map(str, variables)) + "\n0\n"
        + ",\n".join(SOURCE.encode(poly, variables) for poly in generators) + "\n")
    body = OUT.read_text().split("\n", 2)[2]
    require("(" not in body and "**" not in body,
            "canonical msolve syntax guard failed")

    # Exact source coverage: six solved rows + five compatibility rows + five
    # lower cofactors partition all sixteen distinct literal reduced rows.
    solved_labels = [f"cofactor_{edge}_0" for edge in range(1, 5)] \
        + ["cofactor_5_0", "t_023"]
    compatibility_labels = labels[:5]
    lower_labels = [f"cofactor_{edge}_3" for edge in range(1, 6)]
    coverage = solved_labels + compatibility_labels + lower_labels
    literal_labels = [label for label, poly, _ in SOURCE.SOURCE.SOURCE.SOURCE.data()[0]]
    require(len(set(literal_labels)) == 16 and set(coverage) == set(literal_labels),
            "literal sixteen-row source coverage changed")
    result = {
        "status": "UNAUDITED exact-Q A=B=0 full-source reduced chart export",
        "input": OUT.name,
        "input_sha256": sha256(OUT.read_bytes()).hexdigest(),
        "canonical_row_count": len(generators),
        "literal_source_coverage": coverage,
        "solved_literal_rows": solved_labels,
        "compatibility_literal_rows": compatibility_labels,
        "lower_literal_rows": lower_labels,
        "lower_source_sha256": {str(edge): lower_hashes[edge]
                                 for edge in range(1, 6)},
        "lower_profiles": {"1": [487, 15], "2": [487, 17],
                           "3": [472, 15], "4": [472, 16],
                           "5": [504, 16]},
        "source_cofactor33_sha256": metadata["omitted_sha256"],
        "localized_factors": ["b0", "b1", "b3", "d1", "d3", "d4",
                              "Delta", "D0", "Bplus"],
        "scope": (
            "All sixteen distinct literal one-colour rows are represented by "
            "six solve equations, five direct compatibility numerators, and "
            "all five lower cofactor numerators on the frozen live chart. "
            "A=B=0 is imposed. H is not localized; Q4098 is out of scope."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("generic A=B=0 full-source exact export: PASS")
    print("input sha256:", result["input_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
