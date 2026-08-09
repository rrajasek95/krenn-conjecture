#!/usr/bin/env python3
"""Recover the first tau-saturated P5 center from the 207-row Schur block."""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCHUR = load_module(
    "n8_p5_schur_basis_for_degree6_center",
    "verify_n8_p5_normal_transverse_schur_basis.py",
)
REES = SCHUR.REES
P5 = SCHUR.P5
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "4ffd07f0c5c58d1b13c95f5c958d9edd7ab9ee32a92eba0a604aa233cd285009"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    REES.add(target, source, scale)


def multiply(left, right):
    return REES.multiply(left, right)


def monomial(layout, *parameters, coefficient=QQ(1)):
    return {
        tuple(sorted(layout["a"][parameter] for parameter in parameters)):
        QQ(coefficient)
    }


def polynomial(layout, entries):
    answer = {}
    for parameters, coefficient in entries:
        add(answer, monomial(layout, *parameters, coefficient=coefficient))
    return answer


def family_digest(sources):
    digest = sha256()
    for source in sources:
        digest.update(REES.polynomial_digest(source).encode())
    return digest.hexdigest()


def negate(source):
    return {monomial_: -coefficient for monomial_, coefficient in source.items()}


def divide_by_b(source, z44, z45):
    residual = dict(source)
    quotient = {}
    while True:
        candidates = [monomial_ for monomial_ in residual if z45 in monomial_]
        if not candidates:
            break
        selected = max(candidates, key=lambda value: (value.count(z45), value))
        coefficient = residual[selected]
        output = list(selected)
        output.remove(z45)
        output = tuple(output)
        add(quotient, {output: coefficient})
        add(residual, {selected: coefficient}, QQ(-1))
        add(
            residual,
            {tuple(sorted(output + (z44,))): coefficient},
            QQ(-1),
        )
    require(not residual, "pivot graph coefficient is not divisible by b")
    return quotient


def local_product_coefficient(local_monomial, order, series, cache):
    key = local_monomial, order
    if key in cache:
        return cache[key]
    if not local_monomial:
        answer = {(): QQ(1)} if order == 0 else {}
    else:
        variable = local_monomial[0]
        tail = local_monomial[1:]
        answer = {}
        for degree in range(1, order + 1):
            head = series[variable][degree]
            if not head:
                continue
            rest = local_product_coefficient(
                tail, order - degree, series, cache
            )
            if rest:
                add(answer, multiply(head, rest))
    cache[key] = answer
    return answer


def coefficient_on_graph(source, order, series, local_variables, cache):
    answer = {}
    for monomial_, coefficient in source.items():
        local = tuple(
            variable for variable in monomial_ if variable in local_variables
        )
        if len(local) > order:
            continue
        base = tuple(
            variable for variable in monomial_ if variable not in local_variables
        )
        local_coefficient = local_product_coefficient(
            local, order, series, cache
        )
        for graph_monomial, value in local_coefficient.items():
            output = tuple(sorted(base + graph_monomial))
            answer[output] = (
                answer.get(output, QQ(0)) + coefficient * value
            )
            if not answer[output]:
                answer.pop(output)
    return answer


def local_linear_eliminate_normals(
    source, normal_stricts, pivots, layout, local_variables
):
    linear = SCHUR.local_linear(source, local_variables)
    for pivot, normal in zip(pivots, normal_stricts):
        y_variable = layout["y"][pivot]
        coefficient = SCHUR.coefficient_of_local_variable(
            linear, y_variable, local_variables
        )
        if coefficient:
            add(
                linear,
                multiply(
                    coefficient,
                    SCHUR.local_linear(normal, local_variables),
                ),
                QQ(-1),
            )
    require(
        not any(
            SCHUR.coefficient_of_local_variable(
                linear, variable, local_variables
            )
            for variable in layout["y"].values()
        ),
        "normal Schur elimination retained a y-linear term",
    )
    return linear


