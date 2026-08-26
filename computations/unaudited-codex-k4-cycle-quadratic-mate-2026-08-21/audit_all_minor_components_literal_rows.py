#!/usr/bin/env python3
"""Literal-source referee for the modular k4-cycle RUR components.

The producer's ``all_minor_components`` files replay a six-row rank
interface.  They do not establish that the decoded RUR factors satisfy the
whole one-colour source packet.  This referee decodes every irreducible
factor at each frozen prime, reconstructs the p-coordinate point, and
evaluates all 22 literal rows: six permanent equations, four triple rows,
and both selected cofactors on every edge.

This is a finite-field scope audit.  It neither lifts components to
characteristic zero nor launches the arbitrary-mate solve.
"""

from __future__ import annotations

import ast
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
COMPONENT_PATH = BRIDGE / "probe_branch0_cycle_delta_au_open_all_minor_components.py"
PCOORD_PATH = BRIDGE / "probe_branch0_cycle_pcoords.py"
RURS = (
    (1073741827,
     BRIDGE / "results_branch0_cycle_delta_au_open_all_minors_parametrize.param.out"),
    (1073741789,
     BRIDGE / "results_branch0_cycle_delta_au_open_all_minors_p1073741789_parametrize.param.out"),
)
OUT = HERE / "results_all_minor_components_literal_rows.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


COMP = load("k4_literal_component_decoder", COMPONENT_PATH)
PCOORD = load("k4_literal_pcoord_source", PCOORD_PATH)
sp = COMP.sp
nmod_poly = COMP.nmod_poly


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def logical_digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode("ascii")).hexdigest()


def coefficient_payload(value, degree):
    return [int(value[index]) if index < len(value) else 0
            for index in range(degree)]


def value_digest(value, degree):
    return sha256(json.dumps(coefficient_payload(value, degree),
                             separators=(",", ":")).encode("ascii")).hexdigest()


def evaluate_counter(poly, values, modulus, prime):
    """Evaluate a Counter exponent polynomial in F_p[z]/(modulus)."""
    answer = nmod_poly([], prime)
    for exponent, coefficient in poly.items():
        coefficient = Fraction(coefficient)
        scalar = (coefficient.numerator
                  * pow(coefficient.denominator, -1, prime)) % prime
        term = nmod_poly([scalar], prime)
        for value, power in zip(values, exponent):
            require(power >= 0, "the cleared p-coordinate row stayed Laurent")
            if power:
                term = (term * value.pow_mod(power, modulus)) % modulus
        answer = (answer + term) % modulus
    return answer


def parse_rur(prime, path):
    encoded = path.read_text().strip()
    require(encoded.endswith(":"), "frozen RUR lost its delimiter")
    envelope = ast.literal_eval(encoded[:-1])
    payload = envelope[1]
    require(payload[:4] == [prime, 4, 268, ["x", "b1", "d1", "b0"]],
            "RUR header changed")
    require(payload[4] == [0, 0, 0, 1],
            "b0 ceased to be the separating variable")
    data = payload[5][1]
    eliminant = nmod_poly(data[0][1], prime)
    require(eliminant.degree() == 268 and data[1] == [0, [1]],
            "RUR denominator/eliminant contract changed")
    numerators = [nmod_poly(entry[0][1], prime) for entry in data[2]]
    require(len(numerators) == 3, "RUR coordinate numerator count changed")
    unit, factors = eliminant.factor()
    require(int(unit) == 1 and all(multiplicity == 1
                                   for _, multiplicity in factors),
            "RUR eliminant is not monic squarefree")
    return eliminant, numerators, tuple(factor for factor, _ in factors)


def source_interface():
    raw_rows, _ = COMP.SOURCE.SOURCE.data()
    rows = {label: COMP.SOURCE.expression(poly)
            for label, poly, _ in raw_rows}
    derived = COMP.AUDIT.derive(rows)
    interface = COMP.AUDIT.INTERFACE.derive(rows)
    normalized = interface[6]
    p3_p4 = interface[3]
    a0_value = interface[4]
    b0, b1, _, d1, _, d4 = COMP.SOURCE.PARAMETERS
    x = sp.Symbol("x")
    variables4 = (b0, b1, d1, x)
    variables5 = (*variables4, d4)
    matrix_terms = [[COMP.compile_poly(entry, variables5) for entry in row]
                    for row in normalized]
    unknowns = (COMP.SOURCE.P[0], COMP.SOURCE.P[1], COMP.SOURCE.A5)
    selected_expressions = [COMP.SOURCE.P[0], COMP.SOURCE.P[1],
                            p3_p4[COMP.SOURCE.P[2]],
                            p3_p4[COMP.SOURCE.P[3]]]
    selected_forms = []
    for expression in selected_expressions:
        coefficients = [sp.cancel(sp.diff(expression, unknown))
                        for unknown in unknowns]
        constant = sp.cancel(expression.subs({unknown: 0
                                              for unknown in unknowns}))
        require(sp.cancel(expression - sum(coefficient*unknown
                                            for coefficient, unknown in
                                            zip(coefficients, unknowns))
                          - constant) == 0,
                "a selected p expression ceased to be affine")
        selected_forms.append([*coefficients, constant])
    return {
        "derived": derived,
        "variables4": variables4,
        "variables5": variables5,
        "matrix_terms": matrix_terms,
        "selected_forms": selected_forms,
        "a0_value": a0_value,
    }


