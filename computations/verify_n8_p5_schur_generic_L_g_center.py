#!/usr/bin/env python3
"""Recover the generic-L third-bend center from the finite Schur graph."""

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


F2 = load_module(
    "n8_p5_schur_f2_for_generic_L_g",
    "verify_n8_p5_schur_generic_L_f2_center.py",
)
F1 = F2.F1
CENTER = F2.CENTER
REES = F2.REES
P5 = F2.P5
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "46d107934702ade1987b9dea48db7242eadfcfb87e1c6897dc3ee2e183dcc15e"
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
        add(answer, {tuple(sorted(monomial)): QQ(coefficient)})
    return answer


def family_digest(sources):
    digest = sha256()
    for source in sources:
        digest.update(REES.polynomial_digest(source).encode())
    return digest.hexdigest()


def normalize_monomial(monomial, b_variable, inverse_b):
    output = list(monomial)
    cancellations = min(output.count(b_variable), output.count(inverse_b))
    for _ in range(cancellations):
        output.remove(b_variable)
        output.remove(inverse_b)
    return tuple(sorted(output))


def localized_add(target, source, b_variable, inverse_b, scale=QQ(1)):
    for monomial, coefficient in source.items():
        output = normalize_monomial(monomial, b_variable, inverse_b)
        target[output] = target.get(output, QQ(0)) + scale * coefficient
        if not target[output]:
            target.pop(output)


def localized_multiply(left, right, b_variable, inverse_b):
    answer = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            localized_add(
                answer,
                {left_monomial + right_monomial:
                 left_coefficient * right_coefficient},
                b_variable,
                inverse_b,
            )
    return answer


def change_to_b_coordinate(source, z44, z45, b_variable, inverse_b):
    """Replace z45 by b-z44 exactly before localized graph expansion."""

    answer = {}
    replacement = {(b_variable,): QQ(1), (z44,): QQ(-1)}
    for monomial, coefficient in source.items():
        value = {(): coefficient}
        for variable in monomial:
            factor = replacement if variable == z45 else {(variable,): QQ(1)}
            value = localized_multiply(
                value, factor, b_variable, inverse_b
            )
        localized_add(answer, value, b_variable, inverse_b)
    return answer


def dynamic_product_coefficient(
    dynamic_monomial, order, series, cache, b_variable, inverse_b
):
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
                tail, order - degree, series, cache,
                b_variable, inverse_b,
            )
            if rest:
                localized_add(
                    answer,
                    localized_multiply(
                        head, rest, b_variable, inverse_b
                    ),
                    b_variable,
                    inverse_b,
                )
    cache[key] = answer
    return answer


def coefficient_on_localized_graph(
    source, order, series, dynamic_variables, cache, b_variable, inverse_b
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
            dynamic, order, series, cache, b_variable, inverse_b
        )
        for graph_monomial, graph_coefficient in value.items():
            localized_add(
                answer,
                {base + graph_monomial: coefficient * graph_coefficient},
                b_variable,
                inverse_b,
            )
    return answer


