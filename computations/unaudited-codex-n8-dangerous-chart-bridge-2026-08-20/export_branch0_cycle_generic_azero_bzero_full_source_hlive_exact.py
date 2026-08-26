#!/usr/bin/env python3
"""Exact H-live gate on the full-source generic-cycle A=B=0 component."""

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
BASE = HERE / "export_branch0_cycle_generic_azero_bzero_full_source_exact.py"
OUT = HERE / "branch0_cycle_generic_azero_bzero_full_source_hlive_exact.msolve"
OUT_P1 = HERE / "branch0_cycle_generic_azero_bzero_full_source_hlive_p1073741827.msolve"
OUT_BASE_P1 = HERE / "branch0_cycle_generic_azero_bzero_full_source_p1073741827.msolve"
LABELS = HERE / "branch0_cycle_generic_azero_bzero_full_source_hlive_labels.json"
BASE_LABELS = HERE / "branch0_cycle_generic_azero_bzero_full_source_labels.json"
RESULT = HERE / "results_branch0_cycle_generic_azero_bzero_full_source_hlive_export.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load(path: Path):
    spec = importlib.util.spec_from_file_location("generic_ab_full_hlive", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load(BASE)


def derive_hcore(p_solution, a0_solution, a5_solution):
    generic = SOURCE.SOURCE.SOURCE.SOURCE
    hafnian = generic.expression(generic.SOURCE.data()[1])
    value = sp.cancel(hafnian.subs(p_solution).subs(a0_solution).subs(a5_solution))
    numerator, denominator = value.as_numer_denom()
    b0, b1, b3, d1, d3, d4 = generic.PARAMETERS
    delta = b1*d3+b3*d1*d4
    d0 = d1*d4+d3
    require(sp.factor(denominator) == b0*delta**2*d0,
            "literal H solve denominator changed")
    poly = sp.Poly(numerator, *generic.PARAMETERS)
    for divisor in (b1, b3):
        divisor_poly = sp.Poly(divisor, *generic.PARAMETERS)
        require(poly.rem(divisor_poly).is_zero,
                f"literal H live factor {divisor} changed")
        poly = poly.exquo(divisor_poly)
    hcore = poly.primitive()[1].as_expr()
    profile = sp.Poly(hcore, *generic.PARAMETERS)
    require(len(profile.terms()) == 258 and profile.total_degree() == 15,
            "literal H core profile changed")
    require(sp.cancel(value - b1*b3*hcore/(b0*delta**2*d0)) == 0,
            "literal H rational replay failed")
    return hcore, denominator


def main() -> None:
    rows, labels, metadata = SOURCE.SOURCE.SOURCE.derive()
    source_rows = tuple(rows[:6])
    b0, b1, b3, d1, d3, d4 = SOURCE.SOURCE.SOURCE.SOURCE.PARAMETERS
    normalized_t013 = sp.cancel(source_rows[1]/d4)
    a_divisor = sp.cancel(sp.diff(normalized_t013, b3)/(2*b0))
    b_polynomial = sp.cancel(normalized_t013.subs(b3, 0)/2)
    lower, lower_hashes, literal_rows, p_solution, a0_solution, a5_solution = \
        SOURCE.derive_lower_cofactors()
    hcore, h_denominator = derive_hcore(p_solution, a0_solution, a5_solution)
    delta = b1*d3+b3*d1*d4
    d0 = d1*d4+d3
    bplus = b1+d1
    live = sp.expand(b0*b1*b3*d1*d3*d4*delta*d0*bplus)
    z = sp.Symbol("z")
    variables = (*SOURCE.SOURCE.SOURCE.SOURCE.PARAMETERS, z)
    generators = (*source_rows, a_divisor, b_polynomial,
                  lower[1], lower[2], lower[4], lower[5],
                  sp.expand(z*live*hcore-1))
    OUT.write_text(
        ",".join(map(str, variables)) + "\n0\n"
        + ",\n".join(SOURCE.SOURCE.encode(poly, variables)
                      for poly in generators) + "\n")
    modular_variables = SOURCE.SOURCE.SOURCE.SOURCE.PARAMETERS
    modular_generators = (*generators[:-1], sp.expand(live*hcore))
    OUT_P1.write_text(
        ",".join(map(str, modular_variables)) + "\n1073741827\n"
        + ",\n".join(SOURCE.SOURCE.encode(poly, modular_variables)
                      for poly in modular_generators) + "\n")
    base_modular_generators = (*generators[:-1], live)
    OUT_BASE_P1.write_text(
        ",".join(map(str, modular_variables)) + "\n1073741827\n"
        + ",\n".join(SOURCE.SOURCE.encode(poly, modular_variables)
                      for poly in base_modular_generators) + "\n")
    modular_labels = [*labels[:6], "A", "B", "cofactor_1_3",
                      "cofactor_2_3", "cofactor_4_3", "cofactor_5_3",
                      "nine_live_factors_times_Hcore"]
    LABELS.write_text(json.dumps({"labels": modular_labels}, indent=2) + "\n")
    base_labels = [*modular_labels[:-1], "nine_live_factors"]
    BASE_LABELS.write_text(json.dumps({"labels": base_labels}, indent=2) + "\n")
    body = OUT.read_text().split("\n", 2)[2]
    require("(" not in body and "**" not in body,
            "canonical msolve syntax guard failed")
    full_export = json.loads((HERE /
        "results_branch0_cycle_generic_azero_bzero_full_source_export.json").read_text())
    require(len(full_export["literal_source_coverage"]) == 16,
            "full literal source coverage artifact changed")
    result = {
        "status": "UNAUDITED exact-Q A=B=0 full-source H-live export",
        "input": OUT.name,
        "input_sha256": sha256(OUT.read_bytes()).hexdigest(),
        "modular_input": OUT_P1.name,
        "modular_input_sha256": sha256(OUT_P1.read_bytes()).hexdigest(),
        "modular_labels": LABELS.name,
        "base_modular_input": OUT_BASE_P1.name,
        "base_modular_input_sha256": sha256(OUT_BASE_P1.read_bytes()).hexdigest(),
        "base_modular_labels": BASE_LABELS.name,
        "canonical_row_count": len(generators),
        "literal_source_coverage": full_export["literal_source_coverage"],
        "lower_source_sha256": {str(edge): lower_hashes[edge]
                                 for edge in range(1, 6)},
        "hcore_terms_degree": [258, 15],
        "hcore_sha256": sha256(SOURCE.SOURCE.encode(hcore, variables).encode("ascii")).hexdigest(),
        "literal_h_denominator": str(sp.factor(h_denominator)),
        "literal_h_identity": "H=b1*b3*Hcore/(b0*Delta^2*D0)",
        "localized_factors": ["b0", "b1", "b3", "d1", "d3", "d4",
                              "Delta", "D0", "Bplus", "Hcore"],
        "scope": (
            "All sixteen literal one-colour rows on A=B=0, with the frozen "
            "nine chart factors and literal pure H localized. Positive output "
            "would be a genuine one-colour H-live component, not a multi-colour "
            "counterexample. Q4098 remains out of scope."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("generic A=B=0 full-source H-live export: PASS")
    print("input sha256:", result["input_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
