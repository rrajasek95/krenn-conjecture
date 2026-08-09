#!/usr/bin/env python3
"""Analyze the next P5 compatibility tails after the degree-six H0 kill."""

from fractions import Fraction
import importlib.util
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


TAILS = load_module(
    "n8_p5_degree7_mixed_for_compatibility",
    "verify_n8_p5_streamed_degree7_mixed_tails.py",
)
AMBIENT = load_module(
    "n8_ambient_for_p5_degree7_compatibility",
    "analyze_n8_ambient_local_standard_basis.py",
)
P5 = TAILS.P5
CUBIC = P5.CUBIC
QQ = Fraction


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    CUBIC.add_scaled(target, source, scale)


def multiply(left, right):
    return CUBIC.multiply_polynomials(left, right)


def divide_by_b(source):
    """Exact division by b=z44+z45, leading in z44."""

    residual = dict(source)
    quotient = {}
    while True:
        candidates = [monomial for monomial in residual if 44 in monomial]
        if not candidates:
            break
        selected = max(candidates, key=lambda item: (item.count(44), item))
        coefficient = residual[selected]
        output = list(selected)
        output.remove(44)
        output = tuple(output)
        add(quotient, {output: coefficient})
        product = multiply(
            {output: coefficient},
            P5.polynomial((((44,), 1), ((45,), 1))),
        )
        add(residual, product, -1)
    require(not residual, "polynomial is not divisible by z44+z45")
    return quotient


def ambient_p5_arc_forms(reducer, correction):
    values = []
    derivatives = []
    for coordinate_form in reducer._tangent_coordinate_forms:
        tangent_linear = {
            (parameter,): coefficient
            for parameter, coefficient in coordinate_form.items()
        }
        values.append(P5.p5_restriction(tangent_linear))
        derivative = {}
        for parameter, coefficient in coordinate_form.items():
            if correction.get(parameter):
                add(derivative, correction[parameter], coefficient)
        derivatives.append(derivative)
    return values, derivatives


def ambient_arc_derivative(source, values, derivatives):
    answer = {}
    for source_monomial, coefficient in source.items():
        factors = [values[coordinate] for coordinate in source_monomial]
        for position, coordinate in enumerate(source_monomial):
            if not derivatives[coordinate]:
                continue
            term = {(): coefficient}
            for index, factor in enumerate(factors):
                term = multiply(
                    term,
                    derivatives[coordinate] if index == position else factor,
                )
                if not term:
                    break
            add(answer, term)
    return answer


def residual_arc_derivative(state, degree, projector, correction):
    reducer = projector.reducer
    values, derivatives = ambient_p5_arc_forms(reducer, correction)
    multiplier_cache = {}
    functional_cache = {}

    answer = {}
    if degree <= 4:
        answer = ambient_arc_derivative(
            reducer.functional_hasse(state["functional"], degree),
            values,
            derivatives,
        )
    for multiplier, functional in state["corrections"]:
        multiplier_degree = len(next(iter(multiplier)))
        equation_degree = degree - multiplier_degree
        if not 0 <= equation_degree <= 4:
            continue
        multiplier_key = id(multiplier)
        if multiplier_key not in multiplier_cache:
            multiplier_cache[multiplier_key] = ambient_arc_derivative(
                multiplier, values, derivatives
            )
        multiplier_derivative = multiplier_cache[multiplier_key]
        multiplier_value = projector.restrict(multiplier)

        functional_key = tuple(sorted(functional.items())), equation_degree
        if functional_key not in functional_cache:
            ambient = reducer.functional_hasse(functional, equation_degree)
            functional_cache[functional_key] = ambient_arc_derivative(
                ambient, values, derivatives
            )
        equation_derivative = functional_cache[functional_key]
        equation_value, _weighted = projector.functional_factors(
            functional, equation_degree
        )
        if multiplier_derivative and equation_value:
            add(answer, multiply(multiplier_derivative, equation_value), -1)
        if multiplier_value and equation_derivative:
            add(answer, multiply(multiplier_value, equation_derivative), -1)
    return answer


def evaluate(source, point):
    answer = QQ(0)
    for monomial, coefficient in source.items():
        term = coefficient
        for variable in monomial:
            term *= point[variable]
        answer += term
    return answer


