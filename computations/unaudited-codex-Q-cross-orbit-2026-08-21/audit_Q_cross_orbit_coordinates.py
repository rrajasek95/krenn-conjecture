#!/usr/bin/env python3
"""Exact big-cell reduction of cross-colour compatibility on the Q0 orbit."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20"
S6_PATH = BASE / "audit_weight0_support6_char0_component.py"
OUT = HERE / "results_Q_cross_orbit_coordinates.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


S6 = load("Q_cross_orbit_support6", S6_PATH)
w = sp.sqrt(2)
half = sp.Rational(1, 2)


def k_to_sympy(value):
    # The frozen support-six artifact uses z^2+2z-1 and z=-1+sqrt(2).
    return sp.Rational(value[0]) + sp.Rational(value[1]) * (-1+w)


def evaluate(poly, entries):
    answer = sp.Integer(0)
    for monomial, coefficient in poly.items():
        term = sp.Integer(coefficient)
        for variable in monomial:
            term *= entries[variable]
        answer += term
    return sp.expand(answer)


def derivative(poly, variable):
    return S6.derivative(poly, variable)


def frozen_q_and_matrix():
    entries = tuple(k_to_sympy(value) for value in S6.raw_entries())
    values = tuple(evaluate(S6.SCREEN.q_poly(index), entries)
                   for index in range(16))
    expected = {
        3: -2*(1+w), 5: 2*(w-1), 6: 2,
        9: -2, 10: 2*(1+w), 12: -2*(w-1),
    }
    observed_support = {index for index, value in enumerate(values)
                        if value != 0}
    require(observed_support == set(expected), "frozen Q0 support changed")
    require(all(sp.factor(values[index]-value, extension=w) == 0
                for index, value in expected.items()), "frozen Q0 changed")
    matrix = sp.zeros(4, 4)
    for left in range(4):
        for right in range(left+1, 4):
            coefficient = values[(1 << left) | (1 << right)]
            matrix[left, right] = matrix[right, left] = coefficient
    require(sp.factor(matrix.det(), extension=w) == 80,
            "Q0 quadratic matrix determinant changed")
    return entries, values, matrix


def direct_box_reduction(matrix):
    xs = sp.symbols("x0:4")
    ds = sp.symbols("d0:4")
    xvec, dvec = sp.Matrix(xs), sp.Matrix(ds)
    C = sp.expand(half*(xvec.T*matrix*xvec)[0])
    gradient = matrix*xvec
    direct = {}
    reduced = {}
    for left in range(4):
        for right in range(left+1, 4):
            point = xvec.copy()
            point[left] += dvec[left]
            point[right] += dvec[right]
            value = sp.expand(half*(point.T*matrix*point)[0])
            formula = sp.expand(
                C + dvec[left]*gradient[left]
                + dvec[right]*gradient[right]
                + matrix[left, right]*dvec[left]*dvec[right])
            require(sp.expand(value-formula) == 0,
                    "box evaluation reduction failed")
            direct[(left, right)] = value
            reduced[(left, right)] = formula
    return xs, ds, C, direct, reduced


def d_components(matrix):
    r, u, t = sp.symbols("r u t")
    d = (sp.Integer(1), r, u, t)
    E = {(i, j): sp.expand(matrix[i, j]*d[i]*d[j])
         for i in range(4) for j in range(i+1, 4)}
    sums = (E[0, 1]+E[2, 3], E[0, 2]+E[1, 3],
            E[0, 3]+E[1, 2])
    equations = (sp.expand(sums[0]-sums[1]),
                 sp.expand(sums[0]-sums[2]))
    resultant = sp.factor(sp.resultant(*equations, t), extension=w)
    f1 = r+(3-2*w)*u
    f2 = r*u+(1+w)*r+(1-w)*u+1
    ratio = sp.factor(resultant/(f1*f2), extension=w)
    require(sp.expand(ratio-(4+4*w)) == 0,
            "d-component resultant changed")

    components = (
        {
            "name": "A",
            "r": -(3-2*w)*u,
            "t": (w-1)*u*(u+1+w)/(u-1-w),
            "resultant_factor": f1,
        },
        {
            "name": "B",
            "r": ((w-1)*u-1)/(u+1+w),
            "t": sp.Integer(-1),
            "resultant_factor": f2,
        },
    )
    for component in components:
        substitutions = {r: component["r"], t: component["t"]}
        require(all(sp.factor(eq.subs(substitutions), extension=w) == 0
                    for eq in equations),
                f"d-component {component['name']} failed")

    # At exactly the excluded parameter values some d_i vanishes; hence no
    # localized GL2 point was discarded by the rational parametrizations.
    exceptional = (sp.Integer(0), 1+w, -1-w)
    exceptional_solutions = {}
    for value in exceptional:
        sols = sp.solve([eq.subs(u, value) for eq in equations], [r, t],
                        dict=True)
        require(sols and all(value == 0 or sol[r] == 0 or sol[t] == 0
                             for sol in sols),
                "an exceptional parameter retained all nonzero d entries")
        exceptional_solutions[sp.sstr(value)] = [
            {str(key): sp.sstr(sp.factor(val, extension=w))
             for key, val in sol.items()} for sol in sols]
    return u, equations, resultant, components, exceptional_solutions


def reconstruction_component(matrix, u, component):
    C = sp.symbols("C")
    d = sp.Matrix((1, component["r"], u, component["t"]))
    E = {(i, j): sp.expand(matrix[i, j]*d[i]*d[j])
         for i in range(4) for j in range(i+1, 4)}
    edge_sums = {edge: -value for edge, value in E.items()}
    v0 = half*(edge_sums[0, 1]+edge_sums[0, 2]-edge_sums[1, 2])
    v1 = half*(edge_sums[0, 1]+edge_sums[1, 2]-edge_sums[0, 2])
    v2 = half*(edge_sums[0, 2]+edge_sums[1, 2]-edge_sums[0, 1])
    v3 = edge_sums[0, 3]-v0
    v = sp.Matrix((v0, v1, v2, v3))
    for i in range(4):
        for j in range(i+1, 4):
            require(sp.factor(v[i]+v[j]+E[i, j], extension=w) == 0,
                    f"v reconstruction failed on {component['name']}")
    Dinv = sp.diag(*[sp.Integer(1)/entry for entry in d])
    R = Dinv*matrix.inv()*Dinv
    shifted = v-half*C*sp.ones(4, 1)
    phi_rational = sp.cancel(C-half*(shifted.T*R*shifted)[0])
    numerator, denominator = phi_rational.as_numer_denom()
    polynomial = sp.Poly(sp.expand(numerator), C)
    require(polynomial.degree() == 2,
            f"C reconstruction ceased to be quadratic on {component['name']}")
    aa, bb, cc = polynomial.all_coeffs()
    discriminant = sp.expand(bb*bb-4*aa*cc)
    factorization = sp.factor_list(sp.Poly(discriminant, u, extension=w))
    odd_factors = [factor.monic().as_expr()
                   for factor, exponent in factorization[1]
                   if exponent % 2]
    squarefree = sp.factor(sp.prod(odd_factors), extension=w)
    if component["name"] == "A":
        expected = ((u**2+3+2*w)
                    * (u**2+4*(1+w)*u+15+10*w))
    else:
        expected = ((u**2+3+2*w)
                    * (u**2-sp.Rational(4, 5)*(1+w)*u
                       + sp.Rational(1, 5)*(3+2*w)))
    require(sp.factor(squarefree-expected, extension=w) == 0,
            f"squarefree C discriminant changed on {component['name']}")
    expected_factorization = sp.factor_list(
        sp.Poly(expected, u, extension=w))[1]
    require(len(expected_factorization) == 2
            and all(exponent == 1 and factor.degree() == 2
                    for factor, exponent in expected_factorization),
            f"C cover became reducible/square on {component['name']}")

    # Given a root C, this is the exact inverse reconstruction.  The six
    # required output coordinates then vanish identically.
    x = matrix.inv()*Dinv*shifted
    for i in range(4):
        for j in range(i+1, 4):
            value = sp.cancel(C + d[i]*(matrix*x)[i]
                              + d[j]*(matrix*x)[j]
                              + matrix[i, j]*d[i]*d[j])
            require(sp.factor(value.as_numer_denom()[0], extension=w) == 0,
                    f"reconstructed compatibility row failed on {component['name']}")
    return {
        "name": component["name"],
        "d1": sp.sstr(sp.factor(component["r"], extension=w)),
        "d2": "u",
        "d3": sp.sstr(sp.factor(component["t"], extension=w)),
        "excluded_u": ["0", "1+sqrt(2)", "-1-sqrt(2)"],
        "C_equation": (
            "C - 1/2*(v-C/2*1)^T*D^-1*M^-1*D^-1*(v-C/2*1)=0"),
        "C_discriminant_squarefree_part": sp.sstr(expected),
        "cover_verdict": (
            "irreducible quadratic cover over Q(sqrt(2))(u); the squarefree "
            "part is a product of two distinct irreducible quadratics"),
        "x_reconstruction": "x=M^-1*D^-1*(v-C/2*1), y=x+d",
        "cleared_C_denominator_terms": len(sp.Poly(denominator, u).terms()),
    }


def lie_stabilizer(matrix, q_values):
    columns = []
    labels = []
    for site in range(4):
        for output_bit in range(2):
            for input_bit in range(2):
                column = [sp.Integer(0)]*16
                for index, value in enumerate(q_values):
                    if value == 0 or ((index >> site) & 1) != input_bit:
                        continue
                    out = ((index & ~(1 << site))
                           | (output_bit << site))
                    column[out] += value
                columns.append(column)
                labels.append((site, output_bit, input_bit))
    action = sp.Matrix(16, 16, lambda row, col: columns[col][row])
    rank = action.rank()
    require(rank == 12 and len(action.nullspace()) == 4,
            "Q0 Lie stabilizer dimension changed")
    return rank, labels


def normal_form(q_values):
    # Diagonal local gauges can make each complementary pair equal.  These
    # six desired pair products are mutually consistent (their complementary
    # products all equal one), so a solution t_i exists over Q(sqrt(2),i).
    I = sp.I
    desired = {3: 2, 12: 2, 5: 2, 10: 2, 6: 2*I, 9: 2*I}
    pair_products = {}
    for index, target in desired.items():
        pair_products[index] = sp.factor(target/q_values[index], extension=w)
    require(sp.simplify(pair_products[3]*pair_products[12]) == 1
            and sp.simplify(pair_products[5]*pair_products[10]) == 1
            and sp.simplify(pair_products[6]*pair_products[9]) == 1,
            "normal-form diagonal gauge consistency changed")
    parameters = (sp.Integer(2), 2+2*I, 2-2*I, sp.Integer(-2))
    a, b, c, d = parameters
    canonical = {
        0: (a+d)/2, 15: (a+d)/2,
        3: (a-d)/2, 12: (a-d)/2,
        5: (b+c)/2, 10: (b+c)/2,
        6: (b-c)/2, 9: (b-c)/2,
    }
    require(all(sp.expand(canonical[index]-desired.get(index, 0)) == 0
                for index in canonical), "Verstraete normal form changed")
    return pair_products, parameters


def cofactor_tangent(entries):
    _, hafnian = S6.SCREEN.PROBE.equations(S6.SCREEN.branch_bits(51))
    q_polys = [S6.SCREEN.q_poly(index) for index in range(16)]
    cofactor_polys = [derivative(hafnian, variable)
                      for variable in range(24)]
    jq = sp.Matrix([[evaluate(derivative(poly, variable), entries)
                     for variable in range(24)] for poly in q_polys])
    jc = sp.Matrix([[evaluate(derivative(poly, variable), entries)
                     for variable in range(24)] for poly in cofactor_polys])
    require((jq.rank(), jc.rank(), jq.col_join(jc).rank()) == (14, 23, 24),
            "Q/cofactor tangent ranks changed")
    tangent = sp.zeros(24, 1)
    assignments = {
        1: (1-w)/2, 2: (w-1)/2,
        5: (w-1)/2, 6: (1-w)/2,
        9: sp.Rational(1, 2), 10: -sp.Rational(1, 2), 13: 1,
    }
    for index, value in assignments.items():
        tangent[index] = value
    q_change = jq*tangent
    cofactor_change = jc*tangent
    require(q_change == sp.zeros(16, 1),
            "declared tangent stopped fixing Q to first order")
    require(sp.factor(cofactor_change[13]-(w-2), extension=w) == 0,
            "declared cofactor tangent must-fire changed")
    return {
        "Q_jacobian_rank_at_Q0_presentation": 14,
        "cofactor_jacobian_rank": 23,
        "stacked_rank": 24,
        "kernel_tangent_nonzero_entries": {
            str(index): sp.sstr(value) for index, value in assignments.items()},
        "cofactor13_derivative_on_tangent": "-2+sqrt(2)",
        "conclusion": (
            "The 24 edge-entry cofactors vary on a first-order fibre of the "
            "six-block-to-Q map. They therefore are not a regular standard "
            "covariant determined by the four-qubit tensor Q alone; they are "
            "presentation-level Hafnian-gradient data."),
    }


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    entries, q_values, matrix = frozen_q_and_matrix()
    _, _, _, direct, _ = direct_box_reduction(matrix)
    u, d_equations, resultant, components, exceptional = d_components(matrix)
    component_records = [reconstruction_component(matrix, u, component)
                         for component in components]
    action_rank, _ = lie_stabilizer(matrix, q_values)
    pair_products, parameters = normal_form(q_values)
    cofactor_record = cofactor_tangent(entries)

    result = {
        "status": "UNAUDITED exact Q0 cross-orbit coordinate reduction PASS",
        "field": "Q(sqrt(2)); normal-form comparison adjoins i",
        "left_Q_support": [3, 5, 6, 9, 10, 12],
        "compatibility_reduction": {
            "direct_orbit_not_closure": (
                "Right rows are literal GL2 rows [1,x_i],[1,y_i], with "
                "d_i=y_i-x_i nonzero. Thus the calculation parametrizes a "
                "dense big cell of the actual orbit g.Q0, not merely an "
                "invariant fibre or orbit closure."),
            "equation_count": len(direct),
            "equations": (
                "F(x+1_{ij}d)=C+u_i+u_j+q_ij*d_i*d_j=0 for all i<j"),
            "definitions": (
                "F(t)=sum q_ij*t_i*t_j, C=F(x), "
                "u_i=d_i*(M*x)_i, v_i=u_i+C/2"),
            "eliminated_condition": (
                "E01+E23=E02+E13=E03+E12, Eij=q_ij*d_i*d_j"),
            "d_resultant_d0_equal_1": sp.sstr(resultant),
            "exceptional_parameters_have_a_zero_d": exceptional,
        },
        "components_in_big_row_chart": component_records,
        "dimension_ledger": {
            "normalized_row_direction_component": 1,
            "restore_common_weight2_scaling": 2,
            "restore_eight_output_row_scalars_GL_preimage": 10,
            "Q0_GL2x4_orbit_dimension": action_rank,
            "Q0_stabilizer_dimension": 16-action_rank,
            "compatible_tensor_family_dimension_each": 6,
            "component_guard": (
                "The two irreducible components are proved in the localized "
                "big-cell GL preimage. A disconnected stabilizer could in "
                "principle identify their images; no claim that the two "
                "constructible image families are distinct global orbit-"
                "intersection components is made."),
        },
        "verstraete_normal_form": {
            "convention": (
                "G_abcd has coefficients (a+d)/2 on 0000,1111; "
                "(a-d)/2 on 0011,1100; (b+c)/2 on 0101,1010; "
                "(b-c)/2 on 0110,1001"),
            "parameters_a_b_c_d": [sp.sstr(value) for value in parameters],
            "squared_parameter_multiset": ["4", "4", "8*i", "-8*i"],
            "diagonal_gauge_pair_products": {
                str(index): sp.sstr(value)
                for index, value in sorted(pair_products.items())},
            "invariant_guard": (
                "The collision a^2=d^2 makes this a non-regular stratum. "
                "Equality of Luque-Thibon polynomial invariants identifies "
                "at most the closed-orbit/invariant fibre data; it is not "
                "used here to infer orbit equality. Orbit membership above "
                "comes from the literal local GL2 row parametrization."),
        },
        "cofactor_covariant_referee": cofactor_record,
        "scope_guard": (
            "This is a dense big-cell calculation for the exact Q0 orbit. "
            "Other row charts are obtained by local bit-chart changes, but "
            "their boundary gluing and the finite stabilizer action have not "
            "been globally component-classified."),
        "source_hash": sha256(S6_PATH.read_bytes()).hexdigest(),
        "must_fire": [
            "six cross equations reduce to two d quadrics",
            "d resultant has the two declared factors",
            "both C covers have nonsquare quartic discriminant",
            "Q0 orbit tangent rank is 12",
            "a dQ-zero tangent has dCof13=-2+sqrt(2)",
        ],
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("Q0 cross-orbit coordinates: PASS")
    print("components/dim:", len(component_records), 6)
    print("cofactor tangent ranks:", 14, 23, 24)
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
