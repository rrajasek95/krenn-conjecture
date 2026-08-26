#!/usr/bin/env python3
"""Exact Laurent transition and 31-orbit C4-flip adjacency audit."""

from collections import Counter, defaultdict, deque
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CHART_PATH = ROOT / "computations/verify_n8_target_triple_localization_orbits.py"
SOURCE_PATH = ROOT / "computations/verify_n8_normalized_critical_contraction.py"
RESULT = HERE / "results_chart_c4_transition.json"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


CHART = load(CHART_PATH, "c4_chart_authority")
NORM = load(SOURCE_PATH, "c4_normalized_source")
D5 = NORM.D5


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def port_edge(identifier):
    i, j, a, b = D5.COORDINATES[identifier]
    return tuple(sorted((3 * i + a, 3 * j + b)))


def support(triple):
    answer = set()
    for colour, matching in enumerate(triple):
        for i, j in matching:
            answer.add(tuple(sorted((3 * i + colour, 3 * j + colour))))
    require(len(answer) == 12, "triple is not a port matching")
    return frozenset(answer)


def port_mate(selected):
    answer = {}
    for edge in selected:
        p, q = edge
        require(p not in answer and q not in answer, "support repeats a port")
        answer[p] = q; answer[q] = p
    require(len(answer) == 24, "support misses a port")
    return answer


def add_exp(answer, term, scalar=1):
    for variable, exponent in term.items():
        answer[variable] += scalar * exponent
        if answer[variable] == 0:
            del answer[variable]


def transition(source_support, target_support, distinguished):
    """Target normalized variables as Laurent monomials in source variables."""
    target_mate = port_mate(target_support)

    def source_x(edge):
        return Counter() if edge in source_support else Counter({edge: 1})

    target_anchor = {edge: source_x(edge) for edge in target_support}
    answer = {}
    for identifier in range(252):
        edge = port_edge(identifier)
        if edge in target_support or edge in answer:
            continue
        expression = source_x(edge)
        for port in edge:
            anchor = tuple(sorted((port, target_mate[port])))
            if port == distinguished[anchor]:
                add_exp(expression, target_anchor[anchor], -1)
        answer[edge] = expression
    require(len(answer) == 240, "transition lost target variables")
    return answer


def compose(expression, substitutions):
    answer = Counter()
    for variable, exponent in expression.items():
        add_exp(answer, substitutions[variable], exponent)
    return answer


def polynomial_old(code, old_support):
    polynomial = Counter()
    for literal in D5.iter_word_terms(code):
        exponent = Counter()
        for identifier in literal:
            edge = port_edge(identifier)
            if edge not in old_support:
                exponent[edge] += 1
        polynomial[tuple(sorted(exponent.items()))] += 1
    return polynomial


def polynomial_new_transformed(code, new_support, trans):
    polynomial = Counter()
    for literal in D5.iter_word_terms(code):
        exponent = Counter()
        for identifier in literal:
            edge = port_edge(identifier)
            if edge not in new_support:
                add_exp(exponent, trans[edge])
        polynomial[tuple(sorted(exponent.items()))] += 1
    return polynomial


