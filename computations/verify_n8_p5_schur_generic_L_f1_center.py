#!/usr/bin/env python3
"""Recover the generic-L first-bend relation from the finite Schur graph."""

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


CENTER = load_module(
    "n8_p5_schur_degree6_for_generic_L_f1",
    "verify_n8_p5_schur_degree6_center.py",
)
SCHUR = CENTER.SCHUR
REES = CENTER.REES
P5 = CENTER.P5
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "f26fd19f3500b1770996ec6446319120eb003d1d5d20aebe08d57bba910b0ef5"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    REES.add(target, source, scale)


def multiply(left, right):
    return REES.multiply(left, right)


def polynomial(entries):
    answer = {}
    for monomial, coefficient in entries:
        monomial = tuple(sorted(monomial))
        answer[monomial] = answer.get(monomial, QQ(0)) + QQ(coefficient)
        if not answer[monomial]:
            answer.pop(monomial)
    return answer


def dynamic_product_coefficient(dynamic_monomial, order, series, cache):
    key = dynamic_monomial, order
    if key in cache:
        return cache[key]
    if not dynamic_monomial:
        answer = {(): QQ(1)} if order == 0 else {}
    else:
        variable = dynamic_monomial[0]
        tail = dynamic_monomial[1:]
        answer = {}
        for degree in range(order + 1):
            head = series[variable][degree]
            if not head:
                continue
            rest = dynamic_product_coefficient(
                tail, order - degree, series, cache
            )
            if rest:
                add(answer, multiply(head, rest))
    cache[key] = answer
    return answer


def coefficient_on_dynamic_graph(
    source, order, series, dynamic_variables, cache
):
    answer = {}
    for monomial, coefficient in source.items():
        dynamic = tuple(
            variable for variable in monomial if variable in dynamic_variables
        )
        base = tuple(
            variable for variable in monomial if variable not in dynamic_variables
        )
        value = dynamic_product_coefficient(
            dynamic, order, series, cache
        )
        for graph_monomial, graph_coefficient in value.items():
            output = tuple(sorted(base + graph_monomial))
            answer[output] = (
                answer.get(output, QQ(0))
                + coefficient * graph_coefficient
            )
            if not answer[output]:
                answer.pop(output)
    return answer


def divide_by_ell(source, z9, z25, z11, z46):
    residual = dict(source)
    quotient = {}
    while True:
        candidates = [
            monomial for monomial in residual
            if z9 in monomial and z25 in monomial
        ]
        if not candidates:
            break
        selected = max(candidates, key=lambda value: (value.count(z9), value))
        coefficient = residual[selected]
        output = list(selected)
        output.remove(z9)
        output.remove(z25)
        output = tuple(output)
        add(quotient, {output: coefficient})
        add(residual, {selected: coefficient}, QQ(-1))
        replacement = tuple(sorted(output + (z11, z46)))
        add(residual, {replacement: coefficient})
    return quotient, residual


def family_digest(sources):
    digest = sha256()
    for source in sources:
        digest.update(REES.polynomial_digest(source).encode())
    return digest.hexdigest()


