#!/usr/bin/env python3
"""Exact small-order S_n x S_3 quotients of the balanced port incidence map.

This is a discovery analyzer for the concrete lemma that the product of the
three pure hafnians lies in the degree-three balanced mixed-hafnian ideal.
It is intentionally restricted to n <= 6; it is not an n=8 component BFS.
"""

import argparse
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
TRIPLES_PATH = HERE / "verify_matching_triple_orbit_counts.py"
SPEC = importlib.util.spec_from_file_location("matching_triples", TRIPLES_PATH)
TRIPLES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TRIPLES)

COLOUR_PERMUTATIONS = tuple(permutations(range(3)))
PRIME = 1009


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], 1):
        remaining = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(remaining):
            answer.append(((first, second),) + tail)
    return tuple(answer)


class PortIncidence:
    def __init__(self, order):
        if order not in (2, 4, 6):
            raise RuntimeError("small-order analyzer is bounded to n=2,4,6")
        self.order = order
        self.matchings = perfect_matchings(range(order))

    def colour_transform(self, mate, permutation):
        answer = [-1] * (3 * self.order)
        for vertex in range(self.order):
            for colour in range(3):
                target = 3 * vertex + permutation[colour]
                other = mate[3 * vertex + colour]
                if other >= 0:
                    other_vertex, other_colour = divmod(other, 3)
                    answer[target] = 3 * other_vertex + permutation[other_colour]
        return tuple(answer)

    def vertex_components(self, mate):
        adjacency = [set() for _ in range(self.order)]
        for port, other in enumerate(mate):
            if other >= 0:
                left, right = port // 3, other // 3
                adjacency[left].add(right)
                adjacency[right].add(left)
        unseen = set(range(self.order))
        components = []
        while unseen:
            root = min(unseen)
            component = {root}
            frontier = [root]
            while frontier:
                vertex = frontier.pop()
                for other in adjacency[vertex]:
                    if other not in component:
                        component.add(other)
                        frontier.append(other)
            unseen -= component
            components.append(component)
        return components

    def rooted_component_code(self, mate, component, root):
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
            raise RuntimeError("component traversal failed")
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

    def vertex_canonical_key(self, mate):
        return tuple(sorted(
            min(self.rooted_component_code(mate, component, root)
                for root in component)
            for component in self.vertex_components(mate)
        ))

    @lru_cache(maxsize=None)
    def canonical_key(self, mate):
        return min(
            self.vertex_canonical_key(self.colour_transform(mate, permutation))
            for permutation in COLOUR_PERMUTATIONS
        )

    @lru_cache(maxsize=None)
    def decode_key(self, key):
        mate = []
        offset = 0
        for component in key:
            for value in component:
                if value < 0:
                    mate.append(-1)
                else:
                    vertex, colour = divmod(value, 3)
                    mate.append(3 * (offset + vertex) + colour)
            offset += len(component) // 3
        if len(mate) != 3 * self.order:
            raise RuntimeError("decoded key has wrong order")
        return tuple(mate)

    def row_from_matching_triple(self, triple):
        mate = [-1] * (3 * self.order)
        for colour, matching in enumerate(triple):
            for left, right in matching:
                first = 3 * left + colour
                second = 3 * right + colour
                mate[first] = second
                mate[second] = first
        return tuple(mate)

    @staticmethod
    def mate_edges(mate):
        return tuple((port, other) for port, other in enumerate(mate)
                     if 0 <= port < other)

    @lru_cache(maxsize=None)
    def incident_columns(self, row_key):
        mate = self.decode_key(row_key)
        answer = set()
        for selected in combinations(self.mate_edges(mate), self.order // 2):
            vertices = []
            colours = []
            for first, second in selected:
                left, left_colour = divmod(first, 3)
                right, right_colour = divmod(second, 3)
                vertices.extend((left, right))
                colours.extend((left_colour, right_colour))
            if len(set(vertices)) != self.order or len(set(colours)) == 1:
                continue
            multiplier = list(mate)
            for first, second in selected:
                multiplier[first] = -1
                multiplier[second] = -1
            answer.add(self.canonical_key(tuple(multiplier)))
        return frozenset(answer)

    @lru_cache(maxsize=None)
    def column_outputs(self, column_key):
        multiplier = self.decode_key(column_key)
        holes = []
        for vertex in range(self.order):
            missing = [colour for colour in range(3)
                       if multiplier[3 * vertex + colour] < 0]
            if len(missing) != 1:
                raise RuntimeError("column does not have one hole per vertex")
            holes.append(missing[0])
        answer = []
        for matching in self.matchings:
            mate = list(multiplier)
            for left, right in matching:
                first = 3 * left + holes[left]
                second = 3 * right + holes[right]
                mate[first] = second
                mate[second] = first
            answer.append(self.canonical_key(tuple(mate)))
        return tuple(answer)

    def target_rows(self):
        setting = TRIPLES.Setting(self.order)
        canonical = setting.index[setting.canonical]
        representatives = {}
        for second in range(setting.count):
            for third in range(setting.count):
                triple = canonical, second, third
                representatives.setdefault(setting.s_n_key(triple), triple)
        union_find = TRIPLES.UnionFind(list(representatives))
        for key, triple in representatives.items():
            for permutation in COLOUR_PERMUTATIONS:
                image = tuple(triple[permutation[colour]] for colour in range(3))
                union_find.union(key, setting.s_n_key(image))
        rows = set()
        for key, triple in representatives.items():
            if union_find.find(key) != key:
                continue
            matchings = tuple(setting.matchings[index] for index in triple)
            rows.add(self.canonical_key(self.row_from_matching_triple(matchings)))
        return rows

    def component(self):
        target = self.target_rows()
        rows = set(target)
        frontier = set(target)
        columns = set()
        layers = []
        while frontier:
            new_rows = set()
            before = len(columns)
            for row in frontier:
                for column in self.incident_columns(row):
                    if column in columns:
                        continue
                    columns.add(column)
                    for output in self.column_outputs(column):
                        if output not in rows:
                            new_rows.add(output)
            rows.update(new_rows)
            frontier = new_rows
            layers.append((len(new_rows), len(columns) - before))
            print("layer", len(layers), layers[-1],
                  "totals", len(rows), len(columns), flush=True)
        return tuple(sorted(rows)), tuple(sorted(columns)), target, tuple(layers)

    def membership(self, rows, columns, target):
        row_index = {row: index for index, row in enumerate(rows)}
        basis = {}
        for column in columns:
            vector = {
                index: coefficient % PRIME
                for index, coefficient in Counter(
                    row_index[row] for row in self.column_outputs(column)
                ).items()
                if coefficient % PRIME
            }
            while vector:
                pivot = min(vector)
                value = vector[pivot]
                if pivot not in basis:
                    inverse = pow(value, -1, PRIME)
                    basis[pivot] = {index: coefficient * inverse % PRIME
                                    for index, coefficient in vector.items()}
                    break
                for index, coefficient in basis[pivot].items():
                    new = (vector.get(index, 0) - value * coefficient) % PRIME
                    if new:
                        vector[index] = new
                    else:
                        vector.pop(index, None)
        # Coinvariant coordinates require actual row-orbit weights.  For the
        # small orders it is cheaper and safer to reconstruct each orbit.
        group = tuple(permutations(range(self.order)))
        target_vector = {}
        for row in target:
            mate = self.decode_key(row)
            orbit = set()
            for vertex_permutation in group:
                for colour_permutation in COLOUR_PERMUTATIONS:
                    transformed = [-1] * (3 * self.order)
                    for vertex in range(self.order):
                        for colour in range(3):
                            source = 3 * vertex + colour
                            other = mate[source]
                            other_vertex, other_colour = divmod(other, 3)
                            target_port = (3 * vertex_permutation[vertex]
                                           + colour_permutation[colour])
                            transformed[target_port] = (
                                3 * vertex_permutation[other_vertex]
                                + colour_permutation[other_colour]
                            )
                    orbit.add(tuple(transformed))
            target_vector[row_index[row]] = len(orbit) % PRIME
        remainder = dict(target_vector)
        while remainder:
            pivot = min(remainder)
            value = remainder[pivot]
            if pivot not in basis:
                break
            for index, coefficient in basis[pivot].items():
                new = (remainder.get(index, 0) - value * coefficient) % PRIME
                if new:
                    remainder[index] = new
                else:
                    remainder.pop(index, None)
        return len(basis), not remainder, len(remainder)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("order", type=int, choices=(2, 4, 6))
    args = parser.parse_args()
    incidence = PortIncidence(args.order)
    rows, columns, target, layers = incidence.component()
    rank, consistent, remainder = incidence.membership(rows, columns, target)
    print({
        "order": args.order,
        "target_orbits": len(target),
        "rows": len(rows),
        "columns": len(columns),
        "rank_mod_1009": rank,
        "target_in_span_mod_1009": consistent,
        "target_remainder": remainder,
        "layers": layers,
    })


if __name__ == "__main__":
    main()
