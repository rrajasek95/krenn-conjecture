#!/usr/bin/env python3
"""Bounded full S_8 x S_3 orbit quotient of the n=8 balanced Macaulay map.

The default run reproduces only the first three incidence-closure layers.
The third layer is already large enough to demote full component closure;
``--max-layers`` is an explicit guard against repeating the unbounded run.
"""

import argparse
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations
import importlib.util
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
SOURCE_PATH = HERE / "verify_n8_full_source_cycle_product_membership.py"
SPEC = importlib.util.spec_from_file_location("n8_source", SOURCE_PATH)
SOURCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SOURCE)

TRIPLES_PATH = HERE / "verify_matching_triple_orbit_counts.py"
TRIPLES_SPEC = importlib.util.spec_from_file_location(
    "n8_matching_triples", TRIPLES_PATH
)
TRIPLES = importlib.util.module_from_spec(TRIPLES_SPEC)
TRIPLES_SPEC.loader.exec_module(TRIPLES)

COLOUR_PERMUTATIONS = tuple(permutations(range(3)))
VERTEX_MATCHINGS = SOURCE.perfect_matchings(tuple(range(8)))
GROUP_ORDER = 40320 * 6
PRIME = 1009


def colour_transform(mate, permutation):
    answer = [-1] * 24
    for vertex in range(8):
        for colour in range(3):
            target_port = 3 * vertex + permutation[colour]
            other = mate[3 * vertex + colour]
            if other >= 0:
                other_vertex, other_colour = divmod(other, 3)
                answer[target_port] = (
                    3 * other_vertex + permutation[other_colour]
                )
    return tuple(answer)


def vertex_components(mate):
    adjacency = [set() for _vertex in range(8)]
    for port, other in enumerate(mate):
        if other >= 0:
            left, right = port // 3, other // 3
            adjacency[left].add(right)
            adjacency[right].add(left)
    unseen = set(range(8))
    components = []
    while unseen:
        first = min(unseen)
        component = {first}
        frontier = [first]
        while frontier:
            vertex = frontier.pop()
            for other in adjacency[vertex]:
                if other not in component:
                    component.add(other)
                    frontier.append(other)
        unseen -= component
        components.append(component)
    return components


def rooted_component_code(mate, component, root):
    order = [root]
    labels = {root: 0}
    for vertex in order:
        for colour in range(3):
            other = mate[3 * vertex + colour]
            if other < 0:
                continue
            other_vertex = other // 3
            if other_vertex not in labels:
                labels[other_vertex] = len(order)
                order.append(other_vertex)
    if set(order) != component:
        raise RuntimeError("root traversal missed a component vertex")
    code = []
    for vertex in order:
        for colour in range(3):
            other = mate[3 * vertex + colour]
            if other < 0:
                code.append(-1)
            else:
                other_vertex, other_colour = divmod(other, 3)
                code.append(3 * labels[other_vertex] + other_colour)
    return tuple(code)


def vertex_canonical_key(mate):
    codes = []
    for component in vertex_components(mate):
        codes.append(min(
            rooted_component_code(mate, component, root)
            for root in component
        ))
    return tuple(sorted(codes))


@lru_cache(maxsize=500000)
def canonical_key(mate):
    return min(
        vertex_canonical_key(colour_transform(mate, permutation))
        for permutation in COLOUR_PERMUTATIONS
    )


@lru_cache(maxsize=None)
def decode_key(key):
    mate = []
    offset = 0
    for component_code in key:
        size = len(component_code) // 3
        for value in component_code:
            if value < 0:
                mate.append(-1)
            else:
                vertex, colour = divmod(value, 3)
                mate.append(3 * (offset + vertex) + colour)
        offset += size
    if len(mate) != 24:
        raise RuntimeError("canonical key did not decode to eight vertices")
    return tuple(mate)


def row_from_matching_triple(triple):
    mate = [-1] * 24
    for colour, matching in enumerate(triple):
        for left, right in matching:
            first = 3 * left + colour
            second = 3 * right + colour
            mate[first] = second
            mate[second] = first
    return tuple(mate)


def mate_edges(mate):
    return tuple(
        (port, other) for port, other in enumerate(mate)
        if 0 <= port < other
    )