def source_graph(base):
    layout = base["layout"]
    tau = base["tau"]
    normal = base["normal"]
    transverse = base["transverse"]
    obstruction = base["obstruction"]
    pivots = base["pivots"]
    local_variables = base["local_variables"]
    first_bend = base["first_bend"]
    second_bend = base["second_bend"]
    third_bend = second_bend + 1
    b_variable = third_bend + 1
    inverse_b = third_bend + 2
    z46 = layout["a"][46]
    z44 = layout["a"][44]
    z45 = layout["a"][45]
    normal = [
        change_to_b_coordinate(
            source, z44, z45, b_variable, inverse_b
        )
        for source in normal
    ]
    transverse = [
        change_to_b_coordinate(
            source, z44, z45, b_variable, inverse_b
        )
        for source in transverse
    ]
    obstruction = [
        change_to_b_coordinate(
            source, z44, z45, b_variable, inverse_b
        )
        for source in obstruction
    ]
    dynamic_variables = local_variables | {z46}
    maximum_order = 6
    series = {
        variable: [{} for _order in range(maximum_order + 1)]
        for variable in dynamic_variables
    }
    series[tau][1] = {(): QQ(1)}
    series[z46][0] = {(z46,): QQ(1)}
    series[z46][1] = {(first_bend,): QQ(1)}
    series[z46][2] = {(second_bend,): QQ(1)}
    series[z46][3] = {(third_bend,): QQ(1)}

    compatibility_orders = []
    transverse_residual_orders = []
    for order in range(1, maximum_order + 1):
        cache = {}
        normal_incoming = [
            coefficient_on_localized_graph(
                source, order, series, dynamic_variables, cache,
                b_variable, inverse_b,
            )
            for source in normal
        ]
        for pivot, incoming in zip(pivots, normal_incoming):
            series[layout["y"][pivot]][order] = CENTER.negate(incoming)

        cache = {}
        transverse_incoming = [
            coefficient_on_localized_graph(
                source, order, series, dynamic_variables, cache,
                b_variable, inverse_b,
            )
            for source in transverse
        ]
        for parameter, incoming in zip(
            P5.P5_NORMAL_VARIABLES, transverse_incoming
        ):
            series[layout["n"][parameter]][order] = CENTER.negate(
                localized_multiply(
                    incoming, {(inverse_b,): QQ(1)},
                    b_variable, inverse_b,
                )
            )

        cache = {}
        require(
            not any(
                coefficient_on_localized_graph(
                    source, order, series, dynamic_variables, cache,
                    b_variable, inverse_b,
                )
                for source in normal
            ),
            f"dynamic normal graph failed at order {order}",
        )
        cache = {}
        transverse_residual_orders.append([
            coefficient_on_localized_graph(
                source, order, series, dynamic_variables, cache,
                b_variable, inverse_b,
            )
            for source in transverse
        ])
        cache = {}
        compatibility = [
            coefficient_on_localized_graph(
                source, order, series, dynamic_variables, cache,
                b_variable, inverse_b,
            )
            for source in obstruction
        ]
        compatibility_orders.append(compatibility)
    return {
        "series": series,
        "third_bend": third_bend,
        "b_variable": b_variable,
        "inverse_b": inverse_b,
        "compatibility_orders": compatibility_orders,
        "transverse_residual_orders": transverse_residual_orders,
    }


