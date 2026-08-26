#!/usr/bin/env python3
"""Reduced exact codimension-three gate on the generic A-open branch."""

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
GCD = HERE / "export_branch0_cycle_generic_q4098_r4885_gcd.py"
OUT = HERE / "branch0_cycle_generic_qrs_codim3_exact.msolve"
OUT5 = HERE / "branch0_cycle_generic_qrstu_codim5_exact.msolve"
RESULT = HERE / "results_branch0_cycle_generic_qrs_codim3_export.json"


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


SOURCE = load("qrs_tree", TREE)
FULL_SOURCE = load("qrs_full", FULL)
GCD_SOURCE = load("qrs_gcd", GCD)


def encode(poly: sp.Expr, variables) -> str:
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


def choose_factor(poly, variables, term_count):
    primitive = sp.Poly(poly, *variables).primitive()[1].as_expr()
    factors = sp.factor_list(primitive)[1]
    matches = [factor for factor, power in factors
               if len(sp.Poly(factor, *variables).terms()) == term_count]
    require(len(matches) == 1, f"expected unique {term_count}-term factor")
    return matches[0], [(len(sp.Poly(f, *variables).terms()),
                         sp.Poly(f, *variables).total_degree(), int(e))
                        for f, e in factors]


def main() -> None:
    rows, labels, _ = SOURCE.SOURCE.derive()
    b0, b1, b3, d1, d3, d4 = SOURCE.SOURCE.SOURCE.PARAMETERS
    variables = (b0, b1, d1, d3, d4)
    compact = [sp.cancel(poly/factor) for poly, factor in zip(
        rows, (b1*b3*d1*d3, d4, b3, b1*b3, 1, 1, 1), strict=True)]
    pivot = compact[1]
    leading = sp.diff(pivot, b3)
    constant = sp.expand(pivot.subs(b3, 0))
    aa = sp.cancel(leading/(2*b0))
    bb = sp.cancel(constant/2)
    # pivot = 2*b0*A*b3 + 2*B, hence b3=-B/(b0*A).  Clearing
    # Delta=b1*d3+b3*d1*d4 therefore gives b0*A*b1*d3-B*d1*d4.
    # The previously used A*b1*d3-B*d1*d4 drops the essential b0.
    delta_numerator = sp.expand(b0*aa*b1*d3-bb*d1*d4)
    dropped_b0_mutation = sp.expand(aa*b1*d3-bb*d1*d4)
    delta_profile = [(len(sp.Poly(factor, *variables).terms()),
                      sp.Poly(factor, *variables).total_degree(), int(power))
                     for factor, power in sp.factor_list(delta_numerator)[1]]
    require((len(sp.Poly(aa, *variables).terms()),
             len(sp.Poly(bb, *variables).terms()),
             len(sp.Poly(delta_numerator, *variables).terms())) == (19, 44, 57)
            and sp.Poly(delta_numerator, *variables).total_degree() == 9
            and delta_profile == [(8, 4, 1), (10, 5, 1)],
            "A/B/Delta numerator profiles changed")
    require(sp.cancel(
        delta_numerator
        - (b0*aa*(b1*d3+b3*d1*d4)).subs(
            b3, -bb/(b0*aa))) == 0,
        "cleared literal Delta/pivot identity changed")
    require(sp.expand(delta_numerator-dropped_b0_mutation) != 0,
            "dropped-b0 hostile Delta guard did not fire")

    retained_specs = ((0, 851), (2, 1342), (3, 324), (4, 1846))
    retained = []
    profiles = {}
    for index, term_count in retained_specs:
        resultant = SOURCE.linear_resultant(compact[index], b3, leading, constant)
        factor, profile = choose_factor(resultant, variables, term_count)
        retained.append(factor)
        profiles[labels[index]] = profile

    gcd_variables, q4098, r4885, _, profile33, profile43 = GCD_SOURCE.derive()
    require(gcd_variables == variables, "Q/R variable order changed")
    lower, lower_hashes, *_ = FULL_SOURCE.derive_lower_cofactors()
    resultant13 = SOURCE.linear_resultant(lower[1], b3, leading, constant)
    s4331, profile13 = choose_factor(resultant13, variables, 4331)
    require(profile13 == [(2, 2, 1), (1, 1, 2), (8, 4, 1), (4331, 25, 1)],
            "Cof(1,3) resultant factor profile changed")
    resultant23 = SOURCE.linear_resultant(lower[2], b3, leading, constant)
    t4750, profile23 = choose_factor(resultant23, variables, 4750)
    resultant53 = SOURCE.linear_resultant(lower[5], b3, leading, constant)
    u3217, profile53 = choose_factor(resultant53, variables, 3217)
    require(profile23 == [(2, 2, 1), (1, 1, 2), (8, 4, 1), (4750, 26, 1)]
            and profile53 == [(2, 2, 1), (1, 1, 3), (8, 4, 1), (3217, 25, 1)],
            "Cof(2/5,3) resultant factor profiles changed")

    d0 = d1*d4+d3
    bplus = b1+d1
    live = sp.expand(b0*b1*d1*d3*d4*d0*bplus*aa*bb*delta_numerator)
    live_profile = sp.Poly(live, *variables)
    require(live_profile.total_degree() == 30,
            "reduced A-open live product degree changed")
    z = sp.Symbol("z")
    all_variables = (*variables, z)
    equations = (*retained, q4098, r4885, s4331, sp.expand(z*live-1))
    OUT.write_text(
        ",".join(map(str, all_variables)) + "\n0\n"
        + ",\n".join(encode(poly, all_variables) for poly in equations) + "\n")
    equations5 = (*retained, q4098, r4885, s4331, t4750, u3217,
                  sp.expand(z*live-1))
    OUT5.write_text(
        ",".join(map(str, all_variables)) + "\n0\n"
        + ",\n".join(encode(poly, all_variables) for poly in equations5) + "\n")
    body = OUT.read_text().split("\n", 2)[2]
    require("(" not in body and "**" not in body,
            "canonical msolve syntax guard failed")
    result = {
        "status": "UNAUDITED exact-Q generic-cycle Q/R/S reduced gate",
        "input": OUT.name,
        "input_sha256": sha256(OUT.read_bytes()).hexdigest(),
        "codim5_input": OUT5.name,
        "codim5_input_sha256": sha256(OUT5.read_bytes()).hexdigest(),
        "equation_labels": ["P851", "P1342", "P324", "P1846",
                            "Q4098", "R4885", "S4331", "live_inverse"],
        "codim5_equation_labels": ["P851", "P1342", "P324", "P1846",
                                   "Q4098", "R4885", "S4331", "T4750",
                                   "U3217", "live_inverse"],
        "retained_resultant_profiles": profiles,
        "cofactor33_profile": profile33,
        "cofactor43_profile": profile43,
        "cofactor13_profile": profile13,
        "cofactor23_profile": profile23,
        "cofactor53_profile": profile53,
        "cofactor13_literal_source_sha256": lower_hashes[1],
        "cofactor23_literal_source_sha256": lower_hashes[2],
        "cofactor53_literal_source_sha256": lower_hashes[5],
        "live_factors": ["b0", "b1", "d1", "d3", "d4", "D0",
                         "Bplus", "A", "B", "TrueDeltaNumerator"],
        "pivot_root": "b3=-B/(b0*A)",
        "literal_delta_identity": (
            "b0*A*Delta|pivot = b0*A*b1*d3-B*d1*d4"),
        "true_delta_numerator_profile": delta_profile,
        "dropped_b0_mutation_fired": True,
        "live_product_terms_degree": [len(live_profile.terms()),
                                      live_profile.total_degree()],
        "scope": (
            "Necessary reduced A-open branch after exact b3 elimination. C8 "
            "is excluded by its separately certified empty direct-source "
            "branch; Q4098,R4885,S4331 and all four retained compatibility "
            "resultants are imposed. UNIT would close this reduced branch. "
            "A nonunit output remains necessary-only until pulled back."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("generic Q/R/S codim3 exact export: PASS")
    print("live terms/degree:", result["live_product_terms_degree"])
    print("input bytes:", OUT.stat().st_size)
    print("codim5 input bytes:", OUT5.stat().st_size)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