@lru_cache(maxsize=None)
def incident_columns(row_key):
    mate = decode_key(row_key)
    edges = mate_edges(mate)
    answer = set()
    for selected in combinations(edges, 4):
        vertices = []
        holes = []
        for first, second in selected:
            first_vertex, first_colour = divmod(first, 3)
            second_vertex, second_colour = divmod(second, 3)
            vertices.extend((first_vertex, second_vertex))
            holes.extend((first_colour, second_colour))
        if len(set(vertices)) != 8 or len(set(holes)) == 1:
            continue
        multiplier = list(mate)
        for first, second in selected:
            multiplier[first] = -1
            multiplier[second] = -1
        answer.add(canonical_key(tuple(multiplier)))
    return frozenset(answer)


@lru_cache(maxsize=None)
def column_outputs(column_key):
    multiplier = decode_key(column_key)
    holes = []
    for vertex in range(8):
        missing = [
            colour for colour in range(3)
            if multiplier[3 * vertex + colour] < 0
        ]
        if len(missing) != 1:
            raise RuntimeError("column does not have one hole at each vertex")
        holes.append(missing[0])
    answer = []
    for matching in VERTEX_MATCHINGS:
        mate = list(multiplier)
        for left, right in matching:
            first = 3 * left + holes[left]
            second = 3 * right + holes[right]
            mate[first] = second
            mate[second] = first
        answer.append(canonical_key(tuple(mate)))
    return tuple(answer)


def propagate_component(source, target, source_root, target_root, mapping, used):
    queue = [(source_root, target_root)]
    added = []

    def fail():
        for old_left, old_right in reversed(added):
            mapping.pop(old_left)
            used.remove(old_right)
        return None

    while queue:
        left, right = queue.pop()
        if left in mapping:
            if mapping[left] != right:
                return fail()
            continue
        if right in used:
            return fail()
        mapping[left] = right
        used.add(right)
        added.append((left, right))
        for colour in range(3):
            source_other = source[3 * left + colour]
            target_other = target[3 * right + colour]
            if (source_other < 0) != (target_other < 0):
                return fail()
            if source_other >= 0:
                source_vertex, source_colour = divmod(source_other, 3)
                target_vertex, target_colour = divmod(target_other, 3)
                if source_colour != target_colour:
                    return fail()
                queue.append((source_vertex, target_vertex))
    return added


def count_vertex_isomorphisms(source, target):
    mapping = {}
    used = set()

    def search():
        if len(mapping) == 8:
            return 1
        source_root = min(set(range(8)) - set(mapping))
        total = 0
        for target_root in set(range(8)) - used:
            added = propagate_component(
                source, target, source_root, target_root, mapping, used
            )
            if added is not None:
                total += search()
                for left, right in reversed(added):
                    mapping.pop(left)
                    used.remove(right)
        return total

    return search()


@lru_cache(maxsize=None)
def stabilizer_order(key):
    mate = decode_key(key)
    return sum(
        count_vertex_isomorphisms(
            colour_transform(mate, permutation), mate
        )
        for permutation in COLOUR_PERMUTATIONS
    )


def enumerate_component(target_rows, maximum_layers):
    rows = set(target_rows)
    frontier = set(target_rows)
    columns = set()
    layers = []
    while frontier:
        new_rows = set()
        new_columns = 0
        for position, row in enumerate(frontier, 1):
            for column in incident_columns(row):
                if column in columns:
                    continue
                columns.add(column)
                new_columns += 1
                for output in column_outputs(column):
                    if output not in rows:
                        new_rows.add(output)
            if position % 1000 == 0:
                print(
                    "scan", position, "/", len(frontier),
                    "newrows", len(new_rows), "columns", len(columns),
                    "canon-cache", canonical_key.cache_info(),
                    flush=True,
                )
        rows.update(new_rows)
        frontier = new_rows
        layers.append((len(new_rows), new_columns))
        print(
            "layer", len(layers), layers[-1],
            "totals", len(rows), len(columns), flush=True,
        )
        if len(layers) >= maximum_layers:
            break
    return (
        tuple(sorted(rows)), tuple(sorted(columns)), tuple(layers),
        not frontier,
    )