def singular_center(
    base, graph, ell, first_relation, second_relation, g_relation
):
    layout = base["layout"]
    first_bend = base["first_bend"]
    second_bend = base["second_bend"]
    third_bend = graph["third_bend"]
    b_variable = graph["b_variable"]
    inverse_b = graph["inverse_b"]
    inverse_z11 = inverse_b + 1
    inverse_z16 = inverse_b + 2
    inverse_z41 = inverse_b + 3
    variable_count = inverse_z41 + 1
    names = [f"x{index}" for index in range(variable_count)]
    for parameter, variable in layout["a"].items():
        names[variable] = f"z{parameter}"
    names[first_bend] = "s"
    names[second_bend] = "t"
    names[third_bend] = "r3"
    names[b_variable] = "b"
    names[inverse_b] = "q"
    names[inverse_z11] = "w"
    names[inverse_z16] = "p16"
    names[inverse_z41] = "p41"

    order6 = graph["compatibility_orders"][5]
    active = set().union(*(
        set(variable for monomial in source for variable in monomial)
        for source in [ell, first_relation, second_relation, g_relation, *order6]
    ))
    special = {
        first_bend, second_bend, third_bend, b_variable, inverse_b,
        inverse_z11, inverse_z16, inverse_z41, 0,
    }
    ring_order = ["r3", "t", "s", "q", "w", "p16", "p41", "b"] + [
        names[index] for index in sorted(active - special)
    ]
    require(len(set(ring_order)) == len(ring_order),
            "Singular G variable names are not unique")
    encode = REES.AMBIENT.singular_polynomial
    a = layout["a"]
    common = polynomial((((a[11], a[16], a[16], a[41]), QQ(1, 2)),))
    u = polynomial((((a[26],), 1), ((b_variable,), 1), ((a[44],), -1)))
    minus_v = polynomial((((a[44],), 1), ((a[26],), -1)))
    expected30 = localized_multiply(
        localized_multiply(common, u, b_variable, inverse_b),
        g_relation, b_variable, inverse_b,
    )
    expected30 = {monomial: -coefficient
                  for monomial, coefficient in expected30.items()}
    expected33 = localized_multiply(
        localized_multiply(common, minus_v, b_variable, inverse_b),
        g_relation, b_variable, inverse_b,
    )

    lines = [f"ring rr=0,({','.join(ring_order)}),dp;"]
    lines.append(f"poly ell={encode(ell, names)};")
    lines.append(f"poly first={encode(first_relation, names)};")
    lines.append(f"poly second={encode(second_relation, names)};")
    lines.append(f"poly grow={encode(g_relation, names)};")
    lines.extend((
        "poly locb=b*q-1;",
        "poly loc11=z11*w-1;",
        "poly loc16=z16*p16-1;",
        "poly loc41=z41*p41-1;",
        "ideal old=ell,first,second,locb,loc11,loc16,loc41;",
        "ideal gold=std(old);",
        '"OLDUNIT",(reduce(1,gold)==0);',
    ))
    nonzero_rows = []
    for row, source in enumerate(order6, 1):
        if not source:
            continue
        nonzero_rows.append(row)
        lines.append(f"poly e{row}={encode(source, names)};")
    lines.append(f"poly expected30={encode(expected30, names)};")
    lines.append(f"poly expected33={encode(expected33, names)};")
    lines.extend((
        "poly old30=reduce(e30,gold);",
        "poly old33=reduce(e33,gold);",
        '"OLD30",size(old30),(old30==0);',
        '"OLD33",size(old33),(old33==0);',
        '"FORM30",(reduce(e30-expected30,gold)==0);',
        '"FORM33",(reduce(e33-expected33,gold)==0);',
        "ideal newer=old,grow;",
        "ideal gnew=std(newer);",
        '"NEWUNIT",(reduce(1,gnew)==0);',
    ))
    for row in nonzero_rows:
        lines.append(f'"ROW",{row},(reduce(e{row},gnew)==0);')
    lines.append("quit;")
    completed = subprocess.run(
        ["/usr/local/bin/Singular", "-q"],
        input="\n".join(lines),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
        check=False,
    )
    require(completed.returncode == 0, "Singular source G reduction failed")
    require("OLDUNIT 0" in completed.stdout
            and "NEWUNIT 0" in completed.stdout,
            "localized G ideal became the unit ideal")
    require("FORM30 1" in completed.stdout and "FORM33 1" in completed.stdout,
            "source G exceptional factorization changed")
    require("OLD30 42 0" in completed.stdout
            and "OLD33 28 0" in completed.stdout,
            "source G exceptional normal forms changed")
    require(
        all(line.endswith(" 1") for line in completed.stdout.splitlines()
            if line.startswith("ROW ")),
        "a sixth-order compatibility row escaped G",
    )
    return {
        "nonzero_rows": nonzero_rows,
        "old_exceptional_normal_form_terms": {"Q30": 42, "Q33": 28},
        "stdout_sha256": sha256(completed.stdout.encode()).hexdigest(),
    }


