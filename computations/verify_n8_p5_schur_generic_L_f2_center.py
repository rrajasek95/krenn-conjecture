#!/usr/bin/env python3
"""Recover the generic-L second-bend center from the finite Schur graph."""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


F1 = load_module(
    "n8_p5_schur_f1_for_generic_L_f2",
    "verify_n8_p5_schur_generic_L_f1_center.py",
)
CENTER = F1.CENTER
SCHUR = F1.SCHUR
REES = F1.REES
P5 = F1.P5
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "8e79e129660da84d1e852e1141e2ef04528fb858047bd8b5cb4c601f43a7058f"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    REES.add(target, source, scale)


def multiply(left, right):
    return REES.multiply(left, right)


def divide_by_monomial(source, divisor):
    answer = {}
    for monomial, coefficient in source.items():
        output = list(monomial)
        for variable in divisor:
            require(variable in output,
                    f"term {monomial} is not divisible by {divisor}")
            output.remove(variable)
        answer[tuple(output)] = coefficient
    return answer


def variable_coefficient(source, variable):
    answer = {}
    for monomial, coefficient in source.items():
        degree = monomial.count(variable)
        require(degree <= 1, f"z{variable} is no longer affine")
        if not degree:
            continue
        output = list(monomial)
        output.remove(variable)
        answer[tuple(output)] = coefficient
    return answer


