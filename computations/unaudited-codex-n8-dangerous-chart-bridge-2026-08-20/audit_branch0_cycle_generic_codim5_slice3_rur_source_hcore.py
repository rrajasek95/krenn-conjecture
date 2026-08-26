#!/usr/bin/env python3
"""Replay the finite codim-five slice against all literal rows and Hcore.

This is a finite-field referee only.  It decodes the degree-eleven msolve
RUR, reconstructs the eliminated ``b3`` coordinate from the literal affine
``t_013`` pivot, reconstructs all Cramer-solved coordinates, and evaluates
all sixteen literal nontrivial source rows and the pure Hafnian in every
irreducible RUR factor.
"""

from __future__ import annotations

import ast
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re
import sys


_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))
from flint import nmod_poly
import sympy as sp


HERE = Path(__file__).resolve().parent
TREE_PATH = HERE / "audit_branch0_cycle_generic_b3_resultant_tree.py"
FULL_PATH = HERE / "export_branch0_cycle_generic_azero_bzero_full_source_exact.py"
HLIVE_PATH = HERE / "export_branch0_cycle_generic_azero_bzero_full_source_hlive_exact.py"
RUR = HERE / "results_codim5_slice3_sub_p1073741827_rur.param.out"
SLICE_INPUT = HERE / "branch0_cycle_generic_codim5_slice3_sub_p1073741827.msolve"
OUTPUT = HERE / "results_codim5_slice3_p1073741827_literal_source_hcore.json"
PRIME = 1073741827


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