def audit():
    data = CENTER.audit(return_data=True)
    layout = data["layout"]
    tau = data["tau"]
    normal = data["normal_stricts"]
    transverse = data["transverse_pivots"]
    obstruction = data["obstruction_stricts"]
    local_variables = data["local_variables"]
    pivots = data["pivots"]
    maximum_order = 4

    first_bend = layout["variable_count"]
    second_bend = first_bend + 1
    z46 = layout["a"][46]
    dynamic_variables = local_variables | {z46}
    series = {
        variable: [{} for _order in range(maximum_order + 1)]
        for variable in dynamic_variables
    }
    series[tau][1] = {(): QQ(1)}
    series[z46][0] = {(z46,): QQ(1)}
    series[z46][1] = {(first_bend,): QQ(1)}
    series[z46][2] = {(second_bend,): QQ(1)}

    compatibility_orders = []
    reduced_L_orders = []
    for order in range(1, maximum_order + 1):
        cache = {}
        normal_incoming = [
            coefficient_on_dynamic_graph(
                source, order, series, dynamic_variables, cache
            )
            for source in normal
        ]
        for pivot, incoming in zip(pivots, normal_incoming):
            series[layout["y"][pivot]][order] = CENTER.negate(incoming)

        cache = {}
        transverse_incoming = [
            coefficient_on_dynamic_graph(
                source, order, series, dynamic_variables, cache
            )
            for source in transverse
        ]
        for parameter, incoming in zip(
            P5.P5_NORMAL_VARIABLES, transverse_incoming
        ):
            series[layout["n"][parameter]][order] = CENTER.negate(
                CENTER.divide_by_b(
                    incoming, layout["a"][44], layout["a"][45]
                )
            )

        cache = {}
        require(
            not any(
                coefficient_on_dynamic_graph(
                    source, order, series, dynamic_variables, cache
                )
                for source in normal + transverse
            ),
            f"dynamic 207-row graph failed at order {order}",
        )
        cache = {}
        compatibility = [
            coefficient_on_dynamic_graph(
                source, order, series, dynamic_variables, cache
            )
            for source in obstruction
        ]
        compatibility_orders.append(compatibility)
        reduced_L_orders.append([
            divide_by_ell(
                source,
                layout["a"][9],
                layout["a"][25],
                layout["a"][11],
                z46,
            )[1]
            for source in compatibility
        ])

    require(not any(reduced_L_orders[0]) and not any(reduced_L_orders[1]),
            "generic-L compatibility appeared before order three")
    require(not any(reduced_L_orders[2]),
            "degree-six compatibility did not vanish on L")

    first_relation = polynomial((
        ((layout["a"][9], layout["a"][29], layout["a"][44]), -1),
        ((layout["a"][0], layout["a"][11], z46), 1),
        ((layout["a"][11], layout["a"][24], z46), -1),
        ((layout["a"][11], layout["a"][26], layout["a"][54]), 1),
        ((first_bend, layout["a"][11]), 1),
    ))
    common = polynomial((
        ((layout["a"][16], layout["a"][16], layout["a"][41]),
         QQ(1, 2)),
    ))
    u = polynomial((
        ((layout["a"][26],), 1),
        ((layout["a"][45],), 1),
    ))
    v = polynomial((
        ((layout["a"][26],), 1),
        ((layout["a"][44],), -1),
    ))
    expected = [{} for _row in range(39)]
    expected[29] = multiply(multiply(common, u), first_relation)
    expected[32] = multiply(multiply(common, v), first_relation)
    require(reduced_L_orders[3] == expected,
            "generic-L Schur graph did not recover F1")

    nonzero = [
        [row + 1, len(source), REES.polynomial_digest(source)]
        for row, source in enumerate(reduced_L_orders[3]) if source
    ]
    ledger = {
        "source": "finite first P5 Rees equations after 207-row Schur graph",
        "component": "L=z9*z25-z11*z46=0",
        "localizers": ["z16", "z41", "z11", "z44+z45"],
        "bend_series": "z46(tau)=z46+tau*s+tau^2*t",
        "first_bend_variable": first_bend,
        "second_bend_variable": second_bend,
        "graph_orders_checked": maximum_order,
        "L_remainder_term_counts": [
            sum(map(len, values)) for values in reduced_L_orders
        ],
        "first_nonzero_L_order": 4,
        "nonzero_F1_rows": nonzero,
        "F1_terms": len(first_relation),
        "F1_sha256": REES.polynomial_digest(first_relation),
        "F1": (
            "-z9*z29*z44+z0*z11*z46-z11*z24*z46+"
            "z11*z26*z54+s*z11"
        ),
        "F1_factorization": {
            "Q30": "1/2*z16^2*z41*(z26+z45)*F1",
            "Q33": "1/2*z16^2*z41*(z26-z44)*F1",
        },
        "compatibility_family_sha256": family_digest(compatibility_orders[3]),
        "L_remainder_family_sha256": family_digest(reduced_L_orders[3]),
        "consequence": (
            "the finite source Schur graph recovers the generic-L first-bend center"
        ),
        "scope_guard": (
            "source-faithful through F1; F2/G and full pure membership remain"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 is not None:
        require(digest == EXPECTED_LEDGER_SHA256,
                "generic-L F1 Schur ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
