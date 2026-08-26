#!/usr/bin/env python3
"""Exact second-variation screen at the balanced n=8 Laurent control.

The bounded screen enumerates every single-colour alternating four-cycle in
one of the three unit matching layers.  Opposite signs give the only choice
that can cancel an existing matching term.  Quadratic corrections on the
four base cells are solved exactly from moment balance and pure normalization.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from functools import reduce
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_laurent_diagonal_second_variation.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


PM8 = tuple(perfect_matchings(range(8)))
LAYERS = {
    0: ((0, 1), (2, 5), (3, 4), (6, 7)),
    1: ((0, 3), (1, 6), (2, 4), (5, 7)),
    2: ((0, 7), (1, 4), (2, 3), (5, 6)),
}
BASE = {(u, v, colour, colour): Fraction(1)
        for colour, edges in LAYERS.items() for u, v in edges}


def edge(u, v):
    return (u, v) if u < v else (v, u)


def get(source, u, v, a, b):
    return source.get((u, v, a, b), 0) if u < v else source.get((v, u, b, a), 0)


def derivative_coefficients(y, z):
    linear = defaultdict(Fraction)
    quadratic = defaultdict(Fraction)
    base_amplitude = defaultdict(Fraction)
    def by_edge(source):
        answer = defaultdict(list)
        for (u, v, a, b), value in source.items():
            if value:
                answer[(u, v)].append((a, b, value))
        return answer

    tables = tuple(map(by_edge, (BASE, y, z)))

    def add_term(target, choices):
        word = [None] * 8
        value = Fraction(1)
        for (u, v), (a, b, coefficient) in choices:
            word[u], word[v] = a, b
            value *= coefficient
        target[tuple(word)] += value

    for matching in PM8:
        base_options = [tables[0][edge] for edge in matching]
        if all(base_options):
            for choices in product(*base_options):
                add_term(base_amplitude, tuple(zip(matching, choices)))
        for chosen in range(4):
            options = [tables[int(index == chosen)][edge]
                       for index, edge in enumerate(matching)]
            if all(options):
                for choices in product(*options):
                    add_term(linear, tuple(zip(matching, choices)))
            options = [tables[2 if index == chosen else 0][edge]
                       for index, edge in enumerate(matching)]
            if all(options):
                for choices in product(*options):
                    add_term(quadratic, tuple(zip(matching, choices)))
        for left, right in combinations(range(4), 2):
            options = [tables[1 if index in (left, right) else 0][edge]
                       for index, edge in enumerate(matching)]
            if all(options):
                for choices in product(*options):
                    add_term(quadratic, tuple(zip(matching, choices)))
    return base_amplitude, linear, quadratic


def correction(colour, y):
    q = {
        site: sum(value * value for (u, v, a, b), value in y.items()
                  if a == colour and b == colour and site in (u, v))
        for site in range(8)
    }
    for u, v in LAYERS[colour]:
        require(q[u] == q[v], (colour, (u, v), q[u], q[v]))

    # Coefficient of t^2 in the pure hafnian coming from two Y cells.
    pure_y2 = Fraction(0)
    for matching in PM8:
        values = [get(y, u, v, colour, colour) for u, v in matching]
        bases = [get(BASE, u, v, colour, colour) for u, v in matching]
        for left, right in combinations(range(4), 2):
            term = values[left] * values[right]
            for other in range(4):
                if other not in (left, right):
                    term *= bases[other]
            pure_y2 += term
    q_edges = [q[u] for u, _ in LAYERS[colour]]
    k = (sum(q_edges) - 2 * pure_y2) / 4
    z = {}
    for u, v in LAYERS[colour]:
        z[(u, v, colour, colour)] = (k - q[u]) / 2
    require(sum(z.values()) + pure_y2 == 0,
            (colour, sum(z.values()), pure_y2))
    return z, {"q": q, "common_second_energy": k, "pure_y2": pure_y2}


def elementary_directions():
    for colour, layer in LAYERS.items():
        for first, second in combinations(layer, 2):
            (a, b), (c, d) = first, second
            for pairing in (((a, c), (b, d)), ((a, d), (b, c))):
                cells = [edge(*pair) for pair in pairing]
                require(cells[0] != cells[1], cells)
                y = {
                    (*cells[0], colour, colour): Fraction(1),
                    (*cells[1], colour, colour): Fraction(-1),
                }
                yield {
                    "colour": colour,
                    "base_edge_pair": (first, second),
                    "new_cells": tuple(cells),
                    "y": y,
                }


def evaluate(y):
    z = {}
    balance = {}
    for colour in range(3):
        part = {cell: value for cell, value in y.items()
                if cell[2:] == (colour, colour)}
        update, data = correction(colour, part)
        z.update(update)
        balance[colour] = data
    base, linear, quadratic = derivative_coefficients(y, z)
    linear_norm = Fraction(0)
    existing_cross = Fraction(0)
    words = set(base) | set(linear) | set(quadratic)
    for word in words:
        if len(set(word)) == 1:
            require(linear[word] == 0, ("pure linear", word))
            require(quadratic[word] == 0,
                    ("pure quadratic", word, quadratic[word]))
            continue
        linear_norm += linear[word] * linear[word]
        existing_cross += 2 * base[word] * quadratic[word]
    return {
        "linear_mixed_norm": linear_norm,
        "existing_mixed_cross": existing_cross,
        "P_second_coefficient": linear_norm + existing_cross,
        "balance": balance,
    }


def add_directions(left, right, sign):
    answer = dict(left)
    for cell, value in right.items():
        answer[cell] = answer.get(cell, Fraction(0)) + sign * value
        if not answer[cell]:
            del answer[cell]
    return answer


def logical_sha(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-count", action="store_true")
    args = parser.parse_args()
    elementary = tuple(elementary_directions())
    records = []
    for item in elementary:
        result = evaluate(item["y"])
        records.append({**{key: value for key, value in item.items() if key != "y"},
                        **result})
    require(len(records) == 36 + int(args.mutate_count), len(records))
    distribution = Counter(record["P_second_coefficient"] for record in records)
    minimum = min(distribution)
    print("directions", len(records))
    print("P2 distribution", dict(sorted(distribution.items())))
    print("minimum", minimum)
    for record in records:
        if record["P_second_coefficient"] == minimum:
            print("minimizer", record)

    pair_distribution = Counter()
    infeasible = 0
    pair_minimum = None
    pair_minimizers = []
    for left, right in combinations(elementary, 2):
        for sign in (Fraction(1), Fraction(-1)):
            y = add_directions(left["y"], right["y"], sign)
            try:
                result = evaluate(y)
            except RuntimeError:
                infeasible += 1
                continue
            value = result["P_second_coefficient"]
            pair_distribution[value] += 1
            if pair_minimum is None or value < pair_minimum:
                pair_minimum = value
                pair_minimizers = [(left, right, sign, result)]
            elif value == pair_minimum:
                pair_minimizers.append((left, right, sign, result))
    print("two-cycle feasible/infeasible", sum(pair_distribution.values()), infeasible)
    print("two-cycle P2 distribution", dict(sorted(pair_distribution.items())))
    print("two-cycle minimum/count", pair_minimum, len(pair_minimizers))
    for left, right, sign, result in pair_minimizers[:12]:
        print("two-cycle minimizer", {"left": left["new_cells"],
                                       "right": right["new_cells"],
                                       "sign": sign, "result": result})
    payload = {
        "status": "PASS exact Laurent real-diagonal cycle second variation",
        "elementary_cycle_directions": len(records),
        "elementary_P2_distribution": {
            str(key): value for key, value in sorted(distribution.items())
        },
        "elementary_minimum": str(minimum),
        "elementary_minimizer_count": sum(value for key, value in distribution.items()
                                           if key == minimum),
        "signed_two_cycle_combinations": sum(pair_distribution.values()),
        "infeasible_two_cycle_combinations": infeasible,
        "two_cycle_P2_distribution": {
            str(key): value for key, value in sorted(pair_distribution.items())
        },
        "two_cycle_minimum": str(pair_minimum),
        "two_cycle_minimizer_count": len(pair_minimizers),
        "scope": (
            "Real diagonal off-support alternating four-cycle rays with exact "
            "second-order moment and pure corrections. This is not the full "
            "252-cell Hessian."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("logical sha256", payload["logical_sha256"])


if __name__ == "__main__":
    main()