TREE = load("codim5_rur_tree", TREE_PATH)
FULL = load("codim5_rur_full", FULL_PATH)
HLIVE = load("codim5_rur_hlive", HLIVE_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def coefficients(value, degree=None):
    if degree is None:
        degree = len(value)
    return [int(value[index]) if index < len(value) else 0
            for index in range(degree)]


def compile_expression(expression, variables):
    numerator, denominator = sp.cancel(expression).as_numer_denom()

    def compile_poly(value):
        rows = []
        for monomial, coefficient in sp.Poly(
                value, *variables, domain=sp.QQ).terms():
            rows.append((monomial, int(coefficient.p), int(coefficient.q)))
        return rows

    return compile_poly(numerator), compile_poly(denominator)


def compile_expanded_integer(text, variable_names):
    names = {name: index for index, name in enumerate(variable_names)}
    answer = Counter()
    value = re.sub(r"\s+", "", text)
    for encoded in re.findall(r"[+-]?[^+-]+", value):
        sign = -1 if encoded.startswith("-") else 1
        if encoded[:1] in "+-":
            encoded = encoded[1:]
        coefficient = sign
        exponent = [0] * len(variable_names)
        for factor in encoded.split("*"):
            if re.fullmatch(r"\d+", factor):
                coefficient *= int(factor)
                continue
            match = re.fullmatch(
                r"([A-Za-z_][A-Za-z0-9_]*)(?:\^(\d+))?", factor)
            require(match is not None and match.group(1) in names,
                    f"unsupported strict msolve factor {factor!r}")
            exponent[names[match.group(1)]] += int(match.group(2) or "1")
        answer[tuple(exponent)] += coefficient
    return [(monomial, coefficient, 1)
            for monomial, coefficient in answer.items() if coefficient]


def evaluate_compiled(compiled, values, modulus, prime):
    answer = nmod_poly([], prime)
    for monomial, numerator, denominator in compiled:
        scalar = numerator * pow(denominator, -1, prime) % prime
        term = nmod_poly([scalar], prime)
        for value, exponent in zip(values, monomial, strict=True):
            if exponent:
                term = term * value.pow_mod(exponent, modulus) % modulus
        answer = (answer + term) % modulus
    return answer


def inverse(value, modulus, prime):
    gcd, coefficient, _ = value.xgcd(modulus)
    require(gcd.degree() == 0 and int(gcd[0]) % prime,
            "nonunit denominator in an irreducible RUR factor")
    return coefficient * pow(int(gcd[0]), -1, prime) % modulus


def evaluate_rational(expression, variables, values, modulus, prime):
    top, bottom = compile_expression(expression, variables)
    numerator = evaluate_compiled(top, values, modulus, prime)
    denominator = evaluate_compiled(bottom, values, modulus, prime)
    return numerator * inverse(denominator, modulus, prime) % modulus


def evaluate_sparse(poly, values, modulus, prime):
    answer = nmod_poly([], prime)
    for monomial, coefficient in poly.items():
        coefficient = Fraction(coefficient)
        scalar = (coefficient.numerator
                  * pow(coefficient.denominator, -1, prime)) % prime
        term = nmod_poly([scalar], prime)
        for value, exponent in zip(values, monomial, strict=True):
            if exponent:
                term = term * value.pow_mod(exponent, modulus) % modulus
        answer = (answer + term) % modulus
    return answer


def parse_rur():
    text = RUR.read_text().strip()
    require(text.endswith(":"), "RUR lost terminal colon")
    envelope = ast.literal_eval(text[:-1])
    require(envelope[0] == 0, "msolve did not return a finite RUR")
    payload = envelope[1]
    require(payload[:4] == [PRIME, 2, 11, ["d3", "d4"]],
            "RUR header/order changed")
    require(payload[4] == [0, 1], "d4 is no longer separating")
    data = payload[5][1]
    require(data[1] == [0, [1]], "RUR acquired a common denominator")
    eliminant = nmod_poly(data[0][1], PRIME)
    numerators = tuple(nmod_poly(entry[0][1], PRIME)
                       for entry in data[2])
    require(len(numerators) == 1, "RUR coordinate count changed")
    unit, factored = eliminant.factor()
    require(int(unit) == 1 and all(exponent == 1
                                   for _, exponent in factored),
            "RUR eliminant is not monic squarefree")
    return eliminant, numerators[0], tuple(factor for factor, _ in factored)


def parse_slice_input():
    lines = SLICE_INPUT.read_text().splitlines()
    require(lines[:2] == ["d3,d4", str(PRIME)],
            "bivariate slice input header changed")
    rows = tuple(value.strip() for value in
                 "\n".join(lines[2:]).split(",") if value.strip())
    require(len(rows) == 10, "bivariate slice input row count changed")
    return tuple(compile_expanded_integer(row, ("d3", "d4"))
                 for row in rows)


def main() -> None:
    eliminant, d3_numerator, factors = parse_rur()
    slice_rows = parse_slice_input()

    core_rows, core_labels, _ = TREE.SOURCE.derive()
    b0, b1, b3, d1, d3, d4 = TREE.SOURCE.SOURCE.PARAMETERS
    compact = [sp.cancel(poly/factor) for poly, factor in zip(
        core_rows, (b1*b3*d1*d3, d4, b3, b1*b3, 1, 1, 1),
        strict=True)]
    pivot = compact[1]
    leading = sp.diff(pivot, b3)
    constant = sp.expand(pivot.subs(b3, 0))
    a_divisor = sp.cancel(leading/(2*b0))
    b_constant = sp.cancel(constant/2)
    require(sp.expand(pivot-leading*b3-constant) == 0,
            "literal affine pivot changed")

    lower, lower_hashes, _, p_solution, a0_solution, a5_solution = \
        FULL.derive_lower_cofactors()
    hcore, h_denominator = HLIVE.derive_hcore(
        p_solution, a0_solution, a5_solution)
    generic = FULL.SOURCE.SOURCE.SOURCE
    raw_rows, raw_hafnian = generic.SOURCE.data()
    raw_labels = tuple(label for label, _, _ in raw_rows)
    require(len(raw_labels) == 16 and len(set(raw_labels)) == 16,
            "literal source row census changed")
    parameters = generic.PARAMETERS
    require(parameters == (b0, b1, b3, d1, d3, d4),
            "generic parameter order changed")

    delta = b1*d3+b3*d1*d4
    d0 = d1*d4+d3
    bplus = b1+d1
    wrong_delta_guard = sp.expand(a_divisor*b1*d3-b_constant*d1*d4)
    actual_delta_numerator = sp.expand(
        b0*a_divisor*b1*d3-b_constant*d1*d4)
    # The second expression is exactly b0*A*Delta after using the pivot.
    require(sp.cancel(actual_delta_numerator
                      - (b0*a_divisor*delta).subs(
                          b3, -b_constant/(b0*a_divisor))) == 0,
            "actual Delta numerator identity changed")

    components = []
    for index, modulus in enumerate(factors):
        parameter = nmod_poly([0, 1], PRIME) % modulus
        # msolve encodes each non-separating coordinate as -numerator.
        d3_value = (-d3_numerator) % modulus
        d4_value = parameter
        inv111 = nmod_poly([pow(111, -1, PRIME)], PRIME)
        b0_value = ((14*d3_value-44*d4_value-744)*inv111) % modulus
        b1_value = ((-268*d3_value-14*d4_value+510)*inv111) % modulus
        d1_value = ((-11*d3_value-235*d4_value+315)*inv111) % modulus
        values5 = (b0_value, b1_value, d1_value, d3_value, d4_value)
        variables5 = (b0, b1, d1, d3, d4)
        a_value = evaluate_rational(
            a_divisor, variables5, values5, modulus, PRIME)
        b_value = evaluate_rational(
            b_constant, variables5, values5, modulus, PRIME)
        b3_value = (-b_value * inverse(b0_value*a_value,
                                       modulus, PRIME)) % modulus
        parameter_values = (
            b0_value, b1_value, b3_value, d1_value, d3_value, d4_value)

        exported_values = tuple(evaluate_compiled(
            row, (d3_value, d4_value), modulus, PRIME) for row in slice_rows)
        require(not any(len(value) for value in exported_values[:-1]),
                f"RUR factor {index} fails a sliced codim-five row")
        require(len(exported_values[-1]),
                f"RUR factor {index} kills the declared live product")

        guards = {
            "b0": b0_value,
            "b1": b1_value,
            "b3": b3_value,
            "d1": d1_value,
            "d3": d3_value,
            "d4": d4_value,
            "D0": evaluate_rational(d0, parameters, parameter_values,
                                     modulus, PRIME),
            "Bplus": evaluate_rational(bplus, parameters, parameter_values,
                                        modulus, PRIME),
            "A": a_value,
            "B": b_value,
            "wrong_Delta_guard": evaluate_rational(
                wrong_delta_guard, variables5, values5, modulus, PRIME),
            "actual_Delta_numerator": evaluate_rational(
                actual_delta_numerator, variables5, values5, modulus, PRIME),
            "actual_Delta": evaluate_rational(
                delta, parameters, parameter_values, modulus, PRIME),
        }
        zero_guards = [label for label, value in guards.items() if not len(value)]
        component = {
            "index": index,
            "degree": modulus.degree(),
            "factor_coefficients": coefficients(
                modulus, modulus.degree()+1),
            "zero_guards": zero_guards,
            "actual_delta_live": bool(len(guards["actual_Delta"])),
        }

        if not len(guards["actual_Delta"]):
            component.update({
                "source_lift_status": "excluded_by_actual_Delta_zero",
                "literal_nonzero_rows": None,
                "pure_hafnian_live": None,
                "Hcore_live": None,
            })
            components.append(component)
            continue

        p_values = tuple(evaluate_rational(
            p_solution[variable], parameters, parameter_values,
            modulus, PRIME) for variable in generic.P)
        a0_value = evaluate_rational(
            a0_solution[generic.A0], parameters, parameter_values,
            modulus, PRIME)
        a5_value = evaluate_rational(
            a5_solution[generic.A5], parameters, parameter_values,
            modulus, PRIME)
        raw_values = (*p_values, a0_value, a5_value, *parameter_values)
        evaluated_rows = tuple(evaluate_sparse(poly, raw_values,
                                               modulus, PRIME)
                               for _, poly, _ in raw_rows)
        nonzero = tuple((label, coefficients(value, modulus.degree()))
                        for label, value in zip(raw_labels, evaluated_rows,
                                                strict=True) if len(value))
        h_value = evaluate_sparse(raw_hafnian, raw_values, modulus, PRIME)
        hcore_value = evaluate_rational(
            hcore, parameters, parameter_values, modulus, PRIME)
        hcore_from_h = (h_value*b0_value*guards["actual_Delta"].pow_mod(2, modulus)
                        * guards["D0"]
                        * inverse(b1_value*b3_value, modulus, PRIME)) % modulus
        require(hcore_value == hcore_from_h,
                f"RUR factor {index} fails the literal H/Hcore identity")
        component.update({
            "source_lift_status": (
                "all_literal_rows_zero" if not nonzero
                else "literal_rows_nonzero"),
            "literal_nonzero_rows": [
                {"label": label, "coefficients": value}
                for label, value in nonzero],
            "literal_zero_row_count": len(raw_rows)-len(nonzero),
            "pure_hafnian_coefficients": coefficients(
                h_value, modulus.degree()),
            "pure_hafnian_live": bool(len(h_value)),
            "Hcore_coefficients": coefficients(
                hcore_value, modulus.degree()),
            "Hcore_live": bool(len(hcore_value)),
        })
        components.append(component)

    result = {
        "status": "UNAUDITED finite-field codim5 literal-source/Hcore replay",
        "prime": PRIME,
        "rur": RUR.name,
        "rur_sha256": file_sha(RUR),
        "slice_input": SLICE_INPUT.name,
        "slice_input_sha256": file_sha(SLICE_INPUT),
        "eliminant_degree": eliminant.degree(),
        "factor_degree_profile": sorted(component["degree"]
                                        for component in components),
        "literal_row_labels": list(raw_labels),
        "lower_source_sha256": {str(edge): lower_hashes[edge]
                                 for edge in range(1, 6)},
        "Hcore_terms_degree": [len(sp.Poly(hcore, *parameters).terms()),
                                sp.Poly(hcore, *parameters).total_degree()],
        "literal_H_denominator": str(sp.factor(h_denominator)),
        "pivot_root": "b3=-B/(b0*A)",
        "declared_delta_guard": "A*b1*d3-B*d1*d4",
        "actual_delta_numerator": "b0*A*b1*d3-B*d1*d4",
        "components": components,
        "scope": (
            "Exact arithmetic in each irreducible factor of the modular "
            "degree-11 three-hyperplane RUR. This replays all sixteen literal "
            "source rows and Hcore only on factors where the actual Cramer "
            "Delta is live. No characteristic-zero assertion is made."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("codim-five literal-source/Hcore RUR replay: PASS")
    for component in components:
        print(component["degree"], component["source_lift_status"],
              component["zero_guards"], component["Hcore_live"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
