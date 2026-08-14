#!/usr/bin/env python3
"""Build the smallest full-site/root-labelled closed balanced chart guard.

Full S8 covariance connects the DQ chart to both endpoint PS charts, but a
presentation-safe chart comparison retains its object/carrier label.  Two
commuting site transpositions give a literal four-object square.  The
physical matching alternates DQ <-> PS, the residual window and pure word
are fixed, and the conjugated root labels return path-independently.

The square is a centered K2,2 complete-row component.  One copy for each
pure target colour is compatible with P0=P1=P2=1; including both required
switch families gives six disjoint labelled squares.  Every relative chart
edge extends the centered detector, so no absolute fixed-source switch is
created.  This is a smallest exact counterguard to any theorem using only
site/root covariance, literal labels and pure normalization to exclude a
closed balanced companion component.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_h2_full_site_groupoid_tag_contraction.py":
        "eb2acb53ca9364ff4639985996f75321800d74b798858cda04084e997a15aa23",
    "notes/h3-h2-full-site-groupoid-tag-contraction.md":
        "47394c03902597892a2a4c01bc488dfc34f782e635e822e946304e1d5686faf1",
    "computations/verify_h3_h2_full_site_chart_swap_pointed_scalar_guard.py":
        "bc35781e0f57bbd1202711e2dc818417d76fa87c69e33d3d4b01540e06865557",
    "notes/h3-h2-full-site-chart-swap-pointed-scalar-guard.md":
        "77771f8eee2a4bbaeb5a9575961efb9c7728833e28bca86d33102806aeffa6c2",
    "computations/verify_uniform_global_centered_k22_normalization_counterguard.py":
        "0e9872d699e172d477a0562442c40d0805a19843e2e21efa47d88a1c1880e1ec",
    "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py":
        "2ac01c9ba571338b4c7b779dbc70d5d0eaacb2fe01a4035833970fa6b9826fe0",
    "computations/verify_h3_hyperbolic_collision_fixed_window_matching_routing_gate.py":
        "b8d02d77213bbb21d68dbad0aa4d6d1263625de012e413547723999d8d87fada",
}
EXPECTED_LEDGER_SHA256 = (
    "c14e3adfb08c8f70e08778129da7a8f0b64651fa4ff698d8f8beb3da598cc053"
)


P, S = 6, 7
ZERO, ONE, TWO, THREE, FOUR, FIVE = range(6)
SITES = tuple(range(8))
NAMES = ("0", "1", "2", "3", "4", "5", "P", "S")
BASE_A = (tuple(sorted((P, S))), tuple(sorted((ZERO, ONE))))
BASE_B = (tuple(sorted((P, ZERO))), tuple(sorted((S, ONE))))
BASE_C = (tuple(sorted((P, ONE))), tuple(sorted((S, ZERO))))
TAILS = (
    ((TWO, THREE), (FOUR, FIVE)),
    ((TWO, FOUR), (THREE, FIVE)),
    ((TWO, FIVE), (THREE, FOUR)),
)
STATES = ((0, 0), (1, 0), (1, 1), (0, 1))
STATE_POSITION = {state: index for index, state in enumerate(STATES)}
SQUARE_EDGES = ((0, 1), (1, 2), (3, 2), (0, 3))
LAMBDA = (Q(1), Q(-1), Q(1), Q(-1))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    columns = tuple(columns)
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def edge(left, right):
    return tuple(sorted((left, right)))


def matching(*edges):
    return tuple(sorted(edges))


def transposition(left, right):
    permutation = list(SITES)
    permutation[left], permutation[right] = right, left
    return tuple(permutation)


def compose(left, right):
    """left after right."""
    return tuple(left[right[site]] for site in SITES)


def act_edge(value, permutation):
    return edge(permutation[value[0]], permutation[value[1]])


def act_matching(value, permutation):
    return matching(*(act_edge(item, permutation) for item in value))


def state_permutation(state, generators):
    answer = tuple(SITES)
    if state[0]:
        answer = compose(generators[0], answer)
    if state[1]:
        answer = compose(generators[1], answer)
    return answer


def component_geometry(name, generators, endpoint_chart, root):
    require(compose(generators[0], generators[1])
            == compose(generators[1], generators[0]),
            ("site generators stopped commuting", name))
    objects = []
    signatures = {}
    for state in STATES:
        permutation = state_permutation(state, generators)
        core = act_matching(BASE_A, permutation)
        expected = BASE_A if sum(state) % 2 == 0 else endpoint_chart
        require(core == matching(*expected),
                ("chart square stopped alternating", name, state, core,
                 expected))
        ports = tuple(permutation[value]
                      for value in (P, S, ZERO, ONE))
        require(len(set(ports)) == 4 and set(ports) == {P, S, ZERO, ONE},
                ("an operation port left the fixed four-set", name, state,
                 ports))
        root_signature = tuple(sorted(
            (act_edge(source, permutation), factor,
             act_edge(target, permutation))
            for source, factor, target in root
        ))
        signatures[state] = root_signature
        objects.append({
            "state": list(state),
            "ports_P_S_0_1": [NAMES[value] for value in ports],
            "physical_core": [NAMES[a] + NAMES[b] for a, b in core],
            "chart": "A=DQ" if sum(state) % 2 == 0 else name,
            "tail_matchings": [
                [NAMES[a] + NAMES[b] for a, b in tail]
                for tail in TAILS
            ],
        })

    # Every edge transports the conjugated root signature literally, and
    # both paths to the opposite corner agree.  The pure words are fixed.
    for coordinate, generator in enumerate(generators):
        for state in STATES:
            target = list(state)
            target[coordinate] ^= 1
            target = tuple(target)
            transported = tuple(sorted(
                (act_edge(source, generator), factor,
                 act_edge(output, generator))
                for source, factor, output in signatures[state]
            ))
            require(transported == signatures[target],
                    ("root signature transport changed", name, state,
                     coordinate, transported, signatures[target]))
    for colour in range(3):
        word = (colour,) * 8
        for generator in generators:
            transported = tuple(word[generator[site]] for site in SITES)
            require(transported == word,
                    ("a pure target word changed", name, colour))
    return {
        "family": name,
        "site_generators": [
            [NAMES[index] for index in pair]
            for pair in ((next(i for i in SITES if generators[0][i] != i),
                          next(i for i in reversed(SITES)
                               if generators[0][i] != i)),
                         (next(i for i in SITES if generators[1][i] != i),
                          next(i for i in reversed(SITES)
                               if generators[1][i] != i)))
        ],
        "objects": objects,
        "root_signatures": {
            repr(state): [
                [NAMES[source[0]] + NAMES[source[1]], str(factor),
                 NAMES[target[0]] + NAMES[target[1]]]
                for source, factor, target in signatures[state]
            ]
            for state in STATES
        },
        "fixed_operation_four_set": ["P", "S", "0", "1"],
        "fixed_residual_window": ["2", "3", "4", "5"],
        "pure_words_fixed": 3,
        "root_transport_flat": True,
        "outside_tail_port_edges": 0,
    }


def connected(vertices, edges):
    if not vertices:
        return False
    seen = {vertices[0]}
    changed = True
    while changed:
        changed = False
        for left, right in edges:
            if left in seen and right not in seen:
                seen.add(right)
                changed = True
            if right in seen and left not in seen:
                seen.add(left)
                changed = True
    return len(seen) == len(vertices)


def bipartition(vertices, edges):
    colour = {}
    for start in vertices:
        if start in colour:
            continue
        colour[start] = 0
        stack = [start]
        while stack:
            current = stack.pop()
            for left, right in edges:
                if current not in (left, right):
                    continue
                other = right if current == left else left
                if other in colour:
                    if colour[other] == colour[current]:
                        return None
                    continue
                colour[other] = 1 - colour[current]
                stack.append(other)
    return colour


def minimal_balanced_census():
    counts = {}
    for size in range(2, 5):
        vertices = tuple(range(size))
        possible = tuple(combinations(vertices, 2))
        count = 0
        for mask in range(1 << len(possible)):
            edges = tuple(possible[index] for index in range(len(possible))
                          if mask & (1 << index))
            degrees = [sum(vertex in item for item in edges)
                       for vertex in vertices]
            if min(degrees) < 2 or not connected(vertices, edges):
                continue
            colours = bipartition(vertices, edges)
            if colours is None:
                continue
            if sum(value == 0 for value in colours.values()) != (
                    sum(value == 1 for value in colours.values())):
                continue
            count += 1
        counts[size] = count
    require(counts == {2: 0, 3: 0, 4: 3},
            ("minimal balanced graph census changed", counts))
    return counts


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    root_b = (
        (edge(P, ZERO), Q(1), edge(P, S)),
        (edge(ZERO, ONE), Q(-1), edge(S, ONE)),
    )
    root_c = (
        (edge(P, ONE), Q(1), edge(P, S)),
        (edge(ZERO, ONE), Q(-1), edge(S, ZERO)),
    )
    families = {
        "B=P0|S1": component_geometry(
            "B=P0|S1",
            (transposition(S, ZERO), transposition(P, ONE)),
            BASE_B,
            root_b,
        ),
        "C=P1|S0": component_geometry(
            "C=P1|S0",
            (transposition(P, ZERO), transposition(S, ONE)),
            BASE_C,
            root_c,
        ),
    }

    # Six monochromatic components: both required switch families in each of
    # the three normalized pure target colours.  Each complete row contains
    # its pure core and the two incident internal companion coordinates.
    components = tuple((colour, family)
                       for colour in range(3) for family in families)
    row_labels = tuple((component, vertex)
                       for component in components for vertex in range(4))
    companion_labels = tuple((component, edge_index)
                             for component in components
                             for edge_index in range(4))
    coordinate_order = tuple(("P", colour) for colour in range(3)) + tuple(
        ("z", component, edge_index)
        for component, edge_index in companion_labels
    )
    coordinate_position = {label: index
                           for index, label in enumerate(coordinate_order)}
    rows = []
    for component, vertex in row_labels:
        colour, _family = component
        row = [Q(0)] * len(coordinate_order)
        row[coordinate_position[("P", colour)]] = 1
        for edge_index, endpoints in enumerate(SQUARE_EDGES):
            if vertex in endpoints:
                row[coordinate_position[("z", component, edge_index)]] = 1
        require(sum(row) == 3, ("complete row degree changed", component,
                               vertex, row))
        rows.append(tuple(row))
    rows = tuple(rows)
    complete_rank = rank(rows)
    require(len(rows) == 24 and complete_rank == 18
            and len(rows) - complete_rank == len(components) == 6,
            ("six-square complete-row rank changed", complete_rank))

    relations = []
    for component in components:
        relation = [Q(0)] * len(rows)
        for vertex, coefficient in enumerate(LAMBDA):
            relation[row_labels.index((component, vertex))] = coefficient
        combined = tuple(sum((relation[column] * rows[column][row]
                              for column in range(len(rows))), Q(0))
                         for row in range(len(coordinate_order)))
        require(not any(combined), ("centered relation changed", component))
        relations.append(tuple(relation))
    require(rank(relations) == 6, "component centered charges coupled")

    evaluation = []
    for label in coordinate_order:
        evaluation.append(Q(1) if label[0] == "P" else Q(-1, 2))
    evaluation = tuple(evaluation)
    require(all(dot(evaluation, row) == 0 for row in rows)
            and evaluation[:3] == (Q(1), Q(1), Q(1)),
            "the pure-normalized complete-row point changed")

    # Presentation-safe chart mapping cylinders.  There is one object/core
    # coordinate at each vertex and one retained carrier at each edge.  The
    # centered detector extends by the edge difference, so all relative bars
    # are killed and the centered object charge remains visible.
    graph_components = []
    graph_width_per_component = 8
    graph_width = len(components) * graph_width_per_component
    graph_columns = []
    graph_charge = [Q(0)] * graph_width
    graph_dual = [Q(0)] * graph_width
    for component_index, component in enumerate(components):
        offset = component_index * graph_width_per_component
        for vertex, coefficient in enumerate(LAMBDA):
            graph_charge[offset + vertex] = coefficient
            graph_dual[offset + vertex] = coefficient / 4
        for edge_index, (source, target) in enumerate(SQUARE_EDGES):
            column = [Q(0)] * graph_width
            column[offset + target] = 1
            column[offset + source] = -1
            column[offset + 4 + edge_index] = -1
            graph_columns.append(tuple(column))
            graph_dual[offset + 4 + edge_index] = (
                LAMBDA[target] - LAMBDA[source]
            ) / 4
        graph_components.append({
            "component": [component[0], component[1]],
            "object_charge": list(map(str, LAMBDA)),
            "cycle_holonomy": "+1",
        })
    graph_columns = tuple(graph_columns)
    graph_charge = tuple(graph_charge)
    graph_dual = tuple(graph_dual)
    require(rank(graph_columns) == len(graph_columns) == 24
            and graph_width - rank(graph_columns) == 24
            and all(dot(graph_dual, column) == 0
                    for column in graph_columns)
            and dot(graph_dual, graph_charge) == len(components)
            and not any(sum(LAMBDA) for _component in components),
            "the relative chart-square detector changed")

    # Every absolute fixed-source chart edge would be a first rank raiser:
    # it drops the retained carrier and is read nontrivially by the extended
    # dual.  Site/root covariance supplies the graph column, not this edge.
    absolute_edge_values = []
    for component_index, _component in enumerate(components):
        offset = component_index * graph_width_per_component
        for source, target in SQUARE_EDGES:
            column = [Q(0)] * graph_width
            column[offset + target] = 1
            column[offset + source] = -1
            absolute_edge_values.append(dot(graph_dual, column))
    require(set(absolute_edge_values) == {Q(1, 2), Q(-1, 2)},
            ("absolute switch stopped raising the centered charge",
             absolute_edge_values))

    minimal_census = minimal_balanced_census()
    ledger = {
        "theorem": "full-site/root closed balanced companion-cycle counterguard",
        "pins": PINS,
        "fixed_window": {
            "operation_sites": ["P", "S", "0", "1"],
            "tail_sites": ["2", "3", "4", "5"],
            "tail_matchings": 3,
            "base_chart": "A=PS|01",
            "switch_families": list(families),
        },
        "literal_site_root_squares": families,
        "full_two_switch_pure_normalized_guard": {
            "pure_target_values": ["P0=1", "P1=1", "P2=1"],
            "components": len(components),
            "complete_rows": len(rows),
            "internal_companions": len(companion_labels),
            "complete_row_rank": complete_rank,
            "complete_row_relation_dimension": len(rows) - complete_rank,
            "relation_basis": "one (1,-1,1,-1) charge per component",
            "exact_point": "P0=P1=P2=1; every internal companion=-1/2",
            "all_rows_vanish_at_exact_point": True,
            "singletons": 0,
            "odd_holonomy_components": 0,
            "outside_tail_fan_edges": 0,
        },
        "presentation_safe_chart_bars": {
            "coordinates": graph_width,
            "relative_graphs": len(graph_columns),
            "rank": rank(graph_columns),
            "H0_dimension": graph_width - rank(graph_columns),
            "boundary": "d beta_e=x_target-x_source-u_e",
            "extended_centered_dual_on_all_graphs": "0",
            "dual_on_six_component_charge": str(dot(graph_dual,
                                                       graph_charge)),
            "absolute_switch_dual_values": sorted(
                {str(value) for value in absolute_edge_values}
            ),
        },
        "minimality": {
            "criterion": (
                "connected simple, minimum row degree two, bipartite and "
                "equal shore sizes"
            ),
            "labelled_candidates_by_vertex_count": minimal_census,
            "smallest_single_switch_component": "C4=K2,2 on four objects",
            "monochromatic_all-pure_guard_components": 3,
            "both_required_switches_all-pure_guard_components": 6,
        },
        "counterguard_consequence": (
            "Literal physical site permutations, their conjugated E01/E02 "
            "root labels, fixed ports/window, and all three pure target "
            "normalizations do not exclude a finite closed balanced "
            "companion component.  They give flat relative chart graphs."
        ),
        "missing_hypothesis": (
            "A positive cycle theorem must use a boundary law stronger than "
            "site/root covariance: some mapping-cylinder carrier must have "
            "an absolute same-word/fine/root/reinsertion landing, or a "
            "mandatory PP/collision face must leave the operation four-set "
            "into an active outside fan.  The pinned physical audits locate "
            "the first proper face at L01 / the occurrence-split collision "
            "cylinder; neither is supplied by the closed groupoid square."
        ),
        "scope": (
            "exact chart-object/root-label and complete-row guard, not a full "
            "ternary decorated-hafnian source.  It refutes an implication "
            "from the listed covariance, label and normalization hypotheses; "
            "recursive PP closure may still exclude the guard by forcing the "
            "stated proper face."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    guard = ledger["full_two_switch_pure_normalized_guard"]
    print("site/root chart squares: A<->B AND A<->C / FLAT")
    print("pure-normalized guard: 6 COMPONENTS / 24 COMPLETE ROWS")
    print("complete-row rank/nullity:", guard["complete_row_rank"],
          guard["complete_row_relation_dimension"])
    print("relative chart graphs: CLOSED BALANCED / NO OUTSIDE TAIL FAN")
    print("first missing law: ABSOLUTE L01 OR COLLISION/PP EXIT")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