INTERFACE = source_interface()
DIRECT_ROWS, HAFNIAN = PCOORD.data()
EXPECTED_DIRECT_LABELS = tuple(
    [f"t_{i}{j}{k}" for i, j, k in ((0, 1, 2), (0, 1, 3),
                                     (0, 2, 3), (1, 2, 3))]
    + [f"cofactor_{edge}_{position}"
       for edge in range(6) for position in (0, 3)])
require(tuple(label for label, _, _ in DIRECT_ROWS) == EXPECTED_DIRECT_LABELS,
        "the direct 16-row source ledger changed")


def decode_component(prime, factor, numerators):
    parameter = nmod_poly([0, 1], prime) % factor
    x_value = (-numerators[0]) % factor
    b1_value = (-numerators[1]) % factor
    d1_value = (-numerators[2]) % factor
    values4 = (parameter, b1_value, d1_value, x_value)
    d4_value = COMP.evaluate_rational(
        INTERFACE["derived"]["d4_value"], INTERFACE["variables4"],
        values4, factor, prime)
    values5 = (*values4, d4_value)
    matrix = [[COMP.evaluate_terms(entry, values5, factor, prime)
               for entry in row] for row in INTERFACE["matrix_terms"]]
    rank_coeff, _, _ = COMP.rref([row[:3] for row in matrix],
                                 factor, prime, 3)
    rank_augmented, pivots, reduced = COMP.rref(matrix, factor, prime, 4)
    require(rank_coeff == rank_augmented == 3,
            "an exported component ceased to be rank-three consistent")
    free, constants, coefficients = COMP.solution_affine(
        reduced, pivots, factor, prime)
    require(not free, "rank-three component retained a free source unknown")

    evaluated_forms = [[COMP.evaluate_rational(
        entry, INTERFACE["variables5"], values5, factor, prime)
        for entry in form] for form in INTERFACE["selected_forms"]]
    selected_values = []
    one = nmod_poly([1], prime)
    for form in evaluated_forms:
        shifted, free_coefficients = COMP.compose_affine(
            form, constants, coefficients, factor, prime)
        require(not free_coefficients, "selected p retained affine freedom")
        selected_values.append((shifted-one) % factor)

    a0_value = COMP.evaluate_rational(
        INTERFACE["a0_value"],
        (*INTERFACE["variables5"],
         COMP.SOURCE.P[0], COMP.SOURCE.P[1], COMP.SOURCE.A5),
        (*values5, *constants), factor, prime)
    b3_value = (x_value*b1_value) % factor
    d3_value = (-x_value*d1_value*d4_value) % factor
    values = (selected_values[0], selected_values[1],
              selected_values[2], selected_values[3],
              a0_value, constants[2], parameter, b1_value, b3_value,
              d1_value, d3_value, d4_value)
    require(len(values) == len(PCOORD.NAMES), "p-coordinate arity changed")
    return values


def literal_census(prime, factor, values, mutation=False):
    degree = factor.degree()
    rows = []
    # The six permanent rows are literal source equations.  In this chart
    # c_e=-(1+a_e*d_e)/b_e, so their evaluated numerator is the exact zero
    # identity 1+a_e*d_e+b_e*c_e=0.  Record them rather than silently
    # dropping them from the p-coordinate source.
    for edge in range(6):
        rows.append({"label": f"permanent_edge_{edge}",
                     "value_coefficients": [0]*degree,
                     "value_sha256": value_digest(nmod_poly([], prime), degree),
                     "zero": True,
                     "evaluation": "1+a_e*d_e+b_e*c_e by chart definition"})

    mutated_fired = False
    for label, poly, _ in DIRECT_ROWS:
        candidate = poly
        if mutation and label == "cofactor_1_3":
            candidate = Counter(poly)
            key = sorted(candidate)[0]
            candidate[key] = -candidate[key]
        value = evaluate_counter(candidate, values, factor, prime)
        if mutation and label == "cofactor_1_3":
            original = evaluate_counter(poly, values, factor, prime)
            mutated_fired = value != original
        rows.append({"label": label,
                     "value_coefficients": coefficient_payload(value, degree),
                     "value_sha256": value_digest(value, degree),
                     "zero": not len(value),
                     "evaluation": "literal cleared p-coordinate source row"})
    require(len(rows) == 22, "literal row ledger ceased to have 22 rows")
    h_value = evaluate_counter(HAFNIAN, values, factor, prime)
    return rows, h_value, mutated_fired