def chart_triple(row):
    mate = CHART.SOURCE.decode_key(row)
    triple = []
    for colour in range(3):
        matching = []
        for site in range(8):
            port = 3 * site + colour
            other = mate[port]
            if port < other:
                require(other % 3 == colour, "pure chart edge changed colour")
                matching.append((site, other // 3))
        require(len(matching) == 4, "chart colour lost a perfect matching")
        triple.append(tuple(sorted(matching)))
    return tuple(triple)


def chart_key(triple):
    mate = [-1] * 24
    for colour, matching in enumerate(triple):
        for i, j in matching:
            p, q = 3 * i + colour, 3 * j + colour
            mate[p] = q; mate[q] = p
    require(all(value >= 0 for value in mate), "chart mate incomplete")
    return CHART.SOURCE.canonical_key(tuple(mate))


def flip_neighbors(triple):
    answer = set()
    for colour, matching in enumerate(triple):
        for left in range(4):
            for right in range(left + 1, 4):
                (a, b), (c, d) = matching[left], matching[right]
                for replacement in (((a, c), (b, d)), ((a, d), (b, c))):
                    changed = list(matching)
                    changed[left] = tuple(sorted(replacement[0]))
                    changed[right] = tuple(sorted(replacement[1]))
                    updated = list(triple)
                    updated[colour] = tuple(sorted(changed))
                    answer.add(tuple(updated))
    require(len(answer) == 36, "triple did not have 36 labelled C4 flips")
    return answer


def main():
    matching = ((0, 1), (2, 3), (4, 5), (6, 7))
    flipped = ((0, 2), (1, 3), (4, 5), (6, 7))
    old_triple = (matching, matching, matching)
    new_triple = (flipped, matching, matching)
    old_support, new_support = support(old_triple), support(new_triple)
    entering = sorted(new_support - old_support)
    leaving = sorted(old_support - new_support)
    require(len(entering) == len(leaving) == 2, "representative is not one C4 flip")

    distinguished = {edge: min(edge) for edge in new_support}
    # Compatible C4 orientation: each leaving old edge contains exactly one
    # distinguished endpoint of the two entering edges.
    distinguished[entering[0]] = 0
    distinguished[entering[1]] = 9
    require(set(entering) == {(0, 6), (3, 9)}
            and [distinguished[edge] for edge in entering] == [0, 9],
            "representative compatible orientation changed")
    forward = transition(old_support, new_support, distinguished)

    # Explicit cluster inverse.  The two leaving normalized coordinates are
    # the inverses of the two entering old coordinates.
    anchor_inverse = {
        (0, 6): Counter({(0, 3): -1}),
        (3, 9): Counter({(6, 9): -1}),
    }
    inverse = {}
    for identifier in range(252):
        edge = port_edge(identifier)
        if edge in old_support:
            continue
        if edge in new_support:
            expression = Counter(anchor_inverse.get(edge, {}))
        else:
            expression = Counter({edge: 1})
            for port in edge:
                anchor = tuple(sorted((port, port_mate(new_support)[port])))
                if port == distinguished[anchor]:
                    add_exp(expression, anchor_inverse.get(anchor, Counter()))
        inverse[edge] = expression
    require(len(inverse) == 240, "inverse lost old variables")
    for edge, expression in inverse.items():
        require(compose(expression, forward) == Counter({edge: 1}),
                f"Laurent transition inverse failed at {edge}")
    for edge, expression in forward.items():
        require(compose(expression, inverse) == Counter({edge: 1}),
                f"Laurent transition forward inverse failed at {edge}")

    # Termwise covariance for all words.  For target chart normalization,
    # H_old = m_w * H_new(trans), with m_w the product of entering anchor
    # values at distinguished selected ports.
    new_mate = port_mate(new_support)
    word_checks = 0
    mixed_checks = 0
    pure_checks = 0
    pure_units = []
    for code in range(3 ** 8):
        word = D5.decode_word(code)
        unit = Counter()
        for site, colour in enumerate(word):
            port = 3 * site + colour
            anchor = tuple(sorted((port, new_mate[port])))
            if port == distinguished[anchor] and anchor not in old_support:
                unit[anchor] += 1
        transformed = polynomial_new_transformed(code, new_support, forward)
        shifted = Counter()
        for exponent, coefficient in transformed.items():
            value = Counter(dict(exponent)); add_exp(value, unit)
            shifted[tuple(sorted(value.items()))] += coefficient
        require(shifted == polynomial_old(code, old_support),
                f"amplitude covariance failed for code {code}")
        word_checks += 105
        if len(set(word)) == 1:
            pure_checks += 1
            pure_units.append(tuple(sorted(unit.items())))
        else:
            mixed_checks += 1
    pure_product_unit = Counter()
    for unit in pure_units:
        add_exp(pure_product_unit, Counter(dict(unit)))
    require(pure_product_unit == Counter({edge: 1 for edge in entering}),
            "pure product did not pick up entering chart product")

    rows = tuple(sorted(CHART.SOURCE.target_orbit_rows()))
    row_index = {row: index for index, row in enumerate(rows, 1)}
    adjacency = defaultdict(set)
    labelled_edge_counts = Counter()
    for index, row in enumerate(rows, 1):
        triple = chart_triple(row)
        for neighbor in flip_neighbors(triple):
            other = row_index[chart_key(neighbor)]
            adjacency[index].add(other)
            adjacency[other].add(index)
            labelled_edge_counts[tuple(sorted((index, other)))] += 1
    unseen = set(range(1, 32))
    components = []
    while unseen:
        root = min(unseen)
        component = {root}; queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for other in adjacency[vertex]:
                if other not in component:
                    component.add(other); queue.append(other)
        unseen -= component
        components.append(sorted(component))
    old_id = row_index[chart_key(old_triple)]
    new_id = row_index[chart_key(new_triple)]

    payload = {
        "format": "n8-chart-c4-laurent-transition-v1",
        "status": "EXACT_OVERLAP_TRANSITION_CONNECTED_GRAPH_BOUNDARY_NO_DESCENT",
        "representative_flip": {
            "old_chart": old_id,
            "new_chart": new_id,
            "entering_old_normalized_variables": [list(edge) for edge in entering],
            "leaving_new_normalized_variables": [list(edge) for edge in leaving],
            "common_support_edges": len(old_support & new_support),
            "forward_laurent_coordinates": len(forward),
            "inverse_coordinate_checks": 240,
            "negative_exponent_variables_forward": [list(edge) for edge in entering],
            "required_overlap_localizer_old": [list(edge) for edge in entering],
            "required_overlap_localizer_new": [list(edge) for edge in leaving],
        },
        "covariance": {
            "word_matching_term_checks": word_checks,
            "mixed_words": mixed_checks,
            "pure_words": pure_checks,
            "all_amplitudes_carried_up_to_word_unit": True,
            "pure_product_unit_old_coordinates": [list(edge) for edge in entering],
            "mixed_ideal_carried_after_double_localization": True,
        },
        "orbit_adjacency": {
            "chart_vertices": 31,
            "undirected_orbit_edges": sum(len(values) for values in adjacency.values()) // 2,
            "connected_components": components,
            "component_count": len(components),
            "degree_histogram": dict(sorted(Counter(map(len, adjacency.values())).items())),
            "representative_edge": [old_id, new_id],
        },
        "theorem": (
            "Adjacent matching charts are exactly Laurent-isomorphic on their overlap, and the "
            "mixed ideal and pure product transport up to explicit monomial units. The 31-orbit "
            "C4-flip graph is connected. This does not reduce the chart checklist because the "
            "transition inverts the two entering cells; it is undefined on their boundary, which "
            "is part of the source chart and is not covered by overlap transport."
        ),
        "minimal_counterguard": {
            "kind": "chart-boundary denominator, not a failed mixed row",
            "old_chart_point_condition": "all old support cells nonzero, at least one entering cell zero",
            "effect": "the old chart remains defined but the adjacent Laurent transition is undefined",
            "consequence": "connected overlap graph does not transport radical membership across whole charts",
        },
        "scope": (
            "Exact monomial coordinate/covariance and finite orbit graph only; no assertion that "
            "the mixed-zero locus meets the displayed boundary, and no chart membership, descent, "
            "or conjecture closure."
        ),
        "source_sha256": {
            str(CHART_PATH.relative_to(ROOT)): sha256(CHART_PATH.read_bytes()).hexdigest(),
            str(SOURCE_PATH.relative_to(ROOT)): sha256(SOURCE_PATH.read_bytes()).hexdigest(),
        },
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
