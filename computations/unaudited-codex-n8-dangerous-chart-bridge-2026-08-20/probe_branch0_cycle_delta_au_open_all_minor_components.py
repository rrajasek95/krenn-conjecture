#!/usr/bin/env python3
"""Classify the modular finite all-minor scheme against the literal packet.

This decodes the frozen msolve parametrization, replays the exact Q/U solve
and the source-derived six-row augmented matrix on each irreducible RUR
factor, and distinguishes inconsistent determinantal false positives from
consistent packet components.  Everything here is modular discovery.
"""

from __future__ import annotations

import ast
import argparse
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
from flint import nmod_poly


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_branch0_cycle_delta_au_open_generic.py"
DEFAULT_RUR_PATH = (HERE /
                    "results_branch0_cycle_delta_au_open_all_minors_parametrize.param.out")
DEFAULT_RESULT = HERE / "results_branch0_cycle_delta_au_open_all_minor_components.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("n8_cycle_delta_all_minor_component_audit", AUDIT_PATH)
sp = AUDIT.sp
SOURCE = AUDIT.SOURCE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def poly_digest(poly):
    coefficients = [int(poly[index]) for index in range(len(poly))]
    return sha256(json.dumps(coefficients,
                             separators=(",", ":")).encode("ascii")).hexdigest()


def field_coefficients(value, degree):
    return [int(value[index]) if index < len(value) else 0
            for index in range(degree)]


def compile_poly(expression, variables):
    poly = sp.Poly(expression, *variables, domain=sp.QQ)
    terms = []
    for monomial, coefficient in poly.terms():
        require(coefficient.q == 1,
                "compiled normalized polynomial acquired a denominator")
        terms.append((monomial, int(coefficient)))
    return terms


def evaluate_terms(terms, values, modulus, prime):
    result = nmod_poly([], prime)
    for monomial, coefficient in terms:
        term = nmod_poly([coefficient % prime], prime)
        for value, exponent in zip(values, monomial):
            if exponent:
                term = (term * value.pow_mod(exponent, modulus)) % modulus
        result = (result + term) % modulus
    return result


def evaluate_rational(expression, variables, values, modulus, prime):
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    top = evaluate_terms(compile_poly(numerator, variables),
                         values, modulus, prime)
    bottom = evaluate_terms(compile_poly(denominator, variables),
                            values, modulus, prime)
    require(len(bottom), "a declared solve denominator vanished")
    gcd, inverse, _ = bottom.xgcd(modulus)
    require(gcd.degree() == 0 and int(gcd[0]) % prime,
            "a solve denominator was nonunit on an RUR component")
    inverse = inverse * pow(int(gcd[0]), -1, prime)
    return (top * inverse) % modulus


def inverse(value, modulus, prime):
    gcd, coefficient, _ = value.xgcd(modulus)
    require(gcd.degree() == 0 and int(gcd[0]) % prime,
            "attempted to invert zero in an RUR component field")
    return (coefficient * pow(int(gcd[0]), -1, prime)) % modulus


def rref(matrix, modulus, prime, columns):
    value = [[entry % modulus for entry in row] for row in matrix]
    rank = 0
    pivots = []
    for column in range(columns):
        pivot = next((row for row in range(rank, len(value))
                      if len(value[row][column])), None)
        if pivot is None:
            continue
        value[rank], value[pivot] = value[pivot], value[rank]
        scale = inverse(value[rank][column], modulus, prime)
        value[rank] = [(entry*scale) % modulus
                       for entry in value[rank]]
        for row in range(len(value)):
            if row == rank or not len(value[row][column]):
                continue
            scale = value[row][column]
            value[row] = [
                (left-scale*right) % modulus
                for left, right in zip(value[row], value[rank])]
        pivots.append(column)
        rank += 1
        if rank == len(value):
            break
    return rank, pivots, value


def solution_affine(rref_matrix, pivots, modulus, prime):
    free = [column for column in range(3) if column not in pivots]
    rows = {pivot: rref_matrix[index]
            for index, pivot in enumerate(pivots) if pivot < 3}
    zero = nmod_poly([], prime)
    constants = []
    coefficients = []
    for variable in range(3):
        if variable not in rows:
            constants.append(zero)
            coefficients.append([
                nmod_poly([1], prime) if column == variable else zero
                for column in free])
            continue
        row = rows[variable]
        constants.append((-row[3]) % modulus)
        coefficients.append([(-row[column]) % modulus for column in free])
    return free, constants, coefficients