def compatibility_tail_data(verbose=True):
    data = TAILS.mixed_tail_data()
    series = data["series"]
    projector = data["projector"]
    degree_six = data["degree_six"]
    degree_seven = data["degree_seven"]
    parts = {
        degree: [series.part(number, degree) for number in range(1, 40)]
        for degree in range(2, 6)
    }
    corrections = P5.expected_corrections()
    jacobian = P5.transverse_jacobian(parts[2])

    residual4 = P5.strict_residual(parts, corrections, 4, degree_six)
    pivot4 = [residual4[row] for row in P5.B_PIVOT_ROWS]
    n4 = {}
    for variable, incoming in zip(P5.P5_NORMAL_VARIABLES, pivot4):
        if incoming:
            quotient = divide_by_b(incoming)
            n4[variable] = {
                monomial: -coefficient
                for monomial, coefficient in quotient.items()
            }

    point = {index: QQ(index + 2) for index in range(56)}
    for variable in (12, 13, 14, 17, 18, 19, 20, 21, 22, 23):
        point[variable] = QQ(0)
    point[15] = point[16]
    if verbose:
        print("n4 nonzero", len(n4), "terms", sum(map(len, n4.values())))
        print("n4 point", [
            evaluate(n4.get(variable, {}), point)
            for variable in P5.P5_NORMAL_VARIABLES
        ])

    q6_n1 = []
    for number in range(1, 40):
        q6_n1.append(
            residual_arc_derivative(
                series._state(number), 6, projector, corrections[0]
            )
        )
    residual5 = P5.strict_residual(parts, corrections + [n4], 5)
    for equation in range(39):
        add(residual5[equation], q6_n1[equation])
        add(residual5[equation], degree_seven[equation])

    b = P5.polynomial((((44,), 1), ((45,), 1)))
    pivot5 = [residual5[row] for row in P5.B_PIVOT_ROWS]
    compatibility = []
    for equation, row in enumerate(jacobian):
        value = multiply(b, residual5[equation])
        for column in range(11):
            if row[column] and pivot5[column]:
                add(value, multiply(row[column], pivot5[column]), -1)
        compatibility.append(value)
    normalized = [
        divide_by_b(value) if value else {}
        for value in compatibility
    ]
    if verbose:
        print("q6 n1 terms", sum(map(len, q6_n1)), max(map(len, q6_n1)))
        print("residual5 terms", sum(map(len, residual5)), max(map(len, residual5)))
        print("compat nonzero", [
            (index + 1, len(value)) for index, value in enumerate(normalized)
            if value
        ])
        print("compat point", [
            (index + 1, evaluate(value, point))
            for index, value in enumerate(normalized) if value
        ])
        names = [f"z{index}" for index in range(56)]
        lines = [f"ring r=0,({','.join(names)}),dp;"]
        for index, value in enumerate(normalized):
            if not value:
                continue
            encoded = AMBIENT.singular_polynomial(value, names)
            lines.append(f"poly h{index + 1}={encoded};")
            lines.append(f'"FACTOR",{index + 1},size(h{index + 1}),'
                         f'factorize(h{index + 1});')
        lines.extend((
            "poly ell=z9*z25-z11*z46;",
            "poly u=z26+z45; poly v=z26-z44;",
            "poly relation=v*h30-u*h33;",
            '"LREL",size(relation),factorize(relation),'
            "(reduce(relation,std(ideal(ell)))==0);",
            "poly difference=h30-h33;",
            '"DIFF",size(difference),factorize(difference);',
        ))
        lines.append("quit;")
        completed = subprocess.run(
            ["/usr/local/bin/Singular", "-q"],
            input="\n".join(lines),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=180,
        )
        require(completed.returncode == 0, "Singular factorization failed")
        print(completed.stdout)
    return {
        "mixed_tail_data": data,
        "parts": parts,
        "corrections": corrections,
        "jacobian": jacobian,
        "n4": n4,
        "q6_n1": q6_n1,
        "residual5": residual5,
        "normalized_compatibility": normalized,
    }


def main():
    compatibility_tail_data()


if __name__ == "__main__":
    main()