def modular_membership(rows, columns, target_rows):
    row_index = {row: index for index, row in enumerate(rows)}
    row_orbit_sizes = {
        row: GROUP_ORDER // stabilizer_order(row) for row in target_rows
    }
    basis = {}
    nonzeros = 0
    for position, column in enumerate(columns):
        entries = Counter(
            row_index[output] for output in column_outputs(column)
        )
        vector = {
            index: coefficient % PRIME
            for index, coefficient in entries.items()
            if coefficient % PRIME
        }
        nonzeros += len(vector)
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                inverse = pow(value, -1, PRIME)
                basis[pivot] = {
                    index: coefficient * inverse % PRIME
                    for index, coefficient in vector.items()
                }
                break
            pivot_row = basis[pivot]
            for index, coefficient in pivot_row.items():
                new_value = (
                    vector.get(index, 0) - value * coefficient
                ) % PRIME
                if new_value:
                    vector[index] = new_value
                else:
                    vector.pop(index, None)
        if position % 1000 == 0:
            print("eliminate", position, "rank", len(basis), flush=True)

    target = {
        row_index[row]: size % PRIME
        for row, size in row_orbit_sizes.items()
        if row in target_rows and size % PRIME
    }
    while target:
        pivot = min(target)
        value = target[pivot]
        if pivot not in basis:
            break
        for index, coefficient in basis[pivot].items():
            new_value = (
                target.get(index, 0) - value * coefficient
            ) % PRIME
            if new_value:
                target[index] = new_value
            else:
                target.pop(index, None)
    return {
        "rows": len(rows),
        "columns": len(columns),
        "nonzeros": nonzeros,
        "rank": len(basis),
        "left_nullity": len(rows) - len(basis),
        "target_in_span": not target,
        "target_remainder": len(target),
    }


def target_orbit_rows():
    """One pure matching triple from each full S_8 x S_3 orbit."""
    setting = TRIPLES.Setting(8)
    canonical = setting.index[setting.canonical]
    representatives = {}
    for second in range(setting.count):
        for third in range(setting.count):
            triple = (canonical, second, third)
            representatives.setdefault(setting.s_n_key(triple), triple)
    union_find = TRIPLES.UnionFind(list(representatives))
    for key, triple in representatives.items():
        for permutation in COLOUR_PERMUTATIONS:
            image = tuple(triple[permutation[colour]] for colour in range(3))
            union_find.union(key, setting.s_n_key(image))
    component_representatives = {}
    for key, triple in representatives.items():
        component_representatives.setdefault(union_find.find(key), triple)
    rows = set()
    for triple in component_representatives.values():
        matchings = tuple(setting.matchings[index] for index in triple)
        rows.add(canonical_key(row_from_matching_triple(matchings)))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max-layers", type=int, default=3,
        help="incidence-closure layer cap (default: 3; the bounded audit)",
    )
    args = parser.parse_args()
    if args.max_layers < 1:
        raise RuntimeError("--max-layers must be positive")

    started = time.time()
    target_rows = target_orbit_rows()
    print("target orbits", len(target_rows),
          "elapsed", time.time() - started, flush=True)
    if len(target_rows) != 31:
        raise RuntimeError("full S8 x S3 target orbit count changed")
    target_orbit_size = sum(
        GROUP_ORDER // stabilizer_order(row) for row in target_rows
    )
    if target_orbit_size != 105 ** 3:
        raise RuntimeError("target row-orbit sizes do not exhaust H0 H1 H2")
    rows, columns, layers, complete = enumerate_component(
        target_rows, args.max_layers
    )
    expected_layers = ((570, 31), (27470, 741), (360818, 17915))
    if args.max_layers == 3:
        if layers != expected_layers:
            raise RuntimeError("bounded three-layer census changed")
        if len(rows) != 388889 or len(columns) != 18687:
            raise RuntimeError("bounded three-layer totals changed")
        print(
            "bounded checkpoint certified; component remains open",
            "elapsed", time.time() - started, flush=True,
        )
        return
    if not complete:
        print(
            "layer cap reached; component remains open", len(rows), len(columns),
            "elapsed", time.time() - started, flush=True,
        )
        return
    print("component complete", len(rows), len(columns),
          "elapsed", time.time() - started, flush=True)
    ledger = modular_membership(rows, columns, target_rows)
    print(ledger, "layers", layers,
          "elapsed", time.time() - started, flush=True)


if __name__ == "__main__":
    main()