def audit():
    base = F2.audit(return_data=True)
    graph = source_graph(base)
    require(not any(
        source
        for values in graph["transverse_residual_orders"]
        for source in values
    ), "localized eleven-row transverse graph did not vanish exactly")
    layout = base["layout"]
    a = layout["a"]
    b_variable = graph["b_variable"]
    inverse_b = graph["inverse_b"]
    first_relation = change_to_b_coordinate(
        base["first_relation"], a[44], a[45], b_variable, inverse_b
    )
    second_relation = change_to_b_coordinate(
        base["second_relation"], a[44], a[45], b_variable, inverse_b
    )
    ell = polynomial((((a[9], a[25]), 1), ((a[11], a[46]), -1)))
    g_relation = polynomial((
        ((a[0], a[26], a[30], a[54]), 1),
        ((a[26], a[30], a[30], a[54]), -1),
        ((a[0], a[7], a[46], a[54]), 1),
        ((a[7], a[24], a[46], a[54]), -1),
        ((a[7], a[30], a[46], a[54]), -1),
        ((a[0], a[26], a[52], a[54]), -1),
        ((a[26], a[30], a[52], a[54]), 1),
        ((a[7], a[46], a[52], a[54]), 1),
        ((a[7], a[26], a[54], a[54]), 1),
        ((base["first_bend"], a[0], a[52]), -1),
        ((base["first_bend"], a[7], a[54]), 1),
        ((base["second_bend"], a[0]), -1),
        ((base["second_bend"], a[52]), -1),
        ((graph["third_bend"],), -1),
    ))
    require(F2.variable_coefficient(g_relation, graph["third_bend"]) == {
        (): QQ(-1)
    }, "G is no longer monic in the third bend")
    singular = singular_center(
        base, graph, ell, first_relation, second_relation, g_relation
    )
    compatibility_orders = graph["compatibility_orders"]
    order6 = compatibility_orders[5]
    ledger = {
        "source": "finite first P5 Rees equations after 207-row Schur graph",
        "component": "dense generic L with F1,F2 adjoined",
        "coordinate_change": "b=z44+z45, z45=b-z44, q=b^-1",
        "localized_graph": {
            "normal_rows": 196,
            "transverse_rows": 11,
            "orders_solved": 6,
            "all_transverse_residuals_zero": True,
            "compatibility_term_counts": [
                sum(map(len, values)) for values in compatibility_orders
            ],
            "compatibility_nonzero_row_counts": [
                sum(bool(source) for source in values)
                for values in compatibility_orders
            ],
            "order6_family_sha256": family_digest(order6),
        },
        "G": {
            "terms": len(g_relation),
            "sha256": REES.polynomial_digest(g_relation),
            "third_bend_coefficient": -1,
            "formula": (
                "z0*z26*z30*z54-z26*z30^2*z54+z0*z7*z46*z54-"
                "z7*z24*z46*z54-z7*z30*z46*z54-z0*z26*z52*z54+"
                "z26*z30*z52*z54+z7*z46*z52*z54+z7*z26*z54^2-"
                "s*z0*z52+s*z7*z54-t*z0-t*z52-r3"
            ),
        },
        "localized_char0_reduction": {
            "old_ideal": "<L,F1,F2,b*q-1,z11*w-1,z16*p16-1,z41*p41-1>",
            "old_ideal_is_nonunit": True,
            "Q30_normal_form_terms": 42,
            "Q33_normal_form_terms": 28,
            "Q30_factor": (
                "-1/2*z11*z16^2*z41*(z26+b-z44)*G"
            ),
            "Q33_factor": (
                "1/2*z11*z16^2*z41*(z44-z26)*G"
            ),
            "new_ideal_is_nonunit": True,
            "nonzero_order6_rows": singular["nonzero_rows"],
            "all_order6_rows_reduce_to_zero_after_G": True,
            "singular_output_sha256": singular["stdout_sha256"],
        },
        "consequence": (
            "the source Schur graph recovers the monic generic-L third-bend center G"
        ),
        "scope_guard": (
            "exact through graph order six; all-order recurrence and full H0/H1 "
            "membership remain unproved"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 is not None:
        require(digest == EXPECTED_LEDGER_SHA256,
                "generic-L G Schur ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