def singular_membership(values, first_relation, second_relation, layout,
                        first_bend, second_bend):
    variable_count = second_bend + 5
    inverse_z11 = second_bend + 1
    inverse_b = second_bend + 2
    inverse_z16 = second_bend + 3
    inverse_z41 = second_bend + 4
    names = [f"x{index}" for index in range(variable_count)]
    for parameter, variable in layout["a"].items():
        names[variable] = f"z{parameter}"
    names[first_bend] = "s"
    names[second_bend] = "t"
    names[inverse_z11] = "w"
    names[inverse_b] = "q"
    names[inverse_z16] = "p16"
    names[inverse_z41] = "p41"
    active = set().union(*(
        set(variable for monomial in source for variable in monomial)
        for source in [first_relation, second_relation, *values]
    ))
    active -= {first_bend, second_bend, 0}
    ring_order = ["t", "s", "w", "q", "p16", "p41"] + [
        names[index] for index in sorted(active)
    ]
    # Index zero is the Rees tau variable and does not occur in this layer.
    require(len(set(ring_order)) == len(ring_order),
            "Singular F2 variable names are not unique")
    lines = [f"ring r=0,({','.join(ring_order)}),dp;"]
    encode = REES.AMBIENT.singular_polynomial
    lines.append("poly ell=z9*z25-z11*z46;")
    lines.append(f"poly first={encode(first_relation, names)};")
    lines.append(f"poly second={encode(second_relation, names)};")
    lines.append(f"poly loc11=z11*w-1;")
    lines.append(f"poly locb=(z44+z45)*q-1;")
    lines.append("poly loc16=z16*p16-1;")
    lines.append("poly loc41=z41*p41-1;")
    lines.append("ideal i=ell,first,second,loc11,locb,loc16,loc41;")
    lines.append("ideal g=std(i);")
    lines.append('"UNIT",(reduce(1,g)==0);')
    for row, source in enumerate(values, 1):
        if not source:
            continue
        lines.append(f"poly e{row}={encode(source, names)};")
        lines.append(f'"ROW",{row},(reduce(e{row},g)==0);')
    lines.append("quit;")
    completed = subprocess.run(
        ["/usr/local/bin/Singular", "-q"],
        input="\n".join(lines),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    require(completed.returncode == 0,
            "Singular generic-L F2 membership failed")
    require("UNIT 0" in completed.stdout,
            "generic-L F1/F2 ideal became the unit ideal")
    require(
        all(line.endswith(" 1") for line in completed.stdout.splitlines()
            if line.startswith("ROW ")),
        "a fifth-order compatibility row escaped F1/F2",
    )
    return sha256(completed.stdout.encode()).hexdigest()


def audit():
    data = F1.audit(return_data=True)
    layout = data["layout"]
    tau = data["tau"]
    series = data["series"]
    dynamic_variables = data["dynamic_variables"]
    normal = data["normal"]
    transverse = data["transverse"]
    obstruction = data["obstruction"]
    pivots = data["pivots"]
    first_bend = data["first_bend"]
    second_bend = data["second_bend"]
    first_relation = data["first_relation"]
    order = 5

    for coefficients in series.values():
        coefficients.append({})

    cache = {}
    normal_incoming = [
        F1.coefficient_on_dynamic_graph(
            source, order, series, dynamic_variables, cache
        )
        for source in normal
    ]
    for pivot, incoming in zip(pivots, normal_incoming):
        series[layout["y"][pivot]][order] = CENTER.negate(incoming)

    cache = {}
    pivot_incoming = [
        F1.coefficient_on_dynamic_graph(
            source, order, series, dynamic_variables, cache
        )
        for source in transverse
    ]
    cache = {}
    obstruction_incoming = [
        F1.coefficient_on_dynamic_graph(
            source, order, series, dynamic_variables, cache
        )
        for source in obstruction
    ]

    # The response to the as-yet-unsolved n^(5) coefficient is the same
    # transverse Jacobian as at the center.  Compute it after the normal
    # linear Schur operation and form compatibility numerators without any
    # division by b.
    local_variables = data["local_variables"]
    normal_eliminated_linear = [
        CENTER.local_linear_eliminate_normals(
            source, normal, pivots, layout, local_variables
        )
        for source in obstruction
    ]
    b = data["schur"]["b"]
    numerators = []
    for row, incoming in enumerate(obstruction_incoming):
        value = multiply(b, incoming)
        for column, parameter in enumerate(P5.P5_NORMAL_VARIABLES):
            coefficient = SCHUR.coefficient_of_local_variable(
                normal_eliminated_linear[row],
                layout["n"][parameter],
                local_variables,
            )
            if coefficient:
                add(value, multiply(coefficient, pivot_incoming[column]), -1)
        numerators.append(value)

    z46 = layout["a"][46]
    L_remainders = [
        F1.divide_by_ell(
            source,
            layout["a"][9],
            layout["a"][25],
            layout["a"][11],
            z46,
        )[1]
        for source in numerators
    ]
    nonzero = [
        [row + 1, len(source), REES.polynomial_digest(source)]
        for row, source in enumerate(L_remainders) if source
    ]
    require([row for row, _terms, _digest in nonzero] == [
        1, 4, 10, 11, 14, 16, 22, 25, 26, 28,
        30, 31, 33, 36, 37, 38,
    ], "generic-L F2 support changed")

    z16 = layout["a"][16]
    z41 = layout["a"][41]
    exceptional = []
    for row in (29, 32):
        core = divide_by_monomial(L_remainders[row], (z16, z16, z41))
        core = {
            monomial: 2 * coefficient
            for monomial, coefficient in core.items()
        }
        exceptional.append(CENTER.divide_by_b(
            core, layout["a"][44], layout["a"][45]
        ))
    difference = dict(exceptional[0])
    add(difference, exceptional[1], QQ(-1))
    # The historical normalized relation is difference/b.  The extra b is
    # not a polynomial factor, but it is a unit on this chart, so difference
    # generates exactly the same localized ideal without introducing an
    # inverse variable into the source polynomial.
    second_relation = difference

    second_bend_coefficient = variable_coefficient(
        second_relation, second_bend
    )
    require(second_bend_coefficient,
            "F2 is not monic up to a generic-L unit in t")
    singular_sha256 = singular_membership(
        L_remainders,
        first_relation,
        second_relation,
        layout,
        first_bend,
        second_bend,
    )

    ledger = {
        "source": "finite first P5 Rees equations after 207-row Schur graph",
        "component": "generic L with F1 adjoined",
        "graph_order": order,
        "compatibility_numerator_nonzero": nonzero,
        "compatibility_numerator_terms": sum(map(len, L_remainders)),
        "compatibility_numerator_sha256": F1.family_digest(L_remainders),
        "exceptional_relations": [
            [len(source), REES.polynomial_digest(source)]
            for source in exceptional
        ],
        "F2_definition": (
            "R30-R33, equivalent to (R30-R33)/(z44+z45) on the b chart"
        ),
        "F2_terms": len(second_relation),
        "F2_sha256": REES.polynomial_digest(second_relation),
        "F2_second_bend_coefficient_terms": len(second_bend_coefficient),
        "F2_second_bend_coefficient_sha256": REES.polynomial_digest(
            second_bend_coefficient
        ),
        "localized_membership": {
            "ideal": (
                "<L,F1,F2,z11*w-1,(z44+z45)*q-1,"
                "z16*p16-1,z41*p41-1>"
            ),
            "ideal_is_nonunit": True,
            "all_16_compatibility_rows_reduce_to_zero": True,
            "singular_output_sha256": singular_sha256,
        },
        "consequence": (
            "the finite source Schur graph recovers the generic-L second-bend center"
        ),
        "scope_guard": (
            "source-faithful through F2; the G row and full H0/H1 membership remain"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 is not None:
        require(digest == EXPECTED_LEDGER_SHA256,
                "generic-L F2 Schur ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