def compose_affine(form, constants, coefficients, modulus, prime):
    one = nmod_poly([1], prime)
    constant = (form[3] + one) % modulus
    for coefficient, value in zip(form[:3], constants):
        constant = (constant + coefficient*value) % modulus
    free_coefficients = []
    for parameter in range(len(coefficients[0])):
        value = nmod_poly([], prime)
        for coefficient, row in zip(form[:3], coefficients):
            value = (value + coefficient*row[parameter]) % modulus
        free_coefficients.append(value)
    return constant, free_coefficients


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rur", type=Path, default=DEFAULT_RUR_PATH)
    parser.add_argument("--result", type=Path, default=DEFAULT_RESULT)
    parser.add_argument("--prime", type=int, default=1073741827)
    args = parser.parse_args()
    rur_path = args.rur
    encoded = rur_path.read_text().strip()
    require(encoded.endswith(":"), "the frozen RUR lost its delimiter")
    envelope = ast.literal_eval(encoded[:-1])
    payload = envelope[1]
    prime = payload[0]
    require(prime == args.prime and payload[1:4] ==
            [4, 268, ["x", "b1", "d1", "b0"]],
            "the frozen RUR header changed")
    require(payload[4] == [0, 0, 0, 1],
            "b0 ceased to be the RUR separating variable")
    data = payload[5][1]
    eliminant = nmod_poly(data[0][1], prime)
    require(eliminant.degree() == 268 and data[1] == [0, [1]],
            "the RUR denominator/eliminant contract changed")
    numerators = [nmod_poly(entry[0][1], prime) for entry in data[2]]
    require(len(numerators) == 3,
            "the RUR coordinate numerator count changed")
    unit, factored = eliminant.factor()
    require(int(unit) == 1 and all(exponent == 1
                                   for _, exponent in factored),
            "the RUR eliminant is no longer monic squarefree")

    raw_rows, _ = SOURCE.SOURCE.data()
    rows = {label: SOURCE.expression(poly) for label, poly, _ in raw_rows}
    derived = AUDIT.derive(rows)
    interface = AUDIT.INTERFACE.derive(rows)
    normalized = interface[6]
    p3_p4 = interface[3]
    a0_value = interface[4]
    b0, b1, _, d1, _, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    variables4 = (b0, b1, d1, x)
    variables5 = (b0, b1, d1, x, d4)
    matrix_terms = [[compile_poly(entry, variables5) for entry in row]
                    for row in normalized]
    unknowns = (SOURCE.P[0], SOURCE.P[1], SOURCE.A5)
    selected_expressions = [SOURCE.P[0], SOURCE.P[1],
                            p3_p4[SOURCE.P[2]], p3_p4[SOURCE.P[3]]]
    selected_forms = []
    for expression in selected_expressions:
        coefficients = [sp.cancel(sp.diff(expression, unknown))
                        for unknown in unknowns]
        constant = sp.cancel(expression.subs({unknown: 0
                                              for unknown in unknowns}))
        require(sp.cancel(expression-sum(coefficient*unknown
                                         for coefficient, unknown in
                                         zip(coefficients, unknowns))
                          - constant) == 0,
                "a selected p expression ceased to be affine")
        selected_forms.append([*coefficients, constant])
    ratio = {SOURCE.PARAMETERS[2]: x*b1,
             SOURCE.PARAMETERS[4]: -x*d1*d4}
    hafnian = SOURCE.expression(SOURCE.SOURCE.data()[1])
    hafnian = sp.cancel(hafnian.subs(ratio).subs(p3_p4).subs(
        SOURCE.A0, a0_value))
    hafnian_variables = (*variables5, *unknowns)
    omitted_labels = tuple(f"cofactor_{edge}_3" for edge in range(1, 6))
    omitted_expressions = [sp.cancel(
        rows[label].subs(ratio).subs(p3_p4).subs(SOURCE.A0, a0_value))
        for label in omitted_labels]

    components = []
    degree_profile = {}
    status_profile = {}
    for index, (factor, exponent) in enumerate(factored):
        degree_profile[factor.degree()] = degree_profile.get(
            factor.degree(), 0) + 1
        parameter = nmod_poly([0, 1], prime) % factor
        # msolve encodes every non-separating coordinate as -numerator.
        x_value = (-numerators[0]) % factor
        b1_value = (-numerators[1]) % factor
        d1_value = (-numerators[2]) % factor
        values4 = (parameter, b1_value, d1_value, x_value)
        d4_value = evaluate_rational(
            derived["d4_value"], variables4, values4, factor, prime)
        values5 = (*values4, d4_value)
        matrix = [[evaluate_terms(entry, values5, factor, prime)
                   for entry in row] for row in matrix_terms]
        rank_coeff, _, _ = rref([row[:3] for row in matrix],
                                factor, prime, 3)
        rank_augmented, pivots, reduced = rref(matrix, factor, prime, 4)
        if rank_coeff != rank_augmented:
            status = "inconsistent_determinantal_false_positive"
            forced_selected = [False]*4
        else:
            free, constants, coefficients = solution_affine(
                reduced, pivots, factor, prime)
            evaluated_forms = [[evaluate_rational(
                entry, variables5, values5, factor, prime)
                for entry in form] for form in selected_forms]
            forced_selected = []
            for form in evaluated_forms:
                constant, free_coefficients = compose_affine(
                    form, constants, coefficients, factor, prime)
                forced_selected.append(
                    not len(constant)
                    and not any(len(entry) for entry in free_coefficients))
            status = ("necessary_subsystem_forces_p1_or_p2_boundary"
                      if any(forced_selected[:2])
                      else "necessary_subsystem_forces_p3_or_p4_boundary"
                      if any(forced_selected[2:])
                      else "necessary_subsystem_selected_possible")
        hafnian_live = None
        omitted_nonzero = None
        field_values = None
        if rank_coeff == rank_augmented == 3:
            require(not free, "a rank-three packet retained a free unknown")
            hafnian_value = evaluate_rational(
                hafnian, hafnian_variables, (*values5, *constants),
                factor, prime)
            hafnian_live = bool(len(hafnian_value))
            if status == "necessary_subsystem_selected_possible" \
                    and not hafnian_live:
                status = "necessary_subsystem_selected_but_hafnian_zero"
            omitted_values = [evaluate_rational(
                expression, hafnian_variables, (*values5, *constants),
                factor, prime) for expression in omitted_expressions]
            omitted_nonzero = [bool(len(value)) for value in omitted_values]
            if status == "necessary_subsystem_selected_possible":
                status = ("full_packet_modular_candidate"
                          if not any(omitted_nonzero)
                          else "necessary_subsystem_fails_omitted_cofactor")
            if factor.degree() == 2:
                selected_values = []
                for form in evaluated_forms:
                    value, free_coefficients = compose_affine(
                        form, constants, coefficients, factor, prime)
                    require(not free_coefficients,
                            "a quadratic rank-three point retained freedom")
                    selected_values.append(
                        (value-nmod_poly([1], prime)) % factor)
                a0_component = evaluate_rational(
                    a0_value, hafnian_variables,
                    (*values5, *constants), factor, prime)
                b3_value = (x_value*b1_value) % factor
                d3_value = (-x_value*d1_value*d4_value) % factor
                names = ("b0", "b1", "b3", "d1", "d3", "d4",
                         "p1", "p2", "p3", "p4", "a0", "a5", "H")
                values = (parameter, b1_value, b3_value, d1_value,
                          d3_value, d4_value, selected_values[0],
                          selected_values[1], selected_values[2],
                          selected_values[3], a0_component, constants[2],
                          hafnian_value)
                field_values = {
                    name: field_coefficients(value, factor.degree())
                    for name, value in zip(names, values)}
        status_profile[status] = status_profile.get(status, 0) + 1
        components.append({
            "index": index,
            "degree": factor.degree(),
            "factor_coefficients": field_coefficients(
                factor, factor.degree() + 1),
            "factor_sha256": poly_digest(factor),
            "rank_coefficient": rank_coeff,
            "rank_augmented": rank_augmented,
            "forced_selected_boundary": forced_selected,
            "pure_hafnian_live": hafnian_live,
            "omitted_lower_cofactor_nonzero": omitted_nonzero,
            "quadratic_field_values": field_values,
            "status": status,
        })

    result = {
        "status": "UNAUDITED modular literal packet component census",
        "prime": prime,
        "rur_file_sha256": sha256(rur_path.read_bytes()).hexdigest(),
        "eliminant_degree": eliminant.degree(),
        "eliminant_sha256": poly_digest(eliminant),
        "factor_degree_profile": {str(key): value
                                  for key, value in sorted(degree_profile.items())},
        "component_status_profile": status_profile,
        "replayed_packet_rows": [
            "cofactor_1_0", "cofactor_2_0", "cofactor_3_0",
            "cofactor_4_0", "cofactor_5_0", "t_012", "t_013",
            "t_023", "t_123", "cofactor_0_0", "cofactor_0_3"],
        "omitted_literal_rows": [
            "cofactor_1_3", "cofactor_2_3", "cofactor_3_3",
            "cofactor_4_3", "cofactor_5_3"],
        "components": components,
        "scope": (
            "Modular discovery only. Each factor is replayed in its exact "
            "finite extension field against the source-derived U/Q solve, "
            "six literal augmented rows, and four selected p_i+1 factors. "
            "The pure Hafnian is evaluated on every rank-three component. "
            "The five displayed lower cofactors are NOT part of this "
            "necessary determinantal subsystem, so a surviving component "
            "is not a full one-colour packet point. No characteristic-zero "
            "point-existence claim is made."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("all-minor modular component census: PASS")
    print("factor degrees:", result["factor_degree_profile"])
    print("statuses:", result["component_status_profile"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