def audit():
    reducer = REES.AMBIENT.LOCAL.LocalReducer()
    normal_sources, obstruction_sources, _cubic = (
        REES.AMBIENT.finite_generators()
    )
    layout = REES.variable_layout(reducer)
    tau = layout["tau"]
    y_variables = frozenset(layout["y"].values())
    n_variables = frozenset(layout["n"].values())
    local_variables = y_variables | n_variables | {tau}
    pivots = tuple(reducer.jacobian_pivots)

    forms0 = REES.coordinate_forms(reducer, layout)
    q_offsets = {}
    for pivot, source in zip(pivots, normal_sources):
        strict, valuation, _maximum = SCHUR.normal_strict(
            source, forms0, tau
        )
        require(valuation == 2, "unshifted normal valuation changed")
        q_offsets[layout["y"][pivot]] = SCHUR.solve_q_offset(
            strict, layout["y"][pivot], tau, y_variables
        )
    forms1 = SCHUR.shifted_forms(forms0, layout, q_offsets, 2)
    forms, _first_correction = SCHUR.first_transverse_shift(
        forms1, reducer, layout
    )

    normal_stricts = []
    for number, source in enumerate(normal_sources, 1):
        strict, valuation, _maximum = SCHUR.normal_strict(source, forms, tau)
        require(valuation == 2,
                f"shifted normal {number} valuation changed")
        normal_stricts.append(strict)

    obstruction_stricts = []
    normal_eliminated = []
    for number, source in enumerate(obstruction_sources, 1):
        strict, record = SCHUR.strict_record(
            "obstruction", number, source, forms, tau
        )
        require(record["valuation"] == 3,
                f"obstruction {number} valuation changed")
        obstruction_stricts.append(strict)
        normal_eliminated.append(local_linear_eliminate_normals(
            strict, normal_stricts, pivots, layout, local_variables
        ))

    transverse_linear = []
    transverse_pivots = []
    for column, row in enumerate(P5.B_PIVOT_ROWS):
        source = dict(obstruction_stricts[row])
        source_linear = SCHUR.local_linear(source, local_variables)
        for pivot, normal in zip(pivots, normal_stricts):
            y_variable = layout["y"][pivot]
            coefficient = SCHUR.coefficient_of_local_variable(
                source_linear, y_variable, local_variables
            )
            if coefficient:
                add(source, multiply(coefficient, normal), QQ(-1))
        value = SCHUR.local_linear(source, local_variables)
        for other, parameter in enumerate(P5.P5_NORMAL_VARIABLES):
            expected = polynomial(
                layout,
                (((44,), 1), ((45,), 1)),
            ) if column == other else {}
            require(
                SCHUR.coefficient_of_local_variable(
                    value, layout["n"][parameter], local_variables
                ) == expected,
                f"transverse pivot row {row + 1} changed",
            )
        transverse_linear.append(value)
        transverse_pivots.append(source)

    b = polynomial(layout, (((44,), 1), ((45,), 1)))
    saturated_initials = []
    for row, source in enumerate(normal_eliminated):
        value = multiply(b, source)
        for column, parameter in enumerate(P5.P5_NORMAL_VARIABLES):
            coefficient = SCHUR.coefficient_of_local_variable(
                source, layout["n"][parameter], local_variables
            )
            if coefficient:
                add(value, multiply(coefficient, transverse_linear[column]), -1)
        require(
            not any(
                SCHUR.coefficient_of_local_variable(
                    value, variable, local_variables
                )
                for variable in y_variables | n_variables
            ),
            f"row {row + 1} retained a Schur variable",
        )
        coefficient = SCHUR.coefficient_of_local_variable(
            value, tau, local_variables
        )
        replay = {
            tuple(sorted((tau,) + monomial)): scalar
            for monomial, scalar in coefficient.items()
        }
        require(value == replay,
                f"row {row + 1} retained another local-linear term")
        saturated_initials.append(coefficient)

    require(not any(saturated_initials),
            "the first Schur graph order acquired premature compatibility")

    # Solve the full 207-row graph coefficient by coefficient.  Since all
    # local variables have positive tau order, order k only sees the new
    # coefficients through the certified identity and bI linear blocks.
    maximum_order = 3
    series = {
        variable: [{} for _order in range(maximum_order + 1)]
        for variable in local_variables
    }
    series[tau][1] = {(): QQ(1)}
    graph_compatibility = []
    graph_terms = []
    z44 = layout["a"][44]
    z45 = layout["a"][45]
    for order in range(1, maximum_order + 1):
        cache = {}
        normal_incoming = [
            coefficient_on_graph(
                source, order, series, local_variables, cache
            )
            for source in normal_stricts
        ]
        for pivot, incoming in zip(pivots, normal_incoming):
            series[layout["y"][pivot]][order] = negate(incoming)

        cache = {}
        transverse_incoming = [
            coefficient_on_graph(
                source, order, series, local_variables, cache
            )
            for source in transverse_pivots
        ]
        for parameter, incoming in zip(
            P5.P5_NORMAL_VARIABLES, transverse_incoming
        ):
            series[layout["n"][parameter]][order] = negate(
                divide_by_b(incoming, z44, z45)
            )

        cache = {}
        require(
            not any(
                coefficient_on_graph(
                    source, order, series, local_variables, cache
                )
                for source in normal_stricts + transverse_pivots
            ),
            f"207-row graph failed to solve order {order}",
        )
        cache = {}
        compatibility = [
            coefficient_on_graph(
                source, order, series, local_variables, cache
            )
            for source in obstruction_stricts
        ]
        graph_compatibility.append(compatibility)
        graph_terms.append(sum(map(len, compatibility)))

    ell = polynomial(layout, (((9, 25), 1), ((11, 46), -1)))
    core = multiply(monomial(layout, 16, 16, 41), ell)
    u = polynomial(layout, (((26,), 1), ((45,), 1)))
    v = polynomial(layout, (((26,), 1), ((44,), -1)))
    g30 = {
        monomial_: -coefficient / 2
        for monomial_, coefficient in multiply(core, u).items()
    }
    g33 = {
        monomial_: -coefficient / 2
        for monomial_, coefficient in multiply(core, v).items()
    }
    expected = [{} for _row in range(39)]
    expected[29] = g30
    expected[32] = g33
    nonzero_orders = [
        [
            (row + 1, len(source), REES.polynomial_digest(source))
            for row, source in enumerate(compatibility) if source
        ]
        for compatibility in graph_compatibility
    ]
    require(nonzero_orders[:2] == [[], []],
            "compatibility appeared before graph order three")
    require(graph_compatibility[2] == expected,
            "207-row Schur saturation did not recover degree-six center")

    difference = dict(g30)
    add(difference, g33, QQ(-1))
    expected_difference = {
        monomial_: -coefficient / 2
        for monomial_, coefficient in multiply(core, b).items()
    }
    require(difference == expected_difference,
            "g30-g33 no longer recovers b times the L center")

    ledger = {
        "source_chart": "finite first P5 Rees chart after 207-row Schur block",
        "normal_rows": 196,
        "transverse_pivot_rows": 11,
        "remaining_mixed_rows": 28,
        "tau_saturation_layer": 1,
        "schur_linear_terms_before_saturation": sum(
            map(len, normal_eliminated)
        ),
        "saturated_initial_terms": sum(map(len, saturated_initials)),
        "saturated_initial_sha256": family_digest(saturated_initials),
        "first_schur_order_nonzero_rows": [],
        "graph_order_term_counts": graph_terms,
        "graph_order_nonzero_rows": nonzero_orders,
        "first_nonzero_graph_order": 3,
        "nonzero_saturated_rows_one_based": [30, 33],
        "normalized_g30": (
            "-1/2*z16^2*z41*(z9*z25-z11*z46)*(z26+z45)"
        ),
        "normalized_g33": (
            "-1/2*z16^2*z41*(z9*z25-z11*z46)*(z26-z44)"
        ),
        "b_chart_saturation": (
            "<g30,g33>:(z44+z45)^infinity="
            "<z16^2*z41*(z9*z25-z11*z46)>"
        ),
        "reduced_components": [
            "z16=0",
            "z41=0",
            "L=z9*z25-z11*z46=0",
        ],
        "generic_L_localizers": [
            "z16", "z41", "z11", "b=z44+z45",
        ],
        "consequence": (
            "the exact finite source Schur quotient recovers the committed "
            "L center at its first tau-saturated layer"
        ),
        "scope_guard": (
            "associated-graded first saturation layer only; F/G and full "
            "H0/H1 scalar or conormal membership are not computed"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 is not None:
        require(digest == EXPECTED_LEDGER_SHA256,
                "Schur degree-six center ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
