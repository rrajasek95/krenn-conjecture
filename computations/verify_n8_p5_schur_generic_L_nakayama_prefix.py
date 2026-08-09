#!/usr/bin/env python3
"""Test the generic-L principal mixed recurrence modulo the next tau order."""

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


G = load_module(
    "n8_p5_schur_g_for_nakayama_prefix",
    "verify_n8_p5_schur_generic_L_g_center.py",
)
F2 = G.F2
REES = G.REES
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "4e36eb6cc9360ad366818339a857c13b9d197a4739aff0c3b9fec0ef99b2b626"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    REES.add(target, source, scale)


def polynomial(entries):
    answer = {}
    for monomial, coefficient in entries:
        add(answer, {tuple(sorted(monomial)): QQ(coefficient)})
    return answer


def center_relations(base, graph):
    layout = base["layout"]
    a = layout["a"]
    b = graph["b_variable"]
    q = graph["inverse_b"]
    first = G.change_to_b_coordinate(
        base["first_relation"], a[44], a[45], b, q
    )
    second = G.change_to_b_coordinate(
        base["second_relation"], a[44], a[45], b, q
    )
    ell = polynomial((((a[9], a[25]), 1), ((a[11], a[46]), -1)))
    grow = polynomial((
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
    return ell, first, second, grow


def truncated_rows(graph, epsilon, depth):
    orders = graph["compatibility_orders"][5:5 + depth]
    answer = []
    for row in range(39):
        value = {}
        for epsilon_degree, sources in enumerate(orders):
            add(value, {
                tuple(sorted(monomial + (epsilon,) * epsilon_degree)):
                coefficient
                for monomial, coefficient in sources[row].items()
            })
        answer.append(value)
    return answer


def pure_prefixes(base, graph, epsilon):
    schur = G.F2.SCHUR.audit(return_data=True)
    require(schur["layout"] == base["layout"],
            "pure and mixed Schur layouts diverged")
    layout = base["layout"]
    b = graph["b_variable"]
    q = graph["inverse_b"]
    dynamic = base["dynamic_variables"]
    coefficients = []
    for source in schur["pure_stricts"]:
        source = G.change_to_b_coordinate(
            source, layout["a"][44], layout["a"][45], b, q
        )
        coefficients.append([
            G.coefficient_on_localized_graph(
                source, order, graph["series"], dynamic, {}, b, q
            )
            for order in range(1, 8)
        ])
    starts = ((4, 5, 6), (5, 6))
    windows = []
    for colour, colour_starts in enumerate(starts):
        for start in colour_starts:
            value = dict(coefficients[colour][start - 1])
            add(value, {
                tuple(sorted(monomial + (epsilon,))): coefficient
                for monomial, coefficient in coefficients[colour][start].items()
            })
            windows.append((colour, start, value))
    return coefficients, windows


def singular_membership(
    base, graph, relations, rows, epsilon, depth, pure_windows
):
    layout = base["layout"]
    a = layout["a"]
    b = graph["b_variable"]
    q = graph["inverse_b"]
    inverse_z11 = epsilon + 1
    inverse_z16 = epsilon + 2
    inverse_z41 = epsilon + 3
    inverse_u = epsilon + 4
    names = [f"x{index}" for index in range(inverse_u + 1)]
    for parameter, variable in a.items():
        names[variable] = f"z{parameter}"
    names[base["first_bend"]] = "s"
    names[base["second_bend"]] = "t"
    names[graph["third_bend"]] = "r3"
    names[b] = "b"
    names[q] = "q"
    names[epsilon] = "e"
    names[inverse_z11] = "w"
    names[inverse_z16] = "p16"
    names[inverse_z41] = "p41"
    names[inverse_u] = "pu"
    active = set().union(*(
        set(variable for monomial in source for variable in monomial)
        for source in [*relations, *rows, *(item[2] for item in pure_windows)]
    ))
    special = {
        0, epsilon, graph["third_bend"], base["second_bend"],
        base["first_bend"], q, inverse_z11, inverse_z16,
        inverse_z41, inverse_u, b,
    }
    ring_order = [
        "e", "r3", "t", "s", "pu", "q", "w", "p16", "p41", "b",
    ] + [names[index] for index in sorted(active - special)]
    require(len(set(ring_order)) == len(ring_order),
            "Nakayama-prefix Singular names collided")
    encode = REES.AMBIENT.singular_polynomial
    ell, first, second, grow = relations
    lines = [f"ring rr=0,({','.join(ring_order)}),dp;"]
    lines.extend((
        f"poly ell={encode(ell, names)};",
        f"poly first={encode(first, names)};",
        f"poly second={encode(second, names)};",
        f"poly grow={encode(grow, names)};",
        "poly locb=b*q-1;",
        "poly loc11=z11*w-1;",
        "poly loc16=z16*p16-1;",
        "poly loc41=z41*p41-1;",
        "poly locu=(z26+b-z44)*pu-1;",
        f"poly selected={encode(rows[29], names)};",
        f"ideal prefix=ell,first,second,locb,loc11,loc16,loc41,locu,e{depth},selected;",
        "ideal gp=std(prefix);",
        '"UNIT",(reduce(1,gp)==0);',
    ))
    nonzero_rows = [row + 1 for row, source in enumerate(rows) if source]
    for row in nonzero_rows:
        lines.append(f"poly m{row}={encode(rows[row - 1], names)};")
        lines.append(
            f'"ROW",{row},size(reduce(m{row},gp)),(reduce(m{row},gp)==0);'
        )
    for colour, start, source in pure_windows:
        lines.append(f"poly h{colour}_{start}={encode(source, names)};")
        lines.append(
            f'"PURE",{colour},{start},size(reduce(h{colour}_{start},gp)),'
            f'(reduce(h{colour}_{start},gp)==0);'
        )
    lines.append("quit;")
    # Singular understands e2 as e^2 in its polynomial syntax.
    completed = subprocess.run(
        ["/usr/local/bin/Singular", "-q"],
        input="\n".join(lines),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
        check=False,
    )
    print(completed.stdout)
    require(completed.returncode == 0,
            "generic-L Nakayama-prefix reduction failed")
    require("UNIT 0" in completed.stdout,
            "generic-L dual-number prefix ideal became unit")
    flags = {}
    sizes = {}
    pure_flags = {}
    pure_sizes = {}
    for line in completed.stdout.splitlines():
        if line.startswith("ROW "):
            _label, row, size, zero = line.split()
            flags[int(row)] = zero == "1"
            sizes[int(row)] = int(size)
        elif line.startswith("PURE "):
            _label, colour, start, size, zero = line.split()
            key = int(colour), int(start)
            pure_flags[key] = zero == "1"
            pure_sizes[key] = int(size)
    require(set(flags) == set(nonzero_rows),
            "Nakayama-prefix row output incomplete")
    require(set(pure_flags) == {
        (colour, start) for colour, start, _source in pure_windows
    }, "pure Nakayama-prefix output incomplete")
    return {
        "flags": flags,
        "sizes": sizes,
        "pure_flags": pure_flags,
        "pure_sizes": pure_sizes,
        "stdout_sha256": sha256(completed.stdout.encode()).hexdigest(),
    }


def audit():
    base = F2.audit(return_data=True)
    depth = 2
    graph = G.source_graph(base, maximum_order=5 + depth)
    epsilon = graph["inverse_b"] + 1
    relations = center_relations(base, graph)
    rows = truncated_rows(graph, epsilon, depth)
    pure_coefficients, pure_windows = pure_prefixes(base, graph, epsilon)
    singular = singular_membership(
        base, graph, relations, rows, epsilon, depth, pure_windows
    )
    failures = [row for row, zero in singular["flags"].items() if not zero]
    ledger = {
        "source": "finite first P5 Rees equations after exact 207-row graph",
        "component": "dense generic L/F1/F2 chart",
        "prefix": f"tau-saturated mixed germs modulo tau^{depth}",
        "graph_compatibility_terms": [
            sum(map(len, graph["compatibility_orders"][order]))
            for order in range(5, 5 + depth)
        ],
        "graph_nonzero_rows": [
            sum(bool(source) for source in graph["compatibility_orders"][order])
            for order in range(5, 5 + depth)
        ],
        "selected_generator": "M30",
        "additional_localizer": "z26+b-z44 = z26+z45",
        "localized_prefix_ideal_is_nonunit": True,
        "rows_in_selected_prefix_ideal": sorted(
            row for row, zero in singular["flags"].items() if zero
        ),
        "escaping_rows": failures,
        "escaping_remainder_sizes": {
            str(row): singular["sizes"][row] for row in failures
        },
        "M33_adds_independent_prefix": 33 in failures,
        "pure_graph_term_counts": [
            [len(source) for source in values]
            for values in pure_coefficients
        ],
        "pure_dual_windows": {
            f"H{colour}_orders_{start}_{start + 1}": {
                "zero_in_selected_prefix_ideal": singular["pure_flags"][
                    colour, start
                ],
                "remainder_size": singular["pure_sizes"][colour, start],
            }
            for colour, start, _source in pure_windows
        },
        "singular_output_sha256": singular["stdout_sha256"],
        "consequence": (
            f"the principal Nakayama recurrence passes modulo tau^{depth}"
            if not failures else
            f"the M30-principal Nakayama recurrence fails modulo tau^{depth}"
        ),
        "scope_guard": (
            "dual-number/source-graph prefix only; no all-order mixed or pure membership"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 is not None:
        require(digest == EXPECTED_LEDGER_SHA256,
                "generic-L Nakayama-prefix ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
