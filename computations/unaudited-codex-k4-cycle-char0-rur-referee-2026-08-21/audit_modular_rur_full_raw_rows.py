#!/usr/bin/env python3
"""Replay every literal branch-0 row on the modular all-minor RUR factors.

The all-minor scheme is only a necessary determinantal locus for the
six-row affine packet.  This referee reconstructs its coordinates directly
from msolve's RUR, verifies all sixteen exported determinant equations and
the live factor, solves the source-derived affine packet, and then evaluates
the complete nontrivial literal branch-0 source list.  In the p-coordinate
chart the six permanent equations vanish identically, leaving four triangle
and twelve cofactor rows.

Everything in this file is finite-field referee data.  No characteristic
zero component or chart-closure claim is made.
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
DANGER = (HERE.parent /
          "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20")
AUDIT_PATH = DANGER / "audit_branch0_cycle_delta_au_open_generic.py"
PCOORD_PATH = DANGER / "probe_branch0_cycle_pcoords.py"
OUTPUT = HERE / "results_modular_rur_full_raw_rows.json"
RUNS = (
    {
        "prime": 1073741827,
        "rur": DANGER / (
            "results_branch0_cycle_delta_au_open_all_minors_"
            "parametrize.param.out"),
        "input": DANGER /
        "branch0_cycle_delta_au_open_all_minors_p1073741827.msolve",
    },
    {
        "prime": 1073741789,
        "rur": DANGER / (
            "results_branch0_cycle_delta_au_open_all_minors_"
            "p1073741789_parametrize.param.out"),
        "input": DANGER / (
            "branch0_cycle_delta_au_open_all_minors_p1073741789.msolve"),
    },
)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("k4_full_raw_referee_audit", AUDIT_PATH)
PCOORD = load("k4_full_raw_referee_pcoords", PCOORD_PATH)
SOURCE = AUDIT.SOURCE


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
    """Parse the strict expanded msolve row without SymPy factor work."""
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
            match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)(?:\^(\d+))?",
                                 factor)
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
            "nonunit denominator in RUR factor")
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


def solve_unique(matrix, modulus, prime):
    """Solve rows c_0 y_0+c_1 y_1+c_2 y_2+constant=0."""
    rows = [[entry % modulus for entry in row[:3]]
            + [(-row[3]) % modulus] for row in matrix]
    rank = 0
    pivot_columns = []
    for column in range(3):
        pivot = next((row for row in range(rank, len(rows))
                      if len(rows[row][column])), None)
        require(pivot is not None, "literal packet coefficient rank below 3")
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = inverse(rows[rank][column], modulus, prime)
        rows[rank] = [entry * scale % modulus for entry in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not len(rows[row][column]):
                continue
            scale = rows[row][column]
            rows[row] = [(left - scale * right) % modulus
                         for left, right in zip(rows[row], rows[rank],
                                                strict=True)]
        pivot_columns.append(column)
        rank += 1
    for row in rows[rank:]:
        require(not any(len(entry) for entry in row[:3])
                or len(row[3]) == 0,
                "inconsistent affine packet survived determinant check")
    require(pivot_columns == [0, 1, 2], "unexpected affine pivots")
    return tuple(rows[index][3] for index in range(3))


def parse_input(path: Path):
    lines = path.read_text().splitlines()
    variables = tuple(value.strip() for value in lines[0].split(","))
    characteristic = int(lines[1])
    rows = tuple(value.strip() for value in
                 "\n".join(lines[2:]).split(",") if value.strip())
    return variables, characteristic, rows


def parse_rur(path: Path, expected_prime):
    text = path.read_text().strip()
    require(text.endswith(":"), "RUR lost terminal colon")
    envelope = ast.literal_eval(text[:-1])
    require(envelope[0] == 0, "msolve did not return a finite RUR envelope")
    payload = envelope[1]
    require(payload[:4] == [expected_prime, 4, 268,
                            ["x", "b1", "d1", "b0"]],
            "RUR header/order changed")
    require(payload[4] == [0, 0, 0, 1],
            "b0 is not the separating coordinate")
    data = payload[5][1]
    require(data[1] == [0, [1]], "RUR acquired a common denominator")
    eliminant = nmod_poly(data[0][1], expected_prime)
    numerators = tuple(nmod_poly(entry[0][1], expected_prime)
                       for entry in data[2])
    require(len(numerators) == 3, "RUR coordinate count changed")
    unit, factors = eliminant.factor()
    require(int(unit) == 1 and all(exponent == 1
                                   for _, exponent in factors),
            "RUR eliminant is not monic squarefree")
    return eliminant, numerators, tuple(factor for factor, _ in factors)


def run_one(spec):
    prime = spec["prime"]
    input_variables, input_prime, input_rows = parse_input(spec["input"])
    require(input_prime == prime and input_variables ==
            ("b0", "b1", "d1", "x") and len(input_rows) == 17,
            "all-minor input interface changed")
    input_compiled = tuple(
        (compile_expanded_integer(row, input_variables),
         [((0, 0, 0, 0), 1, 1)])
        for row in input_rows)

    _, numerators, factors = parse_rur(spec["rur"], prime)
    raw_rows, hafnian = PCOORD.data()
    raw_labels = tuple(label for label, _, _ in raw_rows)
    expected_labels = (
        "t_012", "t_013", "t_023", "t_123",
        "cofactor_0_0", "cofactor_0_3",
        "cofactor_1_0", "cofactor_1_3",
        "cofactor_2_0", "cofactor_2_3",
        "cofactor_3_0", "cofactor_3_3",
        "cofactor_4_0", "cofactor_4_3",
        "cofactor_5_0", "cofactor_5_3",
    )
    require(raw_labels == expected_labels,
            "literal row order changed")

    raw_source, _ = SOURCE.SOURCE.data()
    expressions = {label: SOURCE.expression(poly)
                   for label, poly, _ in raw_source}
    derived = AUDIT.derive(expressions)
    interface = AUDIT.INTERFACE.derive(expressions)
    b0, b1, _, d1, _, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    variables5 = (b0, b1, d1, x, d4)
    unknowns = (SOURCE.P[0], SOURCE.P[1], SOURCE.A5)
    variables8 = (*variables5, *unknowns)
    matrix_compiled = tuple(tuple(compile_expression(entry, variables5)
                                  for entry in row)
                            for row in interface[6])

    components = []
    for index, modulus in enumerate(factors):
        parameter = nmod_poly([0, 1], prime) % modulus
        # msolve stores each non-separating coordinate as its negative
        # numerator when the common denominator is one.
        x_value = (-numerators[0]) % modulus
        b1_value = (-numerators[1]) % modulus
        d1_value = (-numerators[2]) % modulus
        values4 = (parameter, b1_value, d1_value, x_value)

        exported_values = tuple(
            evaluate_compiled(top, values4, modulus, prime)
            * inverse(evaluate_compiled(bottom, values4, modulus, prime),
                      modulus, prime) % modulus
            for top, bottom in input_compiled)
        require(not any(len(value) for value in exported_values[:-1]),
                f"RUR factor {index} fails an exported determinant row")
        require(len(exported_values[-1]),
                f"RUR factor {index} kills the F4SAT live factor")

        d4_value = evaluate_rational(
            derived["d4_value"], (b0, b1, d1, x), values4,
            modulus, prime)
        values5 = (*values4, d4_value)
        matrix = [[evaluate_compiled(top, values5, modulus, prime)
                   * inverse(evaluate_compiled(bottom, values5,
                                               modulus, prime),
                             modulus, prime) % modulus
                   for top, bottom in row] for row in matrix_compiled]
        p1_value, p2_value, a5_value = solve_unique(
            matrix, modulus, prime)
        values8 = (*values5, p1_value, p2_value, a5_value)
        p3_value = evaluate_rational(
            interface[3][SOURCE.P[2]], variables8, values8,
            modulus, prime)
        p4_value = evaluate_rational(
            interface[3][SOURCE.P[3]], variables8, values8,
            modulus, prime)
        a0_value = evaluate_rational(
            interface[4], variables8, values8, modulus, prime)
        b3_value = x_value * b1_value % modulus
        d3_value = -x_value * d1_value * d4_value % modulus
        pcoord_values = (
            p1_value, p2_value, p3_value, p4_value,
            a0_value, a5_value, parameter, b1_value, b3_value,
            d1_value, d3_value, d4_value,
        )
        evaluated = tuple(evaluate_sparse(poly, pcoord_values,
                                          modulus, prime)
                          for _, poly, _ in raw_rows)
        nonzero = tuple((label, coefficients(value, modulus.degree()))
                        for label, value in zip(raw_labels, evaluated,
                                                strict=True) if len(value))
        h_value = evaluate_sparse(hafnian, pcoord_values, modulus, prime)
        components.append({
            "index": index,
            "degree": modulus.degree(),
            "factor_coefficients": coefficients(
                modulus, modulus.degree() + 1),
            "literal_nonzero_rows": [
                {"label": label, "coefficients": value}
                for label, value in nonzero],
            "literal_zero_row_count": len(raw_rows) - len(nonzero),
            "pure_hafnian_coefficients": coefficients(
                h_value, modulus.degree()),
            "pure_hafnian_live": bool(len(h_value)),
        })

    profile = Counter(tuple(row["label"] for row in
                            component["literal_nonzero_rows"])
                      for component in components)
    return {
        "prime": prime,
        "rur_file": spec["rur"].name,
        "rur_file_sha256": file_sha(spec["rur"]),
        "input_file": spec["input"].name,
        "input_file_sha256": file_sha(spec["input"]),
        "component_count": len(components),
        "failure_label_profiles": [
            {"labels": list(labels), "count": count}
            for labels, count in sorted(profile.items())],
        "components": components,
    }


def main():
    runs = [run_one(spec) for spec in RUNS]
    expected_omissions = (
        "cofactor_1_3", "cofactor_2_3", "cofactor_3_3",
        "cofactor_4_3", "cofactor_5_3",
    )
    # Must-fire on the first quadratic component at each prime: it passes
    # all determinantal input rows but fails all five omitted literal rows.
    for run in runs:
        first = run["components"][0]
        require(first["degree"] == 2,
                "first modular factor ceased to be quadratic")
        require(tuple(row["label"] for row in
                      first["literal_nonzero_rows"]) == expected_omissions,
                "the omitted-row must-fire profile changed")
        require(first["pure_hafnian_live"],
                "first quadratic component lost its H-live control")
    result = {
        "status": "UNAUDITED exact finite-field raw-row referee",
        "nontrivial_literal_rows": 16,
        "identically_solved_permanent_rows": 6,
        "determinantal_packet_rows_retained": [
            "t_012", "t_013", "t_023", "t_123",
            "cofactor_0_0", "cofactor_0_3",
            "cofactor_1_0", "cofactor_2_0", "cofactor_3_0",
            "cofactor_4_0", "cofactor_5_0",
        ],
        "literal_rows_omitted_by_determinantal_packet":
        list(expected_omissions),
        "runs": runs,
        "scope": (
            "Exact arithmetic in each irreducible finite-field RUR factor. "
            "The all-minor coordinates and live factor are replayed before "
            "the source solve. Failure of an omitted literal row proves "
            "that component is not a zero of the full branch-0 source. "
            "This makes no characteristic-zero assertion."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("modular all-minor full raw-row referee: PASS")
    for run in runs:
        print(run["prime"], run["failure_label_profiles"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