def audit_prime(prime, rur_path):
    eliminant, numerators, factors = parse_rur(prime, rur_path)
    components = []
    failure_histogram = {}
    omitted_failure_histogram = {}
    mutation_fired = False
    for index, factor in enumerate(factors):
        values = decode_component(prime, factor, numerators)
        rows, h_value, _ = literal_census(prime, factor, values)
        mutated, _, fired = literal_census(prime, factor, values,
                                           mutation=True)
        mutation_fired = mutation_fired or fired
        failed = [row["label"] for row in rows if not row["zero"]]
        omitted = [label for label in failed if label.endswith("_3")
                   and label.startswith("cofactor_")
                   and label != "cofactor_0_3"]
        for label in failed:
            failure_histogram[label] = failure_histogram.get(label, 0) + 1
        for label in omitted:
            omitted_failure_histogram[label] = (
                omitted_failure_histogram.get(label, 0) + 1)
        imposed_labels = {
            "t_012", "t_013", "t_023", "t_123",
            "cofactor_0_0", "cofactor_0_3",
            "cofactor_1_0", "cofactor_2_0", "cofactor_3_0",
            "cofactor_4_0", "cofactor_5_0",
        }
        require(all(row["zero"] for row in rows
                    if row["label"] in imposed_labels),
                "producer's displayed reduced-interface rows do not vanish")
        require(failed, "an all-minor factor unexpectedly passed all source rows")
        require(omitted, "a factor was not killed by an omitted lower cofactor")

        one = nmod_poly([1], prime)
        p_values = values[:4]
        chart_values = values[6:]
        guards = {
            "H_nonzero": bool(len(h_value)),
            "p1_p2_p3_p4_nonzero": [bool(len(value))
                                      for value in p_values],
            "one_plus_p1_p2_p3_p4_nonzero": [
                bool(len((one+value) % factor)) for value in p_values],
            "b0_b1_b3_d1_d3_d4_nonzero": [bool(len(value))
                                            for value in chart_values],
        }
        require(guards["H_nonzero"]
                and all(guards["p1_p2_p3_p4_nonzero"])
                and all(guards["one_plus_p1_p2_p3_p4_nonzero"])
                and all(guards["b0_b1_b3_d1_d3_d4_nonzero"]),
                "a frozen selected-live or H guard failed")
        components.append({
            "factor_index": index,
            "factor_degree": factor.degree(),
            "factor_coefficients": coefficient_payload(
                factor, factor.degree()+1),
            "factor_sha256": COMP.poly_digest(factor),
            "literal_rows": rows,
            "failed_row_labels": failed,
            "omitted_lower_cofactor_failures": omitted,
            "literal_H_coefficients": coefficient_payload(h_value,
                                                            factor.degree()),
            "literal_H_sha256": value_digest(h_value, factor.degree()),
            "guards": guards,
            "status": "REJECTED_BY_OMITTED_LITERAL_COFACTOR",
        })

    require(len(factors) == 16, "frozen factor count changed")
    require(mutation_fired,
            "must-fire mutation of cofactor_1_3 changed no component value")
    return {
        "prime": prime,
        "rur_path": str(rur_path.relative_to(HERE.parent.parent)),
        "rur_sha256": sha256(rur_path.read_bytes()).hexdigest(),
        "eliminant_sha256": COMP.poly_digest(eliminant),
        "factor_count": len(factors),
        "factor_degree_profile": {
            str(degree): sum(factor.degree() == degree for factor in factors)
            for degree in sorted({factor.degree() for factor in factors})},
        "component_status_profile": {
            "REJECTED_BY_OMITTED_LITERAL_COFACTOR": len(factors)},
        "failed_row_component_counts": dict(sorted(failure_histogram.items())),
        "omitted_lower_cofactor_component_counts": dict(
            sorted(omitted_failure_histogram.items())),
        "must_fire": {
            "mutation": "negate the lex-first coefficient of cofactor_1_3",
            "changed_at_least_one_component_value": mutation_fired,
            "reduced_interface_without_omitted_rows_accepts_all_components": True,
            "full_literal_22_row_replay_rejects_all_components": True,
        },
        "components": components,
    }


def main():
    primes = [audit_prime(prime, path) for prime, path in RURS]
    result = {
        "status": "UNAUDITED independent literal-source scope referee PASS",
        "source_ledger": {
            "permanent_rows": [f"permanent_edge_{edge}" for edge in range(6)],
            "triple_rows": ["t_012", "t_013", "t_023", "t_123"],
            "cofactor_rows": [f"cofactor_{edge}_{position}"
                                for edge in range(6) for position in (0, 3)],
            "total": 22,
        },
        "producer_scope_defect": (
            "The frozen component checker used the rank-three necessary "
            "subsystem but did not impose cofactor_1_3 through "
            "cofactor_5_3. Every decoded factor at both primes is killed "
            "by at least one of those five literal rows."),
        "prime_audits": primes,
        "scope": (
            "Finite-field source replay only. The rejected factors are not "
            "points of the full 22-row one-colour packet, so no fixed-left "
            "mate ideal may be built from them. This says nothing about "
            "the positive-dimensional characteristic-zero all-minor "
            "scheme or other finite-field components."),
    }
    result["result_sha256"] = logical_digest(result)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("all-minor full literal-row referee: PASS")
    for audit in primes:
        print(audit["prime"], audit["factor_degree_profile"],
              audit["failed_row_component_counts"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
